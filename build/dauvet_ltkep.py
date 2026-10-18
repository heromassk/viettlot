#!/usr/bin/env python3
"""Dấu vết SỐ LIÊN TIẾP và SỐ KÉP (anh 14/10/2026). Riêng từng game, chấm bằng % kỳ của chính nó ở 50 / 100 / 200 kỳ.
  python build/dauvet_ltkep.py power|mega|loto"""
import json, os, sys
from collections import Counter
B = os.path.dirname(os.path.abspath(__file__))
def active(R, NB, T):
    """Dùng trong goiy.py: luật chuỗi liên tiếp / kép đang kích hoạt cho kỳ T và đạt (đúng ≥70% ở 50 & 100 kỳ, ≥10 lần/200 kỳ).
    Luật: có cặp liền nhau 2 kỳ liền / ≥3 kỳ liền → kỳ sau không có cặp; có kép 2 / ≥3 kỳ liền → kỳ sau không kép."""
    R = [sorted(r) for r in R]; KEP = set(range(11, NB + 1, 11))
    LT = lambda t: any(b == a + 1 for a, b in zip(R[t], R[t][1:])); KP = lambda t: any(v in KEP for v in R[t])
    def run(f, t):
        g = 0
        while g < t and f(t - 1 - g): g += 1
        return g
    out = []
    for nm, f, fk, lab in (('lt', LT, 'lt', 'cặp số liền nhau'), ('kep', KP, 'kep', 'số kép')):
        for k, cond in ((2, lambda t, f=f: run(f, t) == 2), (3, lambda t, f=f: run(f, t) >= 3)):
            if not cond(T): continue
            acc = []; n200 = 0
            for W in (50, 100):   # tối đa 100 kỳ
                ts = [t for t in range(T - W, T) if cond(t)]; n200 = len(ts)
                acc.append(sum(not f(t) for t in ts) / len(ts) * 100 if ts else None)
            if n200 >= 6 and all(v is not None for v in acc[:2]) and acc[0] >= 70 and acc[1] >= 70:
                out.append(dict(lab=f'Có {lab} {k if k == 2 else "≥3"} kỳ liền → kỳ này không có {lab}', spec=dict(k='rng', f=fk, lo=0, hi=0, neg=False),
                                a50=round(acc[0]), a100=round(acc[1]), a200=round(acc[1] or 0), n200=n200))
    return out

if __name__ == '__main__':
    GAME = sys.argv[1]
    key, NB, KB = {'power': ('power655', 55, 6), 'mega': ('mega645', 45, 6), 'loto': ('loto535', 35, 5)}[GAME]
    D = json.load(open(os.path.join(B, 'all_data.json'), encoding='utf-8'))[key]
    R = [sorted(r) for r in D['res']]; DT = D['dates']; T = len(R)
    SES = ['13' if '13h' in d else '21' for d in DT] if GAME == 'loto' else None
    KEP = [n for n in range(11, NB + 1, 11)]
    lt = lambda t: [(a, b) for a, b in zip(R[t], R[t][1:]) if b == a + 1]
    kp = lambda t: [v for v in R[t] if v in KEP]
    LT = {t: lt(t) for t in range(T)}; KP = {t: kp(t) for t in range(T)}
    WS = (50, 100, 200)
    def run(f, t):   # số kỳ liền trước t mà f(u) đúng
        g = 0
        while g < t and f(t - 1 - g): g += 1
        return g
    def cungtruoc(t):
        u = t - 1
        while u >= 0 and SES[u] != SES[t]: u -= 1
        return u
    def pct(cond, ok):
        out, n2 = [], 0
        for W in WS:
            ts = [t for t in range(T - W, T) if cond(t)]; n2 = len(ts)
            out.append(f'{sum(ok(t) for t in ts) * 100 // len(ts)}' if ts else '—')
        return ' / '.join(out) + '%', n2
    print(f'## {GAME} — dấu vết số liên tiếp & số kép, đến {DT[-1]}\n')
    for nm, X in (('Có cặp số liền nhau', LT), ('Có số kép', KP)):
        co = lambda t, X=X: bool(X[t])
        print(f'### {nm} — kỳ sau có không, theo kỳ trước (% kỳ sau CÓ · 50 / 100 / 200 kỳ · số lần trong 200)\n')
        print('| Kỳ trước | Kỳ sau có | Số lần |\n|---|---|---|')
        a, n = pct(lambda t: True, co); print(f'| (mọi kỳ) | {a} | {n} |')
        for lab, c in (('kỳ trước có', lambda t: co(t - 1)), ('kỳ trước không', lambda t: not co(t - 1)),
                       ('không liền 2 kỳ', lambda t: run(lambda u: not co(u), t) == 2), ('không liền ≥3 kỳ', lambda t: run(lambda u: not co(u), t) >= 3),
                       ('có liền 2 kỳ', lambda t: run(co, t) == 2), ('có liền ≥3 kỳ', lambda t: run(co, t) >= 3)):
            a, n = pct(c, co); print(f'| {lab} | {a} | {n} |')
        if SES:
            for lab, c in (('kỳ cùng giờ trước có', lambda t: co(cungtruoc(t))), ('kỳ cùng giờ trước không', lambda t: not co(cungtruoc(t)))):
                a, n = pct(c, co); print(f'| {lab} | {a} | {n} |')
        print()
    # liên tiếp: cặp có dính số kỳ trước không
    print('### Cặp liền nhau: có dính số kỳ trước không (200 kỳ)\n')
    pairs = [(t, p) for t in range(T - 200, T) for p in LT[t]]
    dinh = sum(1 for t, p in pairs if set(p) & set(R[t - 1])); ke = sum(1 for t, p in pairs if not set(p) & set(R[t - 1]) and any(abs(v - w) == 1 for v in p for w in R[t - 1]))
    print(f'{len(pairs)} cặp: {dinh} cặp ({dinh * 100 // len(pairs)}%) có 1 số là số kỳ trước · {ke} cặp ({ke * 100 // len(pairs)}%) kề (±1) số kỳ trước · còn lại {len(pairs) - dinh - ke} cặp không dính\n')
    vt = Counter(min(a // 10, NB // 10) for t, (a, b) in pairs)
    print('Cặp hay nằm ở hàng: ' + ' · '.join(f'{h}x: {vt[h]} cặp' for h in sorted(vt)) + '\n')
    # kép: từng số kép
    print('### Từng số kép (200 kỳ)\n')
    print('| Số | Ra 50 / 100 / 200 kỳ | Đang vắng | Kép kỳ trước ra lại kỳ sau |\n|---|---|---|---|')
    for k in KEP:
        c = [sum(k in R[t] for t in range(T - W, T)) for W in WS]; g = run(lambda u: k not in R[u], T)
        ts = [t for t in range(T - 200, T) if k in R[t - 1]]
        print(f"| {k} | {' / '.join(map(str, c))} lần | {g} kỳ | {sum(k in R[t] for t in ts)}/{len(ts)} |")
    ts = [t for t in range(T - 200, T) if KP[t - 1]]
    ke2 = sum(1 for t in ts if any(abs(a - b) == 11 for a in KP[t - 1] for b in KP[t]))
    print(f'\nKỳ trước có kép → kỳ sau có kép liền kề (11↔22…): {ke2}/{len(ts)} lần')
    print(f"\nHiện tại: kỳ trước {DT[-1]}: {' '.join(f'{v:02d}' for v in R[-1])} · cặp liền nhau: {LT[T - 1] or 'không'} · kép: {KP[T - 1] or 'không'} · "
          f"không có cặp liền {run(lambda u: not LT[u], T)} kỳ · không có kép {run(lambda u: not KP[u], T)} kỳ")

