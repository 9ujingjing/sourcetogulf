# -*- coding: utf-8 -*-
"""
submit_indexnow.py — IndexNow 提交队列
读取 indexing_queue.json 的 pending URL，批量 POST 到 IndexNow，
成功(2xx)则移入 completed 并写回；失败保留在 pending 下次重试。
用法: python3 submit_indexnow.py            # 提交 pending
      python3 submit_indexnow.py --add URL   # 往 pending 追加一个 URL
"""
import json, os, sys, urllib.request, urllib.error

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
    return d

def save(d):
    with open(QUEUE, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)

def add_url(url):
    d = load()
    if url not in d['pending'] and url not in d['completed']:
        d['pending'].append(url)
        save(d)
        print('+ queued:', url)
    else:
        print('= already queued/sent:', url)

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
    if len(sys.argv) > 1 and sys.argv[1] == '--add':
        for u in sys.argv[2:]:
            add_url(u)
    else:
        submit()
