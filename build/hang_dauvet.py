#!/usr/bin/env python3
"""Dấu vết theo HÀNG (đầu số 0x, 1x, 2x…) qua các kỳ (anh 14/10/2026). Chỉ số chính (Loto 5 số, không tính số may mắn).
Mỗi luật chấm bằng chính % kỳ đúng ở khung 10 / 20 / 50 / 100 / 200 kỳ gần, mỗi kỳ chỉ dùng các kỳ trước.
  python build/hang_dauvet.py power|mega|loto"""
import json, os, sys
from collections import Counter
B = os.path.dirname(os.path.abspath(__file__))
GAME = sys.argv[1]
key, NB, KB = {'power': ('power655', 55, 6), 'mega': ('mega645', 45, 6), 'loto': ('loto535', 35, 5)}[GAME]
D = json.load(open(os.path.join(B, 'all_data.json'), encoding='utf-8'))[key]
R = [sorted(r) for r in D['res']]; DT = D['dates']; T = len(R)
H = list(range(NB // 10 + 1))                       # các hàng
SZ = {h: sum(1 for n in range(1, NB + 1) if n // 10 == h) for h in H}
lab = lambda h: f'{h}x'
def dem(r): c = Counter(n // 10 for n in r); return tuple(c.get(h, 0) for h in H)
C = [dem(r) for r in R]
WS = (10, 20, 50, 100, 200)
pct = lambda f: ' / '.join(f'{sum(f(t) for t in range(T - W, T)) / W * 100:.0f}%' for W in WS)

print(f'## {GAME} — dấu vết theo hàng, đến {DT[-1]}\n')
print('Hàng: ' + ' · '.join(f'{lab(h)} ({SZ[h]} số)' for h in H) + '\n')
print('### 20 kỳ gần: mỗi hàng ra mấy số\n')
print('| Kỳ | Kết quả | ' + ' | '.join(lab(h) for h in H) + ' |\n|---|---|' + '---|' * len(H))
for t in range(T - 20, T):
    print(f"| {DT[t]} | {' '.join(f'{n:02d}' for n in R[t])} | " + ' | '.join(str(v) if v else '·' for v in C[t]) + ' |')

print('\n### Mỗi hàng: trung bình số/kỳ và % kỳ vắng hẳn (10 / 20 / 50 / 100 / 200 kỳ)\n')
print('| Hàng | Số/kỳ | % kỳ hàng vắng (0 số) | % kỳ hàng ra ≥2 số | % kỳ hàng ra ≥3 số |\n|---|---|---|---|---|')
for i, h in enumerate(H):
    tb = ' / '.join(f'{sum(C[t][i] for t in range(T - W, T)) / W:.2f}' for W in WS)
    print(f'| {lab(h)} | {tb} | {pct(lambda t: C[t][i] == 0)} | {pct(lambda t: C[t][i] >= 2)} | {pct(lambda t: C[t][i] >= 3)} |')

print('\n### Kiểu chia hàng hay gặp (200 kỳ)\n')
cnt = Counter(C[T - 200:])
print('| Kiểu (' + '-'.join(lab(h) for h in H) + ') | Số kỳ /200 | Lần gần nhất |\n|---|---|---|')
for k, v in cnt.most_common(10):
    last = max(t for t in range(T) if C[t] == k)
    print(f"| {'-'.join(map(str, k))} | {v} | {DT[last]} |")
nh = Counter(sum(1 for v in c if v) for c in C[T - 200:])
print('\nSố hàng có mặt mỗi kỳ (200 kỳ): ' + ' · '.join(f'{k} hàng: {nh[k]} kỳ' for k in sorted(nh)))

# ---- luật / dấu vết ----
def run0(i, t):   # số kỳ liền hàng i vắng tính đến trước kỳ t
    g = 0
    while g < t and C[t - 1 - g][i] == 0: g += 1
    return g
def avg(i, t, W): return sum(C[u][i] for u in range(t - W, t)) / W
L = {}
for i, h in enumerate(H):
    L[f'Hàng {lab(h)} vắng kỳ trước → kỳ này có ≥1 số'] = (lambda t, i=i: C[t - 1][i] == 0, lambda t, i=i: C[t][i] >= 1)
    L[f'Hàng {lab(h)} ra ≥3 kỳ trước → kỳ này ≤1 số'] = (lambda t, i=i: C[t - 1][i] >= 3, lambda t, i=i: C[t][i] <= 1)
    L[f'Hàng {lab(h)} ra ≥2 kỳ trước → kỳ này ≤1 số'] = (lambda t, i=i: C[t - 1][i] >= 2, lambda t, i=i: C[t][i] <= 1)
    L[f'Hàng {lab(h)} vắng ≥2 kỳ liền → kỳ này có ≥1 số'] = (lambda t, i=i: run0(i, t) >= 2, lambda t, i=i: C[t][i] >= 1)
G = {
    'Kỳ này không hàng nào ra ≥4 số': (lambda t: True, lambda t: max(C[t]) <= 3),
    f'Kỳ này có ≥{len(H) - 1} hàng có mặt': (lambda t: True, lambda t: sum(1 for v in C[t] if v) >= len(H) - 1),
    'Hàng nhiều số nhất kỳ trước, kỳ này không còn nhiều nhất (hoặc hòa)': (lambda t: True, lambda t: C[t][C[t - 1].index(max(C[t - 1]))] < max(C[t]) or max(C[t]) == 0),
    'Hàng vắng kỳ trước (bất kỳ) → kỳ này có ≥1 hàng trong số đó ra lại': (lambda t: 0 in C[t - 1], lambda t: any(C[t][i] for i in range(len(H)) if C[t - 1][i] == 0)),
    'Hàng nóng nhất 10 kỳ → kỳ này có ≥1 số': (lambda t: True, lambda t: C[t][max(range(len(H)), key=lambda i: (avg(i, t, 10) / SZ[H[i]], -i))] >= 1),
    'Hàng nguội nhất 10 kỳ (so cỡ hàng) → kỳ này có ≥1 số': (lambda t: True, lambda t: C[t][min(range(len(H)), key=lambda i: (avg(i, t, 10) / SZ[H[i]], i))] >= 1),
    'Kiểu chia hàng kỳ này khác kỳ trước': (lambda t: True, lambda t: C[t] != C[t - 1]),
}
L.update(G)
print('\n### Luật theo hàng — % kỳ đúng (chỉ tính kỳ có điều kiện) 10 / 20 / 50 / 100 / 200 kỳ\n')
print('| Luật | Đúng | Số kỳ có điều kiện (200) | Đạt ≥70% (50 & 100) |\n|---|---|---|---|')
OUT = []
for nm, (cond, ok) in L.items():
    r = []
    for W in WS:
        ts = [t for t in range(T - W, T) if cond(t)]
        r.append(sum(ok(t) for t in ts) / len(ts) * 100 if ts else None)
    n200 = sum(1 for t in range(T - 200, T) if cond(t))
    good = r[2] is not None and r[3] is not None and r[2] >= 70 and r[3] >= 70 and n200 >= 20
    OUT.append((good, r[3] or 0, f"| {nm} | {' / '.join('—' if v is None else f'{v:.0f}%' for v in r)} | {n200} | {'✔' if good else ''} |"))
for _, _, l in sorted(OUT, key=lambda x: (-x[0], -x[1])): print(l)

# ---- dự đoán số lượng từng hàng kỳ tới: theo kỳ trước (Markov 1 bậc, 200 kỳ) ----
print('\n### Đoán số lượng mỗi hàng kỳ tới theo số lượng kỳ trước (học 200 kỳ trước đó) — % kỳ đoán trúng đúng số lượng / trúng ±1\n')
def du(i, t, W=200):
    c = Counter(C[u][i] for u in range(max(1, t - W), t) if C[u - 1][i] == C[t - 1][i])
    return c.most_common(1)[0][0] if c else round(avg(i, t, 20))
print('| Hàng | Đúng số lượng | Lệch ≤1 | Kỳ tới: kỳ trước ra → đoán |\n|---|---|---|---|')
for i, h in enumerate(H):
    print(f"| {lab(h)} | {pct(lambda t: du(i, t) == C[t][i])} | {pct(lambda t: abs(du(i, t) - C[t][i]) <= 1)} | {C[-1][i]} → {du(i, T)} |")
print(f"\nKỳ trước {DT[-1]}: {' '.join(f'{n:02d}' for n in R[-1])} → chia hàng {'-'.join(map(str, C[-1]))}")
