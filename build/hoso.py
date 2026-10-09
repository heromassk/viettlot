"""Hồ sơ từng số + sổ khoảng cách cộng/trừ (anh, 09/10/2026).
python3 build/hoso.py mega|power [--so 36,38]  → build/hoso_<game>.md + .json
- Hồ sơ số: ra 10/20/50/100, đang vắng, nghỉ thường (100 kỳ), ra lại ngay kỳ sau (chính số), theo khoảng vắng hiện tại, nhãn, nhận định.
- Sổ khoảng cách: mỗi kỳ, mỗi số trúng cách số gần nhất của kỳ trước bao nhiêu (0 = trùng, 1, 2, …); thống kê 10/20/50/100 kỳ và kỳ tới."""
import json, os, sys
from statistics import median
B = os.path.dirname(os.path.abspath(__file__))
g = sys.argv[1]; key, N, K = {'mega': ('mega645', 45, 6), 'power': ('power655', 55, 6)}[g]
ASK = [int(x) for x in sys.argv[sys.argv.index('--so') + 1].split(',')] if '--so' in sys.argv else []
D = json.load(open(os.path.join(B, 'all_data.json')))[key]; R = [set(sorted(r)[:K]) for r in D['res']]; T = len(R); dt = D['dates']
rv = lambda n: int(f'{n:02d}'[::-1])
def gaps_of(n, lo, hi):   # các khoảng nghỉ (số kỳ giữa 2 lần ra) trong [lo,hi)
    idx = [t for t in range(lo, hi) if n in R[t]]
    return [idx[i] - idx[i - 1] - 1 for i in range(1, len(idx))], idx
def prof(n):
    c = {W: sum(n in R[t] for t in range(T - W, T)) for W in (10, 20, 50, 100)}
    gap = next((j - 1 for j in range(1, T) if n in R[T - j]), T)
    gl, idx = gaps_of(n, T - 100, T)
    gl2, idx2 = gaps_of(n, T - 200, T)
    again = (sum(1 for t in idx2[:-1] if t + 1 < T and n in R[t + 1]), len([t for t in idx2 if t + 1 < T]))
    # đã vắng đúng `gap` kỳ (≥gap) → kỳ sau ra: theo lịch sử 200 kỳ của chính số
    reach = sum(1 for x in gl2 if x >= gap); hit = sum(1 for x in gl2 if x == gap)
    p_now = hit / reach if reach else None
    med = median(gl) if gl else None
    if gap == 0: lab = 'Nghiêng nghỉ' if again[1] and again[0] / again[1] < 0.12 else 'Bình thường'
    elif med is not None and gap >= max(gl) : lab = 'Vượt nghỉ dài nhất 100 kỳ'
    elif p_now is not None and reach >= 3 and p_now >= 0.25: lab = 'Nghiêng ra'
    elif med is not None and gap < med * 0.5: lab = 'Trong nhịp nghỉ'
    else: lab = 'Bình thường'
    tags = [t for t, ok in (('kép', n % 11 == 0), ('lộn có', rv(n) <= N and rv(n) != n), ('kề ±1', any(abs(n - x) == 1 for x in R[-1])), ('vừa ra', n in R[-1])) if ok]
    return dict(n=n, c=c, gap=gap, med=med, mn=min(gl) if gl else None, mx=max(gl) if gl else None, again=again, p_now=p_now, reach=reach, lab=lab, tags=tags)
P = {n: prof(n) for n in range(1, N + 1)}
# sổ khoảng cách
def dist_row(t):
    return sorted(min(abs(x - y) for y in R[t - 1]) for x in R[t])
rows = [(dt[t], sorted(R[t]), dist_row(t)) for t in range(T - 100, T)]
def dstat(W):
    ds = [d for _, _, r in rows[-W:] for d in r]
    out = {}
    for d in (0, 1, 2, 3, 4, 5):
        out[d] = (sum(x == d for x in ds), sum(any(x == d for x in r) for _, _, r in rows[-W:]))
    out['6+'] = (sum(x >= 6 for x in ds), sum(any(x >= 6 for x in r) for _, _, r in rows[-W:]))
    return out
L = [f'# Hồ sơ số {g.upper()} — sau kỳ {dt[-1]} ({" ".join(f"{x:02d}" for x in sorted(R[-1]))})\n']
L.append('## Sổ khoảng cách: số trúng cách số gần nhất của kỳ trước bao nhiêu\n')
L.append('| Kỳ | Kết quả | Khoảng cách từng số |\n|---|---|---|')
for d, r, ds in rows[-10:]: L.append(f'| {d} | {" ".join(f"{x:02d}" for x in r)} | {" ".join(map(str, ds))} |')
L.append('\n| Khoảng cách | ' + ' | '.join(f'{W} kỳ: số lượt / kỳ có' for W in (10, 20, 50, 100)) + ' |\n|---|---|---|---|---|')
S = {W: dstat(W) for W in (10, 20, 50, 100)}
for d in (0, 1, 2, 3, 4, 5, '6+'):
    L.append(f'| ±{d} | ' + ' | '.join(f'{S[W][d][0]} / {S[W][d][1]}' for W in (10, 20, 50, 100)) + ' |')
for d in (0, 1, 2, 3):
    pool = sorted({x + s for x in R[-1] for s in ((d, -d) if d else (0,)) if 1 <= x + s <= N} - (R[-1] if d else set()))
    L.append(f'\nKỳ tới ±{d}: {" ".join(f"{x:02d}" for x in pool)}')
L.append('\n## Hồ sơ từng số (100 kỳ; ra lại & theo khoảng vắng: 200 kỳ của chính số)\n')
L.append('| Số | Ra 10/20/50/100 | Đang vắng | Nghỉ thường (ngắn–TB–dài) | Ra lại kỳ sau | Vắng mức này → kỳ sau ra | Nhãn | Nhận định |\n|---|---|---|---|---|---|---|---|')
show = sorted(set(ASK) | set(range(1, N + 1)))
for n in show:
    p = P[n]; pn = '—' if p['p_now'] is None else '%d%% (%d)' % (round(p['p_now'] * 100), p['reach'])
    L.append(f"| {'**' if n in ASK else ''}{n:02d}{'**' if n in ASK else ''} | {p['c'][10]}/{p['c'][20]}/{p['c'][50]}/{p['c'][100]} | {p['gap']} | {p['mn']}–{p['med']}–{p['mx']} | {p['again'][0]}/{p['again'][1]} | {pn} | {', '.join(p['tags'])} | **{p['lab']}** |")
open(os.path.join(B, f'hoso_{g}.md'), 'w').write('\n'.join(L) + '\n')
json.dump(dict(last=dt[-1], prof=P, drows=rows[-10:], dstat={W: {str(k): v for k, v in S[W].items()} for W in S}), open(os.path.join(B, f'hoso_{g}.json'), 'w'), ensure_ascii=False)
if ASK:
    for n in ASK: print(P[n])
