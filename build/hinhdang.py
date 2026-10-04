#!/usr/bin/env python3
"""Hình dạng dãy: tổng, chẵn/lẻ, to/nhỏ, cặp liền nhau, số hàng chục, độ trải (max−min), khe lớn nhất, AC (độ phức tạp số học),
cùng đuôi. Chạy tiến: học 200 kỳ trước → tập giá trị gọn nhất chứa ≥q% → kỳ đúng nếu giá trị thật nằm trong.
  python3 build/hinhdang.py power|mega|loto [--W 100] [--q 85]
Báo % kỳ đúng (W gần / W trước), vé giữ lại; rồi gộp tham lam các đặc trưng (mỗi bước thêm cái làm vé giữ lại giảm nhiều nhất
mà % kỳ đúng gộp vẫn ≥ ngưỡng) và in khuôn áp cho kỳ tới."""
import json, os, sys, random
GM = {'power': ('power655', 55, 6), 'mega': ('mega645', 45, 6), 'loto': ('loto535', 35, 5)}
key, NB, KB = GM[sys.argv[1]]
arg = lambda k, d: type(d)(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
W, Q, L, FLOOR = arg('--W', 100), arg('--q', 85), 200, arg('--floor', 60)
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_data.json')))[key]
S = [sorted(r) for r in D['res']]; T = len(S)
random.seed(4); MC = [sorted(random.sample(range(1, NB + 1), KB)) for _ in range(4000)]

def ac(s):
    return len({b - a for i, a in enumerate(s) for b in s[i + 1:]}) - (KB - 1)
F = {
    'Tổng': (lambda s: sum(s), 'range'),
    'Số lẻ': (lambda s: sum(x % 2 for x in s), 'set'),
    f'Số nhỏ (≤{NB // 2})': (lambda s: sum(x <= NB // 2 for x in s), 'set'),
    'Cặp liền nhau': (lambda s: sum(s[i + 1] - s[i] == 1 for i in range(KB - 1)), 'set'),
    'Số hàng chục khác nhau': (lambda s: len({x // 10 for x in s}), 'set'),
    'Độ trải (max−min)': (lambda s: s[-1] - s[0], 'range'),
    'Khe lớn nhất': (lambda s: max(s[i + 1] - s[i] for i in range(KB - 1)), 'range'),
    'AC (độ phức tạp)': (ac, 'set'),
    'Số cặp cùng đuôi': (lambda s: KB - len({x % 10 for x in s}), 'set'),
}
def learn(t, f, kind):
    v = [f(S[u]) for u in range(t - L, t)]
    if kind == 'range':
        v.sort(); n = len(v); k = -(-Q * n // 100)
        i = min(range(n - k + 1), key=lambda i: (v[i + k - 1] - v[i], i)); lo, hi = v[i], v[i + k - 1]
        return lambda x: lo <= x <= hi, f'{lo}–{hi}'
    cnt = {}
    for x in v: cnt[x] = cnt.get(x, 0) + 1
    keep, acc = set(), 0
    for x in sorted(cnt, key=lambda x: -cnt[x]):
        keep.add(x); acc += cnt[x]
        if acc * 100 >= Q * len(v): break
    return (lambda x: x in keep), ','.join(map(str, sorted(keep)))

MCV = {k: [f(s) for s in MC] for k, (f, _) in F.items()}
def evalseg(a, b, feats, step=4):
    ok = 0; keep = 0; n = 0; m = 0
    for t in range(a, b):
        tests = {k: learn(t, F[k][0], F[k][1])[0] for k in feats}
        ok += all(tests[k](F[k][0](S[t])) for k in feats); n += 1
        if t % step == 0:
            keep += sum(all(tests[k](MCV[k][i]) for k in feats) for i in range(len(MC))) / len(MC); m += 1
    return ok / n * 100, keep / m * 100

print(f'## {key} — hình dạng dãy (mỗi đặc trưng giữ tập gọn nhất chứa ≥{Q}% của {L} kỳ trước)\n')
print(f'| Đặc trưng | Đúng {W} kỳ gần | {W} kỳ trước | Vé giữ lại | Áp kỳ tới |\n|---|---|---|---|---|')
single = {}
for k in F:
    r1, kp = evalseg(T - W, T, [k]); r0, _ = evalseg(T - 2 * W, T - W, [k])
    single[k] = (r1, r0, kp)
    print(f'| {k} | **{r1:.0f}%** | {r0:.0f}% | {kp:.0f}% | {learn(T, *F[k])[1]} |')
# gộp tham lam
chosen = []; cur = (100.0, 100.0)
while True:
    best = None
    for k in F:
        if k in chosen: continue
        r1, kp = evalseg(T - W, T, chosen + [k]); r0, _ = evalseg(T - 2 * W, T - W, chosen + [k])
        if min(r1, r0) < FLOOR: continue
        score = (r1 + r0) / 2 - kp
        if best is None or score > best[0]: best = (score, k, r1, r0, kp)
    if not best or best[4] >= cur[1] - 2: break
    chosen.append(best[1]); cur = (best[2], best[4])
    print(f'\n+ {best[1]} → đúng {best[2]:.0f}% ({W} gần) / {best[3]:.0f}% ({W} trước), vé giữ lại {best[4]:.0f}%')
if chosen:
    print('\n**Khuôn gộp áp kỳ tới:** ' + ' · '.join(f'{k} {learn(T, *F[k])[1]}' for k in chosen))
