#!/usr/bin/env python3
"""Theo dõi quẻ NGÀY THÁNG (anh, 07/10/2026: Loto 21h 07/10 thứ 4 ra 04 07 10, MM 07).
Mỗi kỳ lấy các số: dương lịch (thứ T2=2…T7=7, CN=8; ngày; tháng; năm 2 số cuối) và âm lịch (ngày, tháng, năm 2 số cuối),
chỉ giữ số nằm trong dải của trò. Chấm: mỗi số trong nhóm ra bao nhiêu % (chia đều KB/NB), số kỳ ra ≥2 / ≥3 số của nhóm
so với ngẫu nhiên (siêu bội). Khung 50/100 kỳ, 3 đoạn 100 kỳ, cả lịch sử. In số của kỳ tới.
  python3 build/ngaythang.py          # ghi build/ngaythang.md"""
import json, os, datetime, subprocess
from math import comb
HERE = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(os.path.join(HERE, 'all_data.json')))
LF = os.path.join(HERE, 'max3d_lunar.json'); LUN = json.load(open(LF))
def lunar_many(ds):
    need = [d for d in ds if d not in LUN]
    if need:
        js = open(os.path.join(HERE, 'lunar.js'), encoding='utf-8').read() + ';const o={};' + ''.join(
            f'{{const L=solar2lunar({int(d[:2])},{int(d[3:5])},{int(d[6:10])});o["{d}"]=[L.d,L.m,L.y];}}' for d in need) + 'console.log(JSON.stringify(o));'
        LUN.update(json.loads(subprocess.run(['node', '-e', js], capture_output=True, text=True, check=True).stdout))
        json.dump(LUN, open(LF, 'w'))
GAMES = {'power': ('power655', 55, 6, (1, 3, 5)), 'mega': ('mega645', 45, 6, (2, 4, 6)), 'loto': ('loto535', 35, 5, None)}
def sets(ds, NB):
    d = datetime.datetime.strptime(ds[:10], '%d/%m/%Y'); ld, lm, ly = LUN[ds[:10]]
    ok = lambda xs: {x for x in xs if 1 <= x <= NB}
    return {'Dương: thứ–ngày–tháng': ok((d.weekday() + 2, d.day, d.month)),
            'Dương + năm (26)': ok((d.weekday() + 2, d.day, d.month, d.year % 100)),
            'Âm: ngày–tháng': ok((ld, lm)),
            'Âm + năm': ok((ld, lm, ly % 100)),
            'Tất cả (dương + âm + năm)': ok((d.weekday() + 2, d.day, d.month, d.year % 100, ld, lm, ly % 100))}
def nxt(game, last):
    d = datetime.datetime.strptime(last[:10], '%d/%m/%Y')
    if game == 'loto': return (last[:10] + ' 21h') if '13h' in last else (d + datetime.timedelta(days=1)).strftime('%d/%m/%Y') + ' 13h'
    wd = GAMES[game][3]; d += datetime.timedelta(days=1)
    while d.weekday() not in wd: d += datetime.timedelta(days=1)
    return d.strftime('%d/%m/%Y')
out = ['# Theo dõi quẻ ngày tháng (dương, âm, năm) — Power / Mega / Loto', '',
       'Mỗi số trong nhóm ra % (chia đều = 6/55 Power 10,9% · 6/45 Mega 13,3% · 5/35 Loto 14,3%). "≥2 số" = % kỳ có từ 2 số của nhóm ra, so với ngẫu nhiên.', '']
for game, (key, NB, KB, _) in GAMES.items():
    D, R = A[key]['dates'], [set(r) for r in A[key]['res']]; N = len(R)
    lunar_many(list({d[:10] for d in D}) + [nxt(game, D[-1])[:10]])
    P = KB / NB; names = list(sets(D[-1], NB))
    out += [f'## {game.upper()} — {N} kỳ ({D[0][:10]} → {D[-1]})', '',
            '| Nhóm | Mỗi số ra: 50 kỳ · 100 kỳ · cả LS | 3 đoạn 100 kỳ | Kỳ có ≥2 số (thực / ngẫu nhiên) | Kỳ có ≥3 số (thực / ngẫu nhiên) |', '|---|---|---|---|---|']
    for nm in names:
        rec = []
        for t in range(N):
            S = sets(D[t], NB)[nm]; k = len(S); h = len(S & R[t])
            pge = lambda m: sum(comb(k, j) * comb(NB - k, KB - j) for j in range(m, min(k, KB) + 1)) / comb(NB, KB)
            rec.append((h, k, pge(2), pge(3)))
        rate = lambda rs: sum(h for h, *_ in rs) / max(1, sum(k for _, k, *_ in rs))
        f = lambda x: f'{x * 100:.1f}%'
        seg = ' · '.join(f(rate(rec[N - 100 * (i + 1):N - 100 * i])) for i in range(3))
        g2 = sum(h >= 2 for h, *_ in rec); e2 = sum(r[2] for r in rec); g3 = sum(h >= 3 for h, *_ in rec); e3 = sum(r[3] for r in rec)
        out.append(f'| {nm} | {f(rate(rec[-50:]))} · {f(rate(rec[-100:]))} · {f(rate(rec))} | {seg} | {g2} / {e2:.1f} | {g3} / {e3:.1f} |')
    ex = [(D[t], sorted(R[t])) for t in range(N) if len(sets(D[t], NB)['Tất cả (dương + âm + năm)'] & R[t]) >= 3][-5:]
    nd = nxt(game, D[-1]); S = sets(nd, NB)
    out += ['', f'Chia đều {P * 100:.1f}%. Kỳ gần đây ra ≥3 số ngày tháng: ' + ('; '.join(f'{d}: {" ".join(f"{x:02d}" for x in r)}' for d, r in ex) or '—'),
            f'**Kỳ tới {nd}** (âm {LUN[nd[:10]][0]}/{LUN[nd[:10]][1]}): dương {" ".join(f"{x:02d}" for x in sorted(S["Dương + năm (26)"]))} · âm {" ".join(f"{x:02d}" for x in sorted(S["Âm + năm"]))}', '']
open(os.path.join(HERE, 'ngaythang.md'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
