#!/usr/bin/env python3
"""Luật LOẠI trong sổ, chấm trên 4 khung gần 10 / 20 / 50 / 100 kỳ: % kỳ đúng (không số nào bị loại về), cỡ TB,
tỉ lệ ra mỗi số bị loại (so bình quân) ở 100 kỳ. Đạt = đúng ≥70% ở cả khung 50 và 100.
  python3 build/luat_khung.py power|mega|loto"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import theodoi as TD
g = sys.argv[1]; key, NB, KB = TD.GM[g]
D = json.load(open(os.path.join(TD.HERE, 'all_data.json')))[key]
R = [set(r) for r in D['res']]; T = len(R); P = KB / NB * 100
TD.SESS = (['13' if '13h' in x else '21' for x in D['dates']] + ['13' if '21h' in D['dates'][-1] else '21']) if g == 'loto' else []
C = {t: TD.ctx(R, NB, t) for t in range(T - 100, T + 1)}
AP = TD.APPLIED[g]
print(f'## {key} — luật loại, % kỳ đúng ở 4 khung gần (kỳ gần nhất → lùi)\n')
print('| Luật | Đang dùng | Cỡ TB | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | Ra mỗi số (TB ' + f'{P:.1f}%) | Đạt ≥70% | Kỳ tới loại |\n|---|---|---|---|---|---|---|---|---|---|')
for i, lab, f in TD.RULES:
    ok = []; sz = h = 0
    for t in range(T - 100, T):
        try: s = f(R, t, C[t])
        except Exception: s = None
        if s is None: ok.append(None); continue
        s = set(s); sz += len(s); h += len(s & R[t]); ok.append(not (s & R[t]))
    v = [x for x in ok if x is not None]
    if not v: continue
    pc = {W: sum(x for x in ok[-W:] if x is not None) / max(1, sum(x is not None for x in ok[-W:])) * 100 for W in (10, 20, 50, 100)}
    try: nx = ' '.join(f'{n:02d}' for n in sorted(f(R, T, C[T])))
    except Exception: nx = '?'
    dat = '✔' if pc[50] >= 70 and pc[100] >= 70 else '~' if pc[100] >= 70 else '✘'
    print(f'| {i} | {"✔" if i in AP else ""} | {sz / len(v):.1f} | ' + ' | '.join(f'{pc[W]:.0f}%' for W in (10, 20, 50, 100)) +
          f' | {h / max(sz, 1) * 100:.1f}% | {dat} | {nx or "—"} |')
