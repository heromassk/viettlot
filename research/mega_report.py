"""Mega 6/45: so các số liên hệ với ngày quay với kết quả thật của từng kỳ."""
import math, random, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from study import load, zscore, rules as r1
from kinhdich import rules as r2
from more_rules import rules as r3
def p(z): return math.erfc(abs(z)/math.sqrt(2))
mx, c, _, draws = load('mega645'); n = len(draws); cut = int(n*0.6)
R = {**r1(mx), **r2(mx), **r3(mx)}
R = {k: v for k, v in R.items() if not k.startswith('ĐỐI CHỨNG')}
sets = {k: [f(d['info']) for d in draws] for k, f in R.items()}
rows = []
for k, S in sets.items():
    if not sum(map(len, S)): continue
    zA, H, E = zscore(S, draws, c, mx); zT = zscore(S[:cut], draws[:cut], c, mx)[0]; zV = zscore(S[cut:], draws[cut:], c, mx)[0]
    rows.append((zA, k, zT, zV, H, E, sum(map(len, S))/n))
rows.sort()
# ngưỡng may mắn cho toàn bộ quy luật
rng = random.Random(7); nums = [d['nums'] for d in draws]; mz = []
for _ in range(int(sys.argv[1]) if len(sys.argv) > 1 else 500):
    perm = nums[:]; rng.shuffle(perm); fake = [dict(nums=x) for x in perm]
    mz.append(max(abs(zscore(sets[k], fake, c, mx)[0]) for _, k, *_ in rows))
mz.sort(); thr = mz[int(0.95*len(mz))]
print(f'Mega: {n} kỳ, {len(rows)} quy luật. Ngưỡng may mắn (95%): |z| = {thr:.2f}\n')
print('TRÚNG NHIỀU HƠN NGẪU NHIÊN (top 12)')
for zA, k, zT, zV, H, E, sz in rows[::-1][:12]:
    print(f"  {k:44s} ~{sz:4.1f} số/kỳ | trúng {H:4.0f} / kỳ vọng {E:6.1f} ({(H/E-1)*100:+4.0f}%) | z {zA:5.2f} p={p(zA):.3f} | 2 giai đoạn {'cùng chiều' if zT*zV>0 else 'ĐẢO'}")
print('\nTRÚNG ÍT HƠN NGẪU NHIÊN (top 12)')
for zA, k, zT, zV, H, E, sz in rows[:12]:
    print(f"  {k:44s} ~{sz:4.1f} số/kỳ | trúng {H:4.0f} / kỳ vọng {E:6.1f} ({(H/E-1)*100:+4.0f}%) | z {zA:5.2f} p={p(zA):.3f} | 2 giai đoạn {'cùng chiều' if zT*zV>0 else 'ĐẢO'}")
# phân bố z so với lý thuyết
zs = [r[0] for r in rows]
print(f"\nPhân bố: {sum(abs(z)>1.96 for z in zs)} / {len(zs)} quy luật có |z|>1.96 (ngẫu nhiên kỳ vọng ~{0.05*len(zs):.0f}); "
      f"{sum(z>0 for z in zs)} lệch lên, {sum(z<0 for z in zs)} lệch xuống")
# số đơn: gộp tất cả quy luật ra đúng 1 số
single = [k for k in sets if max(len(s) for s in sets[k]) <= 2]
U = [set().union(*(sets[k][i] for k in single)) for i in range(n)]
zU, HU, EU = zscore(U, draws, c, mx)
print(f"\nGộp {len(single)} cách ra số đơn (ngày, tháng, d+m, âm lịch, Can Chi, quẻ...): TB {sum(map(len,U))/n:.1f} số/kỳ phủ; "
      f"trúng TB {HU/n:.2f} số/kỳ, ngẫu nhiên {EU/n:.2f} → z {zU:.2f}")
hits = {}
for i, d in enumerate(draws):
    for k in single:
        for x in sets[k][i] & d['nums']: hits.setdefault(k, []).append(d['info'])
print('\n5 kỳ gần nhất: số trúng liên hệ với ngày')
for i in range(n-5, n):
    d = draws[i]; I = d['info']
    rel = {x: [k for k in single if x in sets[k][i]] for x in sorted(d['nums'])}
    print(f"  {I['d']:02d}/{I['m']:02d}/{I['y']} {' '.join(f'{x:02d}' for x in sorted(d['nums']))}: " +
          '; '.join(f"{x}←{', '.join(v[:3])}{'…' if len(v)>3 else ''}" for x, v in rel.items() if v))
