---
# ===== 机器可读字段（frontmatter，给 scan_library.py 解析）=====
type: customer          # customer | inquiry | quote | product | insight
code: CHANGE-ME-YYYYMM  # 内部唯一码，如 SOGA-2026-09
anon_name: "匿名客户标签"   # 公开内容用的化名，绝不用真名/手机号/账号
market: [UAE]           # 目标市场：UAE / Saudi / Kuwait / Qatar / Bahrain / Oman
product: ["产品1", "产品2"]
source: WhatsApp        # 来源渠道
date: 2026-09-07
status: sample          # won | lost | negotiating | sample | quoted | lead
moq: "200-500"
fob_cny: "¥8-70/box"    # 出厂价区间
landed_aed: "AED 18-60/box"  # 到岸价区间（公开用区间）
pain_points: ["痛点1", "痛点2"]
our_value: ["composite sourcing", "low MOQ", "free logo", "7d sample"]
content_angles: ["角度1", "角度2", "角度3"]   # 每个=一个可写的内容方向
anon_ok: true           # 这个案例能否做成公开内容
compliance: []          # 合规风险：DG / ECAS / SFDA / AdvertiserPermit / 含酒精
media: []               # 素材文件名，如 ["soga-sample-01.jpg"]
deep_links: ["/services/custom-branding-packaging.html"]  # 可内链到站内的页面
notes: ""
---

# 标题（匿名）

> 正文写真实故事（匿名化）：客户是谁、痛点、我们怎么解决、结果。
> 这是内容提炼的「原料」，越具体越好，但**不出现客户真名/号码/账号**。
