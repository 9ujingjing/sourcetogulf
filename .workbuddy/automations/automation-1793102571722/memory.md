# STG 站点每周活跃维护 — 执行记录

## 2026-11-16 (第 1 次, 基线首跑)

- **健康**: 4 页 (主页/solutions/blog/ar) 全部 200 ✓
- **引用基线** (首次记录, 下周对比用):
  - "china sourcing agent UAE small MOQ private label" → sourcetogulf.com/partners.html **#2**, Goodfirms 档案 #3, Clutch 档案未进前 5
  - "white friday 2026 stocking guide china sourcing gulf small business" (当周主题) → sourcetogulf.com **未进前 5** (被中文跨境媒体/竞品博客占据)
- **本周更新**: 白五横条 3weeks→11 days 倒计时+空运窗口收尾措辞、斋月页横条加 checked 16 Nov 标注、两页 byline 刷至 16 Nov、sitemap.xml 修复 2 处乱码日期 (2026-11-0627/0620 → 2026-11-16, 疑似此前批量替换残留)
- **部署**: deploy.sh 成功, Pages built, IndexNow 4 URL HTTP 200, 线上横条内容已验证
- **工程坑 (记入手册 07 候选)**: ①手动只跑 build_blog.py 不跑 sync_header_footer.py 会看到 favicon 被删的假 diff — favicon 由 sync 脚本在构建链最后注入, 全链跑完即恢复; ②sitemap 批量替换日期时旧串未删净会拼成非法日期, 替换后应 grep 校验格式
- **下周建议**: 白五 (11-27) 后一周, 白五横条需改为"已开卖/最后补货空运"口径; 关注引用排名是否有变化
