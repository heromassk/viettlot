#!/usr/bin/env python3
"""Chọn bộ cộng/trừ điểm RIÊNG cho từng cỡ pool 10/15/18/20/25 (anh 14/10/2026: "tùy từng pool phải làm theo
các phương pháp, linh hoạt"). Ứng viên: 17 dấu vết thứ-ngày-tháng (dương + âm) / kỳ trước / kép (dauvet_ngay.py,
điểm +1 −1 +0,5 −0,5) và 20 phương pháp tâm linh của app (+1 +0,5).
Cách chọn (cố định): bắt đầu từ pool tín hiệu không cộng gì; mỗi bước thử mọi ứng viên, lấy cái làm cỡ pool đó tăng
nhiều nhất số kỳ ≥4 số (rồi ≥3 số) ở khung 50 + 100 kỳ, với điều kiện không khung nào (50, 100) giảm ≥3 hay ≥4.
Tối đa 3 bước. Chạy tiến 100 kỳ, mỗi kỳ chỉ dùng dữ liệu trước nó. Ghi build/pool_chon.json (goiy.py đọc).
  python build/kiemtra_app.py 200      # (khi dữ liệu đổi — lấy tâm linh từng kỳ)
  python build/pool_chon.py power|mega|loto"""
import json, os, sys
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B)
import dauvet_ngay as DV
GAME = sys.argv[1]
_src = open(os.path.join(B, 'goiy.py'), encoding='utf-8').read(); _argv = sys.argv; sys.argv = ['goiy.py', GAME]
GY = {'__file__': os.path.join(B, 'goiy.py'), '__name__': 'goiy_head'}
exec(compile(_src[:_src.index('# ---------- Đà tổng')], 'goiy.py', 'exec'), GY); sys.argv = _argv; GY['CUR'] = None
R, T, NB = GY['R'], GY['T'], GY['NB']; DS = GY['D']['dates']
HOLD = os.environ.get('HOLD') == '1'   # kiểm: chọn trên 100 kỳ cũ hơn, chấm trên 100 kỳ gần nhất (chưa thấy lúc chọn)
END = T - 100 if HOLD else T
TS = range(T - 200, T) if HOLD else range(T - 100, T); KS = tuple(int(x) for x in os.environ.get('KS', '10,12,15,18,20,25').split(',')); STEPS = int(os.environ.get('STEPS', '4'))
APP = json.load(open(os.path.join(B, 'kiemtra_app.json'), encoding='utf-8'))[GAME]; T0 = T - len(APP['dates'])
assert APP['L'] == T, 'chạy lại kiemtra_app.py'
DV.lunar_many([DS[t] for t in range(TS[0] - 25, T)])
SIG = {t: GY['signals'](t) for t in TS}
NUMS = {t: DV.cand_nums(R, DS, t, NB) for t in TS}
for x in APP['kx']:
    for t in TS: NUMS[t]['TL: ' + x['nm']] = {n for n in (x['nums'][t - T0] or []) if 1 <= n <= NB}
CAND = [(nm, w) for nm in NUMS[TS[0]] for w in ((1.0, 0.5, 0.25) if nm.startswith('Chạy') else (1.0, 0.5) if nm.startswith('TL: ') or 'đang về' in nm else (1.0, -1.0, 0.5, -0.5))]
if os.environ.get('WBIG') == '1':   # Power: điểm tín hiệu cách nhau xa, ±1 không đổi được pool → thử thêm ±2, ±3
    CAND += [(nm, w * k) for nm, w in list(CAND) if abs(w) == 1.0 for k in (2, 3)]
SELW = tuple(int(x) for x in os.environ.get('SELW', '50,100').split(','))   # khung dùng để chọn (anh 14/10: thêm tùy chọn chỉ 50 kỳ)
_C = {}
def ranks(items):
    key = frozenset(items)
    if key not in _C:
        out = {}
        for t in TS:
            e = {}
            for nm, w in items:
                for n in NUMS[t][nm]: e[n] = e.get(n, 0) + w
            f, s = SIG[t]; out[t] = GY['pool_of'](GY['score'](f, s, e), s, 25)
        _C[key] = out
    return _C[key]
# Số trúng từng kỳ của mỗi bộ cộng điểm (theo cỡ KS) lưu ra đĩa — kỳ cũ đã chấm thì không chấm lại, chỉ chấm kỳ mới rồi tính lại khung
# (anh 23/10/2026: "những cái cũ chấm làm gì khi đã xong rồi"). Mỗi kỳ có dấu vân tay = dữ liệu + tín hiệu + ứng viên của kỳ đó; code
# goiy.py / dauvet_ngay.py đổi thì xoá hết. Kết quả y hệt chấm lại từ đầu.
_H = {}; _HD = None; _FP = {}
_HP = os.path.join(B, '_tmp', f'pool_chon_hits_{GAME}.pkl')
def _canon(x):
    if isinstance(x, dict): return tuple(sorted(((_canon(k), _canon(v)) for k, v in x.items()), key=repr))
    if isinstance(x, (set, frozenset)): return ('s',) + tuple(sorted((_canon(v) for v in x), key=repr))
    if isinstance(x, (list, tuple)): return tuple(_canon(v) for v in x)
    return x
def _hload():
    global _HD, _VER
    import hashlib, pickle
    src = b''.join(open(os.path.join(B, f), 'rb').read() for f in ('goiy.py', 'dauvet_ngay.py'))
    _VER = hashlib.md5(src + repr((KS, sorted((k, v) for k, v in os.environ.items() if k.startswith('GOIY_')))).encode()).hexdigest()
    for t in TS: _FP[t] = hashlib.md5(repr(_canon((DS[t], R[t], SIG[t], NUMS[t]))).encode()).hexdigest()
    try:
        d = pickle.load(open(_HP, 'rb')); _HD = d['h'] if d.get('ver') == _VER else {}
    except Exception: _HD = {}
def hits(items):   # {t: (số trúng ở từng cỡ KS)}
    key = frozenset(items)
    if key not in _H:
        if _HD is None: _hload()
        old = _HD.get(key, {}); out = {}
        for t in TS:
            v = old.get(_FP[t])
            if v is None:
                e = {}
                for nm, w in items:
                    for n in NUMS[t][nm]: e[n] = e.get(n, 0) + w
                f, s = SIG[t]; rk = GY['pool_of'](GY['score'](f, s, e), s, 25); v = tuple(len(set(rk[:K]) & R[t]) for K in KS)
            out[t] = tuple(v)
        _H[key] = out
    return _H[key]
def hsave():
    if _HD is None: return
    import pickle
    cur = set(_FP.values()); new = {}
    for key, m in _HD.items():
        mm = {fp: v for fp, v in m.items() if fp in cur}
        if mm: new[key] = mm
    for key, out in _H.items():
        mm = new.setdefault(key, {})
        for t, v in out.items(): mm[_FP[t]] = bytes(v)
    pickle.dump(dict(ver=_VER, h=new), open(_HP + '.tmp', 'wb'), protocol=pickle.HIGHEST_PROTOCOL); os.replace(_HP + '.tmp', _HP)
def stat(items, K, end=None):   # {W: (số kỳ ≥3, số kỳ ≥4)}
    o = {}; end = end or END
    if K in KS: H = hits(items); i = KS.index(K); hk = lambda t: H[t][i]
    else: rk = ranks(items); hk = lambda t: len(set(rk[t][:K]) & R[t])
    for W in (10, 20, 50, 100):
        hs = [hk(t) for t in range(end - W, end)]; o[W] = (sum(h >= 3 for h in hs), sum(h >= 4 for h in hs))
    return o
fmt = lambda o: ' / '.join(f'{o[W][0] * 100 // W}·{o[W][1] * 100 // W}' for W in (10, 20, 50, 100))
CHON = {}; STAT = {}
START = {'loto': [('TL: Tử vi (Mệnh, Cục, sao Tử Vi)', 1.0)], 'mega': [('TL: Thần số học', 1.0), ('TL: Lộn + kép', 1.0), ('Ngày âm', 1.0)],
         'power': [('TL: Tử vi (Mệnh, Cục, sao Tử Vi)', 1.0)]}[GAME]   # bộ app đang dùng trước 14/10 tối
print(f'## {GAME} — bộ cộng điểm riêng từng cỡ pool (100 kỳ, đến {DS[-1]}). Ô = % kỳ ≥3 số · ≥4 số, khung 10 / 20 / 50 / 100\n')
print('| Pool | Không cộng gì | Bộ chọn | Sau khi cộng |\n|---|---|---|---|')
for K in KS:
    base = stat([], K); res = []
    for start in ([], START):
      cur = [c for c in start if c[0] in NUMS[TS[0]]]; b = stat(cur, K)
      for _ in range(STEPS):
        best = None
        for c in CAND:
            if any(c[0] == x[0] for x in cur): continue
            o = stat(cur + [c], K)
            if any(o[W][j] < b[W][j] for W in tuple(SELW) + (10,) for j in (0, 1)): continue   # + không giảm ở 10 kỳ gần (anh 15/10/2026)
            gain = (sum(o[W][1] - b[W][1] for W in SELW), sum(o[W][0] - b[W][0] for W in SELW))
            if gain > (0, 0) and (best is None or gain > best[0]): best = (gain, c, o)
        if not best: break
        cur.append(best[1]); b = best[2]
      res.append(((sum(b[W][1] for W in SELW), sum(b[W][0] for W in SELW)), cur, b))
    _, cur, b = max(res, key=lambda x: x[0])
    if HOLD:
        st0 = [(c[0], c[1]) for c in START if c[0] in NUMS[TS[0]]]
        print(f"| {K} | chấm 100 kỳ gần: không cộng {fmt(stat([], K, T))} · bộ app cũ {fmt(stat(st0, K, T))} · **bộ chọn từ kỳ cũ {fmt(stat(cur, K, T))}** | {', '.join(f'{nm} {w:+g}' for nm, w in cur)} |")
        continue
    CHON[str(K)] = [[nm, w] for nm, w in cur]; STAT[str(K)] = {str(W): list(b[W]) for W in b}
    lab = ', '.join(f"{nm.replace('TL: ', '')} {w:+g}" for nm, w in cur) or '—'
    print(f'| {K} | {fmt(base)} | {lab} | {fmt(b)} |')
if not HOLD: hsave()
if HOLD or os.environ.get('NOSAVE') == '1': sys.exit()
P = os.path.join(B, 'pool_chon.json')
allc = json.load(open(P, encoding='utf-8')) if os.path.exists(P) else {}
allc.setdefault(GAME, {})
_sf = '' if SELW == (50, 100) else '_'.join(map(str, SELW)); allc[GAME]['chon' + _sf] = CHON; allc[GAME]['stat' + _sf] = STAT; allc[GAME]['den'] = DS[-1]
json.dump(allc, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'\nĐã ghi pool_chon.json [{GAME}]')
