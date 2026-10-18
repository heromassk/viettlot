#!/usr/bin/env python3
"""SỐ TÌNH NGHI (anh 17/10/2026: "xem được cả những số tình nghi, tỉ lệ ra thấp hơn các số khác từ cơ sở của app").
Hai nguồn, chỉ dùng cơ sở sẵn có của app, tối đa 100 kỳ:
  1. Luật loại "gần đạt": mọi luật loại trong sổ kiểm chứng (theodoi.RULES) chấm lùi 100 kỳ; luật đúng ≥NG% ở CẢ khung 50 và 100 kỳ
     → đổi 17/10/2026: tình nghi khi số của luật ra ÍT HƠN các số còn lại (tỉ lệ ra mỗi số) ở cả khung 50 và 100 kỳ. Kèm % đúng.
  2. Hạng cuối bảng điểm: mỗi kỳ xếp hạng mọi số theo điểm tín hiệu của app (đúng cách app dựng pool, chỉ dùng dữ liệu trước kỳ đó),
     nhóm B số cuối bảng (≈20% số của game). Đếm tỉ lệ ra của chính từng nhóm hạng 100 kỳ — so các nhóm của app với nhau.
Ghi nghi.json (goiy.py đưa vào app).   python build/nghi.py loto|mega|power"""
import io, os, sys, json, contextlib
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B)
GAME = sys.argv[1]; NG = int(os.environ.get('NG', '65'))
os.environ['HOLD'] = '1'
src = open(os.path.join(B, 'pool_chon.py'), encoding='utf-8').read(); src = src[:src.index('SIG = {t:')]
sys.argv = ['pool_chon.py', GAME]; G = {'__file__': os.path.join(B, 'pool_chon.py'), '__name__': 'x'}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src, 'pool_chon.py', 'exec'), G)
GY, R, T, NB, DS = G['GY'], G['R'], G['T'], G['NB'], G['DS']
R = [set(r) for r in R]
import theodoi as TD
if GAME == 'loto': TD.SESS = ['13' if '13h' in x else '21' for x in DS] + ['13' if '21h' in DS[-1] else '21']

# 1. luật loại gần đạt
KQ = {}
for t in range(T - 100, T + 1):
    c = TD.ctx(R, NB, t)
    for rid, lab, f in TD.RULES:
        try: nums = set(f(R, t, c))
        except Exception: nums = set()
        o = KQ.setdefault(rid, dict(lab=lab, ok=[], h=[], nxt=[]))
        if t == T: o['nxt'] = sorted(nums)
        else:
            o['ok'].append(None if not nums else not (nums & R[t]))
            rest = set(range(1, NB + 1)) - nums
            o['h'].append((len(nums & R[t]), len(nums), len(rest & R[t]), len(rest)))   # số của luật ra / tổng · số còn lại ra / tổng
luat = []
for rid, o in KQ.items():
    pc, rt = {}, {}
    for W in (10, 50, 100):
        a = [x for x in o['ok'][-W:] if x is not None]
        pc[W] = (round(sum(a) * 100 / len(a)), len(a)) if a else (None, 0)
        hs = o['h'][-W:]; hn = sum(x[1] for x in hs); rn = sum(x[3] for x in hs)
        rt[W] = (round(sum(x[0] for x in hs) * 100 / hn, 1) if hn else None, round(sum(x[2] for x in hs) * 100 / rn, 1) if rn else None, hn)
    # tình nghi: số luật chỉ ra ÍT HƠN các số còn lại ở CẢ khung 50 và 100 kỳ (anh: "tỉ lệ ra thấp hơn các số khác"), đủ ≥20 lượt số
    if o['nxt'] and rt[100][2] >= 20 and rt[50][2] >= 10 and rt[50][0] < rt[50][1] and rt[100][0] < rt[100][1]:
        luat.append(dict(id=rid, lab=o['lab'].replace('Bỏ ', ''), nums=o['nxt'], a10=pc[10][0], a50=pc[50][0], a100=pc[100][0],
                         r50=rt[50][0], o50=rt[50][1], r100=rt[100][0], o100=rt[100][1], n100=rt[100][2]))
# 1b. Mega: số kề ±1 của kỳ Power ngày hôm trước (anh 18/10/2026: Mega ra các số này ~10% so với ~14% số khác ở 50/100 kỳ)
if GAME == 'mega':
    import csv, datetime as DT
    PW = {DT.datetime.strptime(r[0], '%d/%m/%Y').date(): set(map(int, r[1:7])) for r in csv.reader(open(os.path.join(B, '..', 'power655_history.csv'), encoding='utf-8'))}
    dd = lambda x: DT.datetime.strptime(x[:10], '%d/%m/%Y').date()
    def pke(d):
        p = PW.get(d - DT.timedelta(1))
        return None if not p else {m for x in p for m in (x - 1, x + 1) if 1 <= m <= NB} - p
    nx = dd(DS[-1]) + DT.timedelta(1)
    while nx.weekday() not in (2, 4, 6): nx += DT.timedelta(1)
    nums = pke(nx); H = []
    for t in range(T - 100, T):
        k = pke(dd(DS[t]))
        if k: H.append((len(k & R[t]), len(k), len((set(range(1, NB + 1)) - k) & R[t]), NB - len(k), not (k & R[t])))
    if nums and len(H) >= 20:
        rt = {}
        for W in (50, 100):
            h = H[-W:]; hn = sum(x[1] for x in h); rn = sum(x[3] for x in h); rt[W] = (round(sum(x[0] for x in h) * 100 / hn, 1), round(sum(x[2] for x in h) * 100 / rn, 1), hn)
        ac = lambda W: round(sum(x[4] for x in H[-W:]) * 100 / len(H[-W:]))
        if rt[50][0] < rt[50][1] and rt[100][0] < rt[100][1]:
            luat.append(dict(id='pkeke', lab='Số kề ±1 của kỳ Power hôm trước', nums=sorted(nums), a10=ac(10), a50=ac(50), a100=ac(100),
                             r50=rt[50][0], o50=rt[50][1], r100=rt[100][0], o100=rt[100][1], n100=rt[100][2]))
luat.sort(key=lambda x: x['r100'] - x['o100'])

# 2. nhóm hạng theo điểm tín hiệu của app
BG = round(NB * 0.2)
def order(t):
    f, s = GY['signals'](t); return GY['pool_of'](GY['score'](f, s, {}), s, NB)
st = {'dau': [0, 0], 'giua': [0, 0], 'cuoi': [0, 0]}; nk = 0
for t in range(T - 100, T):
    od = order(t); L = len(od)
    if L < 3 * BG: continue
    grp = {'dau': od[:BG], 'giua': od[BG:L - BG], 'cuoi': od[L - BG:]}
    for k, g in grp.items(): st[k][0] += len(set(g) & R[t]); st[k][1] += len(g)
    nk += 1
nhom = {k: dict(pct=round(a * 100 / b, 1) if b else None) for k, (a, b) in st.items()}
od = order(T)
cuoi = od[-BG:]

out = dict(den=DS[-1], ng=NG, luat=luat, bg=BG, nk=nk, nhom=nhom, cuoi=sorted(cuoi))
P = os.path.join(B, 'nghi.json'); allc = json.load(open(P, encoding='utf-8')) if os.path.exists(P) else {}
allc[GAME] = out; json.dump(allc, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'## {GAME} — số tình nghi kỳ sau {DS[-1]}')
print('Luật có số ra ít hơn các số còn lại (cả 50 & 100 kỳ):')
for x in luat: print(f"  {x['lab']}: {x['nums']} — số luật ra {x['r50']}%/{x['r100']}% số kỳ, số khác {x['o50']}%/{x['o100']}% (50/100 kỳ) · luật đúng {x['a50']}/{x['a100']}%")
print(f'Nhóm hạng ({BG} số, {nk} kỳ): mỗi số ra ' + ' · '.join(f"{k} {v['pct']}%" for k, v in nhom.items()) + f' số kỳ · nhóm cuối kỳ tới: {sorted(cuoi)}')
