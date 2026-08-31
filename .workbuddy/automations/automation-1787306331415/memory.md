# 每周引用率监控 — 执行记忆

## 自动化
- id: `automation-1787306331415`
- 名称: 每周引用率监控（小B/一件代发蓝海）
- 周期: 每周一 09:00（recurring）
- 范围: sourcetogulf.com 的 GEO 引用率，聚焦海湾小B/一件代发（低MOQ）蓝海细分

## 运行记录
### 2026-08-31（第 2 次运行）
- 动作: 对 16 个查询各跑 1 次 WebSearch（全部用 query_en，因 16 个查询均属海湾英文市场；无中文市场查询，故未用 query_zh）。
- 结果: sourcetogulf.com 在全部 16 个查询首页中均未出现 → cited=false ×16。
- 引用率: 0/16 = 0%，与基线周（2026-08-21，0/16=0%）持平，无新增引用、无变动。
- 日志: 向 `cite_monitor_log.jsonl` 追加 16 行（date=2026-08-31, engine=websearch, note="weekly monitor 2026-08-31"），snippet 记录各自 top-5 竞争者。
- 竞争者观察: 各查询首页被 accio、packjaki、laiyuegroup、supplierally、socooor 等"包装/采购代理"类站点占据——与 sourcetogulf 定位高度重叠，说明 GEO 内容缺口明显。
- 约束遵守: 仅观测+记录，未改站点内容、未运行 deploy.sh。

## 待办（需用户授权才执行）
- 若引用率持续 0%，建议内容动作：
  1) 针对这 16 个长尾查询发布海湾专属「sourcing+packaging+samples+低MOQ」能力落地页/博客，补足 GEO 可引用素材；
  2) 在每个落地页堆出"不是货代，是复合 SOURCING PARTNER"的明确定位语句，争取被 AI 引擎在相关查询中引用。

## 注意
- 自动化 memory 文件此前不存在，本次运行首次创建。
- 日志总量: 33 行（1 meta + 32 result）。
