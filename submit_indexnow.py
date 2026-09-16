# -*- coding: utf-8 -*-
"""
submit_indexnow.py — IndexNow 提交队列
读取 indexing_queue.json 的 pending URL，批量 POST 到 IndexNow，
成功(2xx)则移入 completed 并写回；失败保留在 pending 下次重试。

⚠️ 历史坑：本脚本原按 URL 去重，只要推过一次就永远不再推，
   导致「页面内容改了但搜索引擎不知道」。2026-09-16 起有两种解法：
     --changed  自动比对本地 HTML 内容哈希，只把改过的页重新入队（推荐）
     --force    手动强制重新入队指定 URL

用法: python3 submit_indexnow.py                 # 提交 pending
      python3 submit_indexnow.py --changed       # 把内容有变化的页重新入队
      python3 submit_indexnow.py --add URL...    # 追加 URL（已推过的会跳过）
      python3 submit_indexnow.py --add --force URL...   # 强制重新入队
      python3 submit_indexnow.py --changed --dry  # 只看哪些变了，不入队
"""
import glob
import hashlib
import json
import os
import sys
import urllib.request
import urllib.error

APP = os.path.dirname(os.path.abspath(__file__))
QUEUE = os.path.join(APP, 'indexing_queue.json')
KEY = '4327527604125695caa1f3a7041de8c9'
HOST = 'sourcetogulf.com'
KEY_LOC = 'https://sourcetogulf.com/%s.txt' % KEY
API = 'https://api.indexnow.org/indexnow'

def load():
    if not os.path.exists(QUEUE):
        return {'pending': [], 'completed': []}
    with open(QUEUE, encoding='utf-8') as f:
        d = json.load(f)
    d.setdefault('pending', [])
    d.setdefault('completed', [])
    d.setdefault('hashes', {})      # url -> 本地文件 md5，用于感知内容变化
    return d

def save(d):
    with open(QUEUE, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)

def add_url(url, force=False):
    d = load()
    if force:
        # 强制：从 completed 移除并重新入队，用于内容已更新、需要再次推送
        if url not in d['pending']:
            d['pending'].append(url)
        d['completed'] = [u for u in d['completed'] if u != url]
        save(d)
        print('+ force queued:', url)
    elif url not in d['pending'] and url not in d['completed']:
        d['pending'].append(url)
        save(d)
        print('+ queued:', url)
    else:
        print('= already queued/sent (use --force to resend):', url)


# ---------------------------------------------------------------- 内容变化感知

def file_md5(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def local_pages():
    """扫描本地 HTML，映射成线上 URL → 内容 md5。
    quote/<客户>/ 是 noindex 的客户专属报价页，不参与推送。"""
    out = {}
    for p in glob.glob(os.path.join(APP, '**', '*.html'), recursive=True):
        rel = os.path.relpath(p, APP).replace(os.sep, '/')
        if rel.startswith('quote/'):
            continue
        if rel == 'index.html':
            url = 'https://%s/' % HOST
        elif rel.endswith('/index.html'):
            url = 'https://%s/%s' % (HOST, rel[:-len('index.html')])
        else:
            url = 'https://%s/%s' % (HOST, rel)
        out[url] = file_md5(p)
    return out


def queue_changed(dry=False):
    d = load()
    pages = local_pages()
    hashes = d['hashes']
    if not hashes:
        # 首次运行：只记录基线，不把全站当成「改过」，避免一次性狂推
        d['hashes'] = pages
        save(d)
        print('= baseline recorded for %d page(s). run again after edits to detect changes.'
              % len(pages))
        return 0
    changed = sorted(u for u, h in pages.items() if hashes.get(u) != h)
    if not changed:
        print('= no page content changed since last run.')
        return 0
    for u in changed:
        print('%s %s' % ('~' if dry else '+', u))
    if dry:
        print('(dry run — %d page(s) would be re-queued)' % len(changed))
        return len(changed)
    for u in changed:
        if u not in d['pending']:
            d['pending'].append(u)
        d['completed'] = [x for x in d['completed'] if x != u]
    d['hashes'].update(pages)
    save(d)
    print('+ queued %d changed page(s). run without args to submit.' % len(changed))
    return len(changed)

def submit():
    d = load()
    pending = d['pending']
    if not pending:
        print('queue empty, nothing to submit.')
        return 0
    body = json.dumps({
        'host': HOST,
        'key': KEY,
        'keyLocation': KEY_LOC,
        'urlList': pending
    }).encode('utf-8')
    req = urllib.request.Request(API, data=body, headers={'Content-Type': 'application/json; charset=utf-8'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            code = r.getcode()
            resp = r.read().decode('utf-8', 'ignore')
    except urllib.error.HTTPError as e:
        code = e.code
        resp = e.read().decode('utf-8', 'ignore') if e.fp else ''
    except Exception as e:
        print('! submit error:', e)
        return len(pending)
    print('IndexNow HTTP %s — %s' % (code, resp[:120]))
    if 200 <= code < 300:
        done = set(pending)
        d['completed'] = list(dict.fromkeys(d['completed'] + pending))
        d['pending'] = [u for u in d['pending'] if u not in done]
        save(d)
        print('✓ moved %d URL(s) to completed.' % len(pending))
        return 0
    else:
        print('! kept %d URL(s) in pending for retry.' % len(pending))
        return len(pending)

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == '--changed':
        queue_changed(dry='--dry' in a)
    elif a and a[0] == '--add':
        force = '--force' in a
        urls = [x for x in a[1:] if not x.startswith('--')]
        if not urls:
            print('用法: submit_indexnow.py --add [--force] URL...')
        for u in urls:
            add_url(u, force=force)
    else:
        submit()
