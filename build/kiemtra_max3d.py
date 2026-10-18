#!/usr/bin/env python3
"""Max 3D+ / Max 3D Pro — thử lại mọi phương pháp app đang có (anh, 13/10/2026) trên 100 và 200 kỳ gần nhất, chạy tiến.
  python build/kiemtra_max3d.py [--md file] [--json file]
Mỗi kỳ quay 20 bộ / 1000 bộ → mỗi bộ ra BQ 2%/kỳ. Chấm từng phương pháp bằng tỉ lệ ra của các bộ nó chọn so với BQ (×1.10 = ra
nhiều hơn 10%) và % kỳ có ≥1 bộ ĐB rơi vào. Luật loại: % kỳ đúng không dùng được (20 bộ/kỳ gần như kỳ nào cũng chạm), nên chấm
bằng tỉ lệ ra của bộ bị loại ≤ BQ. Ổn định = đạt ở cả 100 kỳ gần và 100 kỳ trước đó.
17 phương pháp tâm linh (max3d_tl.js) lấy tỉ số đã chấm sẵn trong build/max3d_tl.json (100 gần / 100 trước)."""
import argparse, json, os, sys
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B)
import max3d_tamlinh as TL
ap = argparse.ArgumentParser(); ap.add_argument('--md'); ap.add_argument('--json'); A = ap.parse_args()
ALL = [f'{i:03d}' for i in range(1000)]
TIEN = {'012', '123', '234', '345', '456', '567', '678', '789'}
BQ = 20 / 1000
bong = lambda s: ''.join(str((int(c) + 5) % 10) for c in s)
quanh = lambda s: {s[:i] + str((int(s[i]) + d) % 10) + s[i + 1:] for i in range(3) for d in (-1, 1)}

def heavy(R, t, WW):
    c = [[1] * 10 for _ in range(3)]
    for r in R[max(0, t - WW):t]:
        for s in r:
            for i, ch in enumerate(s): c[i][int(ch)] += 1
    tot = [sum(x) for x in c]
    return lambda s: (c[0][int(s[0])] / tot[0]) * (c[1][int(s[1])] / tot[1]) * (c[2][int(s[2])] / tot[2]) * 1000

def methods(D, kind, t):
    R = D['res']; prev = R[t - 1]
    WW = 50 if kind == 'plus' else 100; NG = 5 if kind == 'plus' else 30; KP = 340 if kind == 'plus' else 400
    w = heavy(R, t, WW)
    nghi = lambda k: {s for r in R[max(0, t - k):t] for s in r}
    loai_app = nghi(NG) | TIEN | {d * 3 for d in '0123456789'} | {f'00{d}' for d in '0123456789'}
    con = sorted((s for s in ALL if s not in loai_app), key=lambda s: (-w(s) * (0.95 if s[0] == s[2] and s[0] != s[1] else 1), s))
    m = {
        'nghi5': ('loai', 'Bỏ bộ ra trong 5 kỳ gần', nghi(5)),
        'nghi10': ('loai', 'Bỏ bộ ra trong 10 kỳ gần', nghi(10)),
        'nghi30': ('loai', 'Bỏ bộ ra trong 30 kỳ gần', nghi(30)),
        'tien': ('loai', 'Bỏ bộ tiến liên tiếp (012…789)', TIEN),
        'tamhoa': ('loai', 'Bỏ tam hoa (000…999)', {d * 3 for d in '0123456789'}),
        '00x': ('loai', 'Bỏ dạng 00x', {f'00{d}' for d in '0123456789'}),
        'kepkep': ('loai', 'Bộ kép kẹp (aba) — app trừ điểm nhẹ', {s for s in ALL if s[0] == s[2] != s[1]}),
        'nhe': ('loai', 'Bộ có chữ số nhẹ nhất 100 kỳ ở mọi hàng (đang theo dõi)', None),
        'pool_app': ('chon', f'Pool app hiện tại ({KP} bộ)', set(con[:KP])),
        'nang': ('chon', f'{KP} bộ chữ số nặng nhất ({WW} kỳ), không loại gì', set(sorted(ALL, key=lambda s: (-w(s), s))[:KP])),
        'lap20': ('chon', '20 bộ kỳ trước (lặp lại)', set(prev)),
        'db2': ('chon', '2 bộ ĐB kỳ trước', set(prev[:2])),
        'quanh': ('chon', 'Quanh ±1 một chữ số của 20 bộ kỳ trước', set().union(*[quanh(s) for s in prev]) - set(prev)),
    }
    c100 = [[0] * 10 for _ in range(3)]
    for r in R[max(0, t - 100):t]:
        for s in r:
            for i, ch in enumerate(s): c100[i][int(ch)] += 1
    light = [min(range(10), key=lambda d: (c100[i][d], d)) for i in range(3)]
    m['nhe'] = ('loai', m['nhe'][1], {s for s in ALL if any(int(s[i]) == light[i] for i in range(3))})
    for nm, st in TL.bo_methods(D['dates'][t] if t < len(R) else None, prev).items() if t < len(R) else []:
        m['tl_' + nm] = ('chon', 'Tâm linh: ' + nm, set(st))
    return m, w

def run(f, kind):
    D = json.load(open(os.path.join(B, f), encoding='utf-8')); R = D['res']; T = len(R)
    V = {}
    for t in range(T - 400, T):
        m, w = methods(D, kind, t)
        for i, (typ, nm, st) in m.items():
            V.setdefault(i, dict(typ=typ, nm=nm, v={}))['v'][t] = st
        V.setdefault('_w', dict(v={}))['v'][t] = w
    def stat(i, ts):
        h = e = db = 0
        for t in ts:
            st = V[i]['v'][t]; h += sum(s in st for s in R[t]); e += len(st) * BQ; db += any(s in st for s in R[t][:2])
        return dict(lift=h / e if e else None, db=db / len(ts) * 100, sz=sum(len(V[i]['v'][t]) for t in ts) / len(ts))
    def ev(win):
        o = {}
        for i in V:
            if i == '_w': continue
            a, b, c = stat(i, range(win - 100, win)), stat(i, range(win - 200, win - 100)), stat(i, range(win - 200, win))
            ok = (lambda s: s['lift'] <= 1) if V[i]['typ'] == 'loai' else (lambda s: s['lift'] > 1)
            ms = min(a['sz'], b['sz']) * 100 * BQ < 10   # kỳ vọng <10 lần trúng mỗi nửa → ít mẫu
            o[i] = dict(s100=a, s100t=b, s200=c, ms=ms, on=bool(not ms and a['lift'] is not None and ok(a) and ok(b)))
        return o
    EV, EVO = ev(T), ev(T - 200)
    # tâm linh JS: tỉ số đã chấm (acc: [100 gần, 100–200, 200–300, cả lịch sử])
    TJ = json.load(open(os.path.join(B, 'max3d_tl.json'), encoding='utf-8'))[kind]
    big = {m['name']: m['n'] for m in TJ['methods']}   # cỡ bộ quẻ chọn kỳ tới (gần đúng cỡ mọi kỳ)
    TLJS = [dict(nm=n, a=a[0], b=a[1], ms=big.get(n, 0) * 100 * BQ < 10, on=big.get(n, 0) * 100 * BQ >= 10 and (a[0] or 0) > 1 and (a[1] or 0) > 1) for n, a in zip(TJ['names'], TJ['acc'])]
    def build(e, t):
        ex = set().union(*[V[i]['v'][t] for i in e if e[i]['on'] and V[i]['typ'] == 'loai'])
        sc = {s: 0.0 for s in ALL if s not in ex}
        for i in e:
            if e[i]['on'] and V[i]['typ'] == 'chon':
                for s in V[i]['v'][t]:
                    if s in sc: sc[s] += e[i]['s200']['lift'] - 1
        w = V['_w']['v'][t]
        return sorted(sc, key=lambda s: (-sc[s], -w(s), s)), ex
    SZ = (100, 200, 340, 400, 500)
    def pstat(e, ts):
        out = {}
        rk = {t: build(e, t)[0] for t in ts}
        for K in SZ:
            h = sum(sum(s in set(rk[t][:K]) for s in R[t]) for t in ts); db = sum(any(s in set(rk[t][:K]) for s in R[t][:2]) for t in ts)
            out[K] = dict(lift=h / (len(ts) * K * BQ), db=db / len(ts) * 100, tb=h / len(ts))
        return out
    L100, L200 = range(T - 100, T), range(T - 200, T)
    PS = dict(chuan={'100': pstat(EV, L100), '200': pstat(EV, L200)}, cheo={'100': pstat(EVO, L100), '200': pstat(EVO, L200)},
              hien={w: {K: None for K in SZ} for w in ('100', '200')})
    exn = sum(len(build(EV, t)[1]) for t in L200) / 200
    return dict(D=D, V=V, EV=EV, TLJS=TLJS, PS=PS, SZ=SZ, exn=exn, T=T)

lf = lambda v: '—' if v is None else f'×{v:.2f}'
L = []
OUT = {}
for f, kind, name in (('max3d_data.json', 'plus', 'Max 3D+'), ('max3dpro_data.json', 'pro', 'Max 3D Pro')):
    X = run(f, kind); EV, V = X['EV'], X['V']
    L.append(f"## {name} — chấm trên 100 / 200 kỳ gần nhất (đến {X['D']['dates'][-1]}), BQ mỗi bộ ra 2%/kỳ\n")
    L.append('| Phương pháp | Loại / chọn | Cỡ TB (bộ) | Ra so với BQ: 100 / 200 kỳ (100 trước) | Kỳ có ≥1 bộ ĐB rơi vào (200 kỳ) | Đạt |\n|---|---|---|---|---|---|')
    for i in sorted(EV, key=lambda i: (V[i]['typ'], -(EV[i]['s200']['lift'] or 0))):
        e = EV[i]
        L.append(f"| {V[i]['nm']} | {'loại' if V[i]['typ'] == 'loai' else 'chọn'} | {e['s200']['sz']:.0f} | {lf(e['s100']['lift'])} / {lf(e['s200']['lift'])} ({lf(e['s100t']['lift'])}) | {e['s200']['db']:.0f}% | {'✔ đạt' if e['on'] else ('ít mẫu' if e['ms'] else '✘')} |")
    L.append('\n**17 phương pháp tâm linh** (tỉ số ra so với BQ, 100 kỳ gần / 100 trước): ' + ' · '.join(
        f"{x['nm']} {lf(x['a'])}/{lf(x['b'])}{' ✔' if x['on'] else (' (ít mẫu)' if x['ms'] else '')}" for x in X['TLJS']))
    ON = [i for i in EV if EV[i]['on']]
    L.append(f"\n**Pool chuẩn** — loại: {', '.join(V[i]['nm'] for i in ON if V[i]['typ'] == 'loai') or '—'} (TB bỏ {X['exn']:.0f} bộ); cộng điểm: {', '.join(V[i]['nm'] for i in ON if V[i]['typ'] == 'chon') or '—'}; hòa điểm xếp theo chữ số nặng.\n")
    L.append('| Cỡ pool | Pool chuẩn: ×BQ 100 / 200 kỳ | Kỳ có ≥1 ĐB trong pool (200 kỳ) / kỳ vọng theo cỡ | Kiểm chéo (chọn từ 200 kỳ cũ): ×BQ 100 / 200 |\n|---|---|---|---|')
    for K in X['SZ']:
        c1, c2 = X['PS']['chuan']['100'][K], X['PS']['chuan']['200'][K]; x1, x2 = X['PS']['cheo']['100'][K], X['PS']['cheo']['200'][K]
        L.append(f"| {K} | **{lf(c1['lift'])} / {lf(c2['lift'])}** | {c2['db']:.0f}% / {(1 - (1 - K / 1000) ** 2) * 100:.0f}% | {lf(x1['lift'])} / {lf(x2['lift'])} |")
    L.append('')
    OUT[kind] = dict(on=ON, ev={i: dict(nm=V[i]['nm'], typ=V[i]['typ'], **EV[i]) for i in EV}, tljs=X['TLJS'], pools=X['PS'])
txt = '\n'.join(L) + '\n'
print(txt)
if A.md: open(A.md, 'a', encoding='utf-8').write(txt + '\n')
if A.json: json.dump(OUT, open(A.json, 'w', encoding='utf-8'), ensure_ascii=False)
