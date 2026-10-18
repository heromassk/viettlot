"""Dự đoán DẠNG kỳ tới từng mặt (anh 14/10/2026: "kỳ này khả năng cao vào dạng nào").
Mỗi mặt (chẵn–lẻ, nhỏ–lớn, tổng, liên tiếp, trùng kỳ trước, số kép, số lượng từng hàng): đếm trong 200 kỳ trước, mỗi khi
kỳ trước ở CÙNG trạng thái như kỳ vừa quay thì kỳ sau ra giá trị nào → lấy 1–2 giá trị hay gặp nhất (cộng ≥60%).
Chấm lùi: % kỳ giá trị thật nằm trong dự đoán (chạy tiến, khung 50 / 100 kỳ). Riêng từng game.
Loto: chẵn–lẻ, nhỏ–lớn, tổng tính dãy 6 số (có số may mắn).
  du(R, LK, NB, KB, T) -> list dict(mat, du (nhãn), p (% trong 200 kỳ), a50, a100)"""
import os
from collections import Counter

def du(R, LK, NB, KB, T, specs=(), ses=None):
    """specs: luật dạng đang hiệu lực (khuôn + liên hệ) — loại các giá trị trái luật khỏi dự đoán.
    ses: phiên từng kỳ (Loto '13'/'21', gồm cả kỳ tới) → thêm cách đoán theo 10 kỳ gần / 10 kỳ cùng giờ (anh 14/10/2026)."""
    R = [sorted(r) for r in R]; N6 = KB + (1 if LK else 0); H = NB // 10 + 1
    def raw(t):
        s = R[t]; d6 = s + ([LK[t]] if LK else []); hang = [0] * H
        for v in s: hang[v // 10] += 1
        return dict(tong=sum(d6), le=sum(v % 2 for v in d6), nho=sum(v <= NB // 2 for v in s) + (1 if LK and LK[t] <= 6 else 0),
                    lt=min(sum(1 for a, b in zip(s, s[1:]) if b == a + 1), 1), trung=min(len(set(s) & set(R[t - 1])), 2),
                    kep=min(sum(1 for v in s if v % 11 == 0), 1), hang=[min(c, 2) for c in hang])
    F = {t: raw(t) for t in range(T - 420, T)}
    def tband(t):
        xs = sorted(F[u]['tong'] for u in range(t - 100, t)); return xs[len(xs) // 3], xs[len(xs) * 2 // 3]
    TB = {t: tband(t) for t in range(T - 105, T + 1)}
    def val(t, m, tb=None):
        f = F[t]
        if m == 'tong':
            a, b = tb; return 0 if f['tong'] <= a else 2 if f['tong'] > b else 1
        if m.startswith('h'): return f['hang'][int(m[1:])]
        return f[m]
    MATS = [('le', 'Chẵn – lẻ'), ('nho', 'Nhỏ – lớn'), ('tong', 'Tổng'), ('lt', 'Cặp liền nhau'), ('trung', 'Trùng kỳ trước'), ('kep', 'Số kép')] + \
           [(f'h{i}', f'Hàng {i}x') for i in range(H)]
    def name(m, v, t):
        if m == 'le': return f'{N6 - v} chẵn – {v} lẻ'
        if m == 'nho': return f'{v} nhỏ – {N6 - v} lớn'
        if m == 'tong': a, b = TB[t]; return ('≤' + str(a)) if v == 0 else (f'>{b}') if v == 2 else f'{a + 1}–{b}'
        if m == 'lt': return 'có cặp liền nhau' if v else 'không có cặp liền nhau'
        if m == 'trung': return {0: 'không trùng', 1: 'trùng 1 số', 2: 'trùng ≥2 số'}[v]
        if m == 'kep': return 'có số kép' if v else 'không có số kép'
        return {0: 'vắng', 1: '1 số', 2: '≥2 số'}[v]
    def allow(m, v):
        if m == 'tong':
            a, b = TB[T]; lo, hi = ((0, a), (a + 1, b), (b + 1, 9999))[v]
            for sp in specs:
                if sp.get('k') == 'tong' and (hi < sp['lo'] or lo > sp['hi']): return False
                if sp.get('k') == 'rng' and sp['f'] == 'tong':
                    inn = sp['lo'] <= lo and hi <= sp['hi']; out = hi < sp['lo'] or lo > sp['hi']
                    if (not sp['neg'] and out) or (sp['neg'] and inn): return False
            return True
        for sp in specs:
            if m in ('le', 'nho', 'trung', 'lt', 'kep') and sp.get('k') == 'rng' and sp['f'] == m:
                inn = sp['lo'] <= v <= sp['hi']
                if inn == sp['neg']: return False
            if m in ('le', 'nho') and sp.get('k') == m and not (sp['lo'] <= v <= sp['hi']): return False
            if m == 'lt' and sp.get('k') == 'lt' and v > sp['max']: return False
            if m.startswith('h') and sp.get('k') == 'hang' and sp['i'] == int(m[1:]):
                if (sp['op'] == 'le' and v > sp['v']) or (sp['op'] == 'ge' and v < sp['v']): return False
        return True
    def cung(t, k):   # k kỳ cùng giờ gần nhất trước t
        out, u = [], t - 1
        while u >= t - 80 and len(out) < k:
            if ses[u] == ses[t]: out.append(u)
            u -= 1
        return out
    CACH = {'200': 'theo 100 kỳ (kỳ trước giống)', '10': 'theo 10 kỳ gần', 'g10': 'theo 10 kỳ cùng giờ', '20': 'theo 20 kỳ gần', 'g20': 'theo 20 kỳ cùng giờ', 'g200': 'theo 100 kỳ (kỳ cùng giờ trước giống)'}
    def pick(t, m, loc=False, cach='200'):
        """giá trị dự đoán cho kỳ t (chỉ dùng kỳ < t)"""
        tb = TB[t]
        if cach == '10': c = Counter(val(u, m, tb) for u in range(t - 10, t))
        elif cach == 'g10': c = Counter(val(u, m, tb) for u in cung(t, 10))
        elif cach == '20': c = Counter(val(u, m, tb) for u in range(t - 20, t))
        elif cach == 'g20': c = Counter(val(u, m, tb) for u in cung(t, 20))
        elif cach == 'g200':
            p0 = cung(t, 1)[0]; s = val(p0, m, tb)
            c = Counter(val(u, m, tb) for u in range(t - 100, t) if cung(u, 1) and val(cung(u, 1)[0], m, tb) == s)
        else:
            s = val(t - 1, m, tb); c = Counter(val(u, m, tb) for u in range(t - 100, t) if val(u - 1, m, tb) == s)
        n = sum(c.values())
        if n < (5 if cach in ('10', 'g10', '20', 'g20') else 12): c = Counter(val(u, m, tb) for u in range(t - 100, t)); n = sum(c.values())
        top = [(v, k) for v, k in c.most_common() if not loc or allow(m, v)] or c.most_common(); sel, acc = [], 0
        lim = 1 if m in ('lt', 'kep') else 2
        for v, k in top:
            sel.append(v); acc += k
            if acc / n >= 0.6 or len(sel) == lim: break
        return sel, acc / n * 100
    def gop(m, sel):
        """viết gọn, dễ hiểu (anh 14/10: "≥2 số hoặc 1 số" khó hiểu)"""
        S = set(sel)
        if len(S) == 1: return name(m, sel[0], T)
        if m.startswith('h'):
            lo, hi = int(m[1:]) * 10 or 1, min(int(m[1:]) * 10 + 9, NB)
            rg = f' (số {lo:02d}–{hi:02d})'
            return {frozenset({1, 2}): 'có ít nhất 1 số' + rg, frozenset({0, 1}): 'nhiều nhất 1 số (vắng hoặc 1 số)' + rg,
                    frozenset({0, 2}): 'vắng hoặc ≥2 số' + rg}[frozenset(S)]
        if m == 'trung': return {frozenset({0, 1}): 'trùng kỳ trước nhiều nhất 1 số', frozenset({1, 2}): 'trùng kỳ trước ít nhất 1 số',
                                 frozenset({0, 2}): 'không trùng hoặc trùng ≥2 số'}[frozenset(S)]
        if m == 'tong':
            a, b = TB[T]
            return {frozenset({0, 1}): f'tổng ≤{b}', frozenset({1, 2}): f'tổng >{a}', frozenset({0, 2}): f'tổng ≤{a} hoặc >{b} (không rơi vào {a + 1}–{b})'}[frozenset(S)]
        return ' hoặc '.join(name(m, v, T) for v in sel)
    out = []
    for m, lab in MATS:
        best = None
        for cach in ((os.environ.get('DU_CACH') or '200,10,g10,20,g20,g200').split(',') if ses else ('200',)):
            h = {t: val(t, m, TB[t]) in pick(t, m, False, cach)[0] for t in range(T - 100, T)}
            sc = (min(sum(h[t] for t in range(T - 50, T)) * 2, sum(h.values())), sum(h.values()))
            if best is None or sc > best[0]: best = (sc, cach, h)
        _, cach, hit = best
        sel, p = pick(T, m, True, cach)
        out.append(dict(mat=lab, du=gop(m, sel), p=round(p), cach=CACH[cach],
                        a50=round(sum(hit[t] for t in range(T - 50, T)) * 2), a100=round(sum(hit.values()))))
    return out
