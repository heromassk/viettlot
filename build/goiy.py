#!/usr/bin/env python3
"""Gợi ý tiềm năng theo các phương pháp dấu vết cố định (cùng một cách tính qua mọi kỳ).

  python3 build/goiy.py power [--app tl.json] [--G 20] [--k 15] [--linh 54,13]

--app : JSON từ `node build/tamlinh.js <game>` (phiếu tâm linh, pool app, pp tốt nhất 50 kỳ)
--G   : bỏ số vắng >= G kỳ (giả thuyết trọng lượng bi). Mặc định power/mega 20, loto 15
--k   : cỡ pool (mặc định 15)
--linh: số linh cảm của anh (được cộng điểm mạnh)

Mỗi tín hiệu được chấm bằng tỉ lệ đúng của CHÍNH NÓ ở 10/50/200 kỳ gần nhất (không so ngẫu nhiên).
"""
import argparse, json, math, os
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
GAMES = {'power': ('power655', 55, 6, 'Power 6/55'), 'mega': ('mega645', 45, 6, 'Mega 6/45'),
         'loto': ('loto535', 35, 5, 'Loto 5/35')}

ap = argparse.ArgumentParser()
ap.add_argument('game', choices=GAMES)
ap.add_argument('--app'); ap.add_argument('--G', type=int); ap.add_argument('--k', type=int, default=15)
ap.add_argument('--linh', default='')
ap.add_argument('--bo', default='', help='số anh muốn loại tay kỳ này, vd 02,27')
ap.add_argument('--cu', action='store_true', help='cách cũ: tắt các luật loại trừ bổ sung (để so)')
ap.add_argument('--json', help='ghi dữ liệu gợi ý dạng JSON (cho bảng trực quan)')
ap.add_argument('--save', action='store_true', help='ghi gợi ý vào build/goiy_log.jsonl')
A = ap.parse_args()
key, NB, KB, NAME = GAMES[A.game]
G = A.G or (15 if A.cu and A.game == 'loto' else 999 if A.game == 'power' and not A.cu else 20)   # Power: vắng ≥20 đang NGƯỢC (200 kỳ: ra 14.7/11.0%, loại đúng chỉ 51%) → bỏ (05/10)   # ý anh 04/10: loại số vắng ≥20 (cả 3 trò)   # Mega: vắng ≥30 đúng 94% kỳ (suyluan 04/10)   # Loto: số vắng lâu không nên loại (04/10)
D = json.load(open(os.path.join(HERE, 'all_data.json')))[key]
R = [set(r) for r in D['res']]          # cũ -> mới
SES = ['13' if '13h' in x else '21' for x in D['dates']] + ['13' if '21h' in D['dates'][-1] else '21']
T = len(R)
APP = json.load(open(A.app)) if A.app else None
LINH = {int(x) for x in A.linh.replace(' ', ',').split(',') if x.strip()}
BO = {int(x) for x in A.bo.replace(' ', ',').split(',') if x.strip()}
P = KB / NB
# Cửa sổ xét "tính chất bi" (dễ/khó ra, thưa, ra đều…): Power/Mega thay bộ bi định kỳ → chỉ xét WB kỳ gần (anh, 05/10)
WB = int(os.environ.get('GOIY_WB', {'power': '100', 'mega': '100', 'loto': '100'}[A.game]))   # mọi game tối đa 100 kỳ (anh 15/10/2026); Power/Mega (thay bi 1–2 tháng/lần — anh, 05/10); Loto không có bi thật


def feats(t):
    """Đặc trưng từng số chỉ dùng dữ liệu trước kỳ t (R[:t])."""
    f = {}
    for n in range(1, NB + 1):
        g = 0
        while g < t and n not in R[t - 1 - g]:
            g += 1
        c = lambda w: sum(n in R[i] for i in range(max(0, t - w), t))
        w2 = min(WB, t)
        z = (c(WB) - w2 * P) / math.sqrt(w2 * P * (1 - P))
        f[n] = dict(gap=g, c10=c(10), c20=c(20), z=z)
    return f


def signals(t):
    f = feats(t); last = R[t - 1]
    e20 = 20 * P
    hot = {n for n, x in f.items() if x['c10'] >= 3 or x['c20'] >= math.ceil(2 * e20)}
    ke = {m for n in last for m in (n - 1, n + 1) if 1 <= m <= NB} - last
    de = {n for n, x in f.items() if x['z'] > 1}
    kho = {n for n, x in f.items() if x['z'] < -1.5}
    vang = {n for n, x in f.items() if x['gap'] >= G}
    sig = dict(hot=hot, ke=ke, de=de, kho=kho, vang=vang)
    if A.game == 'loto':   # dấu vết riêng Loto (máy tính quay): chuyển kỳ + nóng cùng phiên
        sig['chuyen'] = top8(follow(t))
        ph = SES[t]
        same = [u for u in range(max(0, t - 100), t) if SES[u] == ph]
        sig['phien'] = top8({n: sum(n in R[u] for u in same) for n in range(1, NB + 1)})
    if not A.cu and A.game in ('mega', 'loto'):   # ý anh 04/10: loại trước số "lâu lâu mới ra" (thưa) đang vắng ≥15
        c200 = {n: sum(n in R[u] for u in range(max(0, t - WB), t)) for n in range(1, NB + 1)}
        sig['thua'] = {n for n in range(1, NB + 1) if f[n]['gap'] >= 15 and c200[n] <= 0.85 * min(WB, t) * P}
    if not A.cu:   # luận số / soi cầu có lợi nhẹ (soicau.py 05/10): Loto lô kép, Power cầu Pascal
        if A.game == 'loto' and WSC: sig['kep'] = set(range(11, NB + 1, 11))
        if A.game == 'power' and WSC:
            d = [int(ch) for ch in ''.join(f'{n:02d}' for n in sorted(R[t - 1]))]
            while len(d) > 2: d = [(d[i] + d[i + 1]) % 10 for i in range(len(d) - 1)]
            v = d[0] * 10 + d[1]; sig['pascal'] = {v} if 1 <= v <= NB else set()
    if not A.cu:   # luật loại trừ bổ sung (build/loai_tru.py, 04/10/2026) — chỉ giảm/cộng điểm, không loại hẳn
        if A.game == 'power':
            sig['chin'] = {n for n, x in f.items() if 11 <= x['gap'] <= 15}
            sig['g610'] = {n for n, x in f.items() if 6 <= x['gap'] <= 10}
            sig['tuan'] = R[t - 3] - R[t - 1]   # số của kỳ cùng thứ tuần trước: ra lại ít hơn 3/3 khúc (thu_them.py)
            c100 = {n: sum(n in R[u] for u in range(t - min(100, WB), t)) for n in range(1, NB + 1)}
            sig['it100'] = set(sorted(c100, key=lambda n: (c100[n], n))[:1])   # ra ít nhất 100 kỳ → loại (93/93/91%, loai_nho.py)
        elif A.game == 'mega':
            sig['duoi'] = {n for n in range(1, NB + 1) if n % 10 in {x % 10 for x in last}} - last
            sig['lien2'] = R[t - 1] & R[t - 2]          # ra 2 kỳ liền → loại (đúng 92% kỳ, 100 kỳ gần)
            if WCHM: sig['chin'] = {n for n, x in f.items() if 11 <= x['gap'] <= 15}   # thử: vắng 11–15 "chín" (04/10: 4/6 số về đều vắng 11–14)
            sig['lt3'] = R[t - 1] & R[t - 3]            # ra kỳ trước VÀ kỳ t−3 → loại (90/90/91%)
            sig['zprev'] = {max(R[t - 1])}              # số lớn nhất kỳ trước → loại (88/86/91%)
            q = min(100, WB) // 4; e25 = q * P
            q4 = [{n: sum(n in R[u] for u in range(t - 4 * q + q * i, t - 3 * q + q * i)) for n in range(1, NB + 1)} for i in range(4)]
            sig['ben'] = {n for n in range(1, NB + 1) if all(x[n] > e25 for x in q4)}   # ra nhiều cả 4 đoạn 25 kỳ → +1
        else:
            sig['lap'] = set(last)
            sig['tx15'] = {n for n in last if all(n not in R[u] for u in range(max(0, t - 16), t - 1))}   # tái xuất sau vắng ≥15 → loại (96/93/97%)
            sig['vang1'] = {max(f, key=lambda n: (f[n]['gap'], -n))}                                   # vắng lâu nhất → loại (89/90/89%)
            sig['nong35'] = {n for n in range(1, NB + 1) if sum(n in R[u] for u in range(t - 5, t)) >= 3}  # ra 3 lần/5 kỳ → loại (92/95/91%)
            # Số THÁNG của kỳ t không bị luật này loại (anh 17/10/2026 "ngày tháng đang mạnh"; thang_test.py: không giảm ô nào, tăng kỳ ≥3/≥4 ở mọi cỡ pool)
            _ds = D['dates']
            if t < len(_ds): _m = int(_ds[t][3:5])
            else:
                import datetime as _dt
                _l = _dt.datetime.strptime(_ds[-1][:10], '%d/%m/%Y'); _m = (_l + _dt.timedelta(days=1 if _ds[-1].endswith('21h') else 0)).month
            sig['nong35'].discard(_m)
    if not A.cu:   # số không ra trong VX kỳ gần (anh 19/10/2026; vang_x.py Loto 8 kỳ, vang_x_bi.py Mega 8 kỳ / Power 12 kỳ)
        sig['vang8'] = set(range(1, NB + 1)) - set().union(*R[t - VX:t])
    sig['_td'] = td_sets(t)
    if WMK and not A.cu: sig['_mk'] = mk_rank(t)
    if MIXM and not A.cu: sig['_mix'] = [MIXF[m](t) for m in MIXM.split(',')]
    if A.game == 'loto' and not A.cu: sig['vangph20'] = set(_TD.vang_phien(R, t, 20))   # bỏ số vắng ≥20 kỳ cùng phiên (14/10)
    return f, sig


# ---- Gộp 50/50 hạng (anh duyệt 14/10/2026, pool_moi.py --tung: thử từng phương pháp gắn vào pool đang dùng) ----
# Power: chuỗi ra/vắng bậc 5 chung mọi số, học 100 kỳ — pool 18 ≥3/≥4 số 44·16 / 38·13 (50/100 kỳ) so với 30·6 / 36·13
# Mega:  Markov bộ số bậc 4, học 50 kỳ — pool 18 60·30 / 57·30 so với 54·22 / 54·21
# Điểm cuối = hạng (0..1) của điểm cũ + hạng của phương pháp. GOIY_MIX=0 để tắt (về cách cũ).
def chuoi_rank(t, k=5, W=100):
    m = (1 << k) - 1; P0 = KB / NB
    st = lambda n, u: sum((n in R[u - 1 - i]) << i for i in range(k))
    c = {}; h = {}
    for u in range(max(k, t - W), t):
        for n in range(1, NB + 1):
            x = st(n, u); c[x] = c.get(x, 0) + 1; h[x] = h.get(x, 0) + (n in R[u])
    return {n: (h.get(st(n, t), 0) + 3 * P0) / (c.get(st(n, t), 0) + 3) for n in range(1, NB + 1)}
def mkbac_rank(t, k=4, W=50):
    from itertools import product as _pr
    RL = lambda u: sorted(R[u])
    cur = set(_pr(*[RL(t - k + i) for i in range(k)])); c = {}; tn = {}
    for u in range(max(k, t - W), t):
        for tup in _pr(*[RL(u - k + i) for i in range(k)]):
            if tup in cur:
                c[tup] = c.get(tup, 0) + 1
                for n in R[u]: tn[(tup, n)] = tn.get((tup, n), 0) + 1
    sc = {n: 0.0 for n in range(1, NB + 1)}
    for (tup, n), v in tn.items(): sc[n] += v / c[tup]
    return sc
MIXF = {'chuoi5': chuoi_rank, 'chuoi3': lambda t: chuoi_rank(t, 3, 50), 'mk4': mkbac_rank}
MIXN = {'chuoi5': 'chuỗi ra/vắng bậc 5 (chung mọi số, học 100 kỳ)', 'chuoi3': 'chuỗi ra/vắng bậc 3 (chung mọi số, học 50 kỳ)', 'mk4': 'Markov bộ số bậc 4 (học 50 kỳ)'}
MIXM = os.environ.get('GOIY_MIX', {'power': 'chuoi3,chuoi5', 'mega': 'mk4'}.get(A.game, ''))   # Power 14/10: thêm bậc 3 (pool 18 kỳ ≥3 số 41–70%, ≥4 số 17% ở 100 kỳ)
if MIXM == '0': MIXM = ''
def _r01(d):
    od = sorted(d, key=lambda n: (-d[n], n)); return {n: 1 - i / (NB - 1) for i, n in enumerate(od)}


# ---- Markov bậc 2 (anh, 13/10/2026): cặp (số kỳ t−2, số kỳ t−1) → số kỳ t, học 50 kỳ gần ----
# pool_hoc.py chạy tiến 200 kỳ: Power pool 18 về ≥4 số 14% (pool cũ 10%), ổn định ở cả khung học 50/100/200 kỳ.
# Mega/Loto không hơn pool cũ → tắt (GOIY_MK=0). Điểm = hạng Markov (0..1) × WMK; WMK lớn → Markov quyết định thứ tự.
WMK = float(os.environ.get('GOIY_MK', {'power': '100'}.get(A.game, '0')))
MKW = int(os.environ.get('GOIY_MKW', '50'))
def mk_rank(t, W=None):
    W = W or MKW; cur = {(x, y) for x in R[t - 2] for y in R[t - 1]}; c = {}; tn = {}
    for u in range(max(2, t - W), t):
        for x in R[u - 2]:
            for y in R[u - 1]:
                if (x, y) in cur:
                    c[(x, y)] = c.get((x, y), 0) + 1
                    for n in R[u]: tn[(x, y, n)] = tn.get((x, y, n), 0) + 1
    sc = {n: 0.0 for n in range(1, NB + 1)}
    for (x, y, n), v in tn.items(): sc[n] += v / c[(x, y)]
    od = sorted(sc, key=lambda n: (-sc[n], n))
    return {n: 1 - i / (NB - 1) for i, n in enumerate(od)}


# ---- Luật trong sổ kiểm chứng nghiêng ổn định (rasoat.py 05/10/2026) → trọng số nhỏ (dấu vết = xác suất nghiêng) ----
import sys as _sys
_sys.path.insert(0, HERE)
import theodoi as _TD
WTD = float(os.environ.get('GOIY_TD', {'loto': '1', 'power': '1', 'mega': '1'}[A.game]))   # luật đúng ≥70% ở khung 50 & 100 kỳ và số bị loại ra ≤ TB (luat_khung.py, anh 05/10)
TDW = {   # id luật → dấu trọng số (−: ra ít, +: ra nhiều)
    'power': {'nong35': -1, 'nhip2': -1, 'lt3': -1, 'tx15': -1, 'tx10': -1, 'zprev': -1,
              'nhom_lokep': -1, 'nhom_kep': 1, 'nhom_pascal': 1, 'nhom_cau2': 1},
    'mega': {'nong35': -1, 'tx15': -1, 'nong10': -1, 'nhieu100': -1, 'nhip2': -1},
    'loto': {'lt3': -1, 'nhip2': -1,   # 14/10: bỏ 'tx10' (số tái xuất ra 36/33/20/16% > TB)
             'nhipmin100': -1, 'nhom_nhip80': -1, 'nhom_nhip': -1, 'nhom_lokep': -1,
             'nhom_k7': 1, 'nhom_k9': 1, 'nhom_kep': 1, 'nhom_pascal': 1, 'nhom_keplk': 1, 'txph13': -1},
}[A.game]
if os.environ.get('GOIY_TDW'): TDW = json.loads(os.environ['GOIY_TDW'])   # thử bộ trọng số khác
_RF = {i: f for i, l, f in _TD.RULES}; _CF = {i: f for i, l, f in _TD.CLAIMS}
if A.game == 'loto': _TD.SESS = SES
def td_sets(t):
    if not WTD or A.cu: return {}
    c = _TD.ctx(R, NB, t); out = {}
    for i, sg in TDW.items():
        if i in _RF: out[i] = (sg, _RF[i](R, t, c))
        elif i in _CF: out[i] = (sg, set(_CF[i](R, t, c, NB, KB)[1]))
    return out


def top8(c):
    return set(sorted(c, key=lambda n: (-c[n], n))[:8])


def follow(t):
    """Số a ở kỳ t-1 → các số hay ra ngay sau a trong lịch sử trước t."""
    c = {n: 0 for n in range(1, NB + 1)}
    last = R[t - 1]
    for u in range(1, t):
        k = len(R[u - 1] & last)
        if k:
            for b in R[u]: c[b] += k
    return c


def score(f, s, extra=None):
    sc = {}
    for n in range(1, NB + 1):
        v = 2 * (n in s['hot']) + 1 * (n in s['ke']) + 1 * (n in s['de']) - 1.5 * (n in s['kho'])
        v += 1.5 * (n in s.get('chuyen', ())) + 1 * (n in s.get('phien', ()))
        v += WCHIN * (n in s.get('chin', ())) - WG610 * (n in s.get('g610', ())) \
            - WDUOI * (n in s.get('duoi', ())) - WLAP * (n in s.get('lap', ())) - WTUAN * (n in s.get('tuan', ())) \
            + 1 * (n in s.get('ben', ())) + WSC * (n in s.get('kep', ())) + WSC * (n in s.get('pascal', ()))
        v += WV8 * (n in s.get('vang8', ()))
        v += sum(WTD * sg for sg, st in s.get('_td', {}).values() if n in st)
        v += WMK * s.get('_mk', {}).get(n, 0)
        v += min(f[n]['c20'], 6) * 0.15            # độ nóng mềm để tách hoà
        if extra:
            v += extra.get(n, 0)
        sc[n] = v
    if s.get('_mix'):   # gộp 50/50 hạng với phương pháp đã duyệt
        rs = [_r01(sc)] + [_r01(m) for m in s['_mix']]; sc = {n: sum(r[n] for r in rs) for n in sc}
    return sc


LOAI = {'power': ('it100',), 'mega': ('lien2', 'lt3', 'zprev', 'thua'), 'loto': ('vang1', 'nong35', 'thua', 'vangph20')}   # Loto 14/10: bỏ 'tx15' — số tái xuất dạo này hay về lại (ra 50/42/25/20% ở 10/20/50/100 kỳ)
def loai_of(s):
    out = set()
    for k in LOAI[A.game]: out |= s.get(k, set())
    return out

def pool_of(sc, s, k):
    lo = loai_of(s) | (BO if s is CUR else set())
    cand = [n for n in sc if n not in s['vang'] and n not in lo]
    return sorted(cand, key=lambda n: (-sc[n], n))[:k]


# ---------- Backtest: tỉ lệ đúng của chính từng tín hiệu ----------
WCHIN, WG610, WDUOI, WLAP = (float(x) for x in os.environ.get('GOIY_W', '1 0.5 0.5 1').split())
WSC = float(os.environ.get('GOIY_SC', '0'))   # lô kép (Loto), Pascal (Power): thử 05/10 — pool không đổi rõ → tắt, chỉ theo dõi trong sổ
WCHM = float(os.environ.get('GOIY_CHM', '1'))   # Mega: +1 số vắng 11–15 (pool 15: 2.12→2.22 ở 50 kỳ)
WTUAN = float(os.environ.get('GOIY_WT', '0.5'))
# Số vắng VX kỳ (anh duyệt 19/10/2026): + điểm WV8 và mỗi vé ≥1 số trong nhóm. Loto 8 kỳ +0.5 · Mega 8 kỳ +1 · Power 12 kỳ chỉ luật vé
# (pool Power đã gộp hạng chuỗi ra/vắng, cộng điểm không đổi pool).
VX = int(os.environ.get('GOIY_VX', {'loto': 8, 'mega': 8, 'power': 12}[A.game]))
WV8 = float(os.environ.get('GOIY_V8', {'loto': 0.5, 'mega': 1, 'power': 0}[A.game]))   # Loto: + điểm nhỏ cho số vắng 8 kỳ (anh 19/10/2026)
SIGS = ('hot', 'ke', 'de', 'kho', 'vang') + (('chuyen', 'phien') if A.game == 'loto' else ()) + (() if A.cu else
        {'power': ('chin', 'g610', 'tuan', 'it100'), 'mega': ('duoi', 'lien2', 'ben', 'lt3', 'zprev', 'thua', 'chin'), 'loto': ('lap', 'tx15', 'vang1', 'nong35', 'thua')}[A.game])
import random
random.seed(5)
MC = [set(random.sample(range(1, NB + 1), KB)) for _ in range(300)]
HALF = KB // 2
# ---- Loto DÃY 6 SỐ (anh, 14/10/2026): tổng, chẵn/lẻ, nhỏ/lớn tính trên 5 số chính + số may mắn đứng cuối (MM 1–12: nhỏ 1–6, lớn 7–12).
# Phần chọn số 1–35 (pool, tín hiệu, Markov) vẫn chỉ dùng 5 số chính.
DAY6 = A.game == 'loto'
LKA = D.get('lk') or []
NDAY = KB + 1 if DAY6 else KB
class D6(frozenset):
    """Tập 5 số chính (giao/hợp như set) kèm số may mắn .mm"""
    def __new__(cls, xs, mm=None):
        o = super().__new__(cls, xs); o.mm = mm; return o
def day6(x): return sorted(x) + ([x.mm] if getattr(x, 'mm', None) else [])
def odd_n(x): return sum(v % 2 for v in day6(x))
def small_n(x): return sum((v <= 6) if i >= KB else (v <= NB // 2) for i, v in enumerate(day6(x)))
def XT(t): return D6(R[t], LKA[t]) if DAY6 else R[t]
if DAY6: MC = [D6(m, random.randint(1, 12)) for m in MC]

def claims(t, rk):
    """Các khẳng định về kỳ t (chỉ dùng dữ liệu trước t). Trả về [(nhãn, tập số hiển thị, hàm kiểm)]."""
    last, p2 = R[t - 1], R[t - 2]
    c20 = {n: sum(n in R[u] for u in range(t - 20, t)) for n in range(1, NB + 1)}
    gp = {}
    for n in range(1, NB + 1):
        g = 0
        while g < t and n not in R[t - 1 - g]: g += 1
        gp[n] = g
    hot10 = set(sorted(c20, key=lambda n: (-c20[n], gp[n], n))[:10])
    v8 = set(range(1, NB + 1)) - set().union(*R[t - VX:t])
    ke = {m for n in last for m in (n - 1, n, n + 1) if 1 <= m <= NB}
    # (15/10/2026) bỏ khẳng định "Pool 10/15/20 có …": chấm bằng pool thô, không phải pool đang hiện — xem bảng pool thật (pool_app.py)
    return [
        ('Có ≥1 số của 2 kỳ gần nhất', last | p2, lambda x: bool(x & (last | p2))),
        ('Có ≥1 số trong 10 số nóng nhất 20 kỳ', hot10, lambda x: bool(x & hot10)),
        ('Có ≥1 số trùng hoặc kề ±1 kỳ trước', ke, lambda x: bool(x & ke)),
        ('Không trùng ≥2 số với kỳ trước', last, lambda x: len(x & last) < 2),
        (f'Chẵn/lẻ cân ({NDAY // 2}±1 số lẻ' + (', dãy 6 số gồm MM)' if DAY6 else ')'), None, lambda x: abs(odd_n(x) - NDAY / 2) <= 1),
        (f'Nhỏ/lớn cân ({NDAY // 2}±1 số ≤{NB // 2}' + ('; MM ≤6)' if DAY6 else ')'), None, lambda x: abs(small_n(x) - NDAY / 2) <= 1),
        (f'Rải ≥{KB - 2} hàng chục', None, lambda x: len({n // 10 for n in x}) >= KB - 2),
    ] + [(f'Có ≥1 số vắng {VX} kỳ (không ra trong {VX} kỳ gần)', v8, lambda x: bool(x & v8))]

def backtest(W=100):
    """Chạy tiến W kỳ: mỗi kỳ ghi số trúng của từng tín hiệu, pool 10/15/20 và từng khẳng định."""
    recs = []
    for t in range(T - W, T):
        f, s = signals(t)
        rk = pool_of(score(f, s), s, 20)
        sig = {k: (len(s[k] & R[t]), len(s[k])) for k in SIGS}
        cl = [(lab, fn(XT(t)), sum(fn(m) for m in MC) / len(MC)) for lab, _, fn in claims(t, rk)]
        recs.append(dict(sig=sig, h={k: len(set(rk[:k]) & R[t]) for k in (7, 8, 9, 10, 12, 15, 18, 20)}, cl=cl, rk=rk, t=t))
    return recs

def summ(recs):
    W = len(recs); out = {}
    for k in SIGS:
        a = sum(r['sig'][k][0] for r in recs); b = sum(r['sig'][k][1] for r in recs)
        if k in ('kho', 'vang'): a = b - a
        out[k] = (a / b * 100 if b else None, b / W)
    hs = [r['h'][A.k] if A.k in (10, 15, 20) else r['h'][15] for r in recs]
    out['pool'] = (sum(hs) / W, sum(h >= 3 for h in hs) / W * 100, hs[-10:])
    out['dist'] = [sum(h >= j for h in hs) / W * 100 for j in range(1, 5)]
    out['tiers'] = {k: [sum(r['h'][k] >= j for r in recs) / W * 100 for j in range(1, 5)] + [sum(r['h'][k] for r in recs) / W] for k in (10, 15, 18, 20)}
    out['claims'] = [(recs[0]['cl'][i][0], sum(r['cl'][i][1] for r in recs) / W * 100, sum(r['cl'][i][2] for r in recs) / W * 100)
                     for i in range(len(recs[0]['cl']))]
    return out


# ---------- Đà tổng ----------
sums = [sum(r) + (LKA[i] if DAY6 else 0) for i, r in enumerate(D['res'])]   # Loto: tổng dãy 6 số
def corr(a, b):
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
    return num / den if den else 0
s50 = sums[-51:]
c50 = corr(s50[:-1], s50[1:])
mid = KB * (NB + 1) / 2
srt = sorted(sums[-100:])   # tối đa 100 kỳ (anh 15/10/2026)
q25, q75 = srt[25], srt[75]
last10 = sums[-10:]; m10 = sum(last10) / 10
sd10 = math.sqrt(sum((x - m10) ** 2 for x in last10) / 9)
# Đà tổng TẮT cả 3 game (anh 15/10/2026, chấm lùi): khoảng theo đà (TB 10 kỳ ± độ lệch) chỉ đúng 60–70%, những kỳ đà bật ở Power
# đúng 11/22; khoảng 50% giữa (q25–q75) đúng 43–60%. Dùng khoảng 80% (10%–90% của 200 kỳ): đúng 81–82% Loto, 81–88% Mega, 74–77% Power.
DA = False
SLO, SHI = srt[10], srt[90]
# Đà kiểu "tổng kỳ sau CÙNG PHÍA mốc giữa với kỳ trước" (ghi chú Power: tương quan ≈ +0.36) — báo riêng, kèm % đúng của chính nó
# ở những kỳ đà bật (200 kỳ, mỗi kỳ chỉ dùng dữ liệu trước nó). Không dùng làm khoảng tổng: cắt nửa khoảng chỉ đúng ~60% (anh 15/10/2026).
DA_INFO = None
if c50 > 0.2:
    _on = [t for t in range(len(sums) - 100, len(sums)) if corr(sums[t - 51:t - 1], sums[t - 50:t]) > 0.2]
    _k = sum((sums[t] <= mid) == (sums[t - 1] <= mid) for t in _on)
    DA_INFO = dict(r=round(c50, 2), last=sums[-1], mid=round(mid), cao=sums[-1] > mid, k=_k, n=len(_on))

# ---------- Hiện tại ----------
f, s = signals(T)
CUR = s
extra = {}
if APP:
    votes = APP['votes']
    top_v = sorted(range(1, NB + 1), key=lambda n: (-votes[n], n))[:12]
    v5 = sorted(votes[1:], reverse=True)[4]
    strong = [n for n in top_v if votes[n] >= v5]            # tâm linh mạnh: phiếu ≥ mức của số thứ 5 (chỉ để hiển thị, cảnh báo, vé cân nhắc)
    by_m = {}
    for name, nums in APP.get('methods', []):
        for n in nums: by_m.setdefault(n, []).append(name)
    b15 = (APP.get('best50') or {}).get('15') or {}
    # Cộng điểm tâm linh vào pool (anh duyệt 14/10/2026, kiemtra_tamlinh.py): bỏ cách cộng chung "top 12 phiếu +1, mạnh +0,5"
    # (không giúp, Loto còn kém đi); thay bằng phương pháp đã chứng minh giúp pool của từng game, +1 cho mỗi số nó chọn.
    # Bỏ luôn "cứu số tâm linh khỏi luật loại" và +0,5 pool app / PP tốt 50 kỳ (chưa từng được chấm, pool đã chấm không có chúng).
    TLDUNG = {'loto': ['Tử vi (Mệnh, Cục, sao Tử Vi)'], 'mega': ['Thần số học', 'Lộn + kép'], 'power': ['Tử vi (Mệnh, Cục, sao Tử Vi)']}[A.game]
    MNUM = {name: nums for name, nums in APP.get('methods', [])}
    for name in TLDUNG:
        for n in MNUM.get(name, []):
            if 1 <= n <= NB: extra[n] = extra.get(n, 0) + 1
    rescued = []
def next_date(last):   # ngày kỳ tới theo lịch quay (Mega T4/T6/CN, Power T3/T5/T7, Loto 13h/21h hằng ngày)
    import datetime as _dt
    d = _dt.datetime.strptime(last[:10], '%d/%m/%Y')
    if A.game == 'loto':
        return f"{last[:10]} 21h" if '13h' in last else f"{(d + _dt.timedelta(days=1)).strftime('%d/%m/%Y')} 13h"
    days = {'mega': (2, 4, 6), 'power': (1, 3, 5)}[A.game]
    d += _dt.timedelta(days=1)
    while d.weekday() not in days: d += _dt.timedelta(days=1)
    return d.strftime('%d/%m/%Y')
# Mega: số = NGÀY ÂM của kỳ quay +1 điểm (pool_ngay.py 14/10/2026: pool 18 ≥3·≥4 tăng ở 20/50/100 kỳ, anh duyệt "tăng là dùng")
NGAYAM = None
if A.game == 'mega':
    import subprocess as _sp
    _nd = (APP['next'] if APP else next_date(D['dates'][-1]))[:10]
    _dd, _mm, _yy = map(int, _nd.split('/'))
    _js = open(os.path.join(HERE, 'lunar.js'), encoding='utf-8').read() + f';console.log(solar2lunar({_dd},{_mm},{_yy}).d)'
    NGAYAM = int(_sp.run(['node', '-e', _js], capture_output=True, text=True, check=True).stdout)
    extra[NGAYAM] = extra.get(NGAYAM, 0) + 1
for n in LINH: extra[n] = extra.get(n, 0) + 3
# Dấu vết ngày "đang chạy" (thứ/ngày/tháng dương-âm về ≥3/10 hoặc ≥4/20 kỳ gần) — anh 14/10/2026.
# Cộng điểm RIÊNG theo cỡ pool cho dấu vết 1 số (chay_test: Mega +0,5 tăng pool 10/18/20 ở cả 100 kỳ cũ và gần; pool 15 giảm → không cộng;
# Loto, Power không tăng → không cộng). Mỗi cỡ pool có thứ hạng riêng (POOLS), app hiện theo cỡ anh chọn.
import dauvet_ngay as _DV
CHAY = _DV.dang_chay(R, D['dates'], T, NB)
CHAYW = {'mega': {10: 0.5, 18: 0.5, 20: 0.5}}.get(A.game, {})
CHAY1 = sorted({ns[0] for _, _, _, ns in CHAY if len(ns) == 1})
def _ex(w):
    e = dict(extra)
    for n in CHAY1: e[n] = e.get(n, 0) + w
    return e
import pool_app as _PA   # pool từng cỡ: MỘT hàm dùng chung với phần chấm lùi (anh 15/10/2026: "rà cách app chọn pool")
POOLS = {K: pool_of(score(f, s, _ex(CHAYW.get(K, 0))), s, min(K, NB - len(s['vang']))) for K in _PA.ks_of(A.game)}
extra = _ex(CHAYW.get(18, 0))   # pool chính = pool 18
# Mega, Power: mỗi cỡ pool một bộ cộng/trừ điểm riêng (pool_chon.py, anh 14/10/2026: "đúng ở 50 & 100 kỳ gần là dùng").
# Thay cho tâm linh chung (TLDUNG) + ngày âm + CHAYW. Linh cảm / loại tay vẫn giữ.
POOLCHON, POOLCHON_THEO = _PA.chon(A.game)
POOLCHON = POOLCHON or None
HANGCAP = _PA.HANGCAP.get(A.game); HANG_ON = []
if POOLCHON:
    CN = _DV.cand_nums(R, D['dates'], T, NB)
    for name, nums in (APP or {}).get('methods', []): CN['TL: ' + name] = {n for n in nums if 1 <= n <= NB}
    _lin = {n: 3.0 for n in LINH}
    def _exK(K):
        e = dict(_lin)
        for nm, w in POOLCHON.get(str(K), []):
            for n in CN.get(nm, ()): e[n] = e.get(n, 0) + w
        return e
    HANG_ON = _PA.hang_on(R, T, NB, A.game)
    POOLS = _PA.make(dict(NB=NB, pool_of=pool_of, score=score, MIXF=MIXF), R, T, f, s, CN, A.game, extra0=_lin, C=POOLCHON)
    extra = _exK(18); NGAYAM = None; CHAYW = {}
    if APP: TLDUNG = sorted({nm[4:] for nm, w in POOLCHON.get('18', []) if nm.startswith('TL: ')})
sc = score(f, s, extra)
pool = pool_of(sc, s, A.k)
hot_out = sorted(s['hot'] - set(pool))
rank = pool_of(sc, s, min(25, NB - len(s['vang'])))
# pool theo CÁCH CŨ (trước 14/10) để chấm song song trong sổ: bỏ gộp 50/50 và luật loại mới của Loto
_so = {k: v for k, v in s.items() if k not in ('_mix', 'vangph20')}
RANK_CU = pool_of(score(f, _so, extra), _so, min(20, NB - len(s['vang'])))
CL_NOW = claims(T, rank)
HOT10 = next(c[1] for c in CL_NOW if c[0].startswith('Có ≥1 số trong 10'))
KE1 = next(c[1] for c in CL_NOW if c[0].startswith('Có ≥1 số trùng'))

# ---------- Số May Mắn Loto: tối đa 3 số, có thứ tự ưu tiên (anh 14/10/2026; tính trước để gắn vào vé) ----------
MM = []
MMRANK = {}
if A.game == 'loto':
    LK = D['lk']
    mg = {k: next((g for g in range(len(LK)) if LK[-1 - g] == k), len(LK)) for k in range(1, 13)}
    # anh 14/10/2026: "tối đa 3 số may mắn và phải có độ ưu tiên". Cách: nóng 10 kỳ trong ±3 quanh MM kỳ trước
    # (somayman_soluong.py: ổn định nhất trong 14 cách ở 3 số, đúng 42/33/32/30% ở 50/100/200/500 kỳ; hòa → số lần ra 50 kỳ).
    # Thứ tự trả về = ưu tiên 1 → 3. Ưu tiên 1 về nhiều nhất ở cả 4 khung (18/17/13/11%); ưu tiên 2 và 3 gần ngang nhau.
    # anh 21/10/2026: thêm "chiều nghiêng" (âm dương) theo MM kỳ trước CÙNG BUỔI m — 21h: m ≤6 → số lớn hơn m, m ≥7 → nhỏ hơn m;
    # 13h: chỉ m ≥7 → nhỏ hơn m (ghi-chu 21/10). Số đúng chiều +1 vào số lần ra 10 kỳ khi xếp. Và chỉ gợi ý 2 số (anh 21/10/2026).
    # mm_chieu.py: 2 số trúng 35/36/27/24% ở 20/50/100/200 kỳ (cách cũ 30/32/25/22%).
    MMK = int(os.environ.get('GOIY_MMK', '2'))
    A_NEXT_LOTO = APP['next'] if APP else next_date(D['dates'][-1])
    DL = D['dates']
    def mm_lean(t):
        nd = DL[t] if t < len(DL) else A_NEXT_LOTO
        g = nd[-3:]; m = next((LK[u] for u in range(t - 1, -1, -1) if DL[u].endswith(g)), None)
        if m is None: return None
        if m >= 7: return lambda k: k < m
        if m <= 6 and g == '21h': return lambda k: k > m
        return None
    def mm_pick(t):
        c10 = {k: sum(LK[u] == k for u in range(max(0, t - 10), t)) for k in range(1, 13)}
        c50 = {k: sum(LK[u] == k for u in range(max(0, t - 50), t)) for k in range(1, 13)}
        ok = [k for k in range(1, 13) if t < 1 or abs(k - LK[t - 1]) <= 3]
        f = mm_lean(t)
        return sorted(ok, key=lambda k: (-c10[k] - (1 if f and f(k) else 0), -c50[k], k))[:MMK]
    MM = mm_pick(len(LK))
    hm = []; MMH = []; hr = []   # chạy lại 100 kỳ: mỗi kỳ chỉ dùng số may mắn các kỳ trước
    for t in range(len(LK) - 100, len(LK)):
        pk = mm_pick(t)
        hm.append(LK[t] in pk); hr.append(pk.index(LK[t]) if LK[t] in pk else -1)
        MMH.append(dict(d=D['dates'][t], goi=list(pk), ra=LK[t], dung=LK[t] in pk))
    MMRATE = {W: round(sum(hm[-W:]) / W * 100) for W in (10, 20, 50, 100)}
    MMRANK = {W: [round(sum(r == i for r in hr[-W:]) / W * 100) for i in range(len(MM))] for W in (50, 100)}
# chia số may mắn cho vé theo ưu tiên: 7 vé → ưu tiên 1 ×3, ưu tiên 2 ×2, ưu tiên 3 ×2 (lặp lại nếu nhiều vé hơn)
MM_PRI = (0, 1, 0, 2, 0, 1, 2)
def mm_for(i):
    if not MM: return None
    return MM[MM_PRI[i % len(MM_PRI)]] if len(MM) == 3 else MM[i % len(MM)]
CUR_MM = None   # số may mắn của vé đang dựng (Loto dãy 6 số)
TMM = []        # số may mắn từng vé

# ---------- Vé: lõi + vệ tinh ----------
NL = 2 if KB == 5 else 3
core = []
for n in pool:   # Mega: lõi không chứa ≥2 số của kỳ trước (khẳng định "không trùng ≥2 số" đúng 88%)
    if len(core) < NL and not (A.game == 'mega' and not A.cu and n in R[-1] and len(set(core) & R[-1]) >= 1):
        core.append(n)
sat = [n for n in pool if n not in core]

RELAX = ['đủ ràng buộc', 'bỏ điều kiện ≥2 số >31', 'mượn số ngoài pool (điểm cao kế tiếp)']
EXT = [n for n in sorted(sc, key=lambda n: (-sc[n], n)) if n not in s['vang'] and n not in loai_of(s) and n not in BO and n not in pool][:10]

def ok(tk, lv):
    tk = sorted(tk)
    if not SLO <= sum(tk) + (CUR_MM or 0) <= SHI: return False
    if lv == 0 and A.game != 'loto' and sum(x > 31 for x in tk) < 2: return False
    if not A.cu and bad_ticket(tk): return False
    return not any(tk[i] + 2 == tk[i + 1] + 1 == tk[i + 2] for i in range(len(tk) - 2))

def bad_ticket(tk):
    """Luật loại vé — kỳ thật hiếm khi vi phạm (1–8%, ổn định 3 khúc)."""
    d6 = D6(tk, CUR_MM) if DAY6 else set(tk)
    odd = odd_n(d6); low = small_n(d6)
    dec = {}
    for x in tk: dec[x // 10] = dec.get(x // 10, 0) + 1
    x = set(tk)
    if (len(x & R[-1]) >= 3 or odd in (0, NDAY) or low in (0, NDAY)
            or (KB == 6 and max(dec.values()) >= 4) or max(tk) < NB * 2 // 3):
        return True
    if A.game == 'power' and len(dec) < 4: return True          # rải ≥4 hàng chục: 78–80% kỳ thật, giữ 75% vé
    if A.game == 'mega':                                          # khẳng định Mega có dấu vết (khang_dinh.py)
        if not x & (R[-1] | R[-2]) or not x & HOT10: return True
        if not x & KE1 or len(x & R[-1]) >= 2 or abs(odd - 3) > 1 or abs(low - 3) > 1 or len(dec) < 4: return True
    return False

def pick(base, cands, need, used):
    for lv in range(3):
        cs = cands + EXT if lv == 2 else cands
        best = None
        for c in combinations(cs, need):
            tk = sorted(base + list(c))
            if tk in DONE or not ok(tk, lv): continue
            v = (sum(sc[n] for n in c) - 2 * sum(used.get(n, 0) for n in c), [-n for n in c])
            if best is None or v > best[0]: best = (v, tk)
        if best: return best[1], lv
    c = sorted(cands, key=lambda n: (used.get(n, 0), -sc[n]))[:need]
    return sorted(base + c), 3

tickets, used, DONE = [], {}, []
# Anh 14/10/2026: rải vé thì KHÔNG có lõi — 6 vé đầu của bảng bao phủ "3 nếu 4" trên pool 18 (ve_test.py: Mega 50/100 kỳ
# có vé ≥3: 22%/19%, ≥4: 6%/3% so với kiểu lõi 16%/16%, 2%/1%; Loto, Power cũng ngang hoặc hơn ở 100 kỳ).
RAIVE = not A.cu
if RAIVE:
    from bao_phu import bao_phu as _bp
    _P18 = (POOLS.get(18) if 'POOLS' in globals() else None) or rank[:18]
    core = []
    for w in _bp(len(_P18), KB, 3, 4)[:6]:
        CUR_MM = mm_for(len(tickets)) if DAY6 and MM else None
        tk = sorted(_P18[i] for i in w); tickets.append(('rải đều pool 18', tk, 0)); DONE.append(tk); TMM.append(CUR_MM)
# Chẵn–lẻ vé rải (anh 14/10/2026: dấu vết "3C-3L hiếm khi ra 3 kỳ liền" mà vé vẫn 3-3): đổi 1 số trong vé (lấy số pool 18 khác chẵn/lẻ,
# hạng cao nhất) để tránh kiểu chẵn–lẻ đang khó ra. ve_cl.py: mọi game tránh 3-3 khi 2 kỳ liền 3-3 (không mất gì);
# Power tránh luôn kiểu chẵn–lẻ kỳ trước (tăng nhẹ vé ≥3). Loto tính dãy 6 số.
CL_TRANH = set()
VELUAT = None   # bộ luật dạng của vé (xuất cho app tự bốc vé từ pool của anh, 16/10/2026)
if RAIVE:
    _ev = lambda x, mm: sum(v % 2 == 0 for v in x) + ((mm % 2 == 0) if mm else 0)
    # Đối chiếu dữ liệu (anh 14/10/2026: "app phải đối chiếu dữ liệu, mấy suy luận đó hiển nhiên"): mỗi vé phải vừa
    # khuôn dạng kỳ tới (khuon.py) + luật liên hệ kỳ trước đang hiệu lực (lienhe_dang.py) + chẵn–lẻ ở trên.
    # Vé trái → đổi ít số nhất (1 rồi 2 số) bằng số trong pool 18 (thiếu thì pool 25), ưu tiên số hạng cao.
    import khuon as _KH, lienhe_dang as _LH
    # MỌI luật lọc vé dựng ở luat_ve.py (khuôn + kép + nhịp tổng + giới hạn tổng + liên hệ + chuỗi + chẵn–lẻ) — cùng một hàm với phần
    # chấm lùi cả bộ (anh 15/10/2026: "kiểm tra lại hết các luật").
    import luat_ve as _LV
    _BV = _LV.build(R, LKA if DAY6 else None, NB, KB, T, A.game)
    KHUON = dict(_BV['khuon']); KHUON['rules'] = _BV['rules']; KHUON['lienhe'] = _BV['lienhe']
    CL_TRANH = _BV['cl']
    _lvj = os.path.join(HERE, 'luat_ve.json')   # % lọt THẬT của cả bộ khi áp tiến (luat_ve.py), thay cho % tự chấm trong mẫu của khuon.build
    if os.path.exists(_lvj):
        _lv = json.load(open(_lvj, encoding='utf-8')).get(A.game) or {}
        if _lv: KHUON['pass50'], KHUON['pass100'], KHUON['tien'] = _lv['pass50'], _lv['pass100'], True
        if _lv: KHUON['pass10'] = _lv.get('pass10')
        if _lv: KHUON['tien'], KHUON['tien10'] = _lv.get('tien'), _lv.get('tien10')   # % lọt CHẤM TIẾN (chọn bằng kỳ trước, thử kỳ sau)
    _SPECS = _BV['specs']
    _prev = sorted(R[-1])
    _V8 = (set(range(1, NB + 1)) - set().union(*R[T - VX:T])) if not A.cu else set()   # mỗi vé ≥1 số vắng VX kỳ (anh 19/10/2026)
    def _okv(x, mm): return _ev(x, mm) not in CL_TRANH and all(_KH.check(sp, x, mm, _prev, NB, KB) for sp in _SPECS) and (not _V8 or bool(set(x) & _V8))
    VELUAT = dict(specs=_SPECS, cl=sorted(CL_TRANH), prev=_prev)
    _CAND = list(_P18) + [n for n in (POOLS.get(25) or rank) if n not in _P18]
    from itertools import combinations as _cb
    _POS = lambda c: _CAND.index(c) if c in _CAND else len(_CAND)   # số ngoài danh sách (vd tâm linh ngoài pool) xếp cuối
    def _fixve(_tk, _mm, protect=()):
        """đổi ít số nhất (1→3) để vé vừa mọi luật dạng; giữ nguyên số trong protect. Trả (vé mới, số số đã đổi) hoặc (vé cũ, 0)."""
        if _okv(_tk, _mm): return _tk, 0
        _best = None
        for _m in (1, 2, 3):
            for _out in _cb([v for v in _tk if v not in protect], _m):
                _keep = [v for v in _tk if v not in _out]
                for _inn in _cb([c for c in _CAND[:22] if c not in _tk], _m):
                    _x = sorted(_keep + list(_inn))
                    if _x in DONE or not _okv(_x, _mm): continue
                    # số đã có ở ≥3 vé khác thì tránh (anh 15/10/2026: "đã rải vé thì không có lõi") — chỉ khi còn cách khác
                    _v = (-sum(_USE[c] >= 3 for c in _inn), -sum(_POS(c) for c in _inn), sum(_POS(c) for c in _out))
                    if _best is None or _v > _best[0]: _best = (_v, _x)
            if _best: return _best[1], _m
        return _tk, 0
    from collections import Counter as _Cn
    _USE = _Cn(v for _t in tickets for v in _t[1])   # số lần mỗi số có mặt trong 7 vé hiện tại (vé đang xét tính cả vé chưa đổi)
    for _j, (_kd, _tk, _lv) in enumerate(tickets):
        _USE.subtract(_tk)
        _x, _m = _fixve(_tk, TMM[_j] if _j < len(TMM) else None)
        if _m: tickets[_j] = (_kd + f' (đối chiếu dạng: đổi {_m} số)', _x, _lv); DONE[_j] = _x
        _USE.update(tickets[_j][1])
for i in range(0 if RAIVE else 3):
    CUR_MM = mm_for(len(tickets)) if DAY6 and MM else None
    tk, lv = pick(core, sat, KB - NL, used); tickets.append(('lõi+vệ tinh', tk, lv)); DONE.append(tk); TMM.append(CUR_MM)
    for n in tk: used[n] = used.get(n, 0) + 1
for i in range(0 if RAIVE else 2):   # 2 vé trải: 1 số lõi + phần pool ít dùng
    CUR_MM = mm_for(len(tickets)) if DAY6 and MM else None
    tk, lv = pick([core[i]], [n for n in pool if n not in core], KB - 1, used); tickets.append(('trải', tk, lv)); DONE.append(tk); TMM.append(CUR_MM)
    for n in tk: used[n] = used.get(n, 0) + 1

# ---------- In ----------
fm = lambda xs: ' '.join(f'{n:02d}' for n in sorted(xs)) or '—'
nd = APP['next'] if APP else next_date(D['dates'][-1])
print(f'## Gợi ý {NAME} — kỳ {nd}\n')
print(f'Kỳ gần nhất {D["dates"][-1]}: **{fm(R[-1])}** (tổng {sums[-1]})\n')
print('### Tín hiệu dấu vết (cùng một cách tính mọi kỳ)\n')
RECS = backtest(100)   # tối đa 100 kỳ
if os.environ.get('GOIY_RKDUMP'):   # nghiên cứu pool 12/15 (anh 21/10/2026): xuất thứ hạng app (top 20) từng kỳ, chấm lùi
    json.dump({D['dates'][r['t']]: r['rk'] for r in backtest(int(os.environ.get('GOIY_RKW', '200')))}, open(os.environ['GOIY_RKDUMP'], 'w'))
B = {W: summ(RECS[-W:]) for W in (10, 50, 100)}
if os.environ.get('GOIY_BAO'):   # bao k số theo thứ hạng pool (anh 19/10/2026): mỗi kỳ chấm lại, kỳ có ≥3 / ≥4 / đủ KB số trong k số đầu
    from math import comb as _cmb
    for _k in (6, 7, 8, 9, 10, 12):
        for _W in (50, 100):
            _m = [len(set(r['rk'][:_k]) & R[r['t']]) for r in RECS[-_W:]]
            print(f'BAO {_k} ({_cmb(_k, KB)} vé) {_W} kỳ: TB {sum(_m) / _W:.2f} | ≥3 {sum(x >= 3 for x in _m)} ≥4 {sum(x >= 4 for x in _m)} ={KB} {sum(x >= KB for x in _m)}')
pc = lambda v: '—' if v is None else f'{v:.0f}%'
rows = [('hot', 'Nóng (c10≥3 hoặc c20≥2×kỳ vọng)', 'tỉ lệ ra/số'),
        ('ke', 'Kề ±1 kỳ trước', 'tỉ lệ ra/số'),
        ('de', 'Bóng dễ ra (z100>1)', 'tỉ lệ ra/số'),
        ('kho', 'Bóng khó ra (z100<−1.5)', 'loại đúng'),
        ('vang', f'Vắng ≥{G} kỳ (bỏ khỏi pool)', 'loại đúng')]
if A.game == 'loto':
    rows += [('chuyen', 'Chuyển kỳ (số hay theo sau số kỳ trước), top 8', 'tỉ lệ ra/số'),
             ('phien', 'Nóng cùng phiên 100 kỳ, top 8', 'tỉ lệ ra/số')]
rows += [x for x in (('chin', 'Vắng 11–15 kỳ — "chín" (+điểm)', 'tỉ lệ ra/số'), ('g610', 'Vắng 6–10 kỳ (−điểm)', 'loại đúng'),
                     ('duoi', 'Cùng đuôi số kỳ trước (−điểm)', 'loại đúng'), ('lap', 'Số vừa ra kỳ trước (−điểm)', 'loại đúng'), ('tuan', 'Số kỳ cùng thứ tuần trước (−điểm)', 'loại đúng'), ('lien2', 'Ra 2 kỳ liền (bỏ khỏi pool)', 'loại đúng'), ('lt3', 'Ra kỳ trước & kỳ t−3 (bỏ)', 'loại đúng'), ('zprev', 'Số lớn nhất kỳ trước (bỏ)', 'loại đúng'),
                     ('it100', 'Ra ít nhất 100 kỳ (bỏ)', 'loại đúng'), ('tx15', 'Tái xuất sau vắng ≥15 (bỏ)', 'loại đúng'), ('vang1', 'Vắng lâu nhất (bỏ)', 'loại đúng'), ('nong35', 'Ra 3 lần/5 kỳ (bỏ)', 'loại đúng'), ('ben', 'Ra nhiều cả 4 đoạn 25 kỳ (+điểm)', 'tỉ lệ ra/số'), ('thua', 'Lâu lâu mới ra (200 kỳ ≤85% kỳ vọng) & vắng ≥15 (bỏ)', 'loại đúng')) if x[0] in SIGS]
print('| Tín hiệu | Số hiện tại | Đo bằng | 10 kỳ | 50 kỳ | 100 kỳ |\n|---|---|---|---|---|---|')
for k, lab, how in rows:
    print(f'| {lab} | {fm(s[k])} | {how} | ' + ' | '.join(pc(B[W][k][0]) for W in (10, 50, 100)) + ' |')
print(f'\nĐà tổng: tương quan tổng kỳ liền nhau 50 kỳ = **{c50:+.2f}** '
      + (f'→ có đà, TB 10 kỳ {m10:.0f} (giữa {mid:.0f}), khoảng tổng nên chọn **{SLO}–{SHI}**.' if DA
         else f'→ khoảng tổng cho vé: 80% của 200 kỳ **{SLO}–{SHI}**.'))
if DA_INFO:
    print(f"Đà đang bật: tổng kỳ trước {DA_INFO['last']} ({'cao' if DA_INFO['cao'] else 'thấp'} so mốc giữa {DA_INFO['mid']}) → kỳ tới nghiêng tổng "
          f"**{'>' + str(DA_INFO['mid']) if DA_INFO['cao'] else '≤' + str(DA_INFO['mid'])}**. Những kỳ đà bật trong 200 kỳ: cùng phía {DA_INFO['k']}/{DA_INFO['n']} = {DA_INFO['k'] * 100 // max(DA_INFO['n'], 1)}%.")
if APP:
    print(f'\nPhiếu tâm linh top 12: {fm(top_v)}  ·  Pool app ({APP.get("appMethod")}): {fm(APP.get("appPool", []))}'
          f'  ·  PP tốt nhất 50 kỳ (K15): {b15.get("id")} TB {b15.get("tb")} → {fm(b15.get("pool", []))}')
if LINH: print(f'\nSố linh cảm của anh: **{fm(LINH)}** (+3 điểm)')
if BO: print(f'\nSố anh loại tay kỳ này: **{fm(BO)}**')
print(f'\n### Pool {A.k} điểm đồng thuận\n\n**{fm(pool)}**\n')
print(f"Pool 10: **{fm(rank[:10])}**  ·  Pool 20: {fm(rank[:20])}\n")
def why(n):
    t = [lab for k, lab in (('hot', 'nóng'), ('ke', 'kề'), ('de', 'dễ ra'), ('kho', 'khó ra'), ('chuyen', 'chuyển kỳ'), ('phien', 'nóng phiên'), ('chin', 'vắng 11–15'), ('g610', 'vắng 6–10 −'), ('duoi', 'cùng đuôi −'), ('lap', 'vừa ra −'), ('tuan', 'cùng thứ tuần trước −'), ('lien2', 'ra 2 kỳ liền (loại)'), ('lt3', 'ra kỳ trước & t−3 (loại)'), ('zprev', 'z kỳ trước (loại)'), ('it100', 'ít nhất 100 kỳ (loại)'), ('tx15', 'tái xuất (loại)'), ('vang1', 'vắng lâu nhất (loại)'), ('nong35', '3 lần/5 kỳ (loại)'), ('ben', 'ra đều 4 đoạn'), ('thua', 'thưa & vắng ≥15 (loại)')) if n in s.get(k, ())]
    if s.get('_mk'): t.insert(0, f"Markov bậc 2 hạng {round((1 - s['_mk'][n]) * (NB - 1)) + 1}")
    if APP:
        if n in top_v: t.append(f'tâm linh {votes[n]} phiếu')
        for name in TLDUNG:
            if n in MNUM.get(name, []): t.append(f'{name.split(" (")[0]} +1')
    if n in LINH: t.append('linh cảm')
    return ', '.join(t) or '—'
print('| # | Số | Điểm | Cơ sở | c10/c20 | Vắng |\n|---|---|---|---|---|---|')
for i, n in enumerate(rank, 1):
    print(f"| {i}{' ●' if i <= A.k else ''} | **{n:02d}** | {sc[n]:.1f} | {why(n)} | {f[n]['c10']}/{f[n]['c20']} | {f[n]['gap']} |")
if hot_out: print(f'\n⚠️ Số nóng nằm ngoài pool: {fm(hot_out)}')
if APP:
    print(f'\n### Tâm linh — {len(APP.get("methods", []))} quẻ bỏ phiếu\n')
    print('| Số | Phiếu | Quẻ chọn (vài quẻ) | Trạng thái |\n|---|---|---|---|')
    def state(n):
        if n in pool: return f'trong pool #{pool.index(n) + 1}'
        why_out = [lab for k, lab in (('kho', 'khó ra'), ('g610', 'vắng 6–10'), ('duoi', 'cùng đuôi kỳ trước'), ('lap', 'vừa ra kỳ trước')) if n in s.get(k, ())]
        if n in s['vang']: why_out.append(f"bị loại: vắng {f[n]['gap']} kỳ")
        return '**ngoài pool**' + (f" ({', '.join(why_out)})" if why_out else ' (điểm dấu vết thấp)') + (f' · hạng {rank.index(n) + 1}' if n in rank else '')
    for n in top_v:
        tag = ' ★' if n in strong else ''
        res = ' · *đã cứu khỏi luật vắng*' if n in rescued else ''
        print(f"| **{n:02d}**{tag} | {votes[n]} | {', '.join(by_m.get(n, [])[:3])}{'…' if len(by_m.get(n, [])) > 3 else ''} | {state(n)}{res} |")
    day = sorted(sorted(range(1, NB + 1), key=lambda n: (-votes[n], n))[:KB])
    print(f'\nDãy tâm linh (top {KB} phiếu): **{fm(day)}**  ·  ★ = tâm linh mạnh (phiếu ≥ {v5}) · cộng điểm pool chỉ từ: {", ".join(TLDUNG)}')
    strong_out = [n for n in strong if n not in set(POOLS.get(18) or rank[:18])]   # đối chiếu với pool 18 (pool chính)
    if strong_out:
        print(f'\n⚠️ **Tâm linh mạnh nằm ngoài pool: {fm(strong_out)}** — cần cân nhắc (xem vé thay thế bên dưới).')
for W in (10, 50, 100):
    tb, p3, last = B[W]['pool']
    print(f'\nPool {A.k} (không tâm linh/app) chính nó ở {W} kỳ: TB **{tb:.2f}** số/kỳ, ≥3 số {p3:.0f}%' + (f' · 10 kỳ gần: {last}' if W == 10 else '')
          + ('' if W == 10 else ' · kỳ có ≥1/≥2/≥3/≥4 số: ' + ' / '.join(f'{v:.0f}%' for v in B[W]['dist'])))
# ---------- Bảng số vắng lâu (≥15 kỳ) — để anh tự nhận định ----------
def gaps_all(n):
    h = [u for u in range(T) if n in R[u]]
    return [b - a - 1 for a, b in zip(h, h[1:])]
GA = {n: gaps_all(n) for n in range(1, NB + 1)}
def hz(gl, g):   # trong các lần nghỉ đã kéo tới ≥g kỳ, bao nhiêu % ra ngay ở kỳ kế (nghỉ đúng g)
    reach = [x for x in gl if x >= g]
    return (sum(x == g for x in reach) / len(reach) * 100 if reach else None), len(reach)
POOLG = [x for n in GA for x in GA[n]]
VL = []
for n in sorted(range(1, NB + 1), key=lambda n: -f[n]['gap']):
    g = f[n]['gap']
    if g < 15: continue
    c100 = sum(n in R[u] for u in range(T - 50, T)); c200 = sum(n in R[u] for u in range(T - WB, T))   # cột 50 / 100 kỳ
    gl = GA[n]; po, pn = hz(gl, g); pa, _ = hz(POOLG, g)
    long15 = sum(x >= 15 for x in gl) / max(len(gl), 1) * 100
    thua = c200 / (WB * P) * 100
    tl_n = votes[n] if APP else 0
    if n in s['vang'] or n in s.get('thua', set()) or n in s.get('vang1', set()): verdict = 'Loại'
    elif n in (rescued if APP else []): verdict = 'Cân nhắc (tâm linh mạnh)'
    elif thua <= 85 or g >= 20: verdict = 'Nghiêng loại'
    else: verdict = 'Theo dõi'
    VL.append(dict(n=n, gap=g, c100=c100, c200=c200, thua=round(thua), long15=round(long15), maxg=max(gl) if gl else None,
                   po=None if po is None else round(po), pn=pn, pa=None if pa is None else round(pa, 1), tl=tl_n, verdict=verdict))
if CHAY:
    print('\n### Dấu vết ngày đang chạy (về ≥3/10 hoặc ≥4/20 kỳ gần) — anh tự cân nhắc\n\n| Dấu vết | Về 10 kỳ | Về 20 kỳ | Số kỳ này | Trong pool 18 |\n|---|---|---|---|---|')
    for a, b, c, d in CHAY: print(f"| {a} | {b} | {c} | {fm(d)} | {fm([n for n in d if n in rank[:18]])} |")
if VL:
    print(f'\n### Số vắng lâu (≥15 kỳ) — bảng để anh tự nhận định\n')
    print('| Số | Đang vắng | Ra 100 / {} kỳ (kỳ vọng {:.0f} / {:.0f}) | Mức ra {} kỳ | % lần nghỉ ≥15 kỳ (lịch sử) | Nghỉ dài nhất | Khi đã vắng tới mức này: ra ngay kỳ kế (của chính số / mọi số) | Tâm linh | Nhận định |'.format(WB, 100 * P, WB * P, WB))
    print('|---|---|---|---|---|---|---|---|---|')
    for v in VL:
        print(f"| **{v['n']:02d}** | {v['gap']} | {v['c100']} / {v['c200']} | {v['thua']}% | {v['long15']}% | {v['maxg']} | {'—' if v['po'] is None else str(v['po']) + '%'} ({v['pn']} lần) / {v['pa']}% | {v['tl']} phiếu | **{v['verdict']}** |")

# ---------- Bảng số ra nhiều gần đây (10/20 kỳ) — có thể liên quan trọng lượng bi ----------
NONG = []
e10, e20 = 10 * P, 20 * P
for n in range(1, NB + 1):
    c10 = f[n]['c10']; c20 = f[n]['c20']
    if not (c10 >= 3 or c20 >= max(5, round(2 * e20))): continue
    c100 = sum(n in R[u] for u in range(T - 50, T)); c200 = sum(n in R[u] for u in range(T - WB, T))   # cột 50 / 100 kỳ
    q4 = [sum(n in R[u] for u in range(T - 100 + 25 * i, T - 75 + 25 * i)) for i in range(4)]
    # lịch sử của chính số: những lần nó ra ≥c10 lần trong 10 kỳ thì kỳ kế ra bao nhiêu %
    seen = hit = 0
    for t in range(max(10, T - 300), T):
        if sum(n in R[u] for u in range(t - 10, t)) >= min(c10, 3): seen += 1; hit += n in R[t]
    lr = c200 / (WB * P) * 100
    if lr >= 115 and sum(x > 25 * P for x in q4) >= 3: kind = 'Nóng bền — có thể bi dễ ra (nặng/nhẹ lệch)'
    elif lr >= 100: kind = 'Nóng, đường dài cũng ra nhiều'
    elif lr >= 85: kind = 'Nóng ngắn hạn (đường dài bình thường)'
    else: kind = 'Đang hồi sau thời gian ra ít'
    if A.game == 'loto': kind = kind.replace(' — có thể bi dễ ra (nặng/nhẹ lệch)', ' (máy tính: không phải bi)')
    NONG.append(dict(n=n, c10=c10, c20=c20, c100=c100, c200=c200, lr=round(lr), q4=q4, gap=f[n]['gap'],
                     nx=None if not seen else round(hit / seen * 100), ns=seen, kind=kind,
                     state='bị loại' if n in (s['vang'] | loai_of(s) | BO) else (f'pool #{rank.index(n) + 1}' if n in rank else 'ngoài pool 20')))
NONG.sort(key=lambda v: (-v['c10'], -v['c20']))
if NONG:
    print(f'\n### Số ra nhiều gần đây (10/20 kỳ) — kỳ vọng {e10:.1f} / {e20:.1f} lần\n')
    print(f'| Số | Ra 10 kỳ | Ra 20 kỳ | Ra 100 / {WB} kỳ | Mức ra {WB} kỳ | 4 đoạn 25 kỳ | Đang vắng | Khi nóng thế này, kỳ kế ra (lịch sử của số) | Trạng thái | Nhận xét |')
    print('|---|---|---|---|---|---|---|---|---|---|')
    for v in NONG:
        print(f"| **{v['n']:02d}** | {v['c10']} | {v['c20']} | {v['c100']} / {v['c200']} | {v['lr']}% | {'/'.join(map(str, v['q4']))} | {v['gap']} | {'—' if v['nx'] is None else str(v['nx']) + '%'} ({v['ns']} lần) | {v['state']} | {v['kind']} |")

# ---------- Nhịp pool (Loto): 5 kỳ gần pool 15 trúng TB ≥ ngưỡng 1/3 tốt nhất → kỳ tới pool hay trúng hơn (400 kỳ: TB 2.40 vs 1.9–2.2, ≥3 số 51% vs 32%)
NHIP = None
if A.game == 'loto':
    hh = [r['h'][15] for r in RECS]; m5 = sum(hh[-5:]) / 5
    ths = sorted(sum(hh[i - 5:i]) / 5 for i in range(5, len(hh))); thr = ths[2 * len(ths) // 3]
    NHIP = dict(m5=round(m5, 2), thr=round(thr, 2), last=hh[-5:], good=m5 >= thr)
    # pool trúng theo phiên 13h / 21h (anh hỏi nên chơi phiên nào, 05/10)
    ss = SES[T - len(RECS):T]; PH = {}
    for ph in ('13', '21'):
        for W in (50, 100):
            ix = [i for i in range(len(RECS)) if ss[i] == ph][-W // 2:]
            PH[f'{ph}_{W}'] = {k: round(sum(RECS[i]['h'][k] for i in ix) / max(len(ix), 1), 2) for k in (10, 15)}
            PH[f'{ph}_{W}']['n'] = len(ix)
    NHIP['phien'] = PH
    print('**Pool trúng theo phiên** (TB số trúng/kỳ, pool 10 · pool 15): ' + ' · '.join(
        f"{ph}h {W // 2} kỳ gần: {PH[f'{ph}_{W}'][10]} · {PH[f'{ph}_{W}'][15]}" for ph in ('13', '21') for W in (50, 100)))
    print(f"\n**Nhịp pool:** 5 kỳ gần pool 15 trúng {hh[-5:]} → TB {m5:.2f} (ngưỡng nhóm tốt {thr:.2f}) → " + ("**ĐANG VÀO NHỊP — kỳ nên đánh mạnh**" if m5 >= thr else "nhịp thường — đánh nhẹ"))

# ---------- Khẳng định kỳ này (đúng ≥70% ở 200 kỳ) ----------
CLR = []
for (lab, st, fn), (lab2, r200, k200), (_, r50, _) in zip(CL_NOW, B[100]['claims'], B[50]['claims']):
    CLR.append(dict(lab=lab, nums=sorted(st) if st else [], r200=r200, r50=r50, keep=k200, trace=r200 - k200 >= 3))
print('\n### Khẳng định kỳ này (đúng ≥70% số kỳ trong 100 kỳ)\n')
print('| Khẳng định | Số liên quan | Đúng 100 kỳ | 50 kỳ gần | Vé giữ lại | Dấu vết |\n|---|---|---|---|---|---|')
for c in sorted(CLR, key=lambda c: -c['r200']):
    if c['r200'] < 70: continue
    print(f"| {c['lab']} | {fm(c['nums']) if c['nums'] and len(c['nums']) <= 20 else '—'} | **{c['r200']:.0f}%** | {c['r50']:.0f}% | {c['keep']:.0f}% | {'✔ đúng > giữ' if c['trace'] else ''} |")
if APP and strong_out:   # vé thay thế: vé 1, đổi số điểm thấp nhất (không phải lõi) bằng tâm linh mạnh ngoài pool
    alt = list(tickets[0][1])
    for n in sorted(strong_out, key=lambda n: -votes[n])[:2]:
        low = min((x for x in alt if x not in core and x not in strong_out), key=lambda x: sc[x], default=None)
        if low is None: break
        alt[alt.index(low)] = n
    alt = sorted(alt)
    _lab = 'cân nhắc tâm linh (thay thế vé 1)'
    if RAIVE:   # đối chiếu dạng cả vé tâm linh, giữ nguyên số tâm linh mạnh; không vừa được thì chỉ giữ 1 số mạnh nhất (anh 15/10/2026)
        _mm0 = TMM[0] if TMM else None; _so = [n for n in sorted(strong_out, key=lambda n: -votes[n]) if n in alt]
        _x, _m = _fixve(alt, _mm0, protect=set(_so))
        if not _okv(_x, _mm0) and len(_so) > 1: _x, _m = _fixve(alt, _mm0, protect=set(_so[:1]))
        alt = _x
        if not _okv(alt, _mm0): _lab += ' — LỆCH KHUÔN, chưa có cách vừa'
    tickets.append((_lab, sorted(alt), 0)); TMM.append(TMM[0] if TMM else None)
# Vé theo TỪNG cỡ pool (anh 16/10/2026: "chọn pool 15, 12 thì đưa ra vé theo pool đó"): rải bao phủ trên pool K, đổi ít số nhất cho
# vừa bộ luật vé, vé thay thế tâm linh khi số tâm linh mạnh nằm ngoài pool K. Pool 18 giữ đúng bộ vé chính (lưu sổ, chấm theo dõi).
TICKETS_K = {}
if RAIVE and 'POOLS' in globals() and POOLS:
    from collections import Counter as _Cn2
    def _fix2(tk, mm, cand, done, use, protect=()):
        if _okv(tk, mm): return tk, 0
        pos = lambda c: cand.index(c) if c in cand else len(cand)
        best = None
        for m in (1, 2, 3):
            for out in _cb([v for v in tk if v not in protect], m):
                keep = [v for v in tk if v not in out]
                for inn in _cb([c for c in cand[:22] if c not in tk], m):
                    x = sorted(keep + list(inn))
                    if x in done or not _okv(x, mm): continue
                    v = (-sum(use[c] >= 3 for c in inn), -sum(pos(c) for c in inn), sum(pos(c) for c in out))
                    if best is None or v > best[0]: best = (v, x)
            if best: return best[1], m
        return tk, 0
    def gen_ve(K):
        P = POOLS[K]; cand = list(P) + [n for n in (POOLS.get(25) or rank) if n not in P]
        tks, mms = [], []
        for w in _bp(len(P), KB, 3, 4)[:6]:
            mms.append(mm_for(len(tks)) if DAY6 and MM else None); tks.append([f'rải đều pool {K}', sorted(P[i] for i in w)])
        done = [t[1] for t in tks]; use = _Cn2(v for t in tks for v in t[1])
        for j in range(len(tks)):
            use.subtract(tks[j][1]); x, m = _fix2(tks[j][1], mms[j], cand, done, use)
            if m: tks[j] = [tks[j][0] + f' (đối chiếu dạng: đổi {m} số)', x]; done[j] = x
            use.update(tks[j][1])
        so = [n for n in sorted(strong, key=lambda n: -votes[n]) if n not in set(P)] if APP else []
        if so and tks:
            alt = list(tks[0][1])
            for n in so[:2]:
                low = min((x for x in alt if x not in strong), key=lambda x: sc[x], default=None)
                if low is None: break
                alt[alt.index(low)] = n
            alt = sorted(alt); x, _ = _fix2(alt, mms[0], cand, done, use, protect=set(so[:2]))
            if not _okv(x, mms[0]):
                x2, _ = _fix2(alt, mms[0], cand, done, use, protect=set(so[:1])); x = x2 if _okv(x2, mms[0]) else x
            tks.append(['cân nhắc tâm linh (thay thế vé 1)' + ('' if _okv(x, mms[0]) else ' — LỆCH KHUÔN, chưa có cách vừa'), sorted(x)]); mms.append(mms[0])
        return [dict(kind=k, x=x, lv=0, sum=sum(x) + (mm or 0), lk=mm) for (k, x), mm in zip(tks, mms)]
    for K in POOLS:
        if K != 18 and K <= 25: TICKETS_K[str(K)] = gen_ve(K)   # 30, 35 chỉ để xem tỉ lệ trúng, không dựng vé
print(f'\n### {len(tickets)} vé ' + ('(rải đều pool 18, không lõi)' if RAIVE else f'(lõi {fm(core)} + vệ tinh)') + '\n')
for i, (kind, tk, lv) in enumerate(tickets, 1):
    note = RELAX[lv] if lv < 3 else 'không vé nào hợp lệ, lấy theo điểm'
    out = [n for n in tk if n not in pool]
    mm = TMM[i - 1] if i - 1 < len(TMM) else None
    print(f'{i}. **{fm(tk)}**' + (f' + MM **{mm:02d}**' if mm else '') + f' — {kind}, tổng {sum(tk) + (mm or 0)}' + ('' if lv == 0 else f' _({note}' + (f': {fm(out)}' if out else '') + ')_'))

# Số May Mắn Loto (đã tính ở trên)
if A.game == 'loto':
    print(f'\n### Số May Mắn ({len(MM)} số, theo thứ tự ưu tiên — nóng 10 kỳ trong ±3 quanh số kỳ trước, cộng chiều nghiêng cùng buổi)\n\n'
          + ' · '.join(f'ưu tiên {i + 1}: **{k:02d}** (vắng {mg[k]} kỳ, về {MMRANK[50][i]}% / {MMRANK[100][i]}% ở 50/100 kỳ)' for i, k in enumerate(MM))
          + f'\n\nCả {len(MM)} số: chính cách này trúng {sum(hm[-50:]) * 2}% ở 50 kỳ, {sum(hm[-100:])}% ở 100 kỳ.'
          + ' Chia vé (không tính vé thay thế): ' + ', '.join(f'ưu tiên {i + 1} ({k:02d}) {sum(1 for (kd, _, _), m in zip(tickets, TMM) if m == k and not kd.startswith("cân nhắc"))} vé' for i, k in enumerate(MM)) + '.')

# ---------- Rải vé bao phủ trên pool (anh, 13/10/2026; bao_phu.py, kiểu Đại học Manchester) ----------
# "m nếu k": nếu ≥k số về nằm trong pool thì chắc chắn có vé trúng ≥m số. Chạy lại đúng pool của từng kỳ trong 100/200 kỳ.
from bao_phu import bao_phu
THUONG = {'power': {3: 50000, 4: 500000, 5: 40e6, 6: 30e9}, 'mega': {3: 30000, 4: 300000, 5: 10e6, 6: 12e9}}.get(A.game)
LV = [(10, 3, 4), (10, 3, 3), (15, 3, 4), (18, 3, 4), (18, 3, 3)] if KB == 6 else [(10, 2, 2), (10, 3, 4), (10, 3, 3), (15, 3, 4), (18, 2, 2), (18, 3, 4)]
WH = []
for v, m, k in LV:
    if len(rank) < v: continue
    tk = bao_phu(v, KB, m, k)
    def wst(recs):
        dk = g3 = g4 = 0; tien = 0.0; n = 0
        for r in recs:
            pool = r['rk'][:v]
            if len(pool) < v: continue
            res = R[r['t']]; ve = [{pool[i] for i in b} for b in tk]; best = max(len(x & res) for x in ve); n += 1
            dk += len(set(pool) & res) >= k; g3 += best >= 3; g4 += best >= 4
            if THUONG: tien += sum(THUONG.get(len(x & res), 0) for x in ve)
        return dict(n=n, dk=dk / n * 100, g3=g3 / n * 100, g4=g4 / n * 100, thuong=tien / n if THUONG else None)
    WH.append(dict(v=v, m=m, k=k, nve=len(tk), cost=len(tk) * 10000, r100=wst(RECS[-100:]), r200=wst(RECS[-50:]),   # r200 giữ tên cũ, nay là 50 kỳ
                   tickets=[sorted(rank[i] for i in b) for b in tk]))
print('\n### Rải vé bao phủ trên pool\n')
print('| Pool · mức | Số vé | Kỳ đủ điều kiện 100 / 50 | Kỳ có vé ≥3 số 100 / 50 | Kỳ có vé ≥4 số 100 / 50 |' + (' Thưởng TB/kỳ (50) |' if THUONG else ''))
print('|---|---|---|---|---|' + ('---|' if THUONG else ''))
for w in WH:
    a, b = w['r100'], w['r200']
    print(f"| {w['v']} · {w['m']} nếu {w['k']} | {w['nve']} ({w['cost']:,}đ) | {a['dk']:.0f}% / {b['dk']:.0f}% | {a['g3']:.0f}% / {b['g3']:.0f}% | {a['g4']:.0f}% / {b['g4']:.0f}% |".replace(',', '.')
          + (f" {b['thuong']:,.0f}đ |".replace(',', '.') if THUONG else ''))

# Dữ liệu cho bảng trực quan
# Vì sao CHỌN / vì sao LOẠI từng số ở mỗi cỡ pool (anh 15/10/2026: "giải thích tại sao loại các số kia, và tại sao chọn các số này")
LOAI_TEN = {'vang': f'vắng ≥{G} kỳ', 'vang1': 'vắng lâu nhất', 'nong35': 'ra 3 lần trong 5 kỳ', 'thua': '"lâu lâu mới ra" và đang vắng ≥15',
            'vangph20': 'vắng ≥20 kỳ cùng phiên', 'it100': 'ra ít nhất 100 kỳ', 'lien2': 'ra 2 kỳ liền', 'lt3': 'ra kỳ trước và kỳ t−3',
            'zprev': 'số lớn nhất kỳ trước', 'tx15': 'tái xuất sau vắng ≥15'}
POOLWHY = {}
if 'POOLS' in globals() and POOLS:
    _kc = _PA.kepcap(A.game); _gh = _PA.GHIM.get(A.game, {}); _mx = _PA.MIXK.get(A.game, {}); _kn = _PA.KHO_NONG.get(A.game, set())
    def _rk(m): o = sorted(range(1, NB + 1), key=lambda n: (-m.get(n, 0), n)); return {n: i + 1 for i, n in enumerate(o)}
    _MIXR = [(MIXN.get(nm, nm).split(' (')[0], _rk(m)) for nm, m in zip([x for x in MIXM.split(',') if x], s.get('_mix') or [])]
    for K, P in POOLS.items():
        inP = set(P); chon = []; loai = []
        cong = POOLCHON.get(str(K), []) if POOLCHON else []
        for n in sorted(P, key=lambda n: P.index(n)):
            ex = [f"{nm.replace('TL: ', '')} {w:+g}" for nm, w in cong if w > -20 and n in CN.get(nm, ())]
            mr = [f'{lab} hạng {r[n]}' for lab, r in _MIXR]
            if K in _mx: mr += [f"{MIXN.get(m, m).split(' (')[0]} hạng {_rk(MIXF[m](T))[n]}" for m in _mx[K]]
            chon.append(dict(n=n, d=round(sc[n], 1), why=why(n), them=ex, mix=mr))
        for n in range(1, NB + 1):
            if n in inP: continue
            r = [LOAI_TEN.get(k, k) for k in ['vang'] + list(LOAI[A.game]) if n in (s.get(k) or ())]
            if n in BO: r.append('anh loại tay')
            if r: loai.append(dict(n=n, loai='hẳn', why=' · '.join(r))); continue
            g = [nm for nm, w in _gh.get(K, []) if w <= -20 and n in CN.get(nm, ())] + [nm for nm, w in cong if w <= -20 and n in CN.get(nm, ())]
            if g: loai.append(dict(n=n, loai='luật cỡ', why=' · '.join(g))); continue
            if str(K) in _kc and n % 11 == 0: loai.append(dict(n=n, loai='luật cỡ', why=f'giới hạn số kép trong pool {K} (tối đa {_kc[str(K)]})')); continue
            if HANGCAP and K in HANGCAP[1] and n // 10 in HANG_ON: loai.append(dict(n=n, loai='luật cỡ', why=f'hàng {n // 10}x ra nhiều 10 kỳ → pool {K} chỉ giữ 1 số hàng này')); continue
            loai.append(dict(n=n, loai='điểm', d=round(sc[n], 1), why=why(n)))
        note = [f'thứ hạng = trộn 50/50 điểm tín hiệu với {", ".join(lab for lab, _ in _MIXR)}'] if _MIXR else []
        if K in _mx: note.append('pool này trộn thêm ' + ', '.join(MIXN.get(m, m).split(' (')[0] for m in _mx[K]))
        if K in _kn: note.append('không trừ "khó ra" với số đang nóng lại')
        POOLWHY[str(K)] = dict(chon=chon, loai=loai, note=note)

if A.json:
    WHY = {}
    for n in range(1, NB + 1):
        WHY[n] = why(n)
    if RAIVE: KHUON['du'] = __import__('dangdu').du(R, LKA if DAY6 else None, NB, KB, T, _SPECS, (['13' if '13h' in x else '21' for x in D['dates']] + ['13' if '21h' in D['dates'][-1] else '21']) if DAY6 else None)
    if RAIVE: KHUON['ve'] = [_okv(_tk, TMM[_i] if _i < len(TMM) else None) for _i, (_k, _tk, _lv) in enumerate(tickets)]
    J = dict(game=A.game, name=NAME, nb=NB, kb=KB, next=nd, last=D['dates'][-1], lastRes=sorted(R[-1]),
             khuon=KHUON if RAIVE else None,
             res201=[sorted(R[t]) for t in range(T - 201, T)], dates201=D['dates'][T - 201:], lk201=[LKA[t] for t in range(T - 201, T)] if DAY6 else None,   # khối Check dạng (anh 14/10)
             sc={n: round(sc[n], 2) for n in range(1, NB + 1)}, rank=rank, pool=pool, k=A.k,
             why=WHY, gap={n: f[n]['gap'] for n in range(1, NB + 1)}, c10={n: f[n]['c10'] for n in range(1, NB + 1)},
             vang=sorted(s['vang'] | loai_of(s) | BO), hot=sorted(s['hot']), kho=sorted(s['kho']), hotOut=hot_out,
             tiers={k: v for k, v in B[100]['tiers'].items()}, tiers50={k: v for k, v in B[50]['tiers'].items()}, tiers100={k: v for k, v in B[100]['tiers'].items()}, wheel=WH, markov2=WMK > 0, ngayAm=NGAYAM, chay=[dict(nm=a, h10=b, h20=c, nums=d) for a, b, c, d in CHAY], chayW=CHAYW, hangOn=HANG_ON if POOLCHON else [], poolChon=POOLCHON, poolChonTheo=POOLCHON_THEO, pools={str(k): v for k, v in POOLS.items()}, poolWhy=POOLWHY, poolThuc=(json.load(open(os.path.join(HERE, 'pool_thuc.json'), encoding='utf-8')).get(A.game) if os.path.exists(os.path.join(HERE, 'pool_thuc.json')) else None), poolCach=' + '.join(MIXN[m] for m in MIXM.split(',') if m in MIXN),
             hist20=[dict(d=D["dates"][r["t"]], r=sorted(R[r["t"]]), lk=LKA[r["t"]] if DAY6 else None, rk=r["rk"][:20]) for r in reversed(RECS[-20:])],   # 20 kỳ gần: pool chạy lại từng kỳ (mới nhất trước)
             last10=B[10]['pool'][2], claims=CLR, sumRange=[SLO, SHI], da=DA_INFO, c50=round(c50, 2),
             ticketsK=TICKETS_K, veLuat=VELUAT, nghi=((json.load(open(os.path.join(HERE, 'nghi.json'), encoding='utf-8')).get(A.game)) if os.path.exists(os.path.join(HERE, 'nghi.json')) else None), tickets=[dict(kind=k, x=tk, lv=lv, sum=sum(tk) + (TMM[j] or 0 if j < len(TMM) else 0), lk=TMM[j] if j < len(TMM) else None) for j, (k, tk, lv) in enumerate(tickets)], day6=DAY6, core=core, mm=MM,
             mmGap={k: mg[k] for k in MM} if MM else {}, mmRate=MMRATE if MM else None, mmRank={str(W): v for W, v in MMRANK.items()} if MM else None, mmGoi={m['d']: m['goi'] for m in MMH} if MM else {}, mmHist=list(reversed(MMH[-20:])) if MM else None, linh=sorted(LINH),
             tl=dict(votes=votes, top=top_v, strong=strong, rescued=rescued, out=strong_out,
                     day=day, nm=len(APP.get('methods', [])), dung=TLDUNG) if APP else None,
             vl=VL, nong=NONG, nhip=NHIP, sig=[dict(lab=lab, nums=sorted(s[k]), how=how, r=[B[W][k][0] for W in (10, 50, 100)]) for k, lab, how in rows])
    json.dump(J, open(A.json, 'w'), ensure_ascii=False)

# Lưu lại gợi ý để chấm sổ khi có kết quả
if A.save:
    rec = dict(game=A.game, next=nd, last=D['dates'][-1], pool=sorted(pool), rank=rank, core=core,
               tickets=[tk for _, tk, _ in tickets], ticket_mm=TMM, tamlinh=sorted(top_v) if APP else [], tl_strong=sorted(strong) if APP else [], tl_votes={n: votes[n] for n in top_v} if APP else {}, tl_rescued=rescued if APP else [], linh=sorted(LINH),
               signals={k: sorted(v) for k, v in s.items() if k not in ('_td', '_mk', '_mix')}, pool_cach=' + '.join(MIXN[m] for m in MIXM.split(',') if m in MIXN), rank_cu=RANK_CU, khuon=_SPECS if RAIVE else None, pools={str(k): v for k, v in POOLS.items()}, sum_range=[SLO, SHI], mm=MM, markov2=WMK > 0,
               claims=[dict(lab=c['lab'], nums=c['nums'], r200=round(c['r200'])) for c in CLR if c['r200'] >= 70])
    with open(os.path.join(HERE, 'goiy_log.jsonl'), 'a') as fo:
        fo.write(json.dumps(rec, ensure_ascii=False) + '\n')
