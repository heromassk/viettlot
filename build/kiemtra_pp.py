#!/usr/bin/env python3
"""Thử lại MỌI phương pháp app đang có (anh, 13/10/2026) trên 100 và 200 kỳ gần nhất, chạy tiến (mỗi kỳ chỉ dùng dữ liệu trước nó),
rồi chọn phương pháp ổn định để lọc pool chuẩn.
  python build/kiemtra_app.py 400        # lấy 16 PP pool + 20 PP tâm linh từ code app (cần chạy trước, khi dữ liệu đổi)
  python build/kiemtra_pp.py power|mega|loto [--md file] [--json file]

Nhóm phương pháp và cách chấm (chính nó, không so bốc ngẫu nhiên):
  loai : luật loại số — % kỳ đúng (kỳ có số bị loại) + tỉ lệ ra của số bị loại so với bình quân (BQ = số bi/kỳ ÷ tổng số)
  chon : chọn số (tín hiệu +, PP pool top K, tâm linh) — tỉ lệ ra mỗi số so với BQ (×1.10 = ra nhiều hơn BQ 10%)
  it   : tín hiệu "ra ít" (trừ điểm) — tỉ lệ ra so với BQ
  kd   : khẳng định về cả kỳ — % kỳ đúng
Ổn định = đạt ở CẢ 100 kỳ gần VÀ 100 kỳ trước đó (hai nửa của 200 kỳ).
  loai đạt: đúng ≥70% và số bị loại ra ≤ BQ · chon đạt: ra > BQ · it đạt: ra < BQ · kd đạt: đúng ≥70%
Pool chuẩn (cách tính cố định): bỏ hẳn số của các luật loại đạt, thêm dần từ luật mạnh nhất miễn cả nhóm loại gộp vẫn đúng ≥70% kỳ
(luật loại đạt còn lại chuyển thành trừ điểm); điểm mỗi số = Σ (hệ số ra 200 kỳ − 1) của các phương pháp chon/it đạt
chứa số đó; xếp điểm giảm dần. Kiểm chéo: chọn phương pháp + trọng số chỉ từ 200 kỳ CŨ hơn (kỳ −400…−200) rồi chấm pool trên 200 kỳ gần."""
import argparse, json, os, sys
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B)
ap = argparse.ArgumentParser(); ap.add_argument('game', choices=('power', 'mega', 'loto'))
ap.add_argument('--md'); ap.add_argument('--json'); A = ap.parse_args()
GAME = A.game

# ---- goiy.py: nạp phần định nghĩa (tín hiệu, điểm, pool hiện tại, khẳng định) ----
_src = open(os.path.join(B, 'goiy.py'), encoding='utf-8').read()
_argv = sys.argv; sys.argv = ['goiy.py', GAME]
GY = {'__file__': os.path.join(B, 'goiy.py'), '__name__': 'goiy_head'}
exec(compile(_src[:_src.index('# ---------- Đà tổng')], 'goiy.py', 'exec'), GY)
sys.argv = _argv; GY['CUR'] = None
import theodoi as TD
key, NB, KB = TD.GM[GAME]
D = json.load(open(os.path.join(B, 'all_data.json'), encoding='utf-8'))[key]
R = [set(r) for r in D['res']]; T = len(R); BQ = KB / NB
if GAME == 'loto': TD.SESS = GY['SES']
APP = json.load(open(os.path.join(B, 'kiemtra_app.json'), encoding='utf-8'))[GAME]
assert APP['L'] == T, f'kiemtra_app.json có {APP["L"]} kỳ, dữ liệu có {T} kỳ → chạy lại kiemtra_app.py'
W = min(400, len(APP['dates'])); T0 = T - W; KV = int(NB * 0.3 + 0.5)   # top K của PP pool/tâm linh = 30% số (như app)

# ---- danh sách phương pháp: id → dict(nm, nhom, typ, sets[t] | oks[t]) ----
M = {}
def add(i, nm, nhom, typ): M[i] = dict(id=i, nm=nm, nhom=nhom, typ=typ, v={})
for i, l, f in TD.RULES: add('so_' + i, l, 'Luật loại (sổ)', 'loai')
CL_KIND = {}
for i, l, f in TD.CLAIMS:
    kind = f(R, T - 1, TD.ctx(R, NB, T - 1), NB, KB)[0]; CL_KIND[i] = kind
    add('so_' + i, l, 'Khẳng định / nhóm (sổ)', {'atleast': 'kd', 'atmost': 'kd', 'nhomnhieu': 'chon', 'nhomit': 'it'}[kind])
GSIG = {'hot': ('Nóng (c10≥3 hoặc c20≥2×kỳ vọng)', 'chon'), 'ke': ('Kề ±1 kỳ trước', 'chon'), 'de': ('Bóng dễ ra (z>1)', 'chon'),
        'kho': ('Bóng khó ra (z<−1.5)', 'it'), 'chuyen': ('Chuyển kỳ, top 8', 'chon'), 'phien': ('Nóng cùng phiên 100 kỳ, top 8', 'chon'),
        'chin': ('Vắng 11–15 kỳ "chín"', 'chon'), 'g610': ('Vắng 6–10 kỳ', 'it'), 'duoi': ('Cùng đuôi số kỳ trước', 'it'),
        'lap': ('Số vừa ra kỳ trước', 'it'), 'tuan': ('Số kỳ cùng thứ tuần trước', 'it'), 'ben': ('Ra nhiều cả 4 đoạn 25 kỳ', 'chon')}
for k, (nm, typ) in GSIG.items(): add('gy_' + k, nm, 'Tín hiệu gợi ý', typ)
GCL = ('Chẵn/lẻ cân', 'Nhỏ/lớn cân', 'Rải ≥')
for j, lab in enumerate(GCL): add(f'gy_kd{j}', lab + (f'{KB - 2} hàng chục' if j == 2 else f' ({KB // 2}±1)'), 'Khẳng định vé (gợi ý)', 'kd')
for i, x in APP['pm'].items(): add('pm_' + i, f'{i} {x["nm"]}', f'Pool app (top {KV})', 'chon')
for x in APP['kx']:
    add('tl_' + x['id'], x['nm'], 'Tâm linh ' + {'A': '(ngày giờ quay)', 'B': '(bắt số dân gian)', 'C': '(người chơi)', 'D': '(Tarot, Mai Hoa, Kỳ Môn, Tứ trụ)'}[x['g']], 'chon')
add('tl_phieu', f'Tổng phiếu 20 phương pháp tâm linh, top {KV}', 'Tâm linh (tổng phiếu)', 'chon')
NOW_POOL = {}   # pool app hiện tại (goiy.py, không tâm linh) theo kỳ

if GAME == 'loto': TD.SESS = TD.SESS[:T + 1]
for t in range(T0, T + 1):   # t = T: kỳ tới (chỉ lấy tập số, chưa chấm)
    c = TD.ctx(R, NB, t); a = t - T0; NX = t == T
    for i, l, f in TD.RULES: M['so_' + i]['v'][t] = set(f(R, t, c))
    for i, l, f in TD.CLAIMS:
        kind, nums, k = f(R, t, c, NB, KB)
        if NX and kind in ('atleast', 'atmost'): continue
        M['so_' + i]['v'][t] = ((len(set(nums) & R[t]) >= k) if kind == 'atleast' else (len(set(nums) & R[t]) <= k)) if kind in ('atleast', 'atmost') else set(nums)
    fg, s = GY['signals'](t)
    for k in GSIG:
        if k in s: M['gy_' + k]['v'][t] = set(s[k])
    rk = GY['pool_of'](GY['score'](fg, s), s, 20); NOW_POOL[t] = rk
    cl = GY['claims'](t, rk)
    for j, lab in enumerate(GCL if not NX else ()):
        fn = next(c3[2] for c3 in cl if c3[0].startswith(lab)); M[f'gy_kd{j}']['v'][t] = fn(R[t])
    for i, x in APP['pm'].items():
        o = x['ord'][a]
        if o: M['pm_' + i]['v'][t] = set(o[:KV])
    vt = [0] * (NB + 1)
    for x in APP['kx']:
        ns = x['nums'][a]
        if ns is not None:
            M['tl_' + x['id']]['v'][t] = set(ns)
            for n in ns: vt[n] += 1
    M['tl_phieu']['v'][t] = set(sorted(range(1, NB + 1), key=lambda n: (-vt[n], n))[:KV])
M = {i: m for i, m in M.items() if m['v']}

# ---- chấm ----
def stat(m, ts):
    ts = [t for t in ts if t in m['v'] and t < T]
    if m['typ'] == 'kd':
        return dict(n=len(ts), ok=sum(bool(m['v'][t]) for t in ts) / len(ts) * 100 if ts else None)
    ts = [t for t in ts if m['v'][t]]
    sz = sum(len(m['v'][t]) for t in ts); h = sum(len(m['v'][t] & R[t]) for t in ts)
    st = dict(n=len(ts), sz=sz / len(ts) if ts else 0, lift=(h / sz / BQ) if sz else None)
    if m['typ'] == 'loai': st['ok'] = sum(not (m['v'][t] & R[t]) for t in ts) / len(ts) * 100 if ts else None
    if m['typ'] == 'chon': st['any'] = sum(bool(m['v'][t] & R[t]) for t in ts) / len(ts) * 100 if ts else None
    return st

def passes(s):
    """s: chấm 1 khung. Trả về True/False/None (ít mẫu: <15 kỳ áp dụng, hoặc kỳ vọng <10 lần trúng)."""
    if s['n'] < 15: return None
    if 'ok' in s and 'lift' not in s: return s['ok'] >= 70
    if s.get('lift') is None or s['n'] * s['sz'] * BQ < 10 and 'ok' not in s: return None
    if 'ok' in s: return s['ok'] >= 70 and s['lift'] <= 1
    return s['lift'] > 1 if 'any' in s else s['lift'] < 1

def danhgia(win):
    """win = kỳ cuối (không gồm) của khung; chấm 100 gần, 100 trước, 200."""
    h1, h2 = range(win - 100, win), range(win - 200, win - 100)
    out = {}
    for i, m in M.items():
        a, b, c = stat(m, h1), stat(m, h2), stat(m, range(win - 200, win))
        pa, pb = passes(a), passes(b)
        out[i] = dict(s100=a, s100t=b, s200=c, on=(pa is True and pb is True), ms=(pa is None or pb is None))
    return out

def cung(ev, win):
    """Nhóm LOẠI HẲN: thêm dần luật loại đạt (mạnh nhất trước — số bị loại ra ít nhất) miễn cả nhóm gộp vẫn đúng ≥70% số kỳ
    ở cả 100 kỳ gần và 100 kỳ trước của khung. Luật loại đạt còn lại → trừ điểm (hệ số ra − 1)."""
    hard = []
    for i in sorted((i for i, e in ev.items() if e['on'] and M[i]['typ'] == 'loai'), key=lambda i: ev[i]['s200']['lift']):
        ok = all(sum(not (set().union(*[M[j]['v'].get(t, set()) for j in hard + [i]]) & R[t]) for t in h) / len(h) >= 0.7
                 for h in (range(win - 100, win), range(win - 200, win - 100)))
        if ok: hard.append(i)
    return hard

EV = danhgia(T)            # chọn theo 200 kỳ gần (anh dặn)
EV_OLD = danhgia(T - 200)  # để kiểm chéo: chọn chỉ từ kỳ −400…−200
HARD, HARD_OLD = cung(EV, T), cung(EV_OLD, T - 200)

def build(ev, t):
    hard = HARD if ev is EV else HARD_OLD
    ex = set().union(*[M[i]['v'].get(t, set()) for i in hard])
    sc = {n: 0.0 for n in range(1, NB + 1)}
    for i, e in ev.items():
        if e['on'] and i not in hard and M[i]['typ'] != 'kd':
            w = e['s200']['lift'] - 1
            for n in M[i]['v'].get(t, ()): sc[n] += w
    rk = sorted((n for n in sc if n not in ex), key=lambda n: (-sc[n], n))
    return rk, ex

SIZES = {'loto': (6, 8, 10, 12, 15, 18), 'mega': (10, 12, 15, 18, 20), 'power': (10, 12, 15, 18, 20)}[GAME]
def poolstat(rank_of, ts):
    o = {}
    for K in SIZES:
        hs = [len(set(rank_of(t)[:K]) & R[t]) for t in ts]
        o[K] = dict(tb=sum(hs) / len(hs), g=[sum(h >= j for h in hs) / len(hs) * 100 for j in (1, 2, 3, 4)], lift=sum(hs) / len(hs) / (K * BQ))
    return o
LAST = range(T - 100, T); L200 = range(T - 200, T)
EXN = {t: len(build(EV, t)[1]) for t in L200}
PS = {'chuan': {w: poolstat(lambda t: build(EV, t)[0], ts) for w, ts in (('100', LAST), ('200', L200))},
      'cheo': {w: poolstat(lambda t: build(EV_OLD, t)[0], ts) for w, ts in (('100', LAST), ('200', L200))},
      'hien': {w: poolstat(lambda t: NOW_POOL[t], ts) for w, ts in (('100', LAST), ('200', L200))}}
# loại hẳn sai bao nhiêu kỳ (kỳ có ≥1 số trúng nằm trong nhóm bị loại)
EXMISS = {w: sum(bool(build(EV, t)[1] & R[t]) for t in ts) / len(ts) * 100 for w, ts in (('100', LAST), ('200', L200))}

# Số May Mắn Loto
MMR = None
if GAME == 'loto':
    LK = D['lk']
    def mm_gap(t): return {k: next((g for g in range(t) if LK[t - 1 - g] == k), t) for k in range(1, 13)}
    MMM = {'3 số vắng lâu nhất (đang dùng)': lambda t: set(sorted(mm_gap(t), key=lambda k: (-mm_gap(t)[k], k))[:3]),
           'MM kỳ trước + 2 vắng lâu (đề xuất cũ)': lambda t: {LK[t - 1]} | set([k for k in sorted(mm_gap(t), key=lambda k: (-mm_gap(t)[k], k)) if k != LK[t - 1]][:2])}
    MMR = {nm: {w: sum(LK[t] in f(t) for t in ts) / len(ts) * 100 for w, ts in (('100', LAST), ('100t', range(T - 200, T - 100)), ('200', L200))} for nm, f in MMM.items()}

# ---- báo cáo ----
pc = lambda v: '—' if v is None else f'{v:.0f}%'
lf = lambda v: '—' if v is None else f'×{v:.2f}'
fm = lambda xs: ' '.join(f'{n:02d}' for n in sorted(xs)) or '—'
L = [f'## {key} — {len(M)} phương pháp, chấm trên 100 / 200 kỳ gần nhất (đến {D["dates"][-1]}), BQ mỗi số ra {BQ * 100:.1f}%/kỳ\n',
     'Đạt = ổn định ở cả 100 kỳ gần và 100 kỳ trước đó. Luật loại: đúng ≥70% + số bị loại ra ≤ BQ · Chọn số: ra > BQ · Ra ít: ra < BQ · Khẳng định: đúng ≥70%.\n']
TYPN = {'loai': 'Luật loại số', 'chon': 'Chọn số (+)', 'it': 'Tín hiệu ra ít (−)', 'kd': 'Khẳng định'}
for typ in ('loai', 'chon', 'it', 'kd'):
    ids = [i for i in M if M[i]['typ'] == typ]
    if not ids: continue
    L.append(f'\n### {TYPN[typ]} ({len(ids)})\n')
    if typ == 'loai':
        L.append('| Phương pháp | Nhóm | Bỏ TB | Đúng 100 / 200 kỳ | Số bị loại ra (100 / 200 / 100 trước) | Đạt |\n|---|---|---|---|---|---|')
    elif typ == 'kd':
        L.append('| Phương pháp | Nhóm | Đúng 100 / 200 kỳ (100 trước) | Đạt |\n|---|---|---|---|')
    else:
        L.append('| Phương pháp | Nhóm | Cỡ TB | Ra so với BQ: 100 / 200 kỳ (100 trước) | Kỳ có ≥1 số trúng 100 / 200 | Đạt |\n|---|---|---|---|---|---|')
    key_s = (lambda i: -(EV[i]['s200'].get('ok') or 0)) if typ in ('loai', 'kd') else (lambda i: (EV[i]['s200']['lift'] or 0) * (1 if typ == 'chon' else -1) * -1)
    for i in sorted(ids, key=key_s):
        e = EV[i]; a, b, c = e['s100'], e['s100t'], e['s200']
        ok = '✔ đạt' if e['on'] else ('ít mẫu' if e['ms'] else '✘')
        if typ == 'loai':
            L.append(f"| {M[i]['nm']} | {M[i]['nhom']} | {c['sz']:.1f} | {pc(a.get('ok'))} / {pc(c.get('ok'))} | {lf(a['lift'])} / {lf(c['lift'])} / {lf(b['lift'])} | {ok} |")
        elif typ == 'kd':
            L.append(f"| {M[i]['nm']} | {M[i]['nhom']} | {pc(a['ok'])} / {pc(c['ok'])} ({pc(b['ok'])}) | {ok} |")
        else:
            L.append(f"| {M[i]['nm']} | {M[i]['nhom']} | {c['sz']:.1f} | {lf(a['lift'])} / {lf(c['lift'])} ({lf(b['lift'])}) | {pc(a.get('any'))} / {pc(c.get('any'))} | {ok} |")
ON = [i for i in M if EV[i]['on']]
L.append(f'\n### Pool chuẩn — dùng {len(ON)} phương pháp đạt\n')
L.append('- Loại hẳn (cả nhóm đúng ≥70% kỳ): ' + (', '.join(M[i]['nm'] for i in HARD) or '—') + f' · TB bỏ {sum(EXN.values()) / len(EXN):.1f} số/kỳ, kỳ có số trúng bị loại nhầm: {EXMISS["100"]:.0f}% (100 kỳ) / {EXMISS["200"]:.0f}% (200 kỳ)')
L.append('- Cộng điểm: ' + (', '.join(f"{M[i]['nm']} ({lf(EV[i]['s200']['lift'])})" for i in ON if M[i]['typ'] == 'chon') or '—'))
L.append('- Trừ điểm: ' + (', '.join(f"{M[i]['nm']} ({lf(EV[i]['s200']['lift'])})" for i in ON if M[i]['typ'] == 'it' or (M[i]['typ'] == 'loai' and i not in HARD)) or '—'))
L.append('- Khẳng định đạt (dùng lọc vé, không lọc số): ' + (', '.join(M[i]['nm'] for i in ON if M[i]['typ'] == 'kd') or '—'))
L.append('\n| Cỡ pool | Pool chuẩn: TB trúng 100 / 200 kỳ | Kỳ ≥1/≥2/≥3 số (200 kỳ) | Ra so với BQ | Kiểm chéo (chọn từ 200 kỳ cũ): TB 100 / 200 · ×BQ | Pool app hiện tại: TB 100 / 200 · ×BQ |\n|---|---|---|---|---|---|')
for K in SIZES:
    c1, c2 = PS['chuan']['100'][K], PS['chuan']['200'][K]; x1, x2 = PS['cheo']['100'][K], PS['cheo']['200'][K]; h1, h2 = PS['hien']['100'][K], PS['hien']['200'][K]
    L.append(f"| {K} | **{c1['tb']:.2f} / {c2['tb']:.2f}** | {' / '.join(f'{v:.0f}%' for v in c2['g'][:3])} | {lf(c2['lift'])} | {x1['tb']:.2f} / {x2['tb']:.2f} · {lf(x2['lift'])} | {h1['tb']:.2f} / {h2['tb']:.2f} · {lf(h2['lift'])} |")
rk, ex = build(EV, T)
L.append(f'\n**Kỳ tới** — bị loại: {fm(ex)}  ·  xếp hạng: ' + ' '.join(f'{n:02d}' for n in rk[:max(SIZES)]))
if MMR:
    L.append('\n### Số May Mắn (BQ 3 số / 12 = 25%)\n\n| Cách | Trúng 100 kỳ | 100 trước | 200 kỳ |\n|---|---|---|---|')
    for nm, v in MMR.items(): L.append(f"| {nm} | {v['100']:.0f}% | {v['100t']:.0f}% | {v['200']:.0f}% |")
txt = '\n'.join(L) + '\n'
print(txt)
if A.md: open(A.md, 'a', encoding='utf-8').write(txt + '\n')
if A.json:
    json.dump(dict(game=GAME, on=ON, hard=HARD, ev={i: dict(nm=M[i]['nm'], nhom=M[i]['nhom'], typ=M[i]['typ'], **EV[i]) for i in M},
                   pools=PS, exmiss=EXMISS, next=dict(rank=rk, ex=sorted(ex)), mm=MMR), open(A.json, 'w', encoding='utf-8'), ensure_ascii=False)
