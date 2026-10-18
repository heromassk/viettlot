#!/usr/bin/env python3
"""Dấu vết chu kỳ theo HÀNG (anh 14/10/2026): (A) sau bao nhiêu kỳ hàng "đủ số" (mọi số của hàng đều đã về), số còn thiếu
khi hàng gần đủ có về nhanh không; (B) hàng ra ít / nhiều trong 10 kỳ gần thì kỳ sau bù / hãm không.
Chấm bằng % đúng của chính luật, khung 10 / 20 / 50 / 100 / 200 kỳ gần; so các nhóm số với NHAU (không so ngẫu nhiên).
  python build/hang_chuky.py power|mega|loto"""
import json, os, sys
B = os.path.dirname(os.path.abspath(__file__))
GAME = sys.argv[1]
key, NB, KB = {'power': ('power655', 55, 6), 'mega': ('mega645', 45, 6), 'loto': ('loto535', 35, 5)}[GAME]
D = json.load(open(os.path.join(B, 'all_data.json'), encoding='utf-8'))[key]
R = [set(r) for r in D['res']]; DT = D['dates']; T = len(R)
H = list(range(NB // 10 + 1)); NUM = {h: [n for n in range(1, NB + 1) if n // 10 == h] for h in H}
WS = (10, 20, 50, 100, 200)
def gap(n, t):
    g = 0
    while g < t and n not in R[t - 1 - g]: g += 1
    return g
GAP = {t: {n: gap(n, t) for n in range(1, NB + 1)} for t in range(T - 260, T + 1)}

print(f'## {GAME} — chu kỳ theo hàng, đến {DT[-1]}\n')
# ---- (A1) sau bao nhiêu kỳ hàng đủ số ----
print('### (A1) Bắt đầu từ một kỳ bất kỳ: mất bao nhiêu kỳ thì hàng "đủ số" (mọi số của hàng đều đã về)\n')
print('| Hàng | Số trong hàng | Trung vị (200 kỳ) | Đủ trong ≤10 kỳ | ≤15 kỳ | ≤20 kỳ | Trung vị 50 kỳ gần |\n|---|---|---|---|---|---|---|')
def cover(h, s):
    need = set(NUM[h]); k = 0
    while need and s + k < T: need -= R[s + k]; k += 1
    return k if not need else None
for h in H:
    xs = [cover(h, s) for s in range(T - 260, T - 60)]; xs = sorted(x for x in xs if x)
    rec = sorted(x for x in (cover(h, s) for s in range(T - 110, T - 60)) if x)
    med = lambda a: a[len(a) // 2] if a else None
    print(f'| {h}x | {len(NUM[h])} | {med(xs)} kỳ | {sum(x <= 10 for x in xs) * 100 // len(xs)}% | {sum(x <= 15 for x in xs) * 100 // len(xs)}% | {sum(x <= 20 for x in xs) * 100 // len(xs)}% | {med(rec)} kỳ |')

# ---- (A2) hàng gần đủ: số còn thiếu (chưa về trong L kỳ) có về sớm không ----
print('\n### (A2) Số "còn thiếu" của hàng: hàng đã về đủ trừ 1–2 số trong L kỳ gần → số thiếu về trong 1 / 3 / 5 kỳ tới\n')
print('So với nhóm số vắng cùng mức (≥L kỳ) nhưng hàng của nó còn thiếu nhiều (≥3 số). Mỗi ô: % lượt số đó về (200 kỳ) · số lượt\n')
print('| L | Nhóm | Về trong 1 kỳ | trong 3 kỳ | trong 5 kỳ |\n|---|---|---|---|---|')
A2 = {}
for L in (10, 15, 20):
    g1, g2 = [], []
    for t in range(T - 205, T - 5):
        for h in H:
            miss = [n for n in NUM[h] if GAP[t][n] >= L]
            (g1 if 1 <= len(miss) <= 2 else g2 if len(miss) >= 3 else []).extend((n, t) for n in miss)
    def rate(g, k): return sum(any(n in R[t + j] for j in range(k)) for n, t in g) / len(g) * 100 if g else 0
    for lab, g in (('Thiếu 1–2 số (hàng gần đủ)', g1), ('Thiếu ≥3 số', g2)):
        print(f'| {L} | {lab} | {rate(g, 1):.1f}% | {rate(g, 3):.1f}% | {rate(g, 5):.1f}% · {len(g)} lượt |')
    A2[L] = (rate(g1, 1), rate(g2, 1))

# ---- (B) bù / hãm theo tổng 10 kỳ ----
print('\n### (B) Bù / hãm: số lượng hàng ra trong 10 kỳ gần so với mức thường của chính hàng đó (200 kỳ trước) — % kỳ đúng\n')
def c10(i, t): return sum(len(R[u] & set(NUM[H[i]])) for u in range(t - 10, t))
def band(i, t):
    xs = sorted(c10(i, u) for u in range(t - 200, t)); return xs[len(xs) // 5], xs[len(xs) * 4 // 5]
BD = {t: [band(i, t) for i in range(len(H))] for t in range(T - 200, T + 1)}
print('| Hàng | Ra ÍT 10 kỳ (≤ mức thấp) → kỳ sau có ≥1 số | số kỳ | Ra NHIỀU 10 kỳ (≥ mức cao) → kỳ sau ≤1 số | số kỳ | Ra NHIỀU → kỳ sau vắng |\n|---|---|---|---|---|---|')
def pct(cond, ok):
    out = []
    for W in WS:
        ts = [t for t in range(T - W, T) if cond(t)]; out.append(f'{sum(ok(t) for t in ts) * 100 // len(ts)}%' if ts else '—')
    return ' / '.join(out), sum(1 for t in range(T - 200, T) if cond(t))
for i, h in enumerate(H):
    S = set(NUM[h])
    a, na = pct(lambda t: c10(i, t) <= BD[t][i][0], lambda t: len(R[t] & S) >= 1)
    b, nb = pct(lambda t: c10(i, t) >= BD[t][i][1], lambda t: len(R[t] & S) <= 1)
    c, _ = pct(lambda t: c10(i, t) >= BD[t][i][1], lambda t: len(R[t] & S) == 0)
    print(f'| {h}x | {a} | {na} | {b} | {nb} | {c} |')

# ---- hiện trạng ----
print(f'\n### Hiện trạng kỳ tới (sau {DT[-1]})\n')
print('| Hàng | Ra 10 kỳ gần (mức thường) | Trạng thái | Số chưa về 10 kỳ | Số chưa về 15 kỳ |\n|---|---|---|---|---|')
for i, h in enumerate(H):
    lo, hi = BD[T][i]; v = c10(i, T)
    st = 'ra ÍT' if v <= lo else 'ra NHIỀU' if v >= hi else 'bình thường'
    m10 = [n for n in NUM[h] if GAP[T][n] >= 10]; m15 = [n for n in NUM[h] if GAP[T][n] >= 15]
    print(f"| {h}x | {v} ({lo}–{hi}) | {st} | {' '.join(f'{n:02d}' for n in m10) or '— (đủ)'} | {' '.join(f'{n:02d}' for n in m15) or '— (đủ)'} |")

# ---- (C) Nhịp nghỉ của hàng → đoán hàng VẮNG để loại cả hàng (anh 14/10) ----
# Trạng thái mỗi hàng = chuỗi k kỳ gần (0 = vắng, 1 = ra 1 số, 2 = ra ≥2). Học 200 kỳ trước kỳ đang xét:
# trạng thái nào mà kỳ kế tiếp hàng VẮNG ≥ ngưỡng (đủ ≥8 lần) → kỳ này loại cả hàng. Chấm % kỳ loại đúng.
print('\n### (C) Nhịp nghỉ hàng → loại cả hàng khi đoán vắng (học 200 kỳ trước, chạy tiến)\n')
print('| Hàng | Cách (chuỗi k kỳ, ngưỡng) | Loại đúng 10 / 20 / 50 / 100 / 200 | Số lần loại (200 kỳ) |\n|---|---|---|---|')
def stt(i, t, k): return tuple(min(len(R[t - 1 - j] & set(NUM[H[i]])), 2) for j in range(k))
BEST = {}
for i, h in enumerate(H):
    S = set(NUM[h])
    for k in (1, 2, 3, 4):
        for th in (0.6, 0.7):
            def fire(t, k=k, th=th):
                s = stt(i, t, k); n = v = 0
                for u in range(t - 200, t):
                    if stt(i, u, k) == s: n += 1; v += not (R[u] & S)
                return n >= 8 and v / n >= th
            F = {t: fire(t) for t in range(T - 200, T + 1)}
            r = []
            for W in WS:
                ts = [t for t in range(T - W, T) if F[t]]; r.append(sum(not (R[t] & S) for t in ts) / len(ts) * 100 if ts else None)
            n200 = sum(F[t] for t in range(T - 200, T))
            if n200:
                print(f"| {h}x | k={k}, ≥{int(th * 100)}% | {' / '.join('—' if v is None else f'{v:.0f}%' for v in r)} | {n200} |")
                if r[2] is not None and r[3] is not None and r[2] >= 70 and r[3] >= 70 and n200 >= 5:
                    BEST.setdefault(h, []).append((k, th, F[T]))
print('\nĐạt (loại đúng ≥70% ở 50 & 100 kỳ): ' + (' · '.join(f"{h}x k={k} ≥{int(th*100)}%" + (' → KỲ TỚI LOẠI' if f else '') for h, v in BEST.items() for k, th, f in v) or 'không có'))
