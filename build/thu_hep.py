#!/usr/bin/env python3
"""Kết hợp luật vắng + các luật loại khác để thu hẹp pool. Gộp dần (tham lam): mỗi bước thêm luật làm
% kỳ "không mất số nào" giảm ít nhất trên mỗi số bị bỏ thêm. Chấm 100 kỳ gần + 100 kỳ trước.
  python3 build/thu_hep.py power|mega|loto [--min 60]"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import theodoi as TD
g = sys.argv[1]; key, NB, KB = TD.GM[g]
MIN = int(sys.argv[sys.argv.index('--min') + 1]) if '--min' in sys.argv else 60
D = json.load(open(os.path.join(TD.HERE, 'all_data.json')))[key]
R = [set(r) for r in D['res']]; T = len(R)
segs = [(T - 100, T), (T - 200, T - 100)]
EX = {}   # EX[t][id] = tập bị loại
for t in list(range(T - 200, T)) + [T]:
    c = TD.ctx(R, NB, t); EX[t] = {i: f(R, t, c) for i, l, f in TD.RULES}
LAB = {i: l for i, l, f in TD.RULES}
def score(ids):
    out = []
    for a, b in segs:
        ok = lost = bo = 0
        for t in range(a, b):
            e = set().union(*[EX[t][i] for i in ids]) if ids else set()
            h = len(e & R[t]); ok += not h; lost += h; bo += len(e)
        n = b - a; out.append((ok / n * 100, lost / n, bo / n))
    return out
chosen = []; cur = score([])
print(f'## {key} — gộp luật loại (100 kỳ gần | 100 kỳ trước). "Không mất số" = kỳ đó không số bị loại nào về.\n')
print('| Bước | Thêm luật | Bỏ TB/kỳ | Pool còn | Không mất số (gần / trước) | Số trúng mất TB/kỳ | Kỳ tới bỏ thêm |\n|---|---|---|---|---|---|---|')
step = 0
while True:
    best = None
    for i in LAB:
        if i in chosen: continue
        sc = score(chosen + [i]); okm = min(sc[0][0], sc[1][0])
        if okm < MIN: continue
        add = sc[0][2] - cur[0][2]
        if add < 0.15: continue
        cost = ((cur[0][0] - sc[0][0]) + (cur[1][0] - sc[1][0])) / 2 / add   # % kỳ mất cho mỗi số bỏ thêm
        if best is None or cost < best[0]: best = (cost, i, sc)
    if not best: break
    step += 1; chosen.append(best[1]); prev = set().union(*[EX[T][i] for i in chosen[:-1]]) if len(chosen) > 1 else set(); cur = best[2]
    now = set().union(*[EX[T][i] for i in chosen])
    print(f'| {step} | {LAB[best[1]]} | {cur[0][2]:.1f} | {NB - cur[0][2]:.1f} | **{cur[0][0]:.0f}%** / {cur[1][0]:.0f}% | {cur[0][1]:.2f} | {" ".join(f"{n:02d}" for n in sorted(now - prev)) or "—"} |')
now = sorted(set().union(*[EX[T][i] for i in chosen])) if chosen else []
print(f'\n**Kỳ tới bỏ tất cả ({len(now)} số):** {" ".join(f"{n:02d}" for n in now)}')
print(f'**Pool còn lại ({NB - len(now)} số):** {" ".join(f"{n:02d}" for n in range(1, NB + 1) if n not in now)}')
