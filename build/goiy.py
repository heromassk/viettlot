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
ap.add_argument('--mt', type=int, default=0, choices=(0, 9, 12), help='vé ma trận: 12 số → 6 vé (4 nhóm×3, mỗi vé 2 nhóm) hoặc 9 số → 3 vé')
ap.add_argument('--pm', action='store_true', help='ma trận lấy từ pool ±1/±10 số kỳ trước (xếp theo điểm) thay vì pool điểm')
A = ap.parse_args()
key, NB, KB, NAME = GAMES[A.game]
_ct = os.environ.get('GOIY_CT', '')
CT = (tuple(int(x) for x in _ct.split(':')[0].split(',')), int(_ct.split(':')[1])) if _ct else None
G = A.G or (15 if A.cu and A.game == 'loto' else 999 if A.game == 'power' and not A.cu else 20)   # Power: vắng ≥20 đang NGƯỢC (200 kỳ: ra 14.7/11.0%, loại đúng chỉ 51%) → bỏ (05/10)   # ý anh 04/10: loại số vắng ≥20 (cả 3 trò)   # Mega: vắng ≥30 đúng 94% kỳ (suyluan 04/10)   # Loto: số vắng lâu không nên loại (04/10)
D = json.load(open(os.path.join(HERE, 'all_data.json')))[key]
if os.environ.get('GOIY_CUT'):   # chấm lùi: bỏ n kỳ cuối, gợi ý như đứng ở quá khứ
    D = {k: (v[:-int(os.environ['GOIY_CUT'])] if isinstance(v, list) else v) for k, v in D.items()}
R = [set(r) for r in D['res']]          # cũ -> mới
SES = ['13' if '13h' in x else '21' for x in D['dates']] + ['13' if '21h' in D['dates'][-1] else '21']
T = len(R)
APP = json.load(open(A.app)) if A.app else None
LINH = {int(x) for x in A.linh.replace(' ', ',').split(',') if x.strip()}
BO = {int(x) for x in A.bo.replace(' ', ',').split(',') if x.strip()}
P = KB / NB
# Cửa sổ xét "tính chất bi" (dễ/khó ra, thưa, ra đều…): Power/Mega thay bộ bi định kỳ → chỉ xét WB kỳ gần (anh, 05/10)
WB = int(os.environ.get('GOIY_WB', {'power': '100', 'mega': '100', 'loto': '200'}[A.game]))   # Power/Mega tối đa 100 kỳ (thay bi 1–2 tháng/lần — anh, 05/10); Loto không có bi thật


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
    ct = set()
    if CT:   # cộng/trừ qua nhiều kỳ (anh, 08/10/2026): 12 số nhiều phiếu nhất từ ±d qua k kỳ
        v = {}
        for j in range(1, CT[1] + 1):
            for x in R[t - j]:
                for d in CT[0]:
                    for m in (x - d, x + d):
                        if 1 <= m <= NB: v[m] = v.get(m, 0) + 1
        ct = set(sorted((m for m in v if m not in last), key=lambda m: (-v[m], m))[:12])
    de = {n for n, x in f.items() if x['z'] > 1}
    kho = {n for n, x in f.items() if x['z'] < -1.5}
    vang = {n for n, x in f.items() if x['gap'] >= G}
    sig = dict(hot=hot, ke=ke, de=de, kho=kho, vang=vang)
    if A.game == 'loto':   # dấu vết riêng Loto (máy tính quay): chuyển kỳ + nóng cùng phiên
        sig['chuyen'] = top8(follow(t))
        ph = SES[t]
        same = [u for u in range(max(0, t - 200), t) if SES[u] == ph][-100:]
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
    sig['_td'] = td_sets(t)
    sig['ct'] = ct
    return f, sig


# ---- Luật trong sổ kiểm chứng nghiêng ổn định (rasoat.py 05/10/2026) → trọng số nhỏ (dấu vết = xác suất nghiêng) ----
import sys as _sys
_sys.path.insert(0, HERE)
import theodoi as _TD
WTD = float(os.environ.get('GOIY_TD', {'loto': '1', 'power': '1', 'mega': '1'}[A.game]))   # luật đúng ≥70% ở khung 50 & 100 kỳ và số bị loại ra ≤ TB (luat_khung.py, anh 05/10)
TDW = {   # id luật → dấu trọng số (−: ra ít, +: ra nhiều)
    'power': {'nong35': -1, 'nhip2': -1, 'lt3': -1, 'tx15': -1, 'tx10': -1, 'zprev': -1,
              'nhom_lokep': -1, 'nhom_kep': 1, 'nhom_pascal': 1, 'nhom_cau2': 1},
    'mega': {'nong35': -1, 'tx15': -1, 'nong10': -1, 'nhieu100': -1, 'nhip2': -1},
    'loto': {'lt3': -1, 'tx10': -1, 'nhip2': -1, 'nhipmin100': -1, 'nhom_nhip80': -1, 'nhom_nhip': -1, 'nhom_lokep': -1,
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
        v += sum(WTD * sg for sg, st in s.get('_td', {}).values() if n in st)
        v += WCT * (n in s.get('ct', ()))
        v += min(f[n]['c20'], 6) * 0.15            # độ nóng mềm để tách hoà
        if extra:
            v += extra.get(n, 0)
        sc[n] = v
    return sc


LOAI = {'power': ('it100',), 'mega': ('lien2', 'lt3', 'zprev', 'thua'), 'loto': ('tx15', 'vang1', 'nong35', 'thua')}
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
WCT = float(os.environ.get('GOIY_CTW', '0'))   # điểm cộng cho số trong pool cộng/trừ (GOIY_CT='1,16:5')
SIGS = ('hot', 'ke', 'de', 'kho', 'vang') + (('chuyen', 'phien') if A.game == 'loto' else ()) + (() if A.cu else
        {'power': ('chin', 'g610', 'tuan', 'it100'), 'mega': ('duoi', 'lien2', 'ben', 'lt3', 'zprev', 'thua', 'chin'), 'loto': ('lap', 'tx15', 'vang1', 'nong35', 'thua')}[A.game])
import random
random.seed(5)
MC = [set(random.sample(range(1, NB + 1), KB)) for _ in range(300)]
HALF = KB // 2

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
    ke = {m for n in last for m in (n - 1, n, n + 1) if 1 <= m <= NB}
    p10, p15, p20 = set(rk[:10]), set(rk[:15]), set(rk[:20])
    return [
        ('Pool 10 có ≥1 số', p10, lambda x: len(x & p10) >= 1),
        ('Pool 15 có ≥2 số', p15, lambda x: len(x & p15) >= 2),
        ('Pool 20 có ≥2 số', p20, lambda x: len(x & p20) >= 2),
        ('Pool 20 có ≥3 số', p20, lambda x: len(x & p20) >= 3),
        ('Có ≥1 số của 2 kỳ gần nhất', last | p2, lambda x: bool(x & (last | p2))),
        ('Có ≥1 số trong 10 số nóng nhất 20 kỳ', hot10, lambda x: bool(x & hot10)),
        ('Có ≥1 số trùng hoặc kề ±1 kỳ trước', ke, lambda x: bool(x & ke)),
        ('Không trùng ≥2 số với kỳ trước', last, lambda x: len(x & last) < 2),
        (f'Chẵn/lẻ cân ({HALF}±1 số lẻ)', None, lambda x: abs(sum(n % 2 for n in x) - KB / 2) <= 1),
        (f'Nhỏ/lớn cân ({HALF}±1 số ≤{NB // 2})', None, lambda x: abs(sum(n <= NB // 2 for n in x) - KB / 2) <= 1),
        (f'Rải ≥{KB - 2} hàng chục', None, lambda x: len({n // 10 for n in x}) >= KB - 2),
    ]

def pm_pool(t, sc):
    """Pool ±1/±10 của kỳ t−1 (anh, 08/10/2026), xếp theo điểm đồng thuận."""
    p = R[t - 1]; P = {x + d for x in p for d in (-1, 1, -10, 10) if 1 <= x + d <= NB} - p
    if float(os.environ.get('GOIY_PMX', '0.5')) > 0:   # pool điểm 20, số thuộc ±1/±10 +0.5 điểm (chấm lùi 08/10: tốt hơn lấy thuần ±1/±10; GOIY_PMX=0 → thuần)
        top = sorted((n for n in sc if n not in p), key=lambda n: (-sc[n], n))[:20]
        return sorted(top, key=lambda n: (-(sc[n] + float(os.environ.get('GOIY_PMX', '0.5')) * (n in P)), n))
    rk = sorted(P, key=lambda n: (-sc[n], n))
    return rk + sorted((n for n in sc if n not in P and n not in p), key=lambda n: (-sc[n], n))[:max(0, 12 - len(rk))]   # thiếu 12 thì bù số điểm cao (không lấy số kỳ trước)

def backtest(W=200):
    """Chạy tiến W kỳ: mỗi kỳ ghi số trúng của từng tín hiệu, pool 10/15/20 và từng khẳng định."""
    recs = []
    for t in range(T - W, T):
        f, s = signals(t)
        sct = score(f, s); rk = pool_of(sct, s, 20)
        sig = {k: (len(s[k] & R[t]), len(s[k])) for k in SIGS}
        cl = [(lab, fn(R[t]), sum(fn(m) for m in MC) / len(MC)) for lab, _, fn in claims(t, rk)]
        recs.append(dict(rk=(pm_pool(t, sct) if A.pm else rk)[:12], r=R[t], sig=sig, h={k: len(set(rk[:k]) & R[t]) for k in (7, 8, 9, 10, 12, 15, 20)}, cl=cl))
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
    out['tiers'] = {k: [sum(r['h'][k] >= j for r in recs) / W * 100 for j in range(1, 5)] + [sum(r['h'][k] for r in recs) / W] for k in (10, 15, 20)}
    out['claims'] = [(recs[0]['cl'][i][0], sum(r['cl'][i][1] for r in recs) / W * 100, sum(r['cl'][i][2] for r in recs) / W * 100)
                     for i in range(len(recs[0]['cl']))]
    return out


# ---------- Ma trận vòng xoay (anh, 08/10/2026): chia M số pool thành M/3 nhóm × 3 số, mỗi vé = 2 nhóm ----------
def _parts(m):
    def rec(rest):
        if not rest: yield []; return
        a = rest[0]
        for b, c in combinations(rest[1:], 2):
            for tail in rec([x for x in rest[1:] if x not in (b, c)]): yield [(a, b, c)] + tail
    return list(rec(list(range(m))))
PARTS = {9: _parts(9), 12: _parts(12)}

def mt_tickets(nums, chk=None, w=None):
    """Chọn cách chia nhóm: mọi vé chẵn/lẻ 2-4/4-2/3-3 (+ chk nếu có), điểm các vé đều nhau nhất."""
    m = len(nums); w = w or {n: m - i for i, n in enumerate(nums)}; best = None
    for pt in PARTS[m]:
        gs = [[nums[i] for i in g] for g in pt]
        tks = [sorted(a + b) for a, b in combinations(gs, 2)]
        bad = sum(abs(sum(x % 2 for x in tk) - 3) > 1 for tk in tks) * 100 + (sum(not chk(tk) for tk in tks) if chk else 0)
        sw = [sum(w[x] for x in tk) for tk in tks]
        v = (bad, max(sw) - min(sw))
        if best is None or v < best[0]: best = (v, tks)
    return best[1]

def mt_bt(recs, m):
    out = []
    for r in recs:
        tks = mt_tickets(r['rk'][:m])
        out.append((max(len(set(tk) & r['r']) for tk in tks), len(set(r['rk'][:m]) & r['r'])))
    return out

# ---------- Đà tổng ----------
sums = [sum(r) for r in D['res']]
def corr(a, b):
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
    return num / den if den else 0
s50 = sums[-51:]
c50 = corr(s50[:-1], s50[1:])
mid = KB * (NB + 1) / 2
srt = sorted(sums[-200:])
q25, q75 = srt[50], srt[150]
last10 = sums[-10:]; m10 = sum(last10) / 10
sd10 = math.sqrt(sum((x - m10) ** 2 for x in last10) / 9)
DA = c50 > 0.2 and A.game != 'loto'   # Loto: đà tổng không có dấu vết (nghiên cứu 04/10)
SLO, SHI = (int(m10 - sd10), int(m10 + sd10)) if DA else (q25, q75)

# ---------- Hiện tại ----------
f, s = signals(T)
CUR = s
extra = {}
if APP:
    votes = APP['votes']
    top_v = sorted(range(1, NB + 1), key=lambda n: (-votes[n], n))[:12]
    for n in top_v: extra[n] = extra.get(n, 0) + 1
    v5 = sorted(votes[1:], reverse=True)[4]
    strong = [n for n in top_v if votes[n] >= v5]            # tâm linh mạnh: phiếu ≥ mức của số thứ 5
    for n in strong: extra[n] += 0.5
    # Tâm linh mạnh mà bị luật vắng loại → không loại hẳn, để điểm quyết định (anh: "cần cân nhắc")
    rescued = sorted(set(strong) & (s['vang'] | loai_of(s)))
    s['vang'] = s['vang'] - set(rescued)
    for k in LOAI[A.game]:
        if k in s: s[k] = s[k] - set(rescued)
    by_m = {}
    for name, nums in APP.get('methods', []):
        for n in nums: by_m.setdefault(n, []).append(name)
    for n in APP.get('appPool', []): extra[n] = extra.get(n, 0) + 0.5
    b15 = (APP.get('best50') or {}).get('15') or {}
    for n in b15.get('pool', []): extra[n] = extra.get(n, 0) + 0.5
for n in LINH: extra[n] = extra.get(n, 0) + 3
sc = score(f, s, extra)
pool = pool_of(sc, s, A.k)
hot_out = sorted(s['hot'] - set(pool))
rank = pool_of(sc, s, min(20, NB - len(s['vang'])))
CL_NOW = claims(T, rank)
HOT10 = next(c[1] for c in CL_NOW if c[0].startswith('Có ≥1 số trong 10'))
KE1 = next(c[1] for c in CL_NOW if c[0].startswith('Có ≥1 số trùng'))

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
    if not SLO <= sum(tk) <= SHI: return False
    if lv == 0 and A.game != 'loto' and sum(x > 31 for x in tk) < 2: return False
    if not A.cu and bad_ticket(tk): return False
    return not any(tk[i] + 2 == tk[i + 1] + 1 == tk[i + 2] for i in range(len(tk) - 2))

def bad_ticket(tk):
    """Luật loại vé — kỳ thật hiếm khi vi phạm (1–8%, ổn định 3 khúc)."""
    odd = sum(x % 2 for x in tk); low = sum(x <= NB // 2 for x in tk)
    dec = {}
    for x in tk: dec[x // 10] = dec.get(x // 10, 0) + 1
    x = set(tk)
    if (len(x & R[-1]) >= 3 or odd in (0, KB) or low in (0, KB)
            or (KB == 6 and max(dec.values()) >= 4) or max(tk) < NB * 2 // 3):
        return True
    if KB == 6 and abs(odd - 3) > 1: return True                  # anh (06/10/2026): chẵn/lẻ chỉ 2-4, 4-2, 3-3 — không 1:5, 5:1
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
for i in range(3):
    tk, lv = pick(core, sat, KB - NL, used); tickets.append(('lõi+vệ tinh', tk, lv)); DONE.append(tk)
    for n in tk: used[n] = used.get(n, 0) + 1
for i in range(2):   # 2 vé trải: 1 số lõi + phần pool ít dùng
    tk, lv = pick([core[i]], [n for n in pool if n not in core], KB - 1, used); tickets.append(('trải', tk, lv)); DONE.append(tk)
    for n in tk: used[n] = used.get(n, 0) + 1
if A.mt:   # vé ma trận thay cho 5 vé lõi+vệ tinh
    tickets = [(f'ma trận {A.mt} số', tk, 0) for tk in mt_tickets((pm_pool(T, sc) if A.pm else rank)[:A.mt], lambda tk: not bad_ticket(tk), sc)]

# ---------- In ----------
fm = lambda xs: ' '.join(f'{n:02d}' for n in sorted(xs)) or '—'
nd = APP['next'] if APP else '(kỳ tới)'
print(f'## Gợi ý {NAME} — kỳ {nd}\n')
print(f'Kỳ gần nhất {D["dates"][-1]}: **{fm(R[-1])}** (tổng {sums[-1]})\n')
print('### Tín hiệu dấu vết (cùng một cách tính mọi kỳ)\n')
RECS = backtest(200)
B = {W: summ(RECS[-W:]) for W in (10, 50, 200)}
MTB = {}
if A.mt and not os.environ.get('GOIY_CUT'):
    hh = mt_bt(RECS, A.mt)
    for W in (10, 20, 50, 100, 200):
        x = hh[-W:]; MTB[W] = dict(tb=round(sum(h for h, _ in x) / W, 2), g3=round(sum(h >= 3 for h, _ in x) / W * 100), g4=round(sum(h >= 4 for h, _ in x) / W * 100), pool=round(sum(p for _, p in x) / W, 2))
    MTB['doan'] = [round(sum(h for h, _ in hh[i:i + 100][:100]) / 100, 2) for i in (0, 100)]
    print(f'Ma trận {A.mt} số → {len(tickets)} vé, chấm lùi (vé tốt nhất mỗi kỳ): ' + ' · '.join(f"{W} kỳ TB {v['tb']} (pool {v['pool']}) / ≥3: {v['g3']}% / ≥4: {v['g4']}%" for W, v in MTB.items() if W != 'doan') + f"  ·  2 đoạn 100 kỳ TB {MTB['doan']}\n")
pc = lambda v: '—' if v is None else f'{v:.0f}%'
rows = [('hot', 'Nóng (c10≥3 hoặc c20≥2×kỳ vọng)', 'tỉ lệ ra/số'),
        ('ke', 'Kề ±1 kỳ trước', 'tỉ lệ ra/số'),
        ('de', 'Bóng dễ ra (z200>1)', 'tỉ lệ ra/số'),
        ('kho', 'Bóng khó ra (z200<−1.5)', 'loại đúng'),
        ('vang', f'Vắng ≥{G} kỳ (bỏ khỏi pool)', 'loại đúng')]
if A.game == 'loto':
    rows += [('chuyen', 'Chuyển kỳ (số hay theo sau số kỳ trước), top 8', 'tỉ lệ ra/số'),
             ('phien', 'Nóng cùng phiên 100 kỳ, top 8', 'tỉ lệ ra/số')]
rows += [x for x in (('chin', 'Vắng 11–15 kỳ — "chín" (+điểm)', 'tỉ lệ ra/số'), ('g610', 'Vắng 6–10 kỳ (−điểm)', 'loại đúng'),
                     ('duoi', 'Cùng đuôi số kỳ trước (−điểm)', 'loại đúng'), ('lap', 'Số vừa ra kỳ trước (−điểm)', 'loại đúng'), ('tuan', 'Số kỳ cùng thứ tuần trước (−điểm)', 'loại đúng'), ('lien2', 'Ra 2 kỳ liền (bỏ khỏi pool)', 'loại đúng'), ('lt3', 'Ra kỳ trước & kỳ t−3 (bỏ)', 'loại đúng'), ('zprev', 'Số lớn nhất kỳ trước (bỏ)', 'loại đúng'),
                     ('it100', 'Ra ít nhất 100 kỳ (bỏ)', 'loại đúng'), ('tx15', 'Tái xuất sau vắng ≥15 (bỏ)', 'loại đúng'), ('vang1', 'Vắng lâu nhất (bỏ)', 'loại đúng'), ('nong35', 'Ra 3 lần/5 kỳ (bỏ)', 'loại đúng'), ('ben', 'Ra nhiều cả 4 đoạn 25 kỳ (+điểm)', 'tỉ lệ ra/số'), ('thua', 'Lâu lâu mới ra (200 kỳ ≤85% kỳ vọng) & vắng ≥15 (bỏ)', 'loại đúng')) if x[0] in SIGS]
print('| Tín hiệu | Số hiện tại | Đo bằng | 10 kỳ | 50 kỳ | 200 kỳ |\n|---|---|---|---|---|---|')
for k, lab, how in rows:
    print(f'| {lab} | {fm(s[k])} | {how} | ' + ' | '.join(pc(B[W][k][0]) for W in (10, 50, 200)) + ' |')
print(f'\nĐà tổng: tương quan tổng kỳ liền nhau 50 kỳ = **{c50:+.2f}** '
      + (f'→ có đà, TB 10 kỳ {m10:.0f} (giữa {mid:.0f}), khoảng tổng nên chọn **{SLO}–{SHI}**.' if DA
         else f'→ không rõ đà, dùng khoảng tổng thường gặp 200 kỳ **{SLO}–{SHI}**.'))
if APP:
    print(f'\nPhiếu tâm linh top 12: {fm(top_v)}  ·  Pool app ({APP.get("appMethod")}): {fm(APP.get("appPool", []))}'
          f'  ·  PP tốt nhất 50 kỳ (K15): {b15.get("id")} TB {b15.get("tb")} → {fm(b15.get("pool", []))}')
if LINH: print(f'\nSố linh cảm của anh: **{fm(LINH)}** (+3 điểm)')
if BO: print(f'\nSố anh loại tay kỳ này: **{fm(BO)}**')
print(f'\n### Pool {A.k} điểm đồng thuận\n\n**{fm(pool)}**\n')
print(f"Pool 10: **{fm(rank[:10])}**  ·  Pool 20: {fm(rank[:20])}\n")
def why(n):
    t = [lab for k, lab in (('hot', 'nóng'), ('ke', 'kề'), ('de', 'dễ ra'), ('kho', 'khó ra'), ('chuyen', 'chuyển kỳ'), ('phien', 'nóng phiên'), ('chin', 'vắng 11–15'), ('g610', 'vắng 6–10 −'), ('duoi', 'cùng đuôi −'), ('lap', 'vừa ra −'), ('tuan', 'cùng thứ tuần trước −'), ('lien2', 'ra 2 kỳ liền (loại)'), ('lt3', 'ra kỳ trước & t−3 (loại)'), ('zprev', 'z kỳ trước (loại)'), ('it100', 'ít nhất 100 kỳ (loại)'), ('tx15', 'tái xuất (loại)'), ('vang1', 'vắng lâu nhất (loại)'), ('nong35', '3 lần/5 kỳ (loại)'), ('ben', 'ra đều 4 đoạn'), ('thua', 'thưa & vắng ≥15 (loại)')) if n in s.get(k, ())]
    if APP:
        if n in top_v: t.append(f'tâm linh {votes[n]} phiếu')
        if n in APP.get('appPool', []): t.append('pool app')
        if n in b15.get('pool', []): t.append('PP tốt 50 kỳ')
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
    print(f'\nDãy tâm linh (top {KB} phiếu): **{fm(day)}**  ·  ★ = tâm linh mạnh (phiếu ≥ {v5}), +1.5 điểm; top 12 khác +1 điểm')
    strong_out = [n for n in strong if n not in pool]
    if strong_out:
        print(f'\n⚠️ **Tâm linh mạnh nằm ngoài pool: {fm(strong_out)}** — cần cân nhắc (xem vé thay thế bên dưới).')
for W in (10, 50, 200):
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
    c100 = sum(n in R[u] for u in range(T - 100, T)); c200 = sum(n in R[u] for u in range(T - WB, T))
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
    c100 = sum(n in R[u] for u in range(T - 100, T)); c200 = sum(n in R[u] for u in range(T - WB, T))
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
        for W in (50, 200):
            ix = [i for i in range(len(RECS)) if ss[i] == ph][-W // 2:]
            PH[f'{ph}_{W}'] = {k: round(sum(RECS[i]['h'][k] for i in ix) / max(len(ix), 1), 2) for k in (10, 15)}
            PH[f'{ph}_{W}']['n'] = len(ix)
    NHIP['phien'] = PH
    print('**Pool trúng theo phiên** (TB số trúng/kỳ, pool 10 · pool 15): ' + ' · '.join(
        f"{ph}h {W // 2} kỳ gần: {PH[f'{ph}_{W}'][10]} · {PH[f'{ph}_{W}'][15]}" for ph in ('13', '21') for W in (50, 200)))
    print(f"\n**Nhịp pool:** 5 kỳ gần pool 15 trúng {hh[-5:]} → TB {m5:.2f} (ngưỡng nhóm tốt {thr:.2f}) → " + ("**ĐANG VÀO NHỊP — kỳ nên đánh mạnh**" if m5 >= thr else "nhịp thường — đánh nhẹ"))

# ---------- Khẳng định kỳ này (đúng ≥70% ở 200 kỳ) ----------
CLR = []
for (lab, st, fn), (lab2, r200, k200), (_, r50, _) in zip(CL_NOW, B[200]['claims'], B[50]['claims']):
    CLR.append(dict(lab=lab, nums=sorted(st) if st else [], r200=r200, r50=r50, keep=k200, trace=r200 - k200 >= 3))
print('\n### Khẳng định kỳ này (đúng ≥70% số kỳ trong 200 kỳ)\n')
print('| Khẳng định | Số liên quan | Đúng 200 kỳ | 50 kỳ gần | Vé giữ lại | Dấu vết |\n|---|---|---|---|---|---|')
for c in sorted(CLR, key=lambda c: -c['r200']):
    if c['r200'] < 70: continue
    print(f"| {c['lab']} | {fm(c['nums']) if c['nums'] and len(c['nums']) <= 20 else '—'} | **{c['r200']:.0f}%** | {c['r50']:.0f}% | {c['keep']:.0f}% | {'✔ đúng > giữ' if c['trace'] else ''} |")
if APP and strong_out:   # vé thay thế: vé 1, đổi số điểm thấp nhất (không phải lõi) bằng tâm linh mạnh ngoài pool
    alt = list(tickets[0][1])
    for n in sorted(strong_out, key=lambda n: -votes[n])[:2]:
        low = min((x for x in alt if x not in core and x not in strong_out), key=lambda x: sc[x], default=None)
        if low is None: break
        alt[alt.index(low)] = n
    tickets.append(('cân nhắc tâm linh (thay thế vé 1)', sorted(alt), 0))
print(f'\n### {len(tickets)} vé (lõi {fm(core)} + vệ tinh)\n')
for i, (kind, tk, lv) in enumerate(tickets, 1):
    note = RELAX[lv] if lv < 3 else 'không vé nào hợp lệ, lấy theo điểm'
    out = [n for n in tk if n not in pool]
    print(f'{i}. **{fm(tk)}** — {kind}, tổng {sum(tk)}' + ('' if lv == 0 else f' _({note}' + (f': {fm(out)}' if out else '') + ')_'))

# Số May Mắn Loto: xu hướng cân bằng → 3 số vắng lâu nhất
MM = []
if A.game == 'loto':
    LK = D['lk']
    mg = {k: next((g for g in range(len(LK)) if LK[-1 - g] == k), len(LK)) for k in range(1, 13)}
    MM = sorted(mg, key=lambda k: (-mg[k], k))[:3]
    hm = []
    for t in range(len(LK) - 200, len(LK)):
        g = {k: next((x for x in range(t) if LK[t - 1 - x] == k), t) for k in range(1, 13)}
        hm.append(LK[t] in sorted(g, key=lambda k: (-g[k], k))[:3])
    print(f'\n### Số May Mắn (3 số vắng lâu nhất)\n\n**{fm(MM)}** — vắng ' + ', '.join(f'{k:02d}: {mg[k]} kỳ' for k in MM)
          + f'  ·  chính cách này trúng {sum(hm[-50:]) * 2}% ở 50 kỳ, {sum(hm) / 2:.0f}% ở 200 kỳ')

# Dữ liệu cho bảng trực quan
if A.json:
    WHY = {}
    for n in range(1, NB + 1):
        WHY[n] = why(n)
    J = dict(game=A.game, name=NAME, nb=NB, kb=KB, next=nd, last=D['dates'][-1], lastRes=sorted(R[-1]),
             sc={n: round(sc[n], 2) for n in range(1, NB + 1)}, rank=rank, pool=pool, k=A.k,
             why=WHY, gap={n: f[n]['gap'] for n in range(1, NB + 1)}, c10={n: f[n]['c10'] for n in range(1, NB + 1)},
             vang=sorted(s['vang'] | loai_of(s) | BO), hot=sorted(s['hot']), kho=sorted(s['kho']), hotOut=hot_out,
             tiers={k: v for k, v in B[200]['tiers'].items()}, tiers50={k: v for k, v in B[50]['tiers'].items()}, tiers100=summ(RECS[-100:])['tiers'],
             last10=B[10]['pool'][2], hist10=[dict(d=D['dates'][i], r=sorted(R[i]), x=(D['lk'][i] if 'lk' in D else None)) for i in range(T - 10, T)],
             claims=CLR, sumRange=[SLO, SHI], da=DA, c50=round(c50, 2),
             tickets=[dict(kind=k, x=tk, lv=lv, sum=sum(tk)) for k, tk, lv in tickets], core=core, mm=MM,
             mmGap={k: mg[k] for k in MM} if MM else {}, linh=sorted(LINH),
             tl=dict(votes=votes, top=top_v, strong=strong, rescued=rescued, out=strong_out,
                     day=day, nm=len(APP.get('methods', []))) if APP else None,
             vl=VL, nong=NONG, nhip=NHIP, sig=[dict(lab=lab, nums=sorted(s[k]), how=how, r=[B[W][k][0] for W in (10, 50, 200)]) for k, lab, how in rows])
    json.dump(J, open(A.json, 'w'), ensure_ascii=False)

# Lưu lại gợi ý để chấm sổ khi có kết quả
if A.save:
    rec = dict(game=A.game, next=nd, last=D['dates'][-1], pool=sorted(pool), rank=rank, core=core,
               tickets=[tk for _, tk, _ in tickets], tamlinh=sorted(top_v) if APP else [], tl_strong=sorted(strong) if APP else [], tl_rescued=rescued if APP else [], linh=sorted(LINH),
               signals={k: sorted(v) for k, v in s.items() if k != '_td'}, sum_range=[SLO, SHI], mm=MM,
               claims=[dict(lab=c['lab'], nums=c['nums'], r200=round(c['r200'])) for c in CLR if c['r200'] >= 70])
    with open(os.path.join(HERE, 'goiy_log.jsonl'), 'a') as fo:
        fo.write(json.dumps(rec, ensure_ascii=False) + '\n')
