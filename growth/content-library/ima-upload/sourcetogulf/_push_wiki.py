import os, re, json, subprocess, sys

BASE = "/Users/jingjinggu/Desktop/sourcetogulf/Kimi_Agent_货盘供货商定位/app/growth/content-library/ima-upload/sourcetogulf"
os.chdir(BASE)
SPACE = "7688996466303437793"

# 分类 -> [(相对md路径, 飞书文档标题)]
STRUCTURE = {
    "入门与说明": [
        ("00-库说明与红线.md", "00 · 库说明与红线"),
        ("04b-扫描提炼方法论.md", "04b · 扫描提炼方法论"),
        ("05-收件箱示例.md", "05 · 收件箱示例"),
        ("PROMPTS-调用知识库.md", "PROMPTS · 怎么调用这个知识库"),
        ("PROMPTS-同事版.md", "PROMPTS · 同事版（任何 AI 可用）"),
    ],
    "客户案例": [  # soga 已手建，这里只补 zyvo
        ("customers/zyvo-gaming-store.md", "阿曼 Gaming 店（匿名案例）"),
    ],
    "货盘与产品": [
        ("products/activewear-pallet-26oct.md", "女式运动服混装货盘 26OCT"),
        ("products/stationery-dubai-bulk.md", "迪拜文具批量报价"),
    ],
    "报价单": [
        ("quotes/joelle-sample.md", "样品单 Joelle（匿名）"),
        ("quotes/madani-simracing.md", "卡塔尔 MOZA 赛车模拟设备（匿名）"),
        ("quotes/wa-unknown-quote.md", "WA 报价单（匿名隐号）"),
    ],
    "工作痕迹": [
        ("work-traces/content-engine-build-2026-09-24.md", "内容引擎搭建工作痕迹"),
    ],
    "内容机会": [
        ("insights/2026-09-24-content-ideas.md", "内容机会扫描 2026-09-24"),
        ("insights/2026-09-24-sourcing-agent-benchmark.md", "对标研究：各平台涨粉最快的 sourcing agent（v2）"),
        ("insights/2026-09-24-copy-hashtag-playbook.md", "文案句式 + Hashtag 打法（含海湾版 tag 组合）"),
    ],
    "素材资产库": [
        ("assets/sourcetogulf-content-assets-10.md", "内容资产库 · 10 个真实素材（docx 沉淀）"),
    ],
}

EXISTING = {"客户案例": "EqPswlYaKiOGD3kDzHicmvxdnhh"}  # 已建的分类

def strip_frontmatter(text):
    if text.lstrip().startswith('---'):
        m = re.match(r'^\s*---\s*\n.*?\n---\s*\n?', text, re.DOTALL)
        if m:
            return text[m.end():]
    return text

def run(args):
    r = subprocess.run(["lark-cli"] + args, capture_output=True, text=True)
    if r.returncode != 0:
        print("ERR", r.stderr[:300]); return None
    try:
        return json.loads(r.stdout)
    except Exception:
        print("JSON FAIL", r.stdout[:200]); return None

# 1) 建分类节点（幂等：先查空间已有分类，同名复用，避免重跑重复建）
existing_map = {}
res = run(["wiki", "+node-list", "--space-id", SPACE, "--as", "user", "--format", "json"])
if res and res.get("ok"):
    for n in res["data"].get("nodes", []):
        existing_map[n["title"]] = n["node_token"]

cat_tokens = dict(EXISTING)
for cat in STRUCTURE:
    if cat in existing_map:                       # 空间里已存在 → 直接复用
        cat_tokens[cat] = existing_map[cat]
        print(f"[cat reuse] {cat} -> {existing_map[cat]}")
        continue
    if cat in EXISTING:
        continue
    res = run(["wiki", "+node-create", "--space-id", SPACE, "--title", cat, "--as", "user", "--format", "json"])
    if res and res.get("ok"):
        tok = res["data"]["node_token"]
        cat_tokens[cat] = tok
        print(f"[cat new] {cat} -> {tok}")
    else:
        print(f"[cat FAIL] {cat}", res); sys.exit(1)

# 2) 建文档（剥离 frontmatter 后写入；幂等：父节点下同名文档已存在则跳过）
summary = []
os.makedirs("_stage", exist_ok=True)
for cat, docs in STRUCTURE.items():
    parent = cat_tokens[cat]
    have = set()
    res = run(["wiki", "+node-list", "--space-id", SPACE, "--parent-node-token", parent, "--as", "user", "--format", "json"])
    if res and res.get("ok"):
        have = {n["title"] for n in res["data"].get("nodes", [])}
    for rel, title in docs:
        if title in have:
            print(f"[doc skip] {title}（已存在）")
            continue
        text = open(rel, encoding="utf-8").read()
        text = strip_frontmatter(text)
        clean = os.path.join("_stage", os.path.basename(rel))
        open(clean, "w", encoding="utf-8").write(text)
        res = run(["docs", "+create", "--doc-format", "markdown",
                   "--content", f"@{clean}", "--title", title,
                   "--parent-token", parent, "--as", "user", "--format", "json"])
        if res and res.get("ok"):
            url = res["data"]["document"]["url"]
            print(f"[doc] {title} -> {url}")
            summary.append((cat, title, url))
        else:
            print(f"[doc FAIL] {title}", res)

# 3) 输出汇总（含已手建的 soga）
print("\n=== SUMMARY ===")
soga = ("客户案例", "迪拜香水礼盒（匿名案例）", "https://papaclaw.feishu.cn/docx/OHhhd20pNoPYptxgOQqceAf6n4g")
for cat, title, url in [soga] + summary:
    print(f"{cat} | {title} | {url}")
print(f"\n总计节点: {len(cat_tokens)} 分类 + {len(summary)+1} 文档")
