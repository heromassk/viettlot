"""Nhân/chia (anh, 08/10/2026): (A) số kỳ trước ×m hoặc ÷m (m=2,3,4,5) qua k kỳ → pool; tỉ lệ ra mỗi số + pool 12 (bỏ phiếu).
(B) trong cùng dãy có cặp a & a×2 / a×3 bao nhiêu % kỳ. Khung 100/200/500 kỳ. Dùng: python3 build/nhanchia.py power|mega"""
import json, sys, os
g = sys.argv[1]; key, N = {'mega': ('mega645', 45), 'power': ('power655', 55)}[g]
D = json.load(open(os.path.join(os.path.dirname(__file__), 'all_data.json')))[key]
R = [set(sorted(r)[:6]) for r in D['res']]; T = len(R); TB = 600 / N
def votes(t, ms, k):
    v = {}
    for j in range(1, k + 1):
        for x in R[t - j]:
            for m in ms:
                for y in (x * m, x // m if x % m == 0 else 0):
                    if 1 <= y <= N: v[y] = v.get(y, 0) + 1
    return v
print(f'{g.upper()} — (A) nhân/chia số kỳ trước. Mức TB mỗi số {TB:.1f}%\n')
print('| ×÷ | k kỳ | Số trong pool/kỳ | % ra 100 / 200 / 500 | 5 đoạn 100 (500 kỳ) | Pool 12 nhiều phiếu: TB trúng 100/200/500 |')
for ms in ((2,), (3,), (2, 3), (2, 3, 4, 5)):
    for k in (1, 3, 5):
        out = []; segs = []
        for W in (100, 200, 500):
            h = n = 0; ph = 0
            for t in range(T - W, T):
                v = votes(t, ms, k); P = set(v) - R[t - 1]
                h += len(P & R[t]); n += len(P)
                p12 = sorted(P, key=lambda m: (-v[m], m))[:12]; ph += len(set(p12) & R[t])
            out.append((100 * h / n, n / W, ph / W))
        for i in range(5):
            h = n = 0
            for t in range(T - 500 + 100 * i, T - 400 + 100 * i):
                v = votes(t, ms, k); P = set(v) - R[t - 1]; h += len(P & R[t]); n += len(P)
            segs.append(100 * h / n)
        print(f"| ×÷{'/'.join(map(str, ms))} | {k} | {out[1][1]:.1f} | " + ' / '.join(f'{o[0]:.1f}' for o in out) + ' | ' + ' '.join(f'{x:.1f}' for x in segs) + ' | ' + ' / '.join(f'{o[2]:.2f}' for o in out) + ' |')
print(f'\n(B) cùng dãy có cặp a và a×m (% số kỳ):')
for ms in ((2,), (3,), (2, 3)):
    row = []
    for W in (100, 200, 500):
        c = sum(any(a * m in R[t] for a in R[t] for m in ms) for t in range(T - W, T)); row.append(f'{100*c/W:.0f}%')
    print(f"  ×{'/'.join(map(str, ms))}: 100 / 200 / 500 kỳ = " + ' / '.join(row))
