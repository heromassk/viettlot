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
ap.add_argument('--cu', action='store_true', help='cách cũ: tắt các luật loại trừ bổ sung (để so)')
ap.add_argument('--save', action='store_true', help='ghi gợi ý vào build/goiy_log.jsonl')
A = ap.parse_args()
key, NB, KB, NAME = GAMES[A.game]
G = A.G or (999 if A.game == 'loto' and not A.cu else 15 if A.game == 'loto' else 20)   # Loto: số vắng lâu không nên loại (04/10)
D = json.load(open(os.path.join(HERE, 'all_data.json')))[key]
R = [set(r) for r in D['res']]          # cũ -> mới
SES = ['13' if '13h' in x else '21' for x in D['dates']] + ['13' if '21h' in D['dates'][-1] else '21']
T = len(R)
APP = json.load(open(A.app)) if A.app else None
LINH = {int(x) for x in A.linh.replace(' ', ',').split(',') if x.strip()}
P = KB / NB


def feats(t):
    """Đặc trưng từng số chỉ dùng dữ liệu trước kỳ t (R[:t])."""
    f = {}
    for n in range(1, NB + 1):
        g = 0
        while g < t and n not in R[t - 1 - g]:
            g += 1
        c = lambda w: sum(n in R[i] for i in range(max(0, t - w), t))
        w2 = min(200, t)
        z = (c(200) - w2 * P) / math.sqrt(w2 * P * (1 - P))
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
        same = [u for u in range(max(0, t - 200), t) if SES[u] == ph][-100:]
        sig['phien'] = top8({n: sum(n in R[u] for u in same) for n in range(1, NB + 1)})
    if not A.cu:   # luật loại trừ bổ sung (build/loai_tru.py, 04/10/2026) — chỉ giảm/cộng điểm, không loại hẳn
        if A.game == 'power':
            sig['chin'] = {n for n, x in f.items() if 11 <= x['gap'] <= 15}
            sig['g610'] = {n for n, x in f.items() if 6 <= x['gap'] <= 10}
        elif A.game == 'mega':
            sig['duoi'] = {n for n in range(1, NB + 1) if n % 10 in {x % 10 for x in last}} - last
        else:
            sig['lap'] = set(last)
    return f, sig


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
            - WDUOI * (n in s.get('duoi', ())) - WLAP * (n in s.get('lap', ()))
        v += min(f[n]['c20'], 6) * 0.15            # độ nóng mềm để tách hoà
        if extra:
            v += extra.get(n, 0)
        sc[n] = v
    return sc


def pool_of(sc, s, k):
    cand = [n for n in sc if n not in s['vang']]
    return sorted(cand, key=lambda n: (-sc[n], n))[:k]


# ---------- Backtest: tỉ lệ đúng của chính từng tín hiệu ----------
WCHIN, WG610, WDUOI, WLAP = (float(x) for x in os.environ.get('GOIY_W', '1 0.5 0.5 1').split())
SIGS = ('hot', 'ke', 'de', 'kho', 'vang') + (('chuyen', 'phien') if A.game == 'loto' else ()) + (() if A.cu else
        {'power': ('chin', 'g610'), 'mega': ('duoi',), 'loto': ('lap',)}[A.game])
def backtest(W):
    acc = {k: [0, 0] for k in SIGS}   # [số trúng / số bị loại đúng, cỡ tập]
    pool_h = []
    for t in range(T - W, T):
        f, s = signals(t)
        for k in acc:
            hit = len(s[k] & R[t])
            acc[k][0] += (len(s[k]) - hit) if k in ('kho', 'vang') else hit
            acc[k][1] += len(s[k])
        pool_h.append(len(set(pool_of(score(f, s), s, A.k)) & R[t]))
    out = {k: (a / b * 100 if b else None, b / W) for k, (a, b) in acc.items()}
    out['pool'] = (sum(pool_h) / W, sum(h >= 3 for h in pool_h) / W * 100, pool_h[-10:])
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
extra = {}
if APP:
    votes = APP['votes']
    top_v = sorted(range(1, NB + 1), key=lambda n: (-votes[n], n))[:12]
    for n in top_v: extra[n] = extra.get(n, 0) + 1
    for n in APP.get('appPool', []): extra[n] = extra.get(n, 0) + 0.5
    b15 = (APP.get('best50') or {}).get('15') or {}
    for n in b15.get('pool', []): extra[n] = extra.get(n, 0) + 0.5
for n in LINH: extra[n] = extra.get(n, 0) + 3
sc = score(f, s, extra)
pool = pool_of(sc, s, A.k)
hot_out = sorted(s['hot'] - set(pool))

# ---------- Vé: lõi + vệ tinh ----------
NL = 2 if KB == 5 else 3
core, sat = pool[:NL], pool[NL:]

RELAX = ['đủ ràng buộc', 'bỏ điều kiện ≥2 số >31', 'mượn số ngoài pool (điểm cao kế tiếp)']
EXT = [n for n in sorted(sc, key=lambda n: (-sc[n], n)) if n not in s['vang'] and n not in pool][:10]

def ok(tk, lv):
    tk = sorted(tk)
    if not SLO <= sum(tk) <= SHI: return False
    if lv == 0 and A.game != 'loto' and sum(x > 31 for x in tk) < 2: return False
    if not A.cu and lv < 2 and bad_ticket(tk): return False
    return not any(tk[i] + 2 == tk[i + 1] + 1 == tk[i + 2] for i in range(len(tk) - 2))

def bad_ticket(tk):
    """Luật loại vé — kỳ thật hiếm khi vi phạm (1–8%, ổn định 3 khúc)."""
    odd = sum(x % 2 for x in tk); low = sum(x <= NB // 2 for x in tk)
    dec = {}
    for x in tk: dec[x // 10] = dec.get(x // 10, 0) + 1
    return (len(set(tk) & R[-1]) >= 3 or odd in (0, KB) or low in (0, KB)
            or (KB == 6 and max(dec.values()) >= 4) or max(tk) < NB * 2 // 3)

def pick(base, cands, need, used):
    for lv in range(3):
        cs = cands + EXT if lv == 2 else cands
        best = None
        for c in combinations(cs, need):
            tk = sorted(base + list(c))
            if not ok(tk, lv): continue
            v = (sum(sc[n] for n in c) - 2 * sum(used.get(n, 0) for n in c), [-n for n in c])
            if best is None or v > best[0]: best = (v, tk)
        if best: return best[1], lv
    c = sorted(cands, key=lambda n: (used.get(n, 0), -sc[n]))[:need]
    return sorted(base + c), 3

tickets, used = [], {}
for i in range(3):
    tk, lv = pick(core, sat, KB - NL, used); tickets.append(('lõi+vệ tinh', tk, lv))
    for n in tk: used[n] = used.get(n, 0) + 1
for i in range(2):   # 2 vé trải: 1 số lõi + phần pool ít dùng
    tk, lv = pick([core[i]], [n for n in pool if n not in core], KB - 1, used); tickets.append(('trải', tk, lv))
    for n in tk: used[n] = used.get(n, 0) + 1

# ---------- In ----------
fm = lambda xs: ' '.join(f'{n:02d}' for n in sorted(xs)) or '—'
nd = APP['next'] if APP else '(kỳ tới)'
print(f'## Gợi ý {NAME} — kỳ {nd}\n')
print(f'Kỳ gần nhất {D["dates"][-1]}: **{fm(R[-1])}** (tổng {sums[-1]})\n')
print('### Tín hiệu dấu vết (cùng một cách tính mọi kỳ)\n')
B = {W: backtest(W) for W in (10, 50, 200)}
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
                     ('duoi', 'Cùng đuôi số kỳ trước (−điểm)', 'loại đúng'), ('lap', 'Số vừa ra kỳ trước (−điểm)', 'loại đúng')) if x[0] in SIGS]
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
print(f'\n### Pool {A.k} điểm đồng thuận\n\n**{fm(pool)}**\n')
rank = pool_of(sc, s, min(20, NB - len(s['vang'])))
print(f"Pool 10: **{fm(rank[:10])}**  ·  Pool 20: {fm(rank[:20])}\n")
def why(n):
    t = [lab for k, lab in (('hot', 'nóng'), ('ke', 'kề'), ('de', 'dễ ra'), ('kho', 'khó ra'), ('chuyen', 'chuyển kỳ'), ('phien', 'nóng phiên'), ('chin', 'vắng 11–15'), ('g610', 'vắng 6–10 −'), ('duoi', 'cùng đuôi −'), ('lap', 'vừa ra −')) if n in s.get(k, ())]
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
for W in (10, 50, 200):
    tb, p3, last = B[W]['pool']
    print(f'\nPool {A.k} (không tâm linh/app) chính nó ở {W} kỳ: TB **{tb:.2f}** số/kỳ, ≥3 số {p3:.0f}%' + (f' · 10 kỳ gần: {last}' if W == 10 else ''))
print(f'\n### 5 vé (lõi {fm(core)} + vệ tinh)\n')
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

# Lưu lại gợi ý để chấm sổ khi có kết quả
if A.save:
    rec = dict(game=A.game, next=nd, last=D['dates'][-1], pool=sorted(pool), rank=rank, core=core,
               tickets=[tk for _, tk, _ in tickets], tamlinh=sorted(top_v) if APP else [], linh=sorted(LINH),
               signals={k: sorted(v) for k, v in s.items()}, sum_range=[SLO, SHI], mm=MM)
    with open(os.path.join(HERE, 'goiy_log.jsonl'), 'a') as fo:
        fo.write(json.dumps(rec, ensure_ascii=False) + '\n')
