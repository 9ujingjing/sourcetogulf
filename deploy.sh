#!/bin/bash
# sourcetogulf.com 一键部署脚本
# 用法:
#   ./deploy.sh            立即部署当前改动
#   ./deploy.sh "说明"      部署并使用自定义提交说明
#   ./deploy.sh watch       自动模式:监视文件改动,改完 30 秒无操作就自动提交(不推送)
#
# 说明:部署前会自动跑一遍构建(见 build_all),因此改了 products.clean.json 或
#       pricing.json 之后直接 ./deploy.sh 即可,不需要手动跑生成器。
set -e
cd "$(dirname "$0")"

BRANCH="main"
REMOTE="origin"
URL="https://sourcetogulf.com"

# ---------------------------------------------------------------------------
# 构建:把所有数据源渲染成静态页
#   顺序不能乱:
#     1. build_fx.py     —— pricing.json -> pricing.js(浏览器侧常量)
#     2. build_*.py      —— 各页面生成器(Python 侧直接读 pricing.json)
#     3. build_flags.py  —— 把国旗 emoji 换成内联 SVG,注入 products.html
#     4. sync_header_footer.py —— 把 products.html 的 style/header/footer
#                                 同步到手工页(index/about/shipping/services 等)
#   任一步失败就中止部署,绝不带半成品上线。
# ---------------------------------------------------------------------------
BUILDERS="build_fx.py build_products.py build_cat_products.py build_guides.py \
build_personas.py build_solutions.py build_compare.py build_blog.py \
build_answers.py build_partners.py build_ads.py build_rss.py build_arabic.py \
build_flags.py"

build_all() {
  local fail=0
  for s in $BUILDERS; do
    [ -f "$s" ] || continue
    python3 "$s" >/dev/null 2>&1 || { echo "   ✗ $s"; fail=1; }
  done
  # 注意:不能用 `cmd && { ... }` 短路写法 —— 在 `set -e` 下,
  # 若文件不存在导致左侧为假,整个列表返回非 0 会直接终止脚本。
  if [ -f sync_header_footer.py ]; then
    if ! python3 sync_header_footer.py >/dev/null 2>&1; then
      echo "   ✗ sync_header_footer.py"; fail=1
    fi
  fi
  return $fail
}

msg="${1:-}"
if [ "$msg" = "watch" ]; then
  echo "👀 自动提交模式已启动 (Ctrl+C 退出)"
  echo "   监视本目录文件改动, 停止编辑 30 秒后自动【本地提交】(不会推送)"
  echo "   ⚠️  只提交不推送:避免编辑中途的半成品被推到线上"
  echo "   确认没问题后, 手动运行 ./deploy.sh \"说明\" 推送"
  while true; do
    CHANGED=$(git status --porcelain | grep -v '^?? *\.DS_Store' | head -1)
    if [ -n "$CHANGED" ]; then
      echo ""
      echo "📝 $(date '+%H:%M:%S') 检测到改动: $CHANGED"
      echo "   等 30 秒确认编辑完成..."
      sleep 30
      if [ -n "$(git status --porcelain | grep -v '^?? *\.DS_Store' | head -1)" ]; then
        git add -A
        git commit -m "auto: 更新于 $(date '+%Y-%m-%d %H:%M')" --quiet || true
        echo "   ✅ $(date '+%H:%M:%S') 已本地提交(未推送)"
        echo "      推送请运行: ./deploy.sh \"说明\""
      fi
    fi
    sleep 5
  done
fi

# ---- 构建 ----
echo "🔨 构建中..."
if ! build_all; then
  echo ""
  echo "❌ 构建失败,部署已中止(线上未受影响)"
  exit 1
fi
echo "   ✓ 构建完成"

CHANGED=$(git status --porcelain | grep -v '^?? *\.DS_Store' | head -1)
if [ -z "$CHANGED" ]; then
  echo "✨ 没有改动需要部署, 线上已是最新版本"
  exit 0
fi

echo "📦 待部署文件:"
git status --short | head -20

git add -A
git commit -m "${msg:-更新于 $(date '+%Y-%m-%d %H:%M')}" --quiet
git push "$REMOTE" "$BRANCH" --quiet

echo ""
echo "🚀 已推送! GitHub Pages 正在构建 (约 1-2 分钟)"
echo "   线上地址: $URL"
echo ""
echo "⏳ 等待构建完成..."
for i in $(seq 1 12); do
  sleep 15
  STATUS=$(gh api repos/9ujingjing/sourcetogulf/pages/builds/latest --jq '.status' 2>/dev/null || echo "unknown")
  echo "   [$i] 构建状态: $STATUS"
  if [ "$STATUS" = "built" ]; then
    echo ""
    echo "✅ 部署完成! 现在访问: $URL"
    # 构建完成后, 把新页面提交给 Bing / Copilot / ChatGPT 加速收录
    if [ -f submit_indexnow.py ]; then
      echo "📡 提交 IndexNow 队列..."
      python3 submit_indexnow.py || true
    fi
    exit 0
  fi
done
echo "⚠️ 构建耗时较长, 可稍后自行访问确认: $URL"
