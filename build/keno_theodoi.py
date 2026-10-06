#!/usr/bin/env python3
"""Sổ theo dõi Keno (anh, 05/10/2026: "lập đi") — chấm từng kỳ: số đang ra liền / nóng / vắng thì kỳ sau có ra tiếp không.
Chuẩn: mỗi số ra 25%. Muốn bậc 9 hòa vốn nhờ 9/9 thì mỗi số chọn phải ra ~32% → nhóm nào cộng dồn ≥30% (đủ mẫu, z ≥ 3) mới là dấu vết đáng chơi.
Sổ chỉ chấm kỳ SAU ngày lập (id > 298145, sáng 05/10/2026) — cộng dồn theo ngày, không sửa lùi. So thêm 1000 / 5000 kỳ / cả lịch sử.
Dữ liệu: kho vietvudanh/vietlott-data (lay_kq.py tự gọi script này sau khi cập nhật kho; kho bị trùng dòng → đã bỏ trùng).
  python3 build/keno_theodoi.py        # cập nhật sổ + in báo cáo (ghi build/keno_theodoi.json, build/keno_theodoi.md)"""
import json, os, numpy as np
B = os.path.dirname(os.path.abspath(__file__))
SRC = '/home/user/vietvudanh/vietlott-data/data/keno.jsonl'; SO = os.path.join(B, 'keno_theodoi.json'); MD = os.path.join(B, 'keno_theodoi.md')
START = 298145
D = [json.loads(l) for l in open(SRC) if l.strip()]
D = list({d['id']: d for d in D}.values()); D.sort(key=lambda d: int(d['id'].lstrip('#')))
ID = np.array([int(d['id'].lstrip('#')) for d in D])
X = np.zeros((len(D), 80), bool)
for i, d in enumerate(D): X[i, np.array(d['result']) - 1] = True
N = len(X)
C = np.vstack([np.zeros(80, int), np.cumsum(X, 0)])
run = np.zeros((N + 1, 80), int)          # run[t] = đang ra liền bao nhiêu kỳ tính đến kỳ t-1
for t in range(N): run[t + 1] = np.where(X[t], run[t] + 1, 0)
NHOM = {  # tên → hàm chọn số trước kỳ t
    'ra liền 1 kỳ': lambda t: run[t] == 1, 'ra liền 2 kỳ': lambda t: run[t] == 2, 'ra liền 3 kỳ': lambda t: run[t] == 3,
    'ra liền 4 kỳ': lambda t: run[t] == 4, 'ra liền ≥5 kỳ': lambda t: run[t] >= 5,
    'ra ≥5 lần / 10 kỳ': lambda t: C[t] - C[t - 10] >= 5, 'ra 4 lần / 10 kỳ': lambda t: C[t] - C[t - 10] == 4,
    'vắng cả 10 kỳ': lambda t: C[t] - C[t - 10] == 0,
    'ngoài 3 kỳ gần (loại 3 kỳ)': lambda t: C[t] - C[t - 3] == 0, 'ngoài 5 kỳ gần (loại 5 kỳ)': lambda t: C[t] - C[t - 5] == 0,
}
def dem(ts):
    out = {}
    for k, f in NHOM.items():
        h = n = 0
        for t in ts:
            m = f(t); h += int(X[t][m].sum()); n += int(m.sum())
        out[k] = [h, n]
    return out
so = json.load(open(SO)) if os.path.exists(SO) else {'start_id': START, 'last_id': START, 'ngay': {}}
moi = [t for t in range(10, N) if ID[t] > so['last_id']]
for t in moi:   # cộng dồn theo ngày
    day = so['ngay'].setdefault(D[t]['date'], {}); day.setdefault('_ky', 0); day['_ky'] += 1
    for k in NHOM: day.setdefault(k, [0, 0])
    for k, f in NHOM.items():
        m = f(t); day[k][0] += int(X[t][m].sum()); day[k][1] += int(m.sum())
if moi: so['last_id'] = int(ID[moi[-1]])
json.dump(so, open(SO, 'w'), ensure_ascii=False, indent=1)
tong = {k: [sum(v.get(k, [0, 0])[0] for v in so['ngay'].values()), sum(v.get(k, [0, 0])[1] for v in so['ngay'].values())] for k in NHOM}
nky = sum(v['_ky'] for v in so['ngay'].values())
def pct(h, n): return f'{h / n * 100:.1f}%' if n else '–'
def z(h, n): return (h - .25 * n) / np.sqrt(n * .25 * .75) if n else 0
def nhan(h, n):
    if n < 200: return 'chưa đủ mẫu'
    r, zz = h / n, z(h, n)
    if r >= .30 and zz >= 3: return '**ĐÁNG CHÚ Ý — nghiêng mạnh**'
    if zz >= 2: return 'nhỉnh, theo dõi'
    if zz <= -2: return 'thấp hơn TB'
    return 'như ngẫu nhiên'
B1, B5, BA = dem(range(N - 1000, N)), dem(range(N - 5000, N)), None
L = [f'# Sổ theo dõi Keno — lập 05/10/2026 (sau kỳ #{START})', '',
     f'Kho có đến kỳ {D[-1]["id"]} ({D[-1]["date"]}). Sổ đã chấm **{nky} kỳ** sau ngày lập. Chuẩn 25%; cần ~32% ổn định mới đáng chơi (bậc 9 hòa vốn).', '',
     '| Nhóm (trước kỳ) | Sổ cộng dồn | Số lượt | z | 1000 kỳ gần | 5000 kỳ | Nhận định |', '|---|---|---|---|---|---|---|']
for k in NHOM:
    h, n = tong[k]
    L.append(f'| {k} | {pct(h, n)} | {n} | {z(h, n):+.1f} | {pct(*B1[k])} | {pct(*B5[k])} | {nhan(h, n)} |')
L += ['', '## Theo ngày (tỉ lệ ra tiếp)', '', '| Ngày | Kỳ | ' + ' | '.join(NHOM) + ' |', '|' + '---|' * (len(NHOM) + 2)]
for d, v in sorted(so['ngay'].items()):
    L.append(f'| {d} | {v["_ky"]} | ' + ' | '.join(f'{pct(*v.get(k, [0, 0]))} ({v.get(k, [0, 0])[1]})' for k in NHOM) + ' |')
t = N  # số đang theo dõi cho kỳ kế tiếp
L += ['', f'## Đang ra liền sau kỳ {D[-1]["id"]} (để anh theo dõi kỳ kế)', '']
for L0 in range(run[t].max(), 2, -1):
    s = np.flatnonzero(run[t] == L0) + 1
    if len(s): L.append(f'- ra liền {L0} kỳ: ' + ' '.join(f'{n:02d}' for n in s))
open(MD, 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
