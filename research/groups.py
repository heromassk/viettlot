"""Bộ 3 số, bộ 4 số hay về cùng nhau: đếm, so với ngẫu nhiên, và thử chọn theo bộ về nhiều nhất trước mỗi kỳ."""
import sys, os, math, random
from math import comb
from collections import Counter
from itertools import combinations
sys.path.insert(0, os.path.dirname(__file__))
from study import load

def count(D, k):
    cnt, last = Counter(), {}
    for i, s in enumerate(D):
        for g in combinations(sorted(s), k): cnt[g] += 1; last[g] = i
    return cnt, last
if __name__ == '__main__':
    for game in ['power655', 'mega645', 'loto535']:
        mx, c, _, dr = load(game); D = [set(d['nums']) for d in dr]; n = len(D)
        print(f'\n######## {game}: {n} kỳ')
        for k in (3, 4):
            cnt, last = count(D, k); e = n*comb(c, k)/comb(mx, k)
            dist = Counter(cnt.values())
            top = sorted(cnt, key=lambda g: (-cnt[g], -last[g]))[:8]
            rng = random.Random(1); sims = []
            for _ in range(200):
                R = [set(rng.sample(range(1, mx+1), c)) for _ in range(n)]
                cc, _ = count(R, k); sims.append((max(cc.values()), sum(v >= 2 for v in cc.values())))
            sims.sort()
            rep = sum(v >= 2 for v in cnt.values())
            print(f'  BỘ {k}: kỳ vọng mỗi bộ {e:.3f} lần. Số bộ về ≥2 lần: {rep} (ngẫu nhiên thường {sorted(s[1] for s in sims)[100]}, 95%: {sorted(s[1] for s in sims)[5]}–{sorted(s[1] for s in sims)[194]}). '
                  f'Nhiều nhất {max(cnt.values())} lần (ngẫu nhiên thường {sims[100][0]}).')
            print('     Về nhiều nhất: ' + ', '.join(f"{'-'.join(map(str, g))} ({cnt[g]} lần, lần cuối {dr[last[g]]['info']['d']:02d}/{dr[last[g]]['info']['m']:02d}/{dr[last[g]]['info']['y']})" for g in top))
            # chọn 10 bộ về nhiều nhất trước mỗi kỳ
            hit = tot = 0; start = 50
            run, rl = Counter(), {}
            for i in range(n):
                if i >= start:
                    best = sorted(run, key=lambda g: (-run[g], -rl[g]))[:10]
                    hit += sum(set(g) <= D[i] for g in best); tot += len(best)
                for g in combinations(sorted(D[i]), k): run[g] += 1; rl[g] = i
            p = comb(c, k)/comb(mx, k); E = tot*p
            print(f'     Chọn 10 bộ về nhiều nhất trước mỗi kỳ: trúng trọn bộ {hit} lần, ngẫu nhiên {E:.2f} lần')
