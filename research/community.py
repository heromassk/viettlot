"""Kiểm tra các phương pháp phổ biến trong cộng đồng soi cầu (dựa vào kết quả các kỳ trước).
Mỗi phương pháp, trước kỳ i chỉ dùng kỳ < i, cho ra tập số S_i; đếm số trúng so với kỳ vọng |S_i|*c/max."""
import sys, os, math
from collections import Counter, defaultdict
from itertools import permutations
sys.path.insert(0, os.path.dirname(__file__))
from study import load, root
from combo import chi2_sf
BD = {0:5,5:0,1:6,6:1,2:7,7:2,3:8,8:3,4:9,9:4}; BA = {0:7,7:0,1:4,4:1,2:9,9:2,3:6,6:3,5:8,8:5}
def zp(z): return math.erfc(abs(z)/math.sqrt(2))

def digits_of(s): return ''.join(f'{x:02d}' for x in sorted(s))
def pascal(ds):
    d = [int(ch) for ch in ds]
    while len(d) > 2: d = [(a+b) % 10 for a, b in zip(d, d[1:])]
    return d[0]*10 + d[1]

def methods(mx, c):
    R = range(1, mx+1)
    def clip(xs): return {x for x in xs if 1 <= x <= mx}
    M = {}
    M['Lô rơi: số kỳ trước'] = lambda P, st: set(P[-1])
    M['Lô lộn: đảo số kỳ trước (12→21)'] = lambda P, st: clip(int(f'{x:02d}'[::-1]) for x in P[-1]) - set(P[-1])
    M['Bóng dương số kỳ trước'] = lambda P, st: clip(int(''.join(str(BD[int(ch)]) for ch in f'{x:02d}')) for x in P[-1])
    M['Bóng âm số kỳ trước'] = lambda P, st: clip(int(''.join(str(BA[int(ch)]) for ch in f'{x:02d}')) for x in P[-1])
    M['Pascal kết quả kỳ trước'] = lambda P, st: clip([pascal(digits_of(P[-1]))])
    M['Pascal + lộn'] = lambda P, st: clip([pascal(digits_of(P[-1])), int(f'{pascal(digits_of(P[-1])):02d}'[::-1])])
    def cham(P):
        t = sum(int(ch) for ch in digits_of(P[-1])) % 10
        return t
    M['Chạm đuôi = tổng chữ số kỳ trước'] = lambda P, st: {x for x in R if x % 10 == cham(P)}
    M['Chạm đầu = tổng chữ số kỳ trước'] = lambda P, st: {x for x in R if x // 10 == cham(P)}
    M['Bạc nhớ chu kỳ: về cách đây 3–7 kỳ'] = lambda P, st: set().union(*P[-7:-2]) - set().union(*P[-2:]) if len(P) >= 7 else set()
    # Bạc nhớ / Markov: số hay đi sau các số kỳ trước (tính trên toàn bộ các kỳ trước)
    def follow(P, st, k=c):
        F = st['follow']; cnt = st['cnt']
        score = Counter()
        for x in P[-1]:
            for y in R:
                if cnt[x]: score[y] += F[(x, y)]/cnt[x]
        return set(sorted(R, key=lambda y: (-score[y], y))[:k])
    M['Bạc nhớ: số hay đi sau số kỳ trước (Markov)'] = follow
    # Cầu vị trí: ghép chữ số ở vị trí i, j; dùng những cầu đã trúng liên tiếp L kỳ
    def cau(P, st, L):
        alive = set()
        for (i, j) in st['pos']:
            ok = True
            for back in range(1, L+1):
                if len(P) < back+1: ok = False; break
                s = digits_of(P[-1-back]); v = int(s[i]+s[j])
                if v not in P[-back]: ok = False; break
            if ok: alive.add((i, j))
        s = digits_of(P[-1]); return clip(int(s[i]+s[j]) for i, j in alive)
    M['Cầu vị trí chạy 2 kỳ liên tiếp'] = lambda P, st: cau(P, st, 2)
    M['Cầu vị trí chạy 3 kỳ liên tiếp'] = lambda P, st: cau(P, st, 3)
    return M

def run(game, start=30):
    mx, c, _, dr = load(game); D = [set(d['nums']) for d in dr]; n = len(D); cut = start + int((n-start)*0.6)
    info = [d['info'] for d in dr]
    M = methods(mx, c)
    st = {'follow': Counter(), 'cnt': Counter(), 'pos': list(permutations(range(2*c), 2))}
    res = {k: [[0, 0.0, 0.0], [0, 0.0, 0.0]] for k in M}   # [hits, E, Var] cho cũ / mới
    extra = {'Thần số học: số chủ đạo ngày (2–11)': [[0, 0.0, 0.0], [0, 0.0, 0.0]]}
    p = c/mx
    def add(bucket, S, W):
        K = len(S); q = K/mx
        bucket[0] += len(S & W); bucket[1] += c*q; bucket[2] += c*q*(1-q)*(mx-c)/(mx-1) if mx > 1 else 0
    for i in range(1, n):
        P = D[:i]
        if i >= start:
            half = 0 if i < cut else 1
            for k, f in M.items(): add(res[k][half], f(P, st), D[i])
            I = info[i]; s = I['dsum']
            while s > 11: s = sum(map(int, str(s)))
            add(extra['Thần số học: số chủ đạo ngày (2–11)'][half], {s} if 1 <= s <= mx else set(), D[i])
        for x in D[i-1]:
            st['cnt'][x] += 1
            for y in D[i]: st['follow'][(x, y)] += 1
    res.update(extra)
    # hazard: xác suất về theo số kỳ đã vắng
    hz = defaultdict(lambda: [0, 0])
    for x in range(1, mx+1):
        last = None
        for i, s in enumerate(D):
            if last is not None:
                g = i - last - 1
                b = '0' if g == 0 else '1' if g == 1 else '2' if g == 2 else '3–5' if g <= 5 else '6–10' if g <= 10 else '11–20' if g <= 20 else '>20'
                hz[b][1] += 1; hz[b][0] += x in s
            if x in s: last = i
    return mx, c, n, cut-start, n-cut, res, hz

def summary(res):
    out = []
    for k, (a, b) in res.items():
        H = a[0]+b[0]; E = a[1]+b[1]; V = a[2]+b[2]
        if E == 0: continue
        z = (H-E)/math.sqrt(V); za = (a[0]-a[1])/math.sqrt(a[2]) if a[2] else 0; zb = (b[0]-b[1])/math.sqrt(b[2]) if b[2] else 0
        out.append(dict(rule=k, hits=int(H), expected=round(E, 1), lift=round(H/E, 3), z=round(z, 2), p=round(zp(z), 4),
                        z_old=round(za, 2), z_new=round(zb, 2), consistent=za*zb > 0, size=None))
    return sorted(out, key=lambda r: -r['z'])

def dump(game, idxs):
    """Tập số của từng phương pháp khi dự đoán kỳ i (chỉ dùng kỳ < i) — để đối chiếu bản JS."""
    mx, c, _, dr = load(game); D = [set(d['nums']) for d in dr]; M = methods(mx, c)
    st = {'follow': Counter(), 'cnt': Counter(), 'pos': list(permutations(range(2*c), 2))}
    out = {}
    for i in range(1, len(D)+1):
        if i in idxs:
            I = dr[i]['info'] if i < len(D) else None
            out[i] = {k: sorted(f(D[:i], st)) for k, f in M.items()}
        if i < len(D):
            for x in D[i-1]:
                st['cnt'][x] += 1
                for y in D[i]: st['follow'][(x, y)] += 1
    return out

if __name__ == '__main__' and '--json' in sys.argv:
    import json
    res = {g: summary(run(g)[5]) for g in ['power655', 'mega645', 'loto535']}
    json.dump(res, open(sys.argv[sys.argv.index('--json')+1], 'w'), ensure_ascii=False)
    if '--dump' in sys.argv:
        import random
        dd = {}
        for g in ['power655', 'mega645', 'loto535']:
            n = len(load(g)[3]); rng = random.Random(3)
            dd[g] = dump(g, set([n] + rng.sample(range(10, n), 25)))
        json.dump(dd, open(sys.argv[sys.argv.index('--dump')+1], 'w'))
    print('đã ghi')
elif __name__ == '__main__':
    for game in ['power655', 'mega645', 'loto535']:
        mx, c, n, nold, nnew, res, hz = run(game)
        print(f'\n######## {game}: kiểm {nold+nnew} kỳ (cũ {nold}, mới {nnew})')
        rows = []
        for k, (a, b) in res.items():
            H = a[0]+b[0]; E = a[1]+b[1]; V = a[2]+b[2]
            if E == 0: continue
            z = (H-E)/math.sqrt(V); za = (a[0]-a[1])/math.sqrt(a[2]) if a[2] else 0; zb = (b[0]-b[1])/math.sqrt(b[2]) if b[2] else 0
            rows.append((z, k, H, E, za, zb))
        for z, k, H, E, za, zb in sorted(rows, key=lambda r: -abs(r[0])):
            ok = za*zb > 0 and abs(z) >= 1.5
            print(f'  {k:44s} trúng {H:5d}/{E:7.1f} ({(H/E-1)*100:+4.0f}%) z {z:+.2f} p={zp(z):.3f} | cũ {za:+.2f} mới {zb:+.2f} {"★ HY VỌNG NHỎ" if ok and z>0 else ("▼ nên tránh" if ok else "")}')
        pc = c/mx
        print('  CHU KỲ (hazard) — xác suất về ở kỳ tới theo số kỳ đã vắng (lý thuyết %.1f%%):' % (pc*100))
        order = ['0', '1', '2', '3–5', '6–10', '11–20', '>20']
        x2 = 0
        for b in order:
            h, t = hz[b]
            if t: x2 += (h - t*pc)**2/(t*pc*(1-pc))
            print(f'     vắng {b:>5s} kỳ: {h}/{t} = {h/t*100 if t else 0:.1f}%')
        print(f'     kiểm định chung: p = {chi2_sf(x2, len(order)):.3f}')
