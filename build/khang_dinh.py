#!/usr/bin/env python3
"""Tìm các "khẳng định" về kỳ tới đúng ≥70% số kỳ, ổn định qua 3 khúc (chạy tiến, chỉ dùng dữ liệu trước kỳ).
  python3 build/khang_dinh.py power|mega|loto [--W 600]
Mỗi khẳng định ghi: % kỳ đúng (3 khúc, 50 kỳ gần) và % số vé còn giữ lại khi lọc theo nó (độ thu hẹp)."""
import json, os, sys, random
G = {'power': ('power655', 55, 6), 'mega': ('mega645', 45, 6), 'loto': ('loto535', 35, 5)}
g = sys.argv[1]; W = int(sys.argv[sys.argv.index('--W') + 1]) if '--W' in sys.argv else 600
key, NB, KB = G[g]
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_data.json')))[key]
R = [set(r) for r in D['res']]; T = len(R); S0 = T - W
random.seed(11)
MC = [sorted(random.sample(range(1, NB + 1), KB)) for _ in range(400)]
blocks = [(S0 + i * W // 3, S0 + (i + 1) * W // 3) for i in range(3)] + [(T - 50, T)]

def ctx(t):
    last, p2 = R[t - 1], R[t - 2]
    gap = {}
    for n in range(1, NB + 1):
        k = 0
        while k < t and n not in R[t - 1 - k]: k += 1
        gap[n] = k
    c20 = {n: sum(n in R[u] for u in range(t - 20, t)) for n in range(1, NB + 1)}
    c50 = {n: sum(n in R[u] for u in range(t - 50, t)) for n in range(1, NB + 1)}
    hist = lambda f: sorted(f(R[u]) for u in range(t - 200, t))
    pct = lambda h, q: h[int(q * (len(h) - 1))]
    S, MN, MX = hist(sum), hist(min), hist(max)
    hot10 = set(sorted(c20, key=lambda n: (-c20[n], gap[n]))[:10])
    cold3 = set(sorted(c50, key=lambda n: (c50[n], -gap[n]))[:3])
    gap3 = set(sorted(gap, key=lambda n: -gap[n])[:3])
    ke = {m for n in last for m in (n - 1, n, n + 1) if 1 <= m <= NB}
    return dict(last=last, p2=p2, gap=gap, hot10=hot10, cold3=cold3, gap3=gap3, ke=ke,
                s=(pct(S, .15), pct(S, .85)), mn=pct(MN, .75), mx=pct(MX, .25),
                rec5={n for n in gap if gap[n] <= 4})

half = KB // 2
CLAIMS = {
    'Có ≥1 số trong 10 số nóng nhất 20 kỳ': lambda x, c: len(x & c['hot10']) >= 1,
    'Có ≥1 số trùng hoặc kề ±1 kỳ trước': lambda x, c: len(x & c['ke']) >= 1,
    'Có ≥1 số của 2 kỳ gần nhất': lambda x, c: len(x & (c['last'] | c['p2'])) >= 1,
    f'Có ≥{half} số đã ra trong 5 kỳ gần': lambda x, c: len(x & c['rec5']) >= half,
    'KHÔNG ra số nào trong 3 số lạnh nhất 50 kỳ': lambda x, c: not (x & c['cold3']),
    'KHÔNG ra số nào trong 3 số vắng lâu nhất': lambda x, c: not (x & c['gap3']),
    'KHÔNG trùng ≥2 số với kỳ trước': lambda x, c: len(x & c['last']) < 2,
    'Tổng trong khoảng 15–85% của 200 kỳ': lambda x, c: c['s'][0] <= sum(x) <= c['s'][1],
    f'Chẵn/lẻ cân ({half}±1 số lẻ)': lambda x, c: abs(sum(n % 2 for n in x) - KB / 2) <= 1,
    f'Nhỏ/lớn cân ({half}±1 số ≤{NB // 2})': lambda x, c: abs(sum(n <= NB // 2 for n in x) - KB / 2) <= 1,
    'Số nhỏ nhất ≤ mốc 75% lịch sử': lambda x, c: min(x) <= c['mn'],
    'Số lớn nhất ≥ mốc 25% lịch sử': lambda x, c: max(x) >= c['mx'],
    f'Có số ở ≥{KB - 2} chục khác nhau': lambda x, c: len({n // 10 for n in x}) >= KB - 2,
    'Có ≥1 số vắng ≥10 kỳ': lambda x, c: any(c['gap'][n] >= 10 for n in x),
    'Có ≥1 số cùng đuôi với số kỳ trước': lambda x, c: bool({n % 10 for n in x} & {n % 10 for n in c['last']}),
}
SEL = ['Có ≥1 số trùng hoặc kề ±1 kỳ trước', 'KHÔNG trùng ≥2 số với kỳ trước', f'Chẵn/lẻ cân ({half}±1 số lẻ)',
       f'Nhỏ/lớn cân ({half}±1 số ≤{NB // 2})', f'Có số ở ≥{KB - 2} chục khác nhau']
res = {k: [[0, 0, 0] for _ in blocks] for k in CLAIMS}   # đúng, số kỳ, % vé giữ
allok = [[0, 0, 0] for _ in blocks]
for bi, (a, b) in enumerate(blocks):
    for t in range(a, b):
        c = ctx(t); x = R[t]; good_all = True; keep_all = 0
        okmc = {k: [f(set(tk), c) for tk in MC] for k, f in CLAIMS.items()}
        for k, f in CLAIMS.items():
            v = f(x, c); r = res[k][bi]; r[0] += v; r[1] += 1; r[2] += sum(okmc[k]) / len(MC)
        allok[bi][0] += all(CLAIMS[k](x, c) for k in SEL); allok[bi][1] += 1
        allok[bi][2] += sum(all(okmc[k][i] for k in SEL) for i in range(len(MC))) / len(MC)
print(f'## Khẳng định về kỳ tới — {key}, {W} kỳ gần (3 khúc) + 50 kỳ gần nhất\n')
print('| Khẳng định | Đúng: khúc 1 / 2 / 3 | 50 kỳ gần | Vé giữ lại | Đạt ≥70% cả 3 khúc |\n|---|---|---|---|---|')
for k in CLAIMS:
    r = res[k]; pc = [x[0] / x[1] * 100 for x in r]; kp = sum(x[2] for x in r[:3]) / sum(x[1] for x in r[:3]) * 100
    print(f"| {k} | {' / '.join(f'{v:.0f}%' for v in pc[:3])} | {pc[3]:.0f}% | {kp:.0f}% | {'✔' if min(pc[:3]) >= 70 else ''} |")
a = allok
print(f"\n**Gộp {len(SEL)} khẳng định cấu trúc** ({'; '.join(SEL)}): đúng {' / '.join(f'{x[0] / x[1] * 100:.0f}%' for x in a[:3])}, 50 kỳ gần {a[3][0] / a[3][1] * 100:.0f}%, vé giữ lại {sum(x[2] for x in a[:3]) / sum(x[1] for x in a[:3]) * 100:.0f}%")
