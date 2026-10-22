# Dấu vết "tam giác" 3 số trên 2 kỳ liền (anh 22/10/2026). Số xếp tăng dần theo cột.
# ▽: a=kỳ trước cột i, b=kỳ trước cột i+1, c=kỳ sau cột i hoặc i+1.  △: a=kỳ trước cột i, b,c=kỳ sau cột i, i+1.
# Quan hệ: 1 số = tổng / hiệu / tích / thương (chia hết) của 2 số kia.
import json, sys
d = json.load(open('build/all_data.json'))
def rel(x, y):
    o = {x + y, abs(x - y), x * y}
    if x and y % x == 0: o.add(y // x)
    if y and x % y == 0: o.add(x // y)
    return o
def tri3(a, b, c):  # có 1 số = phép tính của 2 số còn lại
    return c in rel(a, b) or b in rel(a, c) or a in rel(b, c)
OPS = {'tổng': lambda a, b: {a + b}, 'hiệu': lambda a, b: {b - a}, 'tích': lambda a, b: {a * b},
       'thương': lambda a, b: {b // a} if a and b % a == 0 and b // a > 1 else set()}
def run(key, nm, NB, gio=None):
    R = d[key]['res']; D = d[key]['dates']
    ix = [i for i in range(len(R)) if gio is None or D[i].endswith(gio)]
    S = [sorted(R[i]) for i in ix]; n = len(S); K = len(S[0])
    print(f'\n=== {nm}{" " + gio if gio else ""} ({n} kỳ)')
    # 1) đếm kỳ có tam giác
    for W in (20, 50, 100):
        a1 = a2 = 0
        for t in range(n - W, n):
            p, c = S[t - 1], S[t]
            v = any(c[j] in rel(p[i], p[i + 1]) for i in range(K - 1) for j in (i, i + 1))
            w = any(tri3(p[i], c[i], c[i + 1]) for i in range(K - 1))
            a1 += v; a2 += w
        print(f'  {W} kỳ: có ▽ {a1}/{W} · có △ {a2}/{W}')
    # 2) đoán trước bằng ▽: nhóm số c sinh từ cặp kề kỳ trước; % ra mỗi số trong nhóm vs số còn lại; và % ra đúng cột i/i+1
    for op in list(OPS) + ['gộp 4 phép']:
        row = []
        for W in (20, 50, 100):
            g = [0, 0, 0]; r = [0, 0]
            for t in range(n - W, n):
                p, c = S[t - 1], S[t]; P = set(p); G = {}
                for i in range(K - 1):
                    vs = set().union(*[f(p[i], p[i + 1]) for f in OPS.values()]) if op == 'gộp 4 phép' else OPS[op](p[i], p[i + 1])
                    for v in vs:
                        if 1 <= v <= NB and v not in P: G.setdefault(v, set()).update({i, i + 1})
                for x in range(1, NB + 1):
                    if x in G:
                        g[0] += 1; g[1] += x in c
                        g[2] += x in c and c.index(x) in G[x]
                    else:
                        r[0] += 1; r[1] += x in c
            row.append(f'{g[0]/W:.1f} số · {g[1]/max(1,g[0])*100:.1f}% (đúng cột {g[2]/max(1,g[0])*100:.1f}%) vs {r[1]/r[0]*100:.1f}%')
        print(f'  ▽ {op:11s}', ' | '.join(row))
for key, nm, NB in (('loto535', 'Loto', 35), ('mega645', 'Mega', 45), ('power655', 'Power', 55)):
    run(key, nm, NB)
for g in ('13h', '21h'):
    run('loto535', 'Loto', 35, g)
