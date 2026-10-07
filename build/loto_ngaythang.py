#!/usr/bin/env python3
"""Loto 5/35 — theo dõi kỹ quẻ ngày tháng (anh, 07/10/2026; kỳ 21h 07/10 thứ 4 ra 04 07 10 14 17 MM 07:
04=thứ, 07=ngày, 10=tháng, 14=thứ+tháng, 17=ngày+tháng → cả 5 số đều từ ngày giờ quay).
Từng thành phần riêng + các tổng, tách phiên 13h/21h, khung 10/20/50/100, 3 đoạn 100 kỳ, cả lịch sử. Số May Mắn trùng ngày tháng.
  python3 build/loto_ngaythang.py      # ghi build/loto_ngaythang.md"""
import json, os, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(os.path.join(HERE, 'all_data.json')))['loto535']; LUN = json.load(open(os.path.join(HERE, 'max3d_lunar.json')))
D, R, MM = A['dates'], [set(r) for r in A['res']], A['lk']; N = len(R); P = 5 / 35
def comp(ds):
    d = datetime.datetime.strptime(ds[:10], '%d/%m/%Y'); ld, lm, ly = LUN[ds[:10]]; th = d.weekday() + 2
    return {'Thứ (T2=2…CN=8)': [th], 'Ngày dương': [d.day], 'Tháng dương': [d.month], 'Năm (26)': [d.year % 100],
            'Ngày âm': [ld], 'Tháng âm': [lm], 'Năm âm (26)': [ly % 100],
            'Thứ + ngày': [th + d.day], 'Thứ + tháng': [th + d.month], 'Ngày + tháng': [d.day + d.month],
            'Thứ + ngày + tháng': [th + d.day + d.month], 'Ngày âm + tháng âm': [ld + lm],
            'NHÓM dương (thứ, ngày, tháng)': [th, d.day, d.month],
            'NHÓM dương + tổng (thứ, ngày, tháng, 3 tổng đôi)': [th, d.day, d.month, th + d.day, th + d.month, d.day + d.month],
            'NHÓM âm (ngày, tháng, tổng)': [ld, lm, ld + lm]}
def nxt(last):
    d = datetime.datetime.strptime(last[:10], '%d/%m/%Y')
    return (last[:10] + ' 21h') if '13h' in last else (d + datetime.timedelta(days=1)).strftime('%d/%m/%Y') + ' 13h'
nd = nxt(D[-1])
if nd[:10] not in LUN:
    import subprocess
    js = open(os.path.join(HERE, 'lunar.js'), encoding='utf-8').read() + f';const L=solar2lunar({int(nd[:2])},{int(nd[3:5])},{int(nd[6:10])});console.log(JSON.stringify([L.d,L.m,L.y]));'
    LUN[nd[:10]] = json.loads(subprocess.run(['node', '-e', js], capture_output=True, text=True, check=True).stdout)
    json.dump(LUN, open(os.path.join(HERE, 'max3d_lunar.json'), 'w'))
names = list(comp(D[-1]))
f = lambda h, n: f'{h / n * 100:.1f}%' if n else '–'
def rate(idx, nm):
    h = n = 0
    for t in idx:
        S = {x for x in comp(D[t])[nm] if 1 <= x <= 35}; n += len(S); h += len(S & R[t])
    return h, n
out = [f'# Loto — quẻ ngày tháng chi tiết ({N} kỳ, {D[0]} → {D[-1]})', '', f'Mỗi số ra bao nhiêu % (chia đều {P * 100:.1f}%). Số ngoài 1–35 bỏ qua.', '',
       '| Thành phần | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 3 đoạn 100 kỳ (gần→xa) | Cả LS | 13h (cả LS) | 21h (cả LS) | Kỳ tới |', '|' + '---|' * 10]
for nm in names:
    cells = [f(*rate(range(N - W, N), nm)) for W in (10, 20, 50, 100)]
    seg = ' · '.join(f(*rate(range(N - 100 * (i + 1), N - 100 * i), nm)) for i in range(3))
    s13 = f(*rate([t for t in range(N) if '13h' in D[t]], nm)); s21 = f(*rate([t for t in range(N) if '21h' in D[t]], nm))
    kt = ' '.join(f'{x:02d}' for x in sorted({x for x in comp(nd)[nm] if 1 <= x <= 35})) or '—'
    out.append(f'| {nm} | ' + ' | '.join(cells) + f' | {seg} | {f(*rate(range(N), nm))} | {s13} | {s21} | {kt} |')
# Số May Mắn trùng thứ / ngày / tháng (chỉ số 1–12)
def mmset(ds):
    c = comp(ds); return {x for k in ('Thứ (T2=2…CN=8)', 'Ngày dương', 'Tháng dương', 'Ngày âm', 'Tháng âm') for x in c[k] if 1 <= x <= 12}
def mmr(idx):
    h = e = 0
    for t in idx: S = mmset(D[t]); h += MM[t] in S; e += len(S) / 12
    return h, e
out += ['', '## Số May Mắn trùng thứ / ngày / tháng (dương, âm) — chỉ tính số 1–12', '', '| Khung | Trúng thực | Kỳ vọng ngẫu nhiên |', '|---|---|---|']
for nm, idx in (('50 kỳ', range(N - 50, N)), ('100 kỳ', range(N - 100, N)), ('200 kỳ', range(N - 200, N)), ('Cả lịch sử', range(N))):
    h, e = mmr(idx); out.append(f'| {nm} | {h} | {e:.1f} |')
out += ['', f'**Kỳ tới {nd}** (âm {LUN[nd[:10]][0]}/{LUN[nd[:10]][1]}): MM ngày tháng ' + ' '.join(f'{x:02d}' for x in sorted(mmset(nd))),
        '', 'Kỳ ra từ 3 số trở lên thuộc nhóm "dương + tổng": ' + '; '.join(
            f'{D[t]}: ' + ' '.join(f'{x:02d}' for x in sorted(R[t])) for t in range(N)
            if len({x for x in comp(D[t])['NHÓM dương + tổng (thứ, ngày, tháng, 3 tổng đôi)'] if 1 <= x <= 35} & R[t]) >= 3)]
open(os.path.join(HERE, 'loto_ngaythang.md'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
