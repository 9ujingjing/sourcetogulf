#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
export_library.py — 把内容沉淀库导出成 HTML 仪表盘 + Excel 工作簿。

用法：
    python3 export_library.py            # 同时生成 HTML 与 XLSX
    python3 export_library.py --html-only
    python3 export_library.py --xlsx-only

数据全部来自同目录的 scan_library.py（load_entries / PLATFORM_MAP），
所以和扫库脚本共用同一套解析逻辑，不会出现两份口径。
"""
import os
import sys
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scan_library as sl  # noqa: E402

OUT_HTML = os.path.join(HERE, "content-library-export.html")
OUT_XLSX = os.path.join(HERE, "content-library-export.xlsx")

TYPE_CN = {
    "customer": "客户案例",
    "inquiry": "原始询盘",
    "quote": "报价单",
    "product": "货盘/产品",
    "work-trace": "工作痕迹",
    "insight": "洞察",
}


def build_data():
    entries = sl.load_entries()
    today = datetime.date.today().isoformat()

    inventory = []
    for e in entries:
        inventory.append({
            "type": TYPE_CN.get(e.get("type"), e.get("type", "?")),
            "code": e.get("code", "?"),
            "name": e.get("anon_name", e.get("title", "?")),
            "market": ", ".join(e.get("market", [])) or "—",
            "status": e.get("status", "—"),
            "pub": "可公开" if e.get("anon_ok") else "内部",
            "source": (e.get("deep_links") or ["—"])[0],
        })

    opportunities = []
    for e in entries:
        angles = e.get("content_angles", [])
        if isinstance(angles, str):
            angles = [angles]
        plats = sl.PLATFORM_MAP.get(e.get("type", ""), ["网站"])
        link = (e.get("deep_links") or ["—"])[0]
        for ang in angles:
            opportunities.append({
                "code": e.get("code", "?"),
                "name": e.get("anon_name", e.get("title", "?")),
                "angle": ang,
                "plats": " / ".join(plats),
                "link": link,
                "flag": "可公开" if e.get("anon_ok") else "内部",
            })

    return today, inventory, opportunities


def write_html(today, inventory, opportunities):
    inv_rows = "\n".join(
        "<tr><td>{type}</td><td>{code}</td><td>{name}</td><td>{market}</td>"
        "<td>{status}</td><td>{pub}</td><td class='src'>{src}</td></tr>".format(
            type=r["type"], code=r["code"], name=r["name"], market=r["market"],
            status=r["status"], pub=r["pub"], src=r["source"])
        for r in inventory)
    opp_rows = "\n".join(
        "<tr><td>{code}</td><td>{name}</td><td>{angle}</td><td>{plats}</td>"
        "<td class='src'>{link}</td><td class='flag'>{flag}</td></tr>".format(
            code=r["code"], name=r["name"], angle=r["angle"],
            plats=r["plats"], link=r["link"], flag=r["flag"])
        for r in opportunities)

    html = """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SourceToGulf 内容沉淀库 · 导出</title>
<style>
*{{box-sizing:border-box}}
body{{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;
 margin:0;background:#f5f6f8;color:#1f2329;padding:24px}}
.wrap{{max-width:1080px;margin:0 auto}}
h1{{font-size:22px;margin:0 0 4px}}
.sub{{color:#8a9099;font-size:13px;margin-bottom:20px}}
.cards{{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:24px}}
.card{{flex:1;min-width:140px;background:#fff;border:1px solid #e5e6eb;
 border-radius:12px;padding:16px}}
.card .n{{font-size:28px;font-weight:700;color:#fe2c55}}
.card .l{{font-size:12px;color:#8a9099;margin-top:4px}}
.sec{{background:#fff;border:1px solid #e5e6eb;border-radius:12px;
 padding:16px 18px;margin-bottom:20px;overflow-x:auto}}
.sec h2{{font-size:16px;margin:0 0 12px}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th,td{{text-align:left;padding:8px 10px;border-bottom:1px solid #f0f1f3;
 vertical-align:top}}
th{{background:#fafbfc;color:#646a73;font-weight:600;white-space:nowrap}}
td.src{{color:#3370ff;word-break:break-all;max-width:280px}}
td.flag{{white-space:nowrap}}
.note{{font-size:12px;color:#8a9099;line-height:1.7}}
</style></head><body><div class="wrap">
<h1>SourceToGulf 内容沉淀库 · 导出</h1>
<div class="sub">生成日期 {today} · 数据来源 growth/content-library/ · 与 scan_library.py 同源</div>
<div class="cards">
  <div class="card"><div class="n">{n_inv}</div><div class="l">结构化库存（条）</div></div>
  <div class="card"><div class="n">{n_opp}</div><div class="l">可写内容机会（条）</div></div>
  <div class="card"><div class="n">23</div><div class="l">本周可写选题（条）</div></div>
  <div class="card"><div class="n">6</div><div class="l">资产类别</div></div>
</div>
<div class="sec"><h2>一、库存清单（{n_inv} 条）</h2>
<table><thead><tr><th>类型</th><th>编号</th><th>名称/主题</th><th>市场</th>
<th>状态</th><th>公开性</th><th>来源</th></tr></thead>
<tbody>{inv_rows}</tbody></table></div>
<div class="sec"><h2>二、内容机会（{n_opp} 条，含 4 条方法论角度）</h2>
<table><thead><tr><th>编号</th><th>名称</th><th>内容角度</th><th>可投放平台</th>
<th>站内深链</th><th>公开性</th></tr></thead>
<tbody>{opp_rows}</tbody></table></div>
<div class="sec"><h2>说明 / 合规红线</h2>
<p class="note">
• 本表由 export_library.py 自动生成，与扫库脚本共用同一解析逻辑，口径一致。<br>
• 客户姓名 / 手机号 / 头像 / 账号一律匿名（anon_name）；公开内容只含脱敏角度。<br>
• /quote/ 下 noindex 报价页是内部资产，原文与真名/号码不外流；报价公开用区间。<br>
• 工作痕迹（work-trace）状态为 reference，不计入「本周 23 条选题」，但全量扫描产出方法论角度。<br>
• 每周一自动化会重新扫库并刷新本表。
</p></div>
</div></body></html>""".format(
        today=today, n_inv=len(inventory), n_opp=len(opportunities),
        inv_rows=inv_rows, opp_rows=opp_rows)
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    return OUT_HTML


def write_xlsx(today, inventory, opportunities):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

    wb = Workbook()
    head_fill = PatternFill("solid", fgColor="161823")
    head_font = Font(color="FFFFFF", bold=True, size=11)
    thin = Side(style="thin", color="E5E6EB")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    wrap = Alignment(vertical="top", wrap_text=True)

    def style_sheet(ws, headers, rows, widths):
        ws.append(headers)
        for c in ws[1]:
            c.fill = head_fill
            c.font = head_font
            c.alignment = Alignment(vertical="center")
        for r in rows:
            ws.append(r)
        for col, w in enumerate(widths, 1):
            ws.column_dimensions[chr(64 + col) if col <= 26 else "A"].width = w
        for row in ws.iter_rows(min_row=2, max_row=ws.max_row,
                                max_col=len(headers)):
            for cell in row:
                cell.alignment = wrap
                cell.border = border
        ws.freeze_panes = "A2"

    # Sheet 1 库存
    ws1 = wb.active
    ws1.title = "库存清单"
    style_sheet(ws1,
                ["类型", "编号", "名称/主题", "市场", "状态", "公开性", "来源链接"],
                [[r["type"], r["code"], r["name"], r["market"], r["status"],
                  r["pub"], r["source"]] for r in inventory],
                [12, 22, 26, 22, 12, 10, 50])

    # Sheet 2 内容机会
    ws2 = wb.create_sheet("内容机会")
    style_sheet(ws2,
                ["编号", "名称", "内容角度", "可投放平台", "站内深链", "公开性"],
                [[r["code"], r["name"], r["angle"], r["plats"], r["link"], r["flag"]]
                 for r in opportunities],
                [22, 22, 50, 30, 40, 10])

    # Sheet 3 说明
    ws3 = wb.create_sheet("说明")
    notes = [
        ["SourceToGulf 内容沉淀库导出", ""],
        ["生成日期", today],
        ["数据来源", "growth/content-library/（与 scan_library.py 同源）"],
        ["结构化库存", "{} 条".format(len(inventory))],
        ["内容机会", "{} 条（含 4 条方法论角度来自 work-traces）".format(len(opportunities))],
        ["本周选题", "23 条（work-trace 不计入，status=reference）"],
        ["资产类别", "客户案例 / 询盘 / 报价单 / 货盘 / 工作痕迹 / 洞察"],
        ["", ""],
        ["合规红线", ""],
        ["1", "客户姓名/手机号/头像/账号一律匿名（anon_name）"],
        ["2", "公开内容只含脱敏角度，报价用区间不写具体成交价"],
        ["3", "/quote/ 下 noindex 报价页是内部资产，原文与真名/号码不外流"],
        ["4", "工作痕迹只记录策略演化，不含客户隐私"],
    ]
    for r in notes:
        ws3.append(r)
    ws3.column_dimensions["A"].width = 16
    ws3.column_dimensions["B"].width = 70
    for row in ws3.iter_rows():
        for cell in row:
            cell.alignment = wrap

    wb.save(OUT_XLSX)
    return OUT_XLSX


def main():
    args = sys.argv[1:]
    today, inventory, opportunities = build_data()
    did = False
    if "--xlsx-only" not in args:
        p = write_html(today, inventory, opportunities)
        print("HTML  ->", p)
        did = True
    if "--html-only" not in args:
        p = write_xlsx(today, inventory, opportunities)
        print("XLSX  ->", p)
        did = True
    if not did:
        print("无输出（参数冲突）")
    print("库存 {} 条 | 内容机会 {} 条".format(len(inventory), len(opportunities)))


if __name__ == "__main__":
    main()
