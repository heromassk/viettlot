#!/usr/bin/env python3
"""Chấm sổ Max 3D+ / Pro khi có kết quả, rồi thêm kỳ đó vào dữ liệu.
  python3 build/max3d_cham.py plus|pro "dd/mm/yyyy" 20 bộ số theo thứ tự giải (ĐB 2, Nhất 4, Nhì 6, Ba 8)
Chấm: cặp gợi ý đã lưu (max3d_goiy_log.jsonl) trúng giải gì (lĩnh cả giải dưới), số bộ trúng nằm trong pool (so với kỳ vọng), 2 bộ ĐB có trong pool không.
Ghi: build/max3d_cham.jsonl; thêm kỳ vào max3d_data.json / max3dpro_data.json (nếu chưa có)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
g, date, R = sys.argv[1], sys.argv[2], sys.argv[3:]
assert len(R) == 20 and all(len(s) == 3 and s.isdigit() for s in R), 'cần đủ 20 bộ 3 chữ số'
PZ = {'plus': {'Đặc biệt': 1e9, 'Nhất': 40e6, 'Nhì': 10e6, 'Ba': 5e6, 'Tư': 1e6, 'Năm': 150e3, 'Sáu': 40e3},
      'pro': {'Đặc biệt': 2e9, 'Phụ Đặc biệt': 400e6, 'Nhất': 30e6, 'Nhì': 10e6, 'Ba': 4e6, 'Tư': 1e6, 'Năm': 100e3, 'Sáu': 40e3}}[g]
def prize(a, b):
    D, N, H, B = R[:2], R[2:6], R[6:12], R[12:]; o = []
    if g == 'pro':
        if a == D[0] and b == D[1]: o.append('Đặc biệt')
        if a == D[1] and b == D[0]: o.append('Phụ Đặc biệt')
    elif a in D and b in D: o.append('Đặc biệt')
    for n, grp in (('Nhất', N), ('Nhì', H), ('Ba', B)):
        if a in grp and b in grp: o.append(n)
    if a in R and b in R: o.append('Tư')
    o += ['Năm' for x in (a, b) if x in D]; o += ['Sáu' for x in (a, b) if x in N + H + B]
    return o, sum(PZ[n] for n in o)
log = [json.loads(l) for l in open(os.path.join(HERE, 'max3d_goiy_log.jsonl'), encoding='utf-8') if l.strip()]
gy = next((x for x in reversed(log) if x['game'] == g and x['next'] == date), None)
rec = dict(game=g, date=date, res=R)
if gy:
    P = set(gy.get('pool', [])); rec['pairs'] = []
    for x, k in zip(gy['pairs'], gy.get('kinds', [''] * len(gy['pairs']))):
        o, v = prize(*x); rec['pairs'].append(dict(x=x, kind=k, giai=o, tien=v))
    if P:
        rec['pool_n'] = len(P); rec['in_pool'] = sum(s in P for s in R); rec['ky_vong'] = round(20 * len(P) / 1000, 1); rec['db_in_pool'] = [s in P for s in R[:2]]
with open(os.path.join(HERE, 'max3d_cham.jsonl'), 'a', encoding='utf-8') as fo: fo.write(json.dumps(rec, ensure_ascii=False) + '\n')
f = os.path.join(HERE, 'max3d_data.json' if g == 'plus' else 'max3dpro_data.json'); D = json.load(open(f))
if date not in D['dates']:
    D['dates'].append(date); D['res'].append(R); D['ids'].append(D['ids'][-1] + 1); json.dump(D, open(f, 'w'))
print(json.dumps(rec, ensure_ascii=False, indent=1))
