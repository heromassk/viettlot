#!/usr/bin/env python3
"""Thử các KHÍA CẠNH MỚI (mượn từ suy luận dãy số nói chung + lô đề), chấm theo từng kỳ, chạy tiến.
  python3 build/khia_canh.py power|mega|loto [--W 100]
A. Nhóm số (tín hiệu cấp số): tỉ lệ ra của nhóm vs nhóm còn lại, ở 3 đoạn W kỳ (gần → xa). Ổn định = cùng chiều cả 3.
B. Hướng (hồi về trung bình / đà): dự đoán kỳ tới tăng hay giảm cho tổng, số lẻ, u, z… — % kỳ đoán đúng.
C. Đặc trưng hình dạng mới (đồng dư, nguyên tố, delta, đối xứng…) — % kỳ đúng với tập gọn chứa ≥85%, vé giữ lại."""
import json, os, sys, random
GM = {'power': ('power655', 55, 6), 'mega': ('mega645', 45, 6), 'loto': ('loto535', 35, 5)}
key, NB, KB = GM[sys.argv[1]]
W = int(sys.argv[sys.argv.index('--W') + 1]) if '--W' in sys.argv else 100
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_data.json')))[key]
R = [set(r) for r in D['res']]; S = [sorted(r) for r in D['res']]; T = len(R)
segs = [(T - W, T), (T - 2 * W, T - W), (T - 3 * W, T - 2 * W)]
PR = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53}
rev = lambda n: int(f'{n:02d}'[::-1])
bong = lambda n: int(''.join(str((int(c) + 5) % 10) for c in f'{n:02d}'))
ok = lambda xs: {x for x in xs if 1 <= x <= NB}

# ---------- A. nhóm số ----------
GROUPS = {
    'Số lộn của kỳ trước (12↔21)': lambda t: ok(rev(n) for n in R[t - 1]) - R[t - 1],
    'Chạm tổng (đầu+đuôi trùng số kỳ trước)': lambda t: {n for n in range(1, NB + 1) if (n // 10 + n % 10) % 10 in {(m // 10 + m % 10) % 10 for m in R[t - 1]}} - R[t - 1],
    'Cách ±2 số kỳ trước': lambda t: ok(m + d for m in R[t - 1] for d in (-2, 2)) - R[t - 1],
    'Số của kỳ t−2 (cách 1 kỳ)': lambda t: R[t - 2] - R[t - 1],
    'Số của kỳ t−3': lambda t: R[t - 3] - R[t - 1] - R[t - 2],
    'Số nguyên tố': lambda t: PR & set(range(1, NB + 1)),
    'Số chia hết cho 3': lambda t: {n for n in range(1, NB + 1) if n % 3 == 0},
    'Cùng vị trí kỳ trước ±1 (theo u..z)': lambda t: ok(m + d for m in S[t - 1] for d in (-1, 0, 1)),
    'Số ra ≥2 lần trong 5 kỳ': lambda t: {n for n in range(1, NB + 1) if sum(n in R[u] for u in range(t - 5, t)) >= 2},
    'Số vừa "tái xuất" (ra kỳ trước sau vắng ≥10)': lambda t: {n for n in R[t - 1] if all(n not in R[u] for u in range(t - 11, t - 1))},
    'Hàng chục ra nhiều nhất kỳ trước': lambda t: (lambda d: {n for n in range(1, NB + 1) if n // 10 == d})(max(range(6), key=lambda d: sum(m // 10 == d for m in R[t - 1]))),
    'Hàng chục vắng mặt kỳ trước': lambda t: {n for n in range(1, NB + 1) if n // 10 not in {m // 10 for m in R[t - 1]}},
}
print(f'## {key} — A. Nhóm số: tỉ lệ ra mỗi số (nhóm / còn lại), 3 đoạn {W} kỳ: gần → xa\n')
print('| Nhóm | Cỡ TB | Đoạn 1 | Đoạn 2 | Đoạn 3 | Kết luận |\n|---|---|---|---|---|---|')
for k, f in GROUPS.items():
    cells, sign, sz = [], [], 0
    for a, b in segs:
        h1 = n1 = h0 = n0 = 0
        for t in range(a, b):
            g = f(t); h = len(g & R[t]); h1 += h; n1 += len(g); h0 += KB - h; n0 += NB - len(g)
        r1, r0 = h1 / max(n1, 1) * 100, h0 / max(n0, 1) * 100
        cells.append(f'{r1:.1f} / {r0:.1f}'); sign.append(r1 - r0); sz += n1 / (b - a)
    st = '▲ ra NHIỀU hơn 3/3' if all(x > 0.3 for x in sign) else '▼ ra ÍT hơn 3/3' if all(x < -0.3 for x in sign) else '—'
    print(f'| {k} | {sz / 3:.1f} | ' + ' | '.join(cells) + f' | {st} |')

# ---------- B. hướng ----------
def med(xs): xs = sorted(xs); return xs[len(xs) // 2]
FEAT = {'Tổng': sum, 'Số lẻ': lambda s: sum(x % 2 for x in s), 'u (số nhỏ nhất)': lambda s: s[0], 'z (số lớn nhất)': lambda s: s[-1],
        f'Số nhỏ (≤{NB // 2})': lambda s: sum(x <= NB // 2 for x in s)}
random.seed(9); MC = [sorted(random.sample(range(1, NB + 1), KB)) for _ in range(3000)]
print(f'\n## B. Hướng kỳ tới — "hồi về trung vị": kỳ trước trên trung vị 200 kỳ → đoán kỳ tới THẤP hơn kỳ trước (và ngược lại). Bằng = sai.\n')
print('| Đại lượng | Đúng đoạn 1 | Đoạn 2 | Đoạn 3 | Vé giữ lại | Áp kỳ tới |\n|---|---|---|---|---|---|')
for k, f in FEAT.items():
    res = []; mv = [f(x) for x in MC]; kp = kn = 0
    for si, (a, b) in enumerate(segs):
        c = n = 0
        for t in range(a, b):
            m = med([f(S[u]) for u in range(t - 200, t)]); cur, nxt = f(S[t - 1]), f(S[t])
            if cur == m: continue
            n += 1; c += (nxt < cur) if cur > m else (nxt > cur)
            if si == 0 and t % 3 == 0: kp += sum((v < cur) if cur > m else (v > cur) for v in mv) / len(mv); kn += 1
        res.append(c / max(n, 1) * 100)
    m = med([f(S[u]) for u in range(T - 200, T)]); cur = f(S[-1])
    tip = '—' if cur == m else (f'kỳ trước {cur} > trung vị {m} → THẤP hơn {cur}' if cur > m else f'kỳ trước {cur} < trung vị {m} → CAO hơn {cur}')
    print(f'| {k} | **{res[0]:.0f}%** | {res[1]:.0f}% | {res[2]:.0f}% | {kp / max(kn, 1) * 100:.0f}% | {tip} |')

# ---------- C. hình dạng mới ----------
SH = {
    'Số chia hết cho 3 (đếm)': lambda s: sum(x % 3 == 0 for x in s),
    'Số nguyên tố (đếm)': lambda s: sum(x in PR for x in s),
    'Delta nhỏ nhất (khe nhỏ nhất)': lambda s: min(s[i + 1] - s[i] for i in range(KB - 1)),
    'Tổng đuôi (mod 10)': lambda s: sum(x % 10 for x in s) % 10,
    'Tổng mod 9': lambda s: sum(s) % 9,
    'Cặp đối xứng (n & N+1−n)': lambda s: sum(NB + 1 - x in s for x in s) // 2,
    'Số khe ≤3': lambda s: sum(s[i + 1] - s[i] <= 3 for i in range(KB - 1)),
}
print(f'\n## C. Đặc trưng hình dạng mới (tập gọn nhất chứa ≥85% của 200 kỳ trước)\n')
print('| Đặc trưng | Đúng đoạn 1 | Đoạn 2 | Vé giữ lại | Áp kỳ tới |\n|---|---|---|---|---|')
def keepset(t, f):
    cnt = {}
    for u in range(t - 200, t): v = f(S[u]); cnt[v] = cnt.get(v, 0) + 1
    ks, acc = set(), 0
    for v in sorted(cnt, key=lambda v: -cnt[v]):
        ks.add(v); acc += cnt[v]
        if acc >= 170: break
    return ks
for k, f in SH.items():
    res = []
    for a, b in segs[:2]:
        res.append(sum(f(S[t]) in keepset(t, f) for t in range(a, b)) / (b - a) * 100)
    ks = keepset(T, f); kp = sum(f(s) in ks for s in MC) / len(MC) * 100
    print(f'| {k} | **{res[0]:.0f}%** | {res[1]:.0f}% | {kp:.0f}% | {",".join(map(str, sorted(ks)))} |')
