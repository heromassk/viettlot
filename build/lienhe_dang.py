#!/usr/bin/env python3
"""Liên hệ giữa các đặc điểm DẠNG qua các kỳ (anh 14/10/2026): kỳ trước có đặc điểm A ở trạng thái s → kỳ sau đặc điểm B
rơi vào trạng thái r. Đặc điểm: tổng (thấp/giữa/cao so 200 kỳ trước), số lẻ, số nhỏ, cặp liền nhau, số kép, trùng kỳ trước,
tổng tăng/giảm so kỳ trước nữa. Loto: tổng, lẻ, nhỏ tính trên dãy 6 số (có số may mắn).
Luật đạt: đúng ≥70% ở khung 50, 100 và 200 kỳ, đủ ≥15 lần (200 kỳ), và cao hơn ≥10 điểm so với khi kỳ trước ở trạng thái
KHÁC của A (để biết đó là liên hệ thật của A, không phải B lúc nào cũng vậy). Mỗi game chạy riêng.
  python build/lienhe_dang.py power|mega|loto"""
import json, os, sys
B = os.path.dirname(os.path.abspath(__file__))
if __name__ == '__main__':
    GAME = sys.argv[1]
    key, NB, KB = {'power': ('power655', 55, 6), 'mega': ('mega645', 45, 6), 'loto': ('loto535', 35, 5)}[GAME]
    D = json.load(open(os.path.join(B, 'all_data.json'), encoding='utf-8'))[key]
    R = [sorted(r) for r in D['res']]; LK = D.get('lk') if GAME == 'loto' else None; DT = D['dates']; T = len(R)
    def raw(t):
        s = R[t]; d6 = s + ([LK[t]] if LK else [])
        return dict(tong=sum(d6), le=sum(v % 2 for v in d6), nho=sum(v <= NB // 2 for v in s) + (1 if LK and LK[t] <= 6 else 0),
                    lt=sum(1 for a, b in zip(s, s[1:]) if b == a + 1), kep=sum(1 for v in s if v % 11 == 0), trung=len(set(s) & set(R[t - 1])))
    F = {t: raw(t) for t in range(T - 420, T)}
    N6 = KB + (1 if LK else 0)
    def tert(t):   # ngưỡng tổng thấp/cao từ 200 kỳ trước t
        xs = sorted(F[u]['tong'] for u in range(t - 200, t)); return xs[len(xs) // 3], xs[len(xs) * 2 // 3]
    TH = {t: tert(t) for t in range(T - 205, T + 1)}
    def st(t):
        """trạng thái các đặc điểm của kỳ t (ngưỡng tổng lấy theo kỳ t)"""
        f = F[t]; a, b = TH[t]; mid = N6 / 2
        return {'Tổng': 'thấp' if f['tong'] <= a else 'cao' if f['tong'] > b else 'giữa',
                'Số lẻ': f'≤{int(mid) - 1}' if f['le'] < mid - 0.5 else f'≥{int(mid) + 1}' if f['le'] > mid + 0.5 else str(int(mid)) if N6 % 2 == 0 else ('ít' if f['le'] < mid else 'nhiều'),
                'Số nhỏ': f'≤{int(mid) - 1}' if f['nho'] < mid - 0.5 else f'≥{int(mid) + 1}' if f['nho'] > mid + 0.5 else str(int(mid)) if N6 % 2 == 0 else ('ít' if f['nho'] < mid else 'nhiều'),
                'Cặp liền nhau': 'có' if f['lt'] else 'không', 'Số kép': 'có' if f['kep'] else 'không', 'Trùng kỳ trước': 'có' if f['trung'] else 'không',
                'Tổng so kỳ trước': 'tăng' if f['tong'] > F[t - 1]['tong'] else 'giảm'}
    S = {t: st(t) for t in range(T - 205, T)}
    FEAT = list(S[T - 1].keys())
    OUT = [f for f in FEAT if f != 'Tổng so kỳ trước']
    WS = (50, 100, 200); rows = []
    for A in FEAT:
        vals = sorted({S[t][A] for t in range(T - 200, T)})
        for s in vals:
            for Bf in OUT:
                outs = sorted({S[t][Bf] for t in range(T - 200, T)})
                # kết quả: 1 trạng thái, hoặc "không phải" 1 trạng thái
                for r in outs:
                    for neg in ((False,) if len(outs) == 2 else (False, True)):
                        hit = (lambda v, r=r, neg=neg: (v != r) if neg else (v == r))
                        acc = []; n200 = 0
                        for W in WS:
                            ts = [t for t in range(T - W, T) if S[t - 1][A] == s]; n200 = len(ts)
                            acc.append(sum(hit(S[t][Bf]) for t in ts) / len(ts) * 100 if ts else None)
                        other = [t for t in range(T - 200, T) if S[t - 1][A] != s]
                        oth = sum(hit(S[t][Bf]) for t in other) / len(other) * 100 if other else None
                        if n200 >= 15 and all(v is not None and v >= 70 for v in acc) and oth is not None and acc[2] - oth >= 10:
                            rows.append((acc[2] - oth, A, s, Bf, ('không ' if neg else '') + r, acc, oth, n200))
    print(f'## {GAME} — liên hệ dạng kỳ trước → kỳ sau, đến {DT[-1]}\n')
    print('| Kỳ trước | Kỳ sau | Đúng 50 / 100 / 200 kỳ | Khi kỳ trước khác trạng thái | Số lần (200) |\n|---|---|---|---|---|')
    for d, A, s, Bf, r, acc, oth, n in sorted(rows, key=lambda x: -x[0]):
        print(f"| {A}: {s} | {Bf}: {r} | {' / '.join(f'{v:.0f}' for v in acc)}% | {oth:.0f}% | {n} |")
    if not rows: print('| — | không có liên hệ đạt | | | |')
    cur = S[T - 1]
    print(f"\nKỳ trước {DT[-1]}: " + ' · '.join(f'{k} {v}' for k, v in cur.items()) + f" (tổng {F[T - 1]['tong']}; ngưỡng thấp/cao {TH[T][0]}/{TH[T][1]})")
    act = [x for x in rows if cur[x[1]] == x[2]]
    print('Đang có hiệu lực kỳ tới: ' + (' · '.join(f"{Bf}: {r} ({acc[0]:.0f}/{acc[1]:.0f}/{acc[2]:.0f}%)" for _, A, s, Bf, r, acc, oth, n in act) or 'không có'))



def active(R, LK, NB, KB, T, game, bh=False):
    """Dùng trong goiy.py: các luật liên hệ ĐẠT đang có hiệu lực cho kỳ T, kèm spec để kiểm vé (khuon.check, k='rng')."""
    R = [sorted(r) for r in R]; N6 = KB + (1 if LK else 0); mid = N6 / 2
    def raw(t):
        s = R[t]; d6 = s + ([LK[t]] if LK else [])
        return dict(tong=sum(d6), le=sum(v % 2 for v in d6), nho=sum(v <= NB // 2 for v in s) + (1 if LK and LK[t] <= 6 else 0),
                    lt=sum(1 for a, b in zip(s, s[1:]) if b == a + 1), kep=sum(1 for v in s if v % 11 == 0), trung=len(set(s) & set(R[t - 1])))
    F = {t: raw(t) for t in range(T - 420, T)}
    TH = {}
    for t in range(T - 205, T + 1):
        xs = sorted(F[u]['tong'] for u in range(t - 100, t)); TH[t] = (xs[len(xs) // 3], xs[len(xs) * 2 // 3])
    def cat3(v): return '≤2' if v < mid - 0.5 else '≥4' if v > mid + 0.5 else '3'
    def st(t):
        f = F[t]; a, b = TH[t]
        return {'Tổng': 'thấp' if f['tong'] <= a else 'cao' if f['tong'] > b else 'giữa', 'Số lẻ': cat3(f['le']), 'Số nhỏ': cat3(f['nho']),
                'Cặp liền nhau': 'có' if f['lt'] else 'không', 'Số kép': 'có' if f['kep'] else 'không',
                'Trùng kỳ trước': 'có' if f['trung'] else 'không', 'Tổng so kỳ trước': 'tăng' if f['tong'] > F[t - 1]['tong'] else 'giảm'}
    S = {t: st(t) for t in range(T - 205, T)}
    FE = list(S[T - 1]); OUTF = [f for f in FE if f != 'Tổng so kỳ trước']; out = []
    FK = {'Tổng': 'tong', 'Số lẻ': 'le', 'Số nhỏ': 'nho', 'Cặp liền nhau': 'lt', 'Số kép': 'kep', 'Trùng kỳ trước': 'trung'}
    PASS = None
    if bh:   # BH (q=0,10) trên MỌI liên hệ (A, trạng thái A, B, kết quả) đủ ≥15 lần ở 200 kỳ; H0: đúng ≤70% (anh 15/10/2026)
        from scipy.stats import binomtest
        fam = []
        for A in FE:
            for s0 in sorted({S[t][A] for t in range(T - 200, T)}):
                ts = [t for t in range(T - 200, T) if S[t - 1][A] == s0]
                if len(ts) < 15: continue
                for Bf in OUTF:
                    outs = sorted({S[t][Bf] for t in range(T - 100, T)})
                    for r in outs:
                        for neg in ((False,) if len(outs) == 2 else (False, True)):
                            k = sum(((S[t][Bf] != r) if neg else (S[t][Bf] == r)) for t in ts)
                            fam.append(((A, s0, Bf, r, neg), binomtest(k, len(ts), 0.70, alternative='greater').pvalue))
        fam.sort(key=lambda x: x[1]); cut = max([i for i, (_, pv) in enumerate(fam, 1) if pv <= 0.10 * i / len(fam)] or [0])
        PASS = {key for key, _ in fam[:cut]}
    a, b = TH[T]
    RG = {'thấp': (0, a), 'giữa': (a + 1, b), 'cao': (b + 1, 9999), '≤2': (0, 2), '3': (3, 3), '≥4': (4, 9), 'có': (1, 9), 'không': (0, 0)}
    for A in FE:
        s = S[T - 1][A]
        for Bf in OUTF:
            outs = sorted({S[t][Bf] for t in range(T - 100, T)})
            for r in outs:
                for neg in ((False,) if len(outs) == 2 else (False, True)):
                    hit = (lambda v, r=r, neg=neg: (v != r) if neg else (v == r)); acc = []
                    for W in (50, 100):
                        ts = [t for t in range(T - W, T) if S[t - 1][A] == s]
                        acc.append(sum(hit(S[t][Bf]) for t in ts) / len(ts) * 100 if ts else None)
                    ts200 = [t for t in range(T - 100, T) if S[t - 1][A] == s]; oth = [t for t in range(T - 100, T) if S[t - 1][A] != s]
                    if len(ts200) < 10 or not oth or any(v is None or v < 70 for v in acc): continue
                    if acc[1] - sum(hit(S[t][Bf]) for t in oth) / len(oth) * 100 < 10: continue
                    if PASS is not None and (A, s, Bf, r, neg) not in PASS: continue
                    lo, hi = RG[r]
                    out.append(dict(lab=f'{A} kỳ trước {s} → {Bf} {"không " if neg else ""}{r}' + (f' ({lo}–{hi})' if Bf == 'Tổng' else ''),
                                    spec=dict(k='rng', f=FK[Bf], lo=lo, hi=hi, neg=neg), a50=round(acc[0]), a100=round(acc[1]), a200=round(acc[1]), n200=len(ts200)))
    return out
