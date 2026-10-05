#!/usr/bin/env python3
"""Max 3D — dò dấu vết BI VẬT LÝ (anh, 05/10/2026: lồng quay khí nén, bi 0–9, mỗi bộ số quay lần lượt hàng trăm → chục → đơn vị).
Mỗi kỳ 20 bộ = 60 lần quay chữ số. Dữ liệu: build/max3d_data.json {"dates": [...], "res": [["123", ... 20 bộ theo thứ tự giải], ...]}
  python3 build/max3d_dauvet.py [--file build/max3d_data.json] [--thu]   (--thu: chạy trên dữ liệu giả lập để kiểm script)
1. Tần suất chữ số 0–9 theo từng hàng trên 4 khung 10/20/50/100 kỳ (+ đoạn 100 kỳ trước).
2. Một lồng hay ba lồng: độ lệch chữ số ở hàng trăm/chục/đơn vị có cùng chiều không.
3. Bi vừa ra có ra lại ngay không (lặp chữ số liên tiếp so với 10%).
4. Dấu vết có giữ qua thời gian không: khối W kỳ liền nhau giống nhau hơn quay ngẫu nhiên không.
5. Dự đoán kỳ kế: 3 chữ số nặng nhất (khung W) ra bao nhiêu % ở kỳ sau (chia đều 30%) — theo từng khung."""
import json, os, sys, random, math
HERE = os.path.dirname(os.path.abspath(__file__))
if '--thu' in sys.argv:
    random.seed(1); w = [1.0] * 10
    res = []
    for t in range(600):
        if t % 20 == 0: w = [random.uniform(0.9, 1.1) for _ in range(10)]   # giả lập thay bi mỗi 20 kỳ
        res.append([''.join(str(random.choices(range(10), w)[0]) for _ in range(3)) for _ in range(20)])
    D = {'dates': [f'k{t}' for t in range(600)], 'res': res}
else:
    f = sys.argv[sys.argv.index('--file') + 1] if '--file' in sys.argv else os.path.join(HERE, 'max3d_data.json')
    D = json.load(open(f))
R = [[[int(c) for c in s] for s in r] for r in D['res']]; T = len(R)
POS = ['trăm', 'chục', 'đơn vị']
def cnt(a, b, pos=None):
    c = [0] * 10
    for t in range(max(0, a), b):
        for s in R[t]:
            for i, d in enumerate(s):
                if pos is None or i == pos: c[d] += 1
    return c
def corr(x, y):
    mx, my = sum(x) / len(x), sum(y) / len(y)
    sx = math.sqrt(sum((a - mx) ** 2 for a in x)); sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return 0 if not sx or not sy else sum((a - mx) * (b - my) for a, b in zip(x, y)) / sx / sy
print(f'## Max 3D — {T} kỳ ({D["dates"][0]} → {D["dates"][-1]})\n')
# 1
print('### 1. Tỉ lệ ra từng chữ số (chia đều 10%) — cả 3 hàng\n')
WS = [(f'{W} kỳ gần', T - W, T) for W in (10, 20, 50, 100) if W <= T] + ([('100 kỳ trước đó', T - 200, T - 100)] if T >= 200 else [])
print('| Chữ số | ' + ' | '.join(n for n, _, _ in WS) + ' |\n|---|' + '---|' * len(WS))
CW = [cnt(a, b) for _, a, b in WS]
for d in range(10):
    print(f'| {d} | ' + ' | '.join(f'{c[d] / sum(c) * 100:.1f}%' for c in CW) + ' |')
# 2
print('\n### 2. Một lồng hay ba lồng? Độ lệch chữ số giữa các hàng (100 kỳ gần)\n')
W = min(100, T); P = [cnt(T - W, T, i) for i in range(3)]
for i in range(3): print(f'- Hàng {POS[i]}: ' + ' '.join(f'{d}:{P[i][d] / sum(P[i]) * 100:.1f}' for d in range(10)))
def poscorr(RR):
    v = []
    for a in range(0, len(RR) - 19, 20):
        q = [[0] * 10 for _ in range(3)]
        for t in range(a, a + 20):
            for x in RR[t]:
                for k, d in enumerate(x): q[k][d] += 1
        v.append((corr(q[0], q[1]) + corr(q[1], q[2]) + corr(q[0], q[2])) / 3)
    return sum(v) / len(v)
real = poscorr(R); sims = sorted(poscorr([[[random.randrange(10) for _ in range(3)] for _ in range(20)] for _ in range(T)]) for _ in range(30))
print(f'- Tương quan độ lệch giữa 3 hàng, TB các khối 20 kỳ trên toàn bộ {T} kỳ: **{real:+.3f}** (quay ngẫu nhiên: {sims[1]:+.3f} … {sims[-2]:+.3f})')
print('  → ' + ('**cùng chiều: giống 1 bộ bi dùng chung cho cả 3 hàng** — chữ số nặng thì nặng ở mọi hàng' if real > sims[-2] else 'không cùng chiều rõ — có thể mỗi hàng 1 lồng/bộ bi riêng, hoặc độ lệch quá nhỏ'))
# 3
rep = n = 0
for t in range(T - W, T):
    seq = [d for s in R[t] for d in s]
    for a, b in zip(seq, seq[1:]): rep += a == b; n += 1
print(f'\n### 3. Bi vừa ra có ra lại ngay không\n\n- Chữ số lặp lại ở lần quay kế tiếp: **{rep / n * 100:.1f}%** (chia đều 10%)')
# 4
print('\n### 4. Dấu vết có giữ không: tương quan tần suất 2 khối W kỳ liền nhau (TB) — so với quay ngẫu nhiên\n')
print('| Khung W | Thực tế | Quay ngẫu nhiên (10 lần thử: thấp nhất … cao nhất) | Nhận xét |\n|---|---|---|---|')
for W in (10, 20, 50, 100):
    if 2 * W + 50 > T: continue
    ts = range(max(2 * W, T - 300), T, 5)
    real = sum(corr(cnt(t - W, t), cnt(t - 2 * W, t - W)) for t in ts) / len(ts)
    sims = []
    for _ in range(10):
        RR = [[[random.randrange(10) for _ in range(3)] for _ in range(20)] for _ in range(T)]
        def cc(a, b):
            c = [0] * 10
            for t in range(a, b):
                for x in RR[t]:
                    for d in x: c[d] += 1
            return c
        sims.append(sum(corr(cc(t - W, t), cc(t - 2 * W, t - W)) for t in ts) / len(ts))
    sims.sort(); lo, hi = sims[0], sims[-1]
    print(f'| {W} | {real:+.3f} | {lo:+.3f} … {hi:+.3f} | {"**có dấu vết giữ lại**" if real > hi else "ngược chiều" if real < lo else "trong vùng ngẫu nhiên"} |')
# 5
print('\n### 5. 3 chữ số nặng nhất của khung W → tỉ lệ ra ở kỳ kế (chia đều 30%), chấm 300 kỳ gần chia 3 đoạn\n')
print('| Khung | Đoạn gần | Đoạn giữa | Đoạn xa |\n|---|---|---|---|')
for W in (10, 20, 50, 100):
    out = []
    for a, b in ((T - 100, T), (T - 200, T - 100), (T - 300, T - 200)):
        if a - W < 0: out.append('—'); continue
        h = m = 0
        for t in range(a, b):
            c = cnt(t - W, t); top = sorted(range(10), key=lambda d: -c[d])[:3]
            nx = cnt(t, t + 1); h += sum(nx[d] for d in top); m += 60
        out.append(f'{h / m * 100:.1f}%')
    print(f'| {W} kỳ | ' + ' | '.join(out) + ' |')
# 6. theo TỪNG HÀNG (nếu mỗi hàng 1 lồng riêng): 3 chữ số nặng nhất của hàng đó → % ra ở hàng đó kỳ kế
print('\n### 6. Theo từng hàng: 3 chữ số nặng nhất của hàng (khung W) → % ra ở hàng đó kỳ kế (chia đều 30%)\n')
print('| Khung | Đoạn gần | Đoạn giữa | Đoạn xa |\n|---|---|---|---|')
for W in (10, 20, 50, 100):
    out = []
    for a, b in ((T - 100, T), (T - 200, T - 100), (T - 300, T - 200)):
        if a - W < 0: out.append('—'); continue
        h = m = 0
        for t in range(a, b):
            for i in range(3):
                c = cnt(t - W, t, i); top = sorted(range(10), key=lambda d: -c[d])[:3]
                h += sum(s[i] in top for s in R[t]); m += 20
        out.append(f'{h / m * 100:.1f}%')
    print(f'| {W} kỳ | ' + ' | '.join(out) + ' |')
# 7. lạnh nhất theo hàng
print('\n### 7. Theo từng hàng: 3 chữ số NHẸ nhất của hàng (khung W) → % ra kỳ kế (chia đều 30%)\n')
print('| Khung | Đoạn gần | Đoạn giữa | Đoạn xa |\n|---|---|---|---|')
for W in (10, 20, 50, 100):
    out = []
    for a, b in ((T - 100, T), (T - 200, T - 100), (T - 300, T - 200)):
        h = m = 0
        for t in range(a, b):
            for i in range(3):
                c = cnt(t - W, t, i); bot = sorted(range(10), key=lambda d: c[d])[:3]
                h += sum(s[i] in bot for s in R[t]); m += 20
        out.append(f'{h / m * 100:.1f}%')
    print(f'| {W} kỳ | ' + ' | '.join(out) + ' |')
