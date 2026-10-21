# Kiểm kỹ thêm 4 cách dùng Fibonacci (anh 21/10/2026). Đếm ở 20 / 50 / 100 kỳ.
import json
d = json.load(open('build/all_data.json')); FIB = {1, 2, 3, 5, 8, 13, 21, 34, 55}
for key, nm, NB in (('loto535', 'Loto', 35), ('mega645', 'Mega', 45), ('power655', 'Power', 55)):
    RS = [sorted(x) for x in d[key]['res']]; R = [set(x) for x in RS]; n = len(R)
    print(f'\n==== {nm}')
    for W in (20, 50, 100):
        T = range(n - W, n)
        # 1) khoảng cách giữa các số liền nhau trong kỳ (đã xếp): bao nhiêu khoảng là số Fibonacci
        gaps = [b - a for t in T for a, b in zip(RS[t], RS[t][1:])]
        gc = {}; [gc.__setitem__(g, gc.get(g, 0) + 1) for g in gaps]
        fibg = sum(v for g, v in gc.items() if g in FIB); allk = len(gaps)
        k_all = sum(all((b - a) in FIB for a, b in zip(RS[t], RS[t][1:])) for t in T)
        # 2) số đang vắng đúng x kỳ, x là số Fibonacci → ra ngay kỳ sau
        st = {}
        for t in T:
            for x in range(1, NB + 1):
                u = t - 1
                while u >= 0 and x not in R[u]: u -= 1
                gp = t - u
                k = 'fib' if gp in FIB else 'khác'
                a = st.setdefault(k, [0, 0]); a[0] += 1; a[1] += x in R[t]
        # 3) số cách số kỳ trước đúng ±Fibonacci (±1 ±2 ±3 ±5 ±8) so với cách ±4 ±6 ±7
        def near(t, D):
            S = set()
            for a in R[t - 1]:
                for dd in D:
                    for b in (a - dd, a + dd):
                        if 1 <= b <= NB and b not in R[t - 1]: S.add(b)
            return S
        f = [len(near(t, (1, 2, 3, 5, 8)) & R[t]) for t in T]; fs = sum(len(near(t, (1, 2, 3, 5, 8))) for t in T)
        o = [len(near(t, (4, 6, 7)) & R[t]) for t in T]; os_ = sum(len(near(t, (4, 6, 7))) for t in T)
        # 4) tổng kỳ này / tổng kỳ trước gần 1,618 hoặc 0,618 (lệch ≤5%)
        sm = [sum(RS[t]) for t in range(n)]
        g4 = sum(any(abs(sm[t] / sm[t - 1] - r) / r <= .05 for r in (1.618, .618)) for t in T)
        print(f' {W} kỳ | khoảng cách là số Fib: {fibg}/{allk} khoảng · kỳ toàn khoảng Fib: {k_all}'
              f' | vắng đúng số Fib → ra: {st["fib"][1]}/{st["fib"][0]} ({st["fib"][1]/st["fib"][0]*100:.1f}%) · vắng số khác: {st["khác"][1]}/{st["khác"][0]} ({st["khác"][1]/st["khác"][0]*100:.1f}%)'
              f' | cách số kỳ trước ±Fib: {sum(f)}/{fs} ({sum(f)/fs*100:.1f}%/số) · ±4,6,7: {sum(o)}/{os_} ({sum(o)/os_*100:.1f}%/số)'
              f' | tổng kỳ ≈ ×1,618/×0,618 tổng kỳ trước: {g4}')
        if W == 100: print('   khoảng cách hay gặp (100 kỳ):', ' '.join(f'{g}:{gc.get(g,0)}' for g in range(1, 14)))
