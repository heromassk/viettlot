#!/usr/bin/env python3
"""Dấu vết số may mắn Loto (anh 14/10/2026). Chấm bằng chính luật: % kỳ đúng ở 10/20/50/100/200 kỳ; luật loại thêm
tỉ lệ ra của số bị loại so với TB (1/12). Đạt: đúng ≥70% ở khung 50 & 100 và số bị loại ra ≤ TB (luật loại);
khẳng định: đúng ≥70% ở khung 50 & 100. Sau đó ghép các luật đạt vào pool 2 số (nóng 10 kỳ) và chấm lại.
  python build/somayman_dauvet.py"""
import json, os
B = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(B, 'all_data.json'), encoding='utf-8'))['loto535']
LK = D['lk']; R = [sorted(r) for r in D['res']]; DT = D['dates']; T = len(LK)
SES = ['13' if '13h' in d else '21' for d in DT] + ['13' if '21h' in DT[-1] else '21']
K12 = list(range(1, 13)); TB = 100 / 12
def gap(t): return {k: next((g for g in range(t) if LK[t - 1 - g] == k), t) for k in K12}
def cnt(t, W): return {k: sum(LK[u] == k for u in range(max(0, t - W), t)) for k in K12}
prev_ses = lambda t: next((u for u in range(t - 1, -1, -1) if SES[u] == SES[t]), None)
LOAI = {
    'Bỏ số may mắn kỳ trước': lambda t: {LK[t - 1]},
    'Bỏ số may mắn 2 kỳ trước': lambda t: {LK[t - 2]},
    'Bỏ số may mắn cùng phiên hôm trước': lambda t: {LK[prev_ses(t)]},
    'Bỏ số ra ≥2 lần trong 5 kỳ': lambda t: {k for k, v in cnt(t, 5).items() if v >= 2},
    'Bỏ số ra ≥3 lần trong 10 kỳ': lambda t: {k for k, v in cnt(t, 10).items() if v >= 3},
    'Bỏ số vắng lâu nhất': lambda t: {max(K12, key=lambda k: (gap(t)[k], -k))},
    'Bỏ số vắng ≥30 kỳ': lambda t: {k for k, g in gap(t).items() if g >= 30},
    'Bỏ số vắng ≥40 kỳ': lambda t: {k for k, g in gap(t).items() if g >= 40},
    'Bỏ số ra ít nhất 100 kỳ': lambda t: {min(K12, key=lambda k: (cnt(t, 100)[k], k))},
    'Bỏ số cách số kỳ trước ≥7': lambda t: {k for k in K12 if abs(k - LK[t - 1]) >= 7},
    'Bỏ số cách số kỳ trước ≥9': lambda t: {k for k in K12 if abs(k - LK[t - 1]) >= 9},
    'Bỏ số trùng 1 số chính kỳ trước': lambda t: {k for k in K12 if k in R[t - 1]},
    'Bỏ số vừa ra lại sau đúng 1 kỳ (ra–vắng 1–ra)': lambda t: {LK[t - 1]} if t >= 3 and LK[t - 3] == LK[t - 1] else set(),
}
KD = {
    'Khác số may mắn kỳ trước': lambda t: LK[t] != LK[t - 1],
    'Cách số may mắn kỳ trước ≤3': lambda t: abs(LK[t] - LK[t - 1]) <= 3,
    'Cách số may mắn kỳ trước ≤5': lambda t: abs(LK[t] - LK[t - 1]) <= 5,
    'Đổi chẵn/lẻ so với kỳ trước': lambda t: LK[t] % 2 != LK[t - 1] % 2,
    'Cùng chẵn/lẻ với kỳ trước': lambda t: LK[t] % 2 == LK[t - 1] % 2,
    'Nhỏ (1–6) nếu kỳ trước lớn, lớn nếu kỳ trước nhỏ': lambda t: (LK[t] <= 6) != (LK[t - 1] <= 6),
    'Cùng nửa (1–6 / 7–12) với kỳ trước': lambda t: (LK[t] <= 6) == (LK[t - 1] <= 6),
    'Nằm trong 6 số ra nhiều nhất 20 kỳ': lambda t: LK[t] in sorted(K12, key=lambda k: (-cnt(t, 20)[k], k))[:6],
    'Nằm trong 6 số ra nhiều nhất 50 kỳ': lambda t: LK[t] in sorted(K12, key=lambda k: (-cnt(t, 50)[k], k))[:6],
    'Đã ra trong 10 kỳ gần': lambda t: cnt(t, 10)[LK[t]] >= 1,
    'Đã ra trong 15 kỳ gần': lambda t: cnt(t, 15)[LK[t]] >= 1,
}
WS = (10, 20, 50, 100, 200)
def win(f, W): return sum(f(t) for t in range(T - W, T)) / W * 100
print(f'## Dấu vết số may mắn Loto — chấm bằng chính luật, đến {DT[-1]} (TB mỗi số ra {TB:.1f}%/kỳ)\n')
print('### Luật loại\n\n| Luật | Bỏ TB | Kỳ đúng 10 / 20 / 50 / 100 / 200 | Số bị loại ra (100 kỳ) | Đạt |\n|---|---|---|---|---|')
OKL = []
for nm, f in LOAI.items():
    ok = [win(lambda t: LK[t] not in f(t), W) for W in WS]
    z = sum(len(f(t)) for t in range(T - 100, T)); h = sum(LK[t] in f(t) for t in range(T - 100, T)); ra = h / z * 100 if z else None
    good = ok[2] >= 70 and ok[3] >= 70 and ra is not None and ra <= TB and z >= 30
    if good: OKL.append(nm)
    print(f"| {nm} | {z / 100:.1f} | {' / '.join(f'{v:.0f}%' for v in ok)} | {'—' if ra is None else f'{ra:.1f}%'} | {'✔' if good else '✘'} |")
print('\n### Khẳng định\n\n| Khẳng định | Kỳ đúng 10 / 20 / 50 / 100 / 200 | Đạt ≥70% (50 & 100) |\n|---|---|---|')
for nm, f in KD.items():
    ok = [win(f, W) for W in WS]
    print(f"| {nm} | {' / '.join(f'{v:.0f}%' for v in ok)} | {'✔' if ok[2] >= 70 and ok[3] >= 70 else '✘'} |")
# ghép vào pool 2 số: nóng 10 kỳ (hòa → 50 kỳ), bỏ số của các luật loại đạt (thêm dần, giữ cả nhóm đúng ≥70%)
def pick(t, loai):
    ex = set().union(*[LOAI[nm](t) for nm in loai]) if loai else set()
    c10, c50 = cnt(t, 10), cnt(t, 50)
    return [k for k in sorted(K12, key=lambda k: (-c10[k], -c50[k], k)) if k not in ex][:2]
print('\n### Pool 2 số: nóng 10 kỳ + bỏ số theo luật loại đạt — % kỳ đoán đúng 10 / 20 / 50 / 100 / 200\n')
print('| Cách | Đúng |\n|---|---|')
print(f"| Nóng 10 kỳ (đang dùng) | {' / '.join(f'{win(lambda t: LK[t] in pick(t, []), W):.0f}%' for W in WS)} |")
for nm in OKL:
    print(f"| + {nm} | {' / '.join(f'{win(lambda t, nm=nm: LK[t] in pick(t, [nm]), W):.0f}%' for W in WS)} |")
if len(OKL) > 1:
    print(f"| + tất cả luật loại đạt | {' / '.join(f'{win(lambda t: LK[t] in pick(t, OKL), W):.0f}%' for W in WS)} |")

# ---- ghép dấu vết "cách số kỳ trước ≤ d" / "đã ra trong 15 kỳ" vào pool 2 số ----
def pick2(t, d=None, r15=False):
    c10, c50, c15 = cnt(t, 10), cnt(t, 50), cnt(t, 15)
    ok = [k for k in K12 if (d is None or abs(k - LK[t - 1]) <= d) and (not r15 or c15[k] >= 1)]
    return sorted(ok or K12, key=lambda k: (-c10[k], -c50[k], k))[:2]
print('\n### Ghép dấu vết vào pool 2 số (nóng 10 kỳ) — % kỳ đoán đúng 10 / 20 / 50 / 100 / 200 / 500\n\n| Cách | Đúng |\n|---|---|')
for lab, kw in (('Nóng 10 kỳ (đang dùng)', {}), ('+ chỉ chọn trong ±5 quanh số kỳ trước', dict(d=5)), ('+ chỉ chọn trong ±4', dict(d=4)), ('+ chỉ chọn trong ±6', dict(d=6)),
                ('+ chỉ chọn số đã ra trong 15 kỳ', dict(r15=True)), ('+ ±5 và đã ra trong 15 kỳ', dict(d=5, r15=True))):
    print(f"| {lab} | {' / '.join(f'{win(lambda t: LK[t] in pick2(t, **kw), W):.0f}%' for W in WS + (500,))} |")
print('\nKỳ tới (+ ±5):', pick2(T, d=5), '· kỳ trước về', LK[-1])
