#!/bin/bash
# sourcetogulf.com 一键部署脚本
# 用法:
#   ./deploy.sh            立即部署当前改动
#   ./deploy.sh "说明"      部署并使用自定义提交说明
#   ./deploy.sh watch       自动模式:监视文件改动,改完 30 秒无操作就自动部署
set -e
cd "$(dirname "$0")"

BRANCH="main"
REMOTE="origin"
URL="https://sourcetogulf.com"

msg="${1:-}"
if [ "$msg" = "watch" ]; then
  echo "👀 自动部署模式已启动 (Ctrl+C 退出)"
  echo "   监视本目录文件改动, 停止编辑 30 秒后自动提交部署"
  LAST_HASH=$(git rev-parse HEAD 2>/dev/null || echo "none")
  while true; do
    CHANGED=$(git status --porcelain | grep -v '^?? *\.DS_Store' | head -1)
    if [ -n "$CHANGED" ]; then
      echo ""
      echo "📝 $(date '+%H:%M:%S') 检测到改动: $CHANGED"
      echo "   等 30 秒确认编辑完成..."
      sleep 30
      # 30 秒后仍有改动才执行
      if [ -n "$(git status --porcelain | grep -v '^?? *\.DS_Store' | head -1)" ]; then
        git add -A
        git commit -m "auto: 更新于 $(date '+%Y-%m-%d %H:%M')" --quiet || true
        git push "$REMOTE" "$BRANCH" --quiet
        echo "✅ $(date '+%H:%M:%S') 已推送, 1-2 分钟后线上生效: $URL"
      fi
    fi
    sleep 5
  done
fi

# ---- 立即部署 ----
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
    exit 0
  fi
done
echo "⚠️ 构建耗时较长, 可稍后自行访问确认: $URL"
