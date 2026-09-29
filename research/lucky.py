"""Số may mắn Loto (1..12): tín hiệu từ các kỳ trước — nóng/lạnh, số gan, bạc nhớ (Markov), theo giờ quay 13h/21h,
và từ 5 số chính kỳ trước. Mỗi tín hiệu chọn tập S trước mỗi kỳ; so tỷ lệ số may mắn thật rơi vào S với |S|/12.
Tách kỳ cũ (60%) / kỳ mới (40%): "hy vọng nhỏ" = cùng dấu ở cả hai nửa và |z| toàn bộ ≥ 1.5.
Chạy: python3 research/lucky.py            (in bảng)
      python3 research/lucky.py --json research/lucky.json [--dump dump.json]"""
import sys, os, math, json, random
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from study import load
L = 12

def rank(past, mode, k):
    """past = danh sách số may mắn các kỳ trước (cũ -> mới). 'hot' = k số về nhiều nhất, 'cold' = ít nhất, 'gan' = lâu chưa về nhất."""
    f = Counter(past); last = {x: -1 for x in range(1, L+1)}
    for j, x in enumerate(past): last[x] = j
    if mode == 'hot':  key = lambda x: (-f[x], -last[x], x)
    elif mode == 'cold': key = lambda x: (f[x], last[x], x)
    else: key = lambda x: (last[x], x)          # gan
    return sorted(range(1, L+1), key=key)[:k]

def markov(past, k, lag=1):
    """Sau số may mắn kỳ (i-lag) = v, trong lịch sử kỳ tiếp theo hay ra số nào nhất (k số)."""
    if len(past) < lag + 1: return []
    v = past[-lag]; f = Counter(past[j+lag] for j in range(len(past)-lag) if past[j] == v)
    return sorted(range(1, L+1), key=lambda x: (-f[x], x))[:k]

def m12(n): return (n-1) % L + 1

def rules():
    """tên -> hàm(ctx) -> tập số (1..12). ctx: lk = số may mắn các kỳ trước, hr = giờ kỳ này, hrs = giờ các kỳ trước, main = 5 số chính kỳ trước."""
    R = {}
    for w in (5, 10, 20, 30, 50, 100, 200, None):
        tag = 'từ đầu' if w is None else f'{w} kỳ gần'
        for mode, lab in (('hot', 'nóng'), ('cold', 'lạnh')):
            for k in (1, 3):
                R[f'{k} số {lab} {tag}'] = (lambda c, w=w, mode=mode, k=k: set(rank(c['lk'][-w:] if w else c['lk'], mode, k)))
        for k in (1, 3):  # chỉ tính các kỳ cùng giờ quay (13h hoặc 21h)
            R[f'{k} số nóng cùng giờ {tag}'] = (lambda c, w=w, k=k: set(rank(c['same'][-w:] if w else c['same'], 'hot', k)))
    for k in (1, 2, 3): R[f'{k} số gan nhất'] = lambda c, k=k: set(rank(c['lk'], 'gan', k))
    R['3 số gan nhất cùng giờ'] = lambda c: set(rank(c['same'], 'gan', 3))
    for k in (1, 3):
        R[f'Bạc nhớ: {k} số hay ra sau số kỳ trước'] = lambda c, k=k: set(markov(c['lk'], k))
        R[f'Bạc nhớ cùng giờ: {k} số hay ra sau số kỳ trước cùng giờ'] = lambda c, k=k: set(markov(c['same'], k))
        R[f'Bạc nhớ cách 2 kỳ: {k} số'] = lambda c, k=k: set(markov(c['lk'], k, 2))
    one = lambda f: (lambda c: {f(c)} if c['lk'] else set())
    R['Lặp lại số kỳ trước'] = one(lambda c: c['lk'][-1])
    R['Lặp lại số kỳ trước cùng giờ'] = lambda c: {c['same'][-1]} if c['same'] else set()
    R['Số kỳ trước ±1'] = lambda c: {m12(c['lk'][-1]-1), m12(c['lk'][-1]+1)} if c['lk'] else set()
    R['Số kỳ trước ±2'] = lambda c: {m12(c['lk'][-1]-2), m12(c['lk'][-1]+2)} if c['lk'] else set()
    R['Đối xứng 13 − số kỳ trước'] = one(lambda c: 13 - c['lk'][-1])
    R['Số kỳ trước + 6 (đối diện vòng 12)'] = one(lambda c: m12(c['lk'][-1] + 6))
    R['Tổng 2 số may mắn gần nhất (mod 12)'] = lambda c: {m12(c['lk'][-1] + c['lk'][-2])} if len(c['lk']) > 1 else set()
    R['5 số chính kỳ trước ≤ 12'] = lambda c: {x for x in c['main'] if x <= L}
    R['5 số chính kỳ trước (mod 12)'] = lambda c: {m12(x) for x in c['main']}
    R['Tổng 5 số chính kỳ trước (mod 12)'] = lambda c: {m12(sum(c['main']))} if c['main'] else set()
    R['Số nhỏ nhất kỳ trước (mod 12)'] = lambda c: {m12(min(c['main']))} if c['main'] else set()
    R['Số lớn nhất kỳ trước (mod 12)'] = lambda c: {m12(max(c['main']))} if c['main'] else set()
    R['Số chẵn (2,4..12) nếu giờ 21h, lẻ nếu 13h'] = lambda c: {x for x in range(1, L+1) if x % 2 == (0 if c['hr'] == 21 else 1)}
    R['Số lẻ nếu giờ 21h, chẵn nếu 13h'] = lambda c: {x for x in range(1, L+1) if x % 2 == (1 if c['hr'] == 21 else 0)}
    R['Số nhỏ 1–6 nếu 13h, lớn 7–12 nếu 21h'] = lambda c: set(range(1, 7)) if c['hr'] == 13 else set(range(7, 13))
    return R

def contexts(draws):
    out = []
    for i, d in enumerate(draws):
        hr = d['info']['h']; past = draws[:i]
        out.append(dict(lk=[p['lucky'] for p in past], hr=hr, same=[p['lucky'] for p in past if p['info']['h'] == hr],
                        main=sorted(past[-1]['nums']) if past else []))
    return out

def z_of(sets, W):
    H = E = V = 0.0
    for S, w in zip(sets, W):
        p = len(S)/L; H += w in S; E += p; V += p*(1-p)
    return ((H-E)/math.sqrt(V) if V else 0.0), H, E

def run(perms=1000):
    mx, c, lmx, draws = load('loto535')
    ctx = contexts(draws); W = [d['lucky'] for d in draws]
    start = 50; n = len(draws); cut = start + int((n-start)*0.6)
    R = rules(); sets = {k: [f(x) for x in ctx] for k, f in R.items()}
    rows = []
    for name, S in sets.items():
        zA, H, E = z_of(S[start:], W[start:]); zO = z_of(S[start:cut], W[start:cut])[0]; zN = z_of(S[cut:], W[cut:])[0]
        if not E: continue
        rows.append(dict(rule=name, size=round(sum(map(len, S[start:]))/(n-start), 1), hits=int(H), expected=round(E, 1), lift=round(H/E, 3),
                         z=round(zA, 2), p=round(math.erfc(abs(zA)/math.sqrt(2)), 4), z_old=round(zO, 2), z_new=round(zN, 2), consistent=zO*zN > 0))
    # ngưỡng may mắn thuần túy: xáo thứ tự số may mắn (giữ nguyên tập dự đoán) — max|z| trên mọi tín hiệu
    rng = random.Random(7); mz = []; Ws = W[start:]
    for _ in range(perms):
        P = Ws[:]; rng.shuffle(P)
        mz.append(max(abs(z_of(sets[r['rule']][start:], P)[0]) for r in rows))
    mz.sort(); thr = mz[int(0.95*perms)]
    return n, start, cut, rows, thr, sets

if __name__ == '__main__':
    n, start, cut, rows, thr, sets = run(int(os.environ.get('PERMS', 1000)))
    if '--json' in sys.argv:
        json.dump(dict(draws=n, start=start, threshold=round(thr, 2), rules=rows), open(sys.argv[sys.argv.index('--json')+1], 'w'), ensure_ascii=False)
        if '--dump' in sys.argv:   # để đối chiếu bản JS
            json.dump({k: [sorted(s) for s in v] for k, v in sets.items()}, open(sys.argv[sys.argv.index('--dump')+1], 'w'), ensure_ascii=False)
        print('đã ghi', len(rows), 'tín hiệu')
    else:
        print(f'Loto số may mắn: kiểm {n-start} kỳ (cũ {cut-start}, mới {n-cut}); ngưỡng may mắn thuần túy max|z| = {thr:.2f}')
        for r in sorted(rows, key=lambda r: -abs(r['z'])):
            ok = r['consistent'] and abs(r['z']) >= 1.5
            print(f"{r['rule']:52s} |S|={r['size']:4.1f} {r['hits']:4d}/{r['expected']:6.1f} ({(r['lift']-1)*100:+4.0f}%) z {r['z']:+.2f} | cũ {r['z_old']:+.2f} mới {r['z_new']:+.2f} {'★' if ok and r['z']>0 else ('▼' if ok else '')}")
