# Kiểm dãy Fibonacci trong kết quả 3 game (anh 21/10/2026)
import json
d = json.load(open('build/all_data.json'))
FIB = [1, 2, 3, 5, 8, 13, 21, 34, 55]
for key, nm, NB, WS in (('loto535', 'Loto', 35, (20, 50, 100, 200)), ('mega645', 'Mega', 45, (20, 50, 100)), ('power655', 'Power', 55, (20, 50, 100))):
    R = [set(x) for x in d[key]['res']]; n = len(R); F = {x for x in FIB if x <= NB}; O = set(range(1, NB + 1)) - F
    print(f'\n{nm}: số Fibonacci {sorted(F)}')
    for W in WS:
        rr = R[-W:]
        hf = sum(len(r & F) for r in rr); ho = sum(len(r & O) for r in rr)
        dist = [sum(len(r & F) == k for r in rr) for k in range(4)]
        tri = sum(any(a + b == c for a in r for b in r for c in r if a < b) for r in rr)
        tf = sum(any(a + b == c and {a, b, c} <= F for a in r for b in r for c in r if a < b) for r in rr)
        cross = sum(any((a + b) in R[t] for a in R[t - 1] for b in R[t - 2]) for t in range(n - W, n))
        print(f'  {W} kỳ: 1 số Fib ra {hf/len(F)/W*100:.1f}% kỳ, 1 số khác ra {ho/len(O)/W*100:.1f}% kỳ'
              f' · số Fib mỗi kỳ 0/1/2/3+: {dist[0]}/{dist[1]}/{dist[2]}/{W-sum(dist[:3])}'
              f' · kỳ có bộ a+b=c: {tri} (cả 3 là Fib: {tf}) · kỳ có số = số kỳ trước + số kỳ trước nữa: {cross}')
LK = d['loto535']['lk']; D = d['loto535']['dates']
for g, nm in ((None, 'liền 2 buổi'), ('13h', '13h'), ('21h', '21h')):
    s = [LK[i] for i in range(len(LK)) if g is None or D[i].endswith(g)]
    print(f'Số May Mắn ({nm}):', ' · '.join(f'{W} kỳ: Fib {sum(x in (1,2,3,5,8) for x in s[-W:])/5/W*100:.1f}% / khác {sum(x not in (1,2,3,5,8) for x in s[-W:])/7/W*100:.1f}% mỗi số' for W in (20, 50, 100, 200)))
