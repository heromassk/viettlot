"""Phân tích thêm bộ số trúng: cặp số hay về cùng, đuôi số, vị trí (số nhỏ nhất/lớn nhất...), delta, và cặp số có dự đoán được không."""
import sys, os, math, random
from math import comb
from collections import Counter
from itertools import combinations
sys.path.insert(0, os.path.dirname(__file__))
from study import load
from combo import chi2_sf

def zp(z): return math.erfc(abs(z)/math.sqrt(2))
if __name__ == '__main__':
    for game in ['power655', 'mega645', 'loto535']:
        mx, c, _, draws = load(game); D = [sorted(d['nums']) for d in draws]; n = len(D)
        print(f'\n######## {game}: {n} kỳ')
        # 1) cặp số về cùng nhau
        pc = Counter(p for s in D for p in combinations(s, 2))
        npairs = comb(mx, 2); ep = n*comb(c, 2)/npairs
        top = pc.most_common(6)
        # ngẫu nhiên thì cặp về nhiều nhất thường bao nhiêu lần?
        rng = random.Random(1); mxs = []
        for _ in range(200):
            cc = Counter(p for _ in range(n) for p in combinations(sorted(rng.sample(range(1, mx+1), c)), 2)); mxs.append(max(cc.values()))
        mxs.sort()
        print(f'1) CẶP SỐ: kỳ vọng mỗi cặp {ep:.2f} lần. Về cùng nhiều nhất: ' + ', '.join(f'{a}-{b}({k})' for (a, b), k in top)
              + f'. Ngẫu nhiên thì cặp nhiều nhất thường {mxs[100]} lần (95%: ≤{mxs[190]}). Cặp chưa từng về cùng: {npairs-len(pc)}/{npairs}')
        # cặp có dự đoán được? chọn cặp về nhiều nhất trong quá khứ, xem kỳ sau có về cùng không
        hit = tot = 0; start = 50
        for i in range(start, n):
            past = Counter(p for s in D[:i] for p in combinations(s, 2))
            best = [p for p, _ in past.most_common(10)]
            tot += len(best); hit += sum(a in D[i] and b in D[i] for a, b in best)
        pr = comb(c, 2)/npairs
        z = (hit - tot*pr)/math.sqrt(tot*pr*(1-pr))
        print(f'   Chọn 10 cặp về cùng nhiều nhất trước mỗi kỳ: trúng cả cặp {hit}/{tot} lần, ngẫu nhiên {tot*pr:.1f} → z {z:.2f} p={zp(z):.3f}')
        # 2) đuôi số (chữ số cuối)
        tail = Counter(x % 10 for s in D for x in s)
        pool = Counter(x % 10 for x in range(1, mx+1))
        et = {t: n*c*pool[t]/mx for t in range(10)}
        x2 = sum((tail[t]-et[t])**2/et[t] for t in range(10))
        print(f'2) ĐUÔI SỐ: p={chi2_sf(x2, 9):.3f}  ' + ' '.join(f'{t}:{tail[t]}/{et[t]:.0f}' for t in range(10)))
        # 3) vị trí trong bộ đã sắp xếp
        print('3) VỊ TRÍ (bộ xếp tăng dần): ' + ' | '.join(f'số thứ {k+1}: TB {sum(s[k] for s in D)/n:.1f} (lt {(k+1)*(mx+1)/(c+1):.1f})' for k in range(c)))
        # 4) delta (khoảng cách giữa các số liền kề trong bộ)
        dl = Counter(min(b-a, 10) for s in D for a, b in zip(s, s[1:]))
        rng = random.Random(2); dls = Counter(min(b-a, 10) for _ in range(100000) for s in [sorted(rng.sample(range(1, mx+1), c))] for a, b in zip(s, s[1:]))
        tot_d = n*(c-1); tot_s = sum(dls.values())
        x2 = sum((dl[k]-dls[k]/tot_s*tot_d)**2/(dls[k]/tot_s*tot_d) for k in dls)
        print(f'4) DELTA (khoảng cách 2 số kề nhau, 10 = ≥10): p={chi2_sf(x2, len(dls)-1):.3f}  ' + ' '.join(f'{k}:{dl[k]}/{dls[k]/tot_s*tot_d:.0f}' for k in sorted(dls)))
