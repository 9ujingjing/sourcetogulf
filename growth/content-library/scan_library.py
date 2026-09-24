#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan_library.py — 扫描内容沉淀库，输出「内容机会表」

用法：
    python3 scan_library.py                 # 输出全部内容机会
    python3 scan_library.py --week           # 只挑本周可写（anon_ok + 进行中状态）
    python3 scan_library.py --markdown       # 输出可直接贴进 insights/ 的 markdown

无第三方依赖。解析每个条目顶部 --- frontmatter --- 的 key: value。
"""
import os
import re
import sys
import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
SUBS = ["customers", "inquiries", "quotes", "products", "work-traces", "assets"]

# 类型 → 默认可投放平台（角度矩阵）
PLATFORM_MAP = {
    "customer": ["LinkedIn 观点长文", "IG 图文卡", "TikTok 15s", "网站 Blog/FAQ", "WhatsApp 目录"],
    "inquiry": ["网站 FAQ", "TikTok 15s", "LinkedIn 观点长文"],
    "quote": ["网站 报价洞察页", "LinkedIn", "Blog How-to"],
    "product": ["IG 实拍", "TikTok 15s", "WhatsApp 目录"],
    "insight": ["全平台"],
    "work-trace": ["LinkedIn 方法论", "网站 Blog", "社媒思维帖"],
    "asset": ["TikTok 选题库", "LinkedIn 话术帖", "网站 FAQ", "WhatsApp 话术库", "IG 图文卡"],
}

ACTIVE_STATUS = {"sample", "quoted", "negotiating", "lead"}


def parse_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    block = m.group(1)
    fm = {}
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if val == "":
            # 可能是块列表：- "item" 多行
            items = []
            j = i + 1
            while j < len(lines) and re.match(r"^\s*-\s+", lines[j]):
                item = re.sub(r"^\s*-\s+", "", lines[j]).strip().strip('"').strip("'")
                items.append(item)
                j += 1
            if items:
                fm[key] = items
                i = j
                continue
            fm[key] = ""
        elif val.startswith("[") and val.endswith("]"):
            items = [v.strip().strip('"').strip("'") for v in val[1:-1].split(",") if v.strip()]
            fm[key] = items
        elif val.lower() in ("true", "false"):
            fm[key] = val.lower() == "true"
        else:
            fm[key] = val.strip('"').strip("'")
        i += 1
    return fm


def load_entries():
    entries = []
    for sub in SUBS:
        d = os.path.join(BASE, sub)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".md") or fn.startswith("_") or fn.lower() == "readme.md":
                continue
            path = os.path.join(d, fn)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            fm = parse_frontmatter(text)
            if not fm:
                continue
            fm["_file"] = os.path.relpath(path, BASE)
            entries.append(fm)
    return entries


def main():
    week = "--week" in sys.argv
    markdown = "--markdown" in sys.argv
    entries = load_entries()

    print("=" * 70)
    print("  内容沉淀库 · 扫描报告  {}".format(datetime.date.today().isoformat()))
    print("=" * 70)

    # 1) 库存概览
    by_type = {}
    by_market = {}
    for e in entries:
        t = e.get("type", "?")
        by_type[t] = by_type.get(t, 0) + 1
        for mk in e.get("market", []):
            by_market[mk] = by_market.get(mk, 0) + 1
    print("\n[库存] 共 {} 条".format(len(entries)))
    print("  按类型: " + ", ".join("{}={}".format(k, v) for k, v in by_type.items()))
    print("  按市场: " + ", ".join("{}={}".format(k, v) for k, v in by_market.items()))

    # 2) 内容机会表
    rows = []
    for e in entries:
        anon_ok = e.get("anon_ok", False)
        if week and (not anon_ok or e.get("status") not in ACTIVE_STATUS):
            continue
        angles = e.get("content_angles", [])
        if isinstance(angles, str):
            angles = [angles]
        plats = PLATFORM_MAP.get(e.get("type", ""), ["网站"])
        link = (e.get("deep_links") or [""])[0]
        for ang in angles:
            rows.append({
                "code": e.get("code", "?"),
                "name": e.get("anon_name", "?"),
                "angle": ang,
                "plats": " / ".join(plats),
                "link": link,
                "anon_ok": anon_ok,
                "status": e.get("status", "?"),
            })

    print("\n[内容机会] 共 {} 条{}".format(len(rows), "（本周可写）" if week else ""))
    if markdown:
        print("\n## 扫描产出 · {}\n".format(datetime.date.today().isoformat()))
        for r in rows:
            flag = "✅可公开" if r["anon_ok"] else "🔒内部"
            print("- **[{}]** {} — {}  | {} | {} | {}".format(
                r["code"], r["name"], r["angle"], r["plats"], r["link"] or "—", flag))
    else:
        for r in rows:
            flag = "PUB" if r["anon_ok"] else "INT"
            print("  [{}] {:<22} {:<10} {}".format(flag, r["code"], r["status"], r["angle"]))
            print("        → 平台: {} | 内链: {}".format(r["plats"], r["link"] or "—"))

    # 3) 本周挑选建议
    if week and rows:
        print("\n[本周建议] 挑 1–2 条写（按状态优先级 sample > quoted > negotiating）：")
        prio = {"sample": 0, "quoted": 1, "negotiating": 2, "lead": 3}
        rows.sort(key=lambda r: prio.get(r["status"], 9))
        for r in rows[:3]:
            print("   • [{}] {} → {}".format(r["code"], r["name"], r["angle"]))

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
