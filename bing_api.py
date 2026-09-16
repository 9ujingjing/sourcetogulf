# -*- coding: utf-8 -*-
"""
bing_api.py — Bing Webmaster Tools API 客户端（JSON 接口，v2026-09）

用途：把 Bing 站长后台的数据拉到本地 + 批量提交 URL，替代手工点后台。

取 API Key（一次，永久有效）：
    https://www.bing.com/webmasters → Settings → API Access → Generate API Key
Key 存放位置（三选一，按优先级）：
    1) 环境变量 BING_API_KEY
    2) ~/.workbuddy/secrets/bing_api_key.txt      ← 推荐，仓库外，不会误提交
    3) <repo>/growth/.bing-api-key                ← 已在 .gitignore 中

用法:
    python3 bing_api.py sites            # 列出已验证的站点
    python3 bing_api.py quota            # 今日剩余提交配额
    python3 bing_api.py stats            # 站点流量总览
    python3 bing_api.py queries [n]      # 查询词（默认前 50）
    python3 bing_api.py pages [n]        # 页面级流量（默认前 50）
    python3 bing_api.py crawl            # 爬取统计
    python3 bing_api.py submit URL...    # 提交指定 URL
    python3 bing_api.py submit --sitemap # 提交 sitemap.xml 里全部 URL
    python3 bing_api.py report           # 全部数据 → growth/bing-report-YYYY-MM-DD.md

注意：API 不提供「逐个 URL 是否已收录」——那只能在站长后台 Index Explorer
     看，或点右上角 Download 导出 CSV。API 给的是流量/爬取/配额/提交。
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime

APP = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://sourcetogulf.com/'
BASE = 'https://ssl.bing.com/webmaster/api.svc/json/'
KEY_PATHS = [
    os.path.expanduser('~/.workbuddy/secrets/bing_api_key.txt'),
    os.path.join(APP, 'growth', '.bing-api-key'),
]
MAX_BATCH = 500          # Bing 单次 SubmitUrlBatch 上限


def get_key():
    k = os.environ.get('BING_API_KEY', '').strip()
    if k:
        return k
    for p in KEY_PATHS:
        if os.path.exists(p):
            with open(p, encoding='utf-8') as f:
                k = f.read().strip()
            if k:
                return k
    sys.exit(
        '找不到 Bing API Key。\n'
        '  1) 打开 https://www.bing.com/webmasters → Settings → API Access → Generate API Key\n'
        '  2) 把 Key 存到 %s\n'
        '     （或设置环境变量 BING_API_KEY）' % KEY_PATHS[0]
    )


def call(endpoint, params=None, body=None):
    """调用 JSON API。GET 传 params，POST 传 body(dict)。返回 d 字段。"""
    key = get_key()
    q = urllib.parse.urlencode({'apikey': key})
    url = '%s%s?%s' % (BASE, endpoint, q)
    data = None
    headers = {'User-Agent': 'BingWebmasterTools/1.0'}
    if body is not None:
        data = json.dumps(body).encode('utf-8')
        headers['Content-Type'] = 'application/json; charset=utf-8'
    if params:
        url += '&' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, data=data, headers=headers,
                                 method='POST' if data else 'GET')
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode('utf-8', 'ignore')
    except urllib.error.HTTPError as e:
        raw = e.read().decode('utf-8', 'ignore') if e.fp else ''
        sys.exit('HTTP %s — %s\n%s' % (e.code, endpoint, raw[:400]))
    except Exception as e:
        sys.exit('请求失败 %s — %s' % (endpoint, e))
    if not raw.strip():
        return None
    try:
        return json.loads(raw).get('d', json.loads(raw))
    except ValueError:
        sys.exit('返回非 JSON：%s' % raw[:300])


def dnet(s):
    """/Date(1788480000000)/ → 2026-09-02（Bing 用 .NET 日期格式）"""
    import re
    m = re.search(r'/Date\((\d+)', s or '')
    if not m:
        return (s or '')[:10]
    return datetime.fromtimestamp(int(m.group(1)) / 1000).strftime('%Y-%m-%d')


def sitemap_urls():
    """读本地 sitemap.xml 的 URL 列表。"""
    path = os.path.join(APP, 'sitemap.xml')
    if not os.path.exists(path):
        sys.exit('找不到 sitemap.xml')
    with open(path, encoding='utf-8') as f:
        txt = f.read()
    urls = []
    for chunk in txt.split('<loc>')[1:]:
        u = chunk.split('</loc>')[0].strip()
        if u:
            urls.append(u)
    return urls


# ---------------------------------------------------------------- 子命令

def cmd_sites():
    for s in call('GetUserSites') or []:
        print('%-40s verified=%s' % (s.get('Url'), s.get('IsVerified')))


def cmd_quota():
    d = call('GetUrlSubmissionQuota', {'siteUrl': SITE}) or {}
    print('今日剩余配额 DailyQuota  = %s' % d.get('DailyQuota'))
    print('本月剩余配额 MonthlyQuota = %s' % d.get('MonthlyQuota'))


def _table(rows, cols, limit):
    if not rows:
        print('(无数据)')
        return
    for r in rows[:limit]:
        cells = [dnet(r[c]) if c == 'Date' else str(r.get(c, '')) for c in cols]
        print('  ' + ' | '.join(cells))


def cmd_stats():
    d = call('GetRankAndTrafficStats', {'siteUrl': SITE}) or []
    _table(d, ['Date', 'Clicks', 'Impressions'], 60)


def cmd_queries(limit=50):
    d = call('GetQueryStats', {'siteUrl': SITE}) or []
    d = sorted(d, key=lambda x: -(x.get('Impressions') or 0))
    _table(d, ['Query', 'Clicks', 'Impressions', 'AvgImpressionPosition'], limit)


def cmd_pages(limit=50):
    # 注意：Bing 的 GetPageStats 返回对象里，页面 URL 放在 Query 字段（API 历史遗留）
    d = call('GetPageStats', {'siteUrl': SITE}) or []
    d = sorted(d, key=lambda x: -(x.get('Impressions') or 0))
    _table(d, ['Query', 'Clicks', 'Impressions'], limit)


def cmd_crawl():
    d = call('GetCrawlStats', {'siteUrl': SITE}) or []
    _table(d, ['Date', 'CrawledPages', 'CrawlErrors', 'InIndex', 'BlockedByRobotsTxt'], 60)


def cmd_submit(urls):
    if not urls:
        sys.exit('没有要提交的 URL')
    ok = 0
    for i in range(0, len(urls), MAX_BATCH):
        chunk = urls[i:i + MAX_BATCH]
        call('SubmitUrlBatch', body={'siteUrl': SITE, 'urlList': chunk})
        ok += len(chunk)
        print('  已提交 %d/%d' % (ok, len(urls)))
    print('✅ 共提交 %d 条（每日上限 10,000）' % ok)


def cmd_report():
    out = []
    out.append('# Bing 站长数据 — %s\n' % date.today().isoformat())
    out.append('站点：%s\n' % SITE)

    q = call('GetUrlSubmissionQuota', {'siteUrl': SITE}) or {}
    out.append('## 提交配额\n- 今日剩余：%s\n- 本月剩余：%s\n'
               % (q.get('DailyQuota'), q.get('MonthlyQuota')))

    st = call('GetRankAndTrafficStats', {'siteUrl': SITE}) or []
    if st:
        tc = sum(x.get('Clicks') or 0 for x in st)
        ti = sum(x.get('Impressions') or 0 for x in st)
        out.append('## 流量合计（全部历史）\n- 点击 %d\n- 曝光 %d\n' % (tc, ti))
        out.append('### 最近 14 天\n')
        out.append('| 日期 | 点击 | 曝光 |\n|---|---|---|')
        for x in st[-14:]:
            out.append('| %s | %s | %s |' % (dnet(x.get('Date')),
                                             x.get('Clicks'), x.get('Impressions')))
        out.append('')

    qs = call('GetQueryStats', {'siteUrl': SITE}) or []
    qs = sorted(qs, key=lambda x: -(x.get('Impressions') or 0))[:30]
    if qs:
        out.append('## 热门查询词 Top 30\n')
        out.append('| 查询词 | 点击 | 曝光 | 平均排名 |\n|---|---|---|---|')
        for x in qs:
            out.append('| %s | %s | %s | %s |' % (
                x.get('Query'), x.get('Clicks'), x.get('Impressions'),
                x.get('AvgImpressionPosition')))
        out.append('')

    ps = call('GetPageStats', {'siteUrl': SITE}) or []
    ps = sorted(ps, key=lambda x: -(x.get('Impressions') or 0))[:30]
    if ps:
        out.append('## 有流量的页面 Top 30\n')
        out.append('| 页面 | 点击 | 曝光 |\n|---|---|---|')
        for x in ps:
            out.append('| %s | %s | %s |' % (x.get('Query'), x.get('Clicks'),
                                             x.get('Impressions')))
        out.append('')

    cs = call('GetCrawlStats', {'siteUrl': SITE}) or []
    if cs:
        out.append('## 爬取统计（最近 14 天）\n')
        out.append('| 日期 | 已爬 | 错误 | 索引中 | 2xx | 301 | 4xx | 5xx | robots 拦截 |\n'
                   '|---|---|---|---|---|---|---|---|---|')
        for x in cs[-14:]:
            out.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                dnet(x.get('Date')), x.get('CrawledPages'), x.get('CrawlErrors'),
                x.get('InIndex'), x.get('Code2xx'), x.get('Code301'),
                x.get('Code4xx'), x.get('Code5xx'), x.get('BlockedByRobotsTxt')))
        out.append('')

    path = os.path.join(APP, 'growth', 'bing-report-%s.md' % date.today().isoformat())
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    print('✅ 报告已写入 %s' % path)


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return
    c = a[0]
    if c == 'sites':
        cmd_sites()
    elif c == 'quota':
        cmd_quota()
    elif c == 'stats':
        cmd_stats()
    elif c == 'queries':
        cmd_queries(int(a[1]) if len(a) > 1 else 50)
    elif c == 'pages':
        cmd_pages(int(a[1]) if len(a) > 1 else 50)
    elif c == 'crawl':
        cmd_crawl()
    elif c == 'submit':
        if len(a) > 1 and a[1] == '--sitemap':
            urls = sitemap_urls()
            print('从 sitemap.xml 读到 %d 条 URL' % len(urls))
            cmd_submit(urls)
        else:
            cmd_submit(a[1:])
    elif c == 'report':
        cmd_report()
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
