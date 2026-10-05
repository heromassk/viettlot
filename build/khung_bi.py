#!/usr/bin/env python3
"""Dấu vết bi theo NHIỀU KHUNG GẦN: 10 / 20 / 50 / 100 kỳ (tối đa 100 — họ thay bi 1–2 tháng/lần).
  python3 build/khung_bi.py power|mega|loto
1. Độ "đồng nhất" giữa các khung: tần suất số ở khối W kỳ có giống khối W kỳ liền trước không (tương quan),
   so với mức tương quan khi quay hoàn toàn ngẫu nhiên (để biết dấu vết có thật hay chỉ là nhiễu).
2. Mỗi khung riêng: nhóm "nóng" (trên kỳ vọng) / "lạnh" ra kỳ kế bao nhiêu % so với trung bình — 3 đoạn 100 kỳ.
3. So các khung với nhau: nóng/lạnh ĐỒNG NHẤT cả 4 khung, "mới nóng" (10,20 nóng — 50,100 lạnh), "mới nguội".
4. Dò "vừa thay bi": tần suất 20 kỳ gần lệch hẳn 50 kỳ trước đó → khi đó khung dài còn đáng tin không.
5. Hiện trạng kỳ tới."""
import json, os, sys, random, math
GM = {'power': ('power655', 55, 6), 'mega': ('mega645', 45, 6), 'loto': ('loto535', 35, 5)}
key, NB, KB = GM[sys.argv[1]]
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_data.json')))[key]
R = [set(r) for r in D['res']]; T = len(R); P = KB / NB
WS = (10, 20, 50, 100)
NUM = range(1, NB + 1)
def cnt(R, a, b): return {n: sum(n in R[u] for u in range(max(0, a), b)) for n in NUM}
def corr(x, y):
    xs = [x[n] for n in NUM]; ys = [y[n] for n in NUM]; mx = sum(xs) / NB; my = sum(ys) / NB
    sx = math.sqrt(sum((a - mx) ** 2 for a in xs)); sy = math.sqrt(sum((b - my) ** 2 for b in ys))
    return 0 if sx == 0 or sy == 0 else sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / sx / sy

# 1. đồng nhất giữa 2 khối liền nhau
random.seed(5); RNDS = [[set(random.sample(list(NUM), KB)) for _ in range(T)] for _ in range(30)]
print(f'## {key} — 1. Hai khối W kỳ liền nhau có giống nhau không (tương quan tần suất từng số, TB trên 300 kỳ gần)\n')
print('| Khung W | Thực tế | Quay ngẫu nhiên: TB (khoảng 90% của 30 lần thử) | Nhận xét |\n|---|---|---|---|')
for W in WS:
    re = [corr(cnt(R, t - W, t), cnt(R, t - 2 * W, t - W)) for t in range(T - 300, T, 5)]
    a = sum(re) / len(re); bs = []
    for RND in RNDS:
        rn = [corr(cnt(RND, t - W, t), cnt(RND, t - 2 * W, t - W)) for t in range(T - 300, T, 5)]; bs.append(sum(rn) / len(rn))
    bs.sort(); lo, hi = bs[1], bs[-2]
    print(f'| {W} | {a:+.3f} | {sum(bs) / len(bs):+.3f} ({lo:+.3f} … {hi:+.3f}) | {"**có dấu vết giữ lại**" if a > hi else "**ngược chiều (đảo)**" if a < lo else "nằm trong vùng ngẫu nhiên"} |')

# 2 + 3. nhóm theo khung, chấm từng kỳ
GR = ['nóng 10', 'lạnh 10', 'nóng 20', 'lạnh 20', 'nóng 50', 'lạnh 50', 'nóng 100', 'lạnh 100',
      'NÓNG đồng nhất 4 khung', 'LẠNH đồng nhất 4 khung', 'mới nóng (10,20↑ 50,100↓)', 'mới nguội (10,20↓ 50,100↑)']
def groups(t):
    r = {W: {n: c / (W * P) for n, c in cnt(R, t - W, t).items()} for W in WS}
    g = {}
    for W in WS:
        g[f'nóng {W}'] = {n for n in NUM if r[W][n] > 1}; g[f'lạnh {W}'] = {n for n in NUM if r[W][n] < 1}
    g['NÓNG đồng nhất 4 khung'] = {n for n in NUM if all(r[W][n] > 1 for W in WS)}
    g['LẠNH đồng nhất 4 khung'] = {n for n in NUM if all(r[W][n] < 1 for W in WS)}
    g['mới nóng (10,20↑ 50,100↓)'] = {n for n in NUM if r[10][n] > 1 and r[20][n] > 1 and r[50][n] < 1 and r[100][n] < 1}
    g['mới nguội (10,20↓ 50,100↑)'] = {n for n in NUM if r[10][n] < 1 and r[20][n] < 1 and r[50][n] > 1 and r[100][n] > 1}
    return g, r
SEG = [(T - 100, T), (T - 200, T - 100), (T - 300, T - 200)]
st = {s: {k: [0, 0] for k in GR} for s in range(3)}
sim = {}
for s, (a, b) in enumerate(SEG):
    for t in range(a, b):
        g, _ = groups(t)
        for k in GR: st[s][k][0] += len(g[k] & R[t]); st[s][k][1] += len(g[k])
        sim[t] = corr(cnt(R, t - 20, t), cnt(R, t - 70, t - 20))
print(f'\n## 2–3. Tỉ lệ ra kỳ kế của mỗi số trong nhóm (trung bình {P * 100:.1f}%) — 3 đoạn 100 kỳ: gần → xa\n')
print('| Nhóm | Cỡ TB | Đoạn 1 | Đoạn 2 | Đoạn 3 | Kết luận |\n|---|---|---|---|---|---|')
for k in GR:
    v = [st[s][k][0] / max(st[s][k][1], 1) * 100 for s in range(3)]; d = [x - P * 100 for x in v]
    c = '▲ ra NHIỀU hơn 3/3' if all(x > 0.3 for x in d) else '▼ ra ÍT hơn 3/3' if all(x < -0.3 for x in d) else ('▲ 2/3' if sum(x > 0.3 for x in d) >= 2 else '▼ 2/3' if sum(x < -0.3 for x in d) >= 2 else '—')
    print(f'| {k} | {sum(st[s][k][1] for s in range(3)) / 300:.1f} | ' + ' | '.join(f'{x:.1f}%' for x in v) + f' | {c} |')

# 4. vừa thay bi?
ts = sorted(sim, key=lambda t: sim[t]); n3 = len(ts) // 3
low, high = set(ts[:n3]), set(ts[-n3:])
print(f'\n## 4. Dò "vừa thay bi": độ giống 20 kỳ gần ↔ 50 kỳ trước đó (300 kỳ). Thấp nhất 1/3 = "lệch hẳn, nghi vừa thay bi"\n')
print('| Nhóm | Khi LỆCH HẲN (nghi thay bi) | Khi bình thường | Khi GIỐNG NHAU |\n|---|---|---|---|')
for k in ('nóng 10', 'nóng 20', 'nóng 50', 'nóng 100', 'lạnh 20', 'lạnh 100', 'NÓNG đồng nhất 4 khung', 'LẠNH đồng nhất 4 khung'):
    out = []
    for S in (low, set(ts) - low - high, high):
        h = m = 0
        for t in S:
            g, _ = groups(t); h += len(g[k] & R[t]); m += len(g[k])
        out.append(f'{h / max(m, 1) * 100:.1f}%')
    print(f'| {k} | ' + ' | '.join(out) + ' |')

# 5. hiện trạng
g, r = groups(T); s_now = corr(cnt(R, T - 20, T), cnt(R, T - 70, T - 20))
pct = sum(sim[t] < s_now for t in sim) / len(sim) * 100
print(f'\n## 5. Hiện trạng kỳ tới (sau {D["dates"][-1]})\n')
print(f'- Độ giống 20 kỳ gần ↔ 50 kỳ trước: **{s_now:+.2f}** (cao hơn {pct:.0f}% các kỳ trong 300 kỳ) → ' +
      ('**lệch hẳn — nghi vừa thay bi**, tin khung 10/20 hơn' if pct < 33 else 'giống nhau — khung dài còn dùng được' if pct > 67 else 'bình thường'))
for k in ('NÓNG đồng nhất 4 khung', 'LẠNH đồng nhất 4 khung', 'mới nóng (10,20↑ 50,100↓)', 'mới nguội (10,20↓ 50,100↑)'):
    print(f'- {k}: ' + (' '.join(f'{n:02d}' for n in sorted(g[k])) or '—'))
print('\n| Số | ' + ' | '.join(f'{W} kỳ' for W in WS) + ' |\n|---|' + '---|' * len(WS))
for n in NUM:
    print(f'| {n:02d} | ' + ' | '.join(f'{round(r[W][n] * W * P)} ({r[W][n]:.1f}×)' for W in WS) + ' |')
