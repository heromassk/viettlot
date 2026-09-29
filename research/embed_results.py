"""Nhúng research/results.json vào index.html (giữa /*RESEARCH_START*/ và /*RESEARCH_END*/).
Chạy sau: python3 research/report.py all 500 --json research/results.json"""
import json, os, re
ROOT = os.path.join(os.path.dirname(__file__), '..')
data = json.load(open(os.path.join(ROOT, 'research', 'results.json'), encoding='utf-8'))
for g in data['games'].values():  # bớt dung lượng: chỉ giữ tên cách lấy số, bỏ dấu cách thừa
    for k in g['recent']: k['links'] = {n: v for n, v in k['links'].items() if v}
cpath = os.path.join(ROOT, 'research', 'community.json')
if os.path.exists(cpath):   # kết quả các phương pháp cộng đồng (research/community.py --json)
    for g, rows in json.load(open(cpath, encoding='utf-8')).items():
        if g in data['games']: data['games'][g]['community'] = rows
rpath = os.path.join(ROOT, 'research', 'recency.json')
if os.path.exists(rpath):   # số nóng/lạnh, cặp hay về cùng theo mốc thời gian (research/recency.py --json)
    for g, rows in json.load(open(rpath, encoding='utf-8')).items():
        if g in data['games']: data['games'][g]['recency'] = rows
js = 'const RESEARCH = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';'
path = os.path.join(ROOT, 'index.html')
h = open(path, encoding='utf-8').read()
h, n = re.subn(r'/\*RESEARCH_START\*/.*?/\*RESEARCH_END\*/', lambda m: '/*RESEARCH_START*/' + js + '/*RESEARCH_END*/', h, flags=re.S)
assert n == 1, 'không tìm thấy vị trí nhúng'
open(path, 'w', encoding='utf-8').write(h)
print('đã nhúng', len(js), 'ký tự')
