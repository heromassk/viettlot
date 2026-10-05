#!/usr/bin/env python3
"""Loto: xem 13h và 21h như 2 dãy riêng (2 "máy"). Mỗi dãy: khung 100 / 200 kỳ gần của chính phiên đó, so với khung liền trước.
  python3 build/phien.py"""
import json, os
from math import comb
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_data.json')))['loto535']
NB, KB = 35, 5; P = KB / NB * 100
ALL = list(zip(D['dates'], D['res'], D['lk']))
for ses in ('13h', '21h'):
    X = [(d, set(r), k) for d, r, k in ALL if ses in d]; R = [x[1] for x in X]; L = [x[2] for x in X]; T = len(R)
    print(f'\n## Phiên {ses} — {T} kỳ (lag 1 = cùng phiên hôm trước). Bình quân mỗi số {P:.1f}%')
    def gap(t, n):
        g = 0
        while g < t and n not in R[t - 1 - g]: g += 1
        return g
    for W in (100, 200):
        A, B = (T - W, T), (T - 2 * W, T - W)
        def rate(fn, a, b):
            h = n = 0
            for t in range(a, b):
                g = fn(t); h += len(g & R[t]); n += len(g)
            return h / max(n, 1) * 100
        def ok(fn, a, b):
            return sum(not (fn(t) & R[t]) for t in range(a, b)) / (b - a) * 100
        lag = ' '.join(f"k{k}:{rate(lambda t: R[t - k], *A):.0f}/{rate(lambda t: R[t - k], *B):.0f}" for k in range(1, 8))
        hot = lambda t, w=W // 2: set(sorted(range(1, NB + 1), key=lambda n: (-sum(n in R[u] for u in range(t - w, t)), n))[:8])
        cold = lambda t, w=W // 2: set(sorted(range(1, NB + 1), key=lambda n: (sum(n in R[u] for u in range(t - w, t)), n))[:8])
        print(f'\n**Khung {W} kỳ phiên {ses}** (gần / trước)')
        print(f'- Số của k kỳ trước (cùng phiên) ra lại: {lag}')
        print(f'- 8 số nóng nhất {W // 2} kỳ → kỳ kế: {rate(hot, *A):.1f} / {rate(hot, *B):.1f}% · 8 số lạnh nhất → {rate(cold, *A):.1f} / {rate(cold, *B):.1f}%')
        for G in (10, 15, 20):
            fn = lambda t, G=G: {n for n in range(1, NB + 1) if gap(t, n) >= G}
            sz = sum(len(fn(t)) for t in range(*A)) / W
            print(f'- Loại số vắng ≥{G} kỳ (phiên): đúng {ok(fn, *A):.0f} / {ok(fn, *B):.0f}% kỳ · bỏ {sz:.1f} · nhóm ra {rate(fn, *A):.1f} / {rate(fn, *B):.1f}%')
        # pool 15 nóng cùng phiên
        p15 = lambda t: set(sorted(range(1, NB + 1), key=lambda n: (-sum(n in R[u] for u in range(t - 50, t)), gap(t, n), n))[:15])
        hs = [len(p15(t) & R[t]) for t in range(*A)]; hs0 = [len(p15(t) & R[t]) for t in range(*B)]
        print(f'- Pool 15 nóng 50 kỳ cùng phiên: TB {sum(hs) / W:.2f} / {sum(hs0) / W:.2f} số, ≥3 số {sum(h >= 3 for h in hs) / W * 100:.0f} / {sum(h >= 3 for h in hs0) / W * 100:.0f}%')
        mmv = lambda t: set(sorted(range(1, 13), key=lambda k: (-next((g for g in range(t) if L[t - 1 - g] == k), t), k))[:3])
        print(f'- MM: 3 số vắng lâu nhất (phiên) trúng {sum(L[t] in mmv(t) for t in range(*A)) / W * 100:.0f} / {sum(L[t] in mmv(t) for t in range(*B)) / W * 100:.0f}% · MM lặp lại hôm trước {sum(L[t] == L[t - 1] for t in range(*A)) / W * 100:.0f} / {sum(L[t] == L[t - 1] for t in range(*B)) / W * 100:.0f}% (bình quân 8%)')
    c = {n: sum(n in R[u] for u in range(T - 100, T)) for n in range(1, NB + 1)}
    print(f'\nHiện trạng phiên {ses} (100 kỳ): nhiều nhất ' + ', '.join(f'{n:02d}({c[n]})' for n in sorted(c, key=lambda n: -c[n])[:6]) + ' · ít nhất ' + ', '.join(f'{n:02d}({c[n]})' for n in sorted(c, key=lambda n: c[n])[:6]))
    print('Vắng lâu (phiên): ' + ', '.join(f'{n:02d}:{gap(T, n)}' for n in sorted(range(1, NB + 1), key=lambda n: -gap(T, n))[:6]))
