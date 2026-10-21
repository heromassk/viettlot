# Cách lai (anh 21/10/2026: "riêng thì tín hiệu rõ hơn, chiều rõ hơn"): tâm / chiều / tổng-hiệu lấy theo dãy CÙNG BUỔI,
# số lần ra đếm liền 2 buổi. Chấm trên mọi kỳ và tách riêng kỳ 13h, 21h.
import json, itertools
d = json.load(open('build/all_data.json'))['loto535']; LK = d['lk']; D = d['dates']; N = len(LK)
SP = {}
for t in range(N):
    g = D[t][-3:]; SP[t] = [u for u in range(t - 1, -1, -1) if D[u].endswith(g)][:2]
def pick(t, cen, w, exc, exs, dirm, bd, thm, bt):
    s1, s2 = SP[t]; m1, m2 = LK[s1], LK[s2]; p1, p2 = LK[t - 1], LK[t - 2]; g = D[t][-3:]
    c = {k: 0 for k in range(1, 13)}; c50 = dict(c)
    for u in range(t - 10, t): c[LK[u]] += 1
    for u in range(t - 50, t): c50[LK[u]] += 1
    C = p1 if cen == 'liền' else m1
    ok = [k for k in range(1, 13) if abs(k - C) <= w and not (exc and k == p1) and not (exs and k == m1)]
    f = None
    if dirm in ('nghiêng', 'cả hai'):
        if m1 >= 7: f = lambda k: k < m1
        elif g == '21h': f = lambda k: k > m1
    if f is None and dirm in ('đảo', 'cả hai') and m1 != m2:
        f = (lambda k: k < m1) if m1 > m2 else (lambda k: k > m1)
    TH = {p1 + p2, abs(p1 - p2)} if thm == 'liền' else {m1 + m2, abs(m1 - m2)} if thm == 'buổi' else set()
    return sorted(ok, key=lambda k: (-c[k] - (bd if f and f(k) else 0) - (bt if k in TH else 0), -c50[k], k))[:2]
idx13 = [t for t in range(N) if D[t].endswith('13h')]; idx21 = [t for t in range(N) if D[t].endswith('21h')]
res = []
for P in itertools.product(('liền', 'buổi'), (3, 4), (True, False), (True, False), ('nghiêng', 'đảo', 'cả hai'), (1, 2), ('liền', 'buổi', 'không'), (1, 2)):
    al = [sum(LK[t] in pick(t, *P) for t in range(N - W, N)) for W in (20, 50, 100, 200)]
    a13 = [sum(LK[t] in pick(t, *P) for t in idx13[-W:]) for W in (50, 100)]
    a21 = [sum(LK[t] in pick(t, *P) for t in idx21[-W:]) for W in (50, 100)]
    res.append((al[1] + al[2] + al[3], al, a13, a21, P))
res.sort(key=lambda x: -x[0])
print('Đang dùng (để so): liền 2 buổi 9/19/29/53 · 13h 50/100: 11/26 · 21h 50/100: 18/27')
for sc, al, a13, a21, P in res[:8]: print(' / '.join(map(str, al)), '| 13h', a13, '| 21h', a21, '|', P)
