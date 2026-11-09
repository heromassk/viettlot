# Loto: 2 số đầu kỳ trước và 2 số đầu kỳ sau có quan hệ tổng/hiệu? (anh 09/11/2026). So với cặp vị trí khác của chính dữ liệu thật.
import json
d = json.load(open('build/all_data.json'))['loto535']; RA = d['res']; DA = d['dates']; NB = 35
def rel(A, B):
    a1, a2 = A; b1, b2 = B; s, h = a1 + a2, abs(a2 - a1); S, H = b1 + b2, abs(b2 - b1)
    r1 = bool({b1, b2} & {s, h}); r2 = bool({a1, a2} & {S, H}); r3 = s == S or h == H
    return r1, r2, r3, r1 or r2 or r3
POS = {'2 số đầu (nhỏ nhất)': lambda r: sorted(r)[:2], '2 số giữa (thứ 2–3)': lambda r: sorted(r)[1:3],
       '2 số cuối (lớn nhất)': lambda r: sorted(r)[-2:], '2 số đầu theo đuôi': lambda r: sorted(r, key=lambda x: (x % 10, x))[:2]}
def run(idx, nm):
    print(f'\n=== {nm}')
    for pn, f in POS.items():
        out = []
        for W in (20, 50, 100):
            c = [0, 0, 0, 0]
            for j in range(len(idx) - W, len(idx)):
                rr = rel(f(RA[idx[j - 1]]), f(RA[idx[j]]))
                for k in range(4): c[k] += rr[k]
            out.append(f'{c[3]:2d}/{W} (sau=tổng/hiệu trước {c[0]}, trước=tổng/hiệu sau {c[1]}, cùng tổng/hiệu {c[2]})')
        print(f'  {pn:22s}', ' | '.join(out))
    # đoán trước: số = tổng / hiệu 2 số đầu kỳ trước → ra ở kỳ sau? (% mỗi số so với số còn lại)
    row = []
    for W in (20, 50, 100):
        g = [0, 0, 0]; o = [0, 0]
        for j in range(len(idx) - W, len(idx)):
            p, c = RA[idx[j - 1]], set(RA[idx[j]]); a1, a2 = sorted(p)[:2]
            G = {x for x in (a1 + a2, a2 - a1) if 1 <= x <= NB} - set(p); first2 = set(sorted(c)[:2])
            for x in range(1, NB + 1):
                if x in G: g[0] += 1; g[1] += x in c; g[2] += x in first2
                else: o[0] += 1; o[1] += x in c
        row.append(f'{g[0]/W:.1f} số · ra {g[1]/max(1,g[0])*100:.1f}% (ở 2 số đầu {g[2]/max(1,g[0])*100:.1f}%) vs số khác {o[1]/o[0]*100:.1f}%')
    print('  Đoán: tổng/hiệu 2 số đầu kỳ trước →', ' | '.join(row))
n = len(RA)
run(list(range(n)), 'Loto liền 2 buổi')
run([i for i in range(n) if DA[i].endswith('13h')], 'Loto 13h (so kỳ 13h trước)')
run([i for i in range(n) if DA[i].endswith('21h')], 'Loto 21h (so kỳ 21h trước)')
