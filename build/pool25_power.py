"""Pool 25 Power (anh duyệt 10/10/2026): xếp hạng = cộng hạng 3 cách
  (1) chéo Mega qua 7 kỳ, (2) vắng ≈ 25 kỳ, (3) vắng ≈ 27 kỳ  → lấy 25 số đầu.
Bước 2: xem hồ sơ từng số (nhãn như hoso.py, tính tại từng kỳ) để loại tiếp.
Chấm 10/20/50/100 kỳ; sổ tiến build/pool25_power_log.jsonl; dữ liệu app build/pool25_power.json.
python3 build/pool25_power.py"""
import json, os, datetime as dt
from statistics import median
import numpy as np
B = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(os.path.join(B, 'all_data.json')))
D = A['power655']; R = [set(r[:6]) for r in D['res']]; T = len(R); NB = 55
dd = lambda s: dt.datetime.strptime(s[:10], '%d/%m/%Y')
MD = [(dd(d), set(r)) for d, r in zip(A['mega645']['dates'], A['mega645']['res'])]
DT = [dd(d) for d in D['dates']]
def nxt(d):   # kỳ Power tới: T3/T5/T7
    d += dt.timedelta(days=1)
    while d.weekday() not in (1, 3, 5): d += dt.timedelta(days=1)
    return d
DT.append(nxt(DT[-1]))
def gap(t, n):
    k = 0
    while k < 300 and n not in R[t - 1 - k]: k += 1
    return k
def hot(t, n, w): return sum(n in R[t - j] for j in range(1, w + 1))
def scores(t):
    meg = [s for e, s in MD if e < DT[t]][-7:]
    s1 = np.array([sum(n in s for s in meg) + 1e-3 * hot(t, n, 100) for n in range(1, NB + 1)])
    gp = np.array([gap(t, n) for n in range(1, NB + 1)], float); h100 = np.array([hot(t, n, 100) for n in range(1, NB + 1)])
    s2 = -abs(gp - 25) + 1e-3 * h100; s3 = -abs(gp - 27) + 1e-3 * h100
    rk = lambda s: np.argsort(np.argsort(s))
    return rk(s1) + rk(s2) + rk(s3)
def pool(t): s = scores(t); return [int(i) + 1 for i in np.argsort(-s + 1e-9 * np.arange(NB))[:25]]
def lab(t, n):   # nhãn hồ sơ số tại kỳ t (chỉ dùng R[:t]) — giống hoso.py
    g = gap(t, n)
    idx = [u for u in range(t - 100, t) if n in R[u]]; gl = [b - a - 1 for a, b in zip(idx, idx[1:])]
    idx2 = [u for u in range(t - 200, t) if n in R[u]]; gl2 = [b - a - 1 for a, b in zip(idx2, idx2[1:])]
    ag = (sum(1 for u in idx2[:-1] if n in R[u + 1]), len(idx2[:-1]))
    reach = sum(x >= g for x in gl2); hit = sum(x == g for x in gl2); p = hit / reach if reach else None
    med = median(gl) if gl else None
    if g == 0: return 'Nghiêng nghỉ' if ag[1] and ag[0] / ag[1] < 0.12 else 'Bình thường'
    if med is not None and gl and g >= max(gl): return 'Vượt nghỉ dài nhất'
    if p is not None and reach >= 3 and p >= 0.25: return 'Nghiêng ra'
    if med is not None and g < med * 0.5: return 'Trong nhịp nghỉ'
    return 'Bình thường'
LABS = ('Nghiêng nghỉ', 'Trong nhịp nghỉ', 'Vượt nghỉ dài nhất', 'Nghiêng ra', 'Bình thường')
ts = range(T - 100, T)
rec = []
for t in ts:
    p = pool(t); L = {n: lab(t, n) for n in p}
    rec.append(dict(t=t, p=p, L=L, r=R[t]))
def frame(f):
    out = {}
    for W in (10, 20, 50, 100):
        x = rec[-W:]; h = [f(e) for e in x]
        out[W] = (sum(len(a & e['r']) for (a, _), e in zip(h, x)) / W, sum(len(a & e['r']) >= 3 for (a, _), e in zip(h, x)) / W * 100,
                  sum(len(a & e['r']) >= 4 for (a, _), e in zip(h, x)) / W * 100, sum(b for _, b in h) / W)
    return out
CASES = {'Pool 25': lambda e: (set(e['p']), 25)}
for drop in (('Nghiêng nghỉ',), ('Trong nhịp nghỉ',), ('Nghiêng nghỉ', 'Trong nhịp nghỉ'), ('Vượt nghỉ dài nhất',)):
    CASES['Loại ' + ' + '.join(drop)] = (lambda drop: lambda e: ({n for n in e['p'] if e['L'][n] not in drop}, len([n for n in e['p'] if e['L'][n] not in drop])))(drop)
F = {k: frame(f) for k, f in CASES.items()}
# mỗi nhãn trong pool: ra bao nhiêu %/số (100 kỳ)
lab_rate = {}
for l in LABS:
    a = sum(1 for e in rec for n in e['p'] if e['L'][n] == l); h = sum(1 for e in rec for n in e['p'] if e['L'][n] == l and n in e['r'])
    lab_rate[l] = (h, a)
# kỳ tới
pn = pool(T); Ln = {n: lab(T, n) for n in pn}
import sys
TLF = sys.argv[sys.argv.index('--tl') + 1] if '--tl' in sys.argv else None   # phiếu tâm linh kỳ tới (tamlinh.js power)
_TL = json.load(open(TLF)) if TLF else None
if _TL and (len(_TL['votes']) != 56 or _TL.get('last', D['dates'][-1]) != D['dates'][-1]): raise SystemExit(f'DỪNG: {TLF} không phải phiếu Power của kỳ mới nhất — chạy lại node build/tamlinh.js power')   # sửa 13/10
VOT = _TL['votes'] if _TL else None
p20 = sorted(n for n in pn if VOT[n] != 3) if VOT else None   # pool 20: bỏ số có đúng 3 phiếu tâm linh (anh 10/10: ≥4 ~30%, 2 nửa 30·30)
LOG = os.path.join(B, 'pool25_power_log.jsonl'); log = [json.loads(l) for l in open(LOG)] if os.path.exists(LOG) else []
for e in log:
    if 'trung' not in e and e['t'] < T:
        e['kq'] = sorted(R[e['t']]); e['trung'] = len(set(e['pool']) & R[e['t']])
        if e.get('pool20'): e['trung20'] = len(set(e['pool20']) & R[e['t']])
nd = DT[T].strftime('%d/%m/%Y')
if not log or log[-1]['t'] != T: log.append(dict(t=T, ky=nd, pool=sorted(pn), nhan=Ln))
else: log[-1].update(pool=sorted(pn), nhan=Ln)   # kỳ chưa quay: cập nhật theo dữ liệu mới nhất (Mega xen giữa) — sửa 13/10, trước bị đóng băng
if p20: log[-1]['pool20'] = p20
if VOT: log[-1]['vt'] = VOT   # lưu phiếu thật để đối chiếu phiếu chấm lại quá khứ (tamlinh_ls)
open(LOG, 'w').write(''.join(json.dumps(e, ensure_ascii=False) + '\n' for e in log))
APP = dict(ky=nd, pool=sorted(pn), pool20=p20 or (log[-1].get('pool20') if log and log[-1]['t'] == T else None), nhan={str(n): Ln[n] for n in pn}, frames={k: {str(W): [round(x, 2) for x in v] for W, v in f.items()} for k, f in F.items()},
           lab_rate={k: v for k, v in lab_rate.items()}, tien=[e for e in log if 'trung' in e][-20:])
json.dump(APP, open(os.path.join(B, 'pool25_power.json'), 'w'), ensure_ascii=False)
print(f'## Pool 25 Power — kỳ {nd}\n\n**{" ".join(f"{n:02d}" for n in sorted(pn))}**\n')
print(f'Pool 20 (bỏ số 3 phiếu tâm linh): **{" ".join(f"{n:02d}" for n in p20)}**\n' if p20 else '')
print('| Cách | Khung 10 · 20 · 50 · 100: ≥4 số | ≥3 số | Trúng TB | Cỡ pool |\n|---|---|---|---|---|')
for k, f in F.items():
    print(f'| {k} | ' + ' · '.join(f'{f[W][2]:.0f}%' for W in (10, 20, 50, 100)) + ' | ' + ' · '.join(f'{f[W][1]:.0f}%' for W in (10, 20, 50, 100)) +
          f' | {f[100][0]:.2f} | {f[100][3]:.1f} |')
print('\n| Nhãn hồ sơ (số trong pool, 100 kỳ) | Lượt | Ra | %/số |\n|---|---|---|---|')
for l, (h, a) in lab_rate.items(): print(f'| {l} | {a} | {h} | {h / a * 100 if a else 0:.1f}% |')
print('\n| Số | Nhãn kỳ tới |\n|---|---|')
for l in LABS:
    xs = [n for n in sorted(pn) if Ln[n] == l]
    if xs: print(f'| {" ".join(f"{n:02d}" for n in xs)} | {l} |')
