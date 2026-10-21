# Xét nốt các cách dùng 2 kỳ gần nhất (anh 21/10/2026). 1 số trong nhóm ra % kỳ so với số còn lại; 20 / 50 / 100 kỳ.
import json
d = json.load(open('build/all_data.json'))
def groups(R, t, NB):
    A, B = R[t - 1], R[t - 2]; U = A | B; G = {}
    G['1a. Tổng ghép: a (kỳ trước) + b (kỳ cách 1 kỳ)'] = {a + b for a in A for b in B if a + b <= NB} - A
    G['1b. Hiệu ghép: |a − b| giữa kỳ trước và kỳ cách 1 kỳ'] = {abs(a - b) for a in A for b in B if a != b} - A
    su = sorted(U); gen = set()
    for i, a in enumerate(su):
        for b in su[i + 1:]:
            for v in (a + b, a + 2 * b, 2 * a + 3 * b):
                if v <= NB: gen.add(v)
    G['2. Fib tổng quát từ 2 kỳ gộp (a+b, a+2b, 2a+3b)'] = gen - A
    # 4. bạn đi cùng: với mỗi số kỳ trước, số hay ra chung với nó nhất trong 100 kỳ trước đó
    co = {}
    for u in range(max(0, t - 101), t - 1):
        for a in R[u]:
            for b in R[u]:
                if a != b: co[(a, b)] = co.get((a, b), 0) + 1
    P = set()
    for a in A:
        c = [(co.get((a, b), 0), b) for b in range(1, NB + 1) if b != a]
        m = max(c)[0]; P |= {b for v, b in c if v == m}
    G['4. Bạn hay đi cùng (100 kỳ) của các số kỳ trước'] = P - A
    return G
def pos_test(RS, n, W):
    # 3. theo vị trí (số nhỏ nhất, thứ 2…): đoán vị trí i kỳ tới bằng 3 cách, trúng nếu lệch ≤2
    k = len(RS[0]); res = {'giữ như kỳ trước': 0, 'tiếp đà (kỳ trước + bước 2 kỳ)': 0, 'đảo đà (kỳ trước − bước 2 kỳ)': 0}; tot = 0
    for t in range(n - W, n):
        for i in range(k):
            v1, v2, v = RS[t - 1][i], RS[t - 2][i], RS[t][i]; st = v1 - v2; tot += 1
            res['giữ như kỳ trước'] += abs(v - v1) <= 2
            res['tiếp đà (kỳ trước + bước 2 kỳ)'] += abs(v - (v1 + st)) <= 2
            res['đảo đà (kỳ trước − bước 2 kỳ)'] += abs(v - (v1 - st)) <= 2
    return res, tot
for key, nm, NB in (('loto535', 'Loto', 35), ('mega645', 'Mega', 45), ('power655', 'Power', 55)):
    R = [set(x) for x in d[key]['res']]; RS = [sorted(x) for x in d[key]['res']]; n = len(R); print(f'\n=== {nm}')
    for lab in groups(R, n - 1, NB):
        row = []
        for W in (20, 50, 100):
            a = [0, 0]; b = [0, 0]
            for t in range(n - W, n):
                S = groups(R, t, NB)[lab]
                for x in range(1, NB + 1):
                    z = a if x in S else b; z[0] += 1; z[1] += x in R[t]
            row.append(f'{a[0]/W:.1f} số · {a[1]/max(1,a[0])*100:.1f}% vs {b[1]/max(1,b[0])*100:.1f}%')
        print(f'  {lab}:\n     ' + ' | '.join(f'{W}: {r}' for W, r in zip((20, 50, 100), row)))
    out = []
    for W in (20, 50, 100):
        r, tot = pos_test(RS, n, W); out.append(f'{W}: ' + ' · '.join(f'{k} {v}/{tot}' for k, v in r.items()))
    print('  3. Theo vị trí (đoán lệch ≤2):\n     ' + '\n     '.join(out))
