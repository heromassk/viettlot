#!/usr/bin/env python3
"""Thử các suy luận LOẠI TRỪ, chấm bằng chính nó qua 3 khúc (chạy tiến, chỉ dùng dữ liệu trước kỳ).
  python3 build/loai_tru.py power|mega|loto [--W 600]
Cấp số: tỉ lệ ra của nhóm bị loại vs nhóm còn lại (cùng kỳ), số trúng mất / kỳ.
Cấp vé: % kỳ thật vi phạm luật (= vé đúng bị loại oan)."""
import json, os, sys
G = {'power': ('power655', 55, 6), 'mega': ('mega645', 45, 6), 'loto': ('loto535', 35, 5)}
g = sys.argv[1]; W = int(sys.argv[sys.argv.index('--W') + 1]) if '--W' in sys.argv else 600
key, NB, KB = G[g]
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_data.json')))[key]
R = [set(r) for r in D['res']]; T = len(R); S0 = max(30, T - W)
blocks = [(S0 + i * (T - S0) // 3, S0 + (i + 1) * (T - S0) // 3) for i in range(3)]

def gap(t, n):
    g = 0
    while g < t and n not in R[t - 1 - g]: g += 1
    return g

def rules(t):
    last = R[t - 1]; prev2 = R[t - 2]
    c10 = {n: sum(n in R[u] for u in range(t - 10, t)) for n in range(1, NB + 1)}
    gp = {n: gap(t, n) for n in range(1, NB + 1)}
    dec = {}
    for n in last: dec[n // 10] = dec.get(n // 10, 0) + 1
    out = {
        'Số vừa ra kỳ trước': set(last),
        'Ra 2 kỳ liền': last & prev2,
        'Quá nóng (≥4 lần/10 kỳ)': {n for n in c10 if c10[n] >= 4},
        'Bóng gương kỳ trước (n↔N+1−n)': {NB + 1 - n for n in last} - last,
        'Cùng đuôi số kỳ trước': {n for n in range(1, NB + 1) if n % 10 in {x % 10 for x in last}} - last,
        'Chục đã ra ≥3 số kỳ trước': {n for n in range(1, NB + 1) if dec.get(n // 10, 0) >= 3} - last,
    }
    for a, b in ((1, 2), (3, 5), (6, 10), (11, 15), (16, 20), (21, 30), (31, 999)):
        out[f'Vắng {a}–{b if b < 999 else "∞"} kỳ'] = {n for n in gp if a <= gp[n] <= b}
    return out

names = list(rules(S0).keys())
st = {k: [[0, 0, 0, 0] for _ in blocks] for k in names}   # hit_ex, n_ex, hit_rest, n_rest
for bi, (a, b) in enumerate(blocks):
    for t in range(a, b):
        for k, ex in rules(t).items():
            h = len(ex & R[t]); x = st[k][bi]
            x[0] += h; x[1] += len(ex); x[2] += KB - h; x[3] += NB - len(ex)
print(f'## Loại trừ cấp số — {key}, {T - S0} kỳ gần chia 3 khúc\n')
print('| Luật loại | Loại TB/kỳ | Tỉ lệ ra nhóm bị loại (3 khúc) | Nhóm còn lại | Trúng mất/kỳ | Ổn định |\n|---|---|---|---|---|---|')
for k in names:
    xs = st[k]; n = sum(b - a for a, b in blocks)
    r_ex = [x[0] / x[1] * 100 if x[1] else 0 for x in xs]; r_re = [x[2] / x[3] * 100 for x in xs]
    good = sum(e < r for e, r in zip(r_ex, r_re))
    print(f"| {k} | {sum(x[1] for x in xs) / n:.1f} | {' / '.join(f'{v:.1f}%' for v in r_ex)} | {' / '.join(f'{v:.1f}%' for v in r_re)} | {sum(x[0] for x in xs) / n:.2f} | {'✔ ' if good == 3 else ('✘ ' if good == 0 else '~ ')}{good}/3 |")

# ---- cấp vé
S = [sum(r) for r in R]
def tk_rules(t):
    s = sorted(R[t]); last = R[t - 1]
    hist = sorted(S[max(0, t - 200):t]); lo, hi = hist[len(hist) // 10], hist[9 * len(hist) // 10]
    dec = {}
    for n in s: dec[n // 10] = dec.get(n // 10, 0) + 1
    odd = sum(n % 2 for n in s); low = sum(n <= NB // 2 for n in s)
    return {
        'Tổng ngoài 10–90% của 200 kỳ': not lo <= S[t] <= hi,
        'Toàn chẵn hoặc toàn lẻ': odd in (0, KB),
        'Toàn nhỏ hoặc toàn lớn': low in (0, KB),
        '≥3 số liên tiếp': any(s[i] + 2 == s[i + 2] and s[i] + 1 == s[i + 1] for i in range(KB - 2)),
        f'≥{KB - 2} số cùng chục': max(dec.values()) >= KB - 2,
        '≥3 số trùng kỳ trước': len(R[t] & last) >= 3,
        '≥2 số trùng kỳ trước': len(R[t] & last) >= 2,
        'Không có số nào ≥ 2/3 dải': max(s) < NB * 2 // 3,
    }
print(f'\n## Loại trừ cấp vé — % kỳ thật vi phạm (vé đúng bị loại oan), 3 khúc\n')
print('| Luật loại vé | Khúc 1 | Khúc 2 | Khúc 3 |\n|---|---|---|---|')
tn = list(tk_rules(S0).keys())
for k in tn:
    print(f'| {k} | ' + ' | '.join(f"{sum(tk_rules(t)[k] for t in range(a, b)) / (b - a) * 100:.1f}%" for a, b in blocks) + ' |')
