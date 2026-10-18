#!/usr/bin/env python3
"""CHẤM TIẾN cách chọn pool (anh 15/10/2026: "pool dạo này lệch khá nhiều" — đáng tin = suy luận từ dữ liệu cũ và nó đúng).
Cứ mỗi 10 kỳ (b = T−100, T−90, …, T−10): chọn lại bộ cộng/trừ điểm từng cỡ pool đúng như pool_chon.py nhưng CHỈ bằng 100 kỳ trước b,
rồi dựng pool (pool_app.make: + luật ghim, giới hạn kép, luật hàng) cho 10 kỳ b … b+9 và chấm. So với pool KHÔNG cộng điểm (chỉ tín hiệu).
Không kỳ nào dùng dữ liệu cũ hơn 100 kỳ để chọn. Riêng từng game.
  python build/pool_tien.py loto|mega|power"""
import io, os, sys, contextlib, json
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B)
GAME = sys.argv[1]
os.environ['HOLD'] = '1'   # pool_chon: dựng tín hiệu / ứng viên cho 200 kỳ để mỗi khối có đủ 100 kỳ phía trước
src = open(os.path.join(B, 'pool_chon.py'), encoding='utf-8').read(); src = src[:src.index('CHON = {}; STAT = {}')]
sys.argv = ['pool_chon.py', GAME]; G = {'__file__': os.path.join(B, 'pool_chon.py'), '__name__': 'x'}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src, 'pool_chon.py', 'exec'), G)
full = open(os.path.join(B, 'pool_chon.py'), encoding='utf-8').read()
st0 = full.index('START = {'); exec(full[st0:full.index(chr(10), full.index('[GAME]', st0))], G)   # bộ khởi đầu của pool_chon.py
import pool_app as PA
GY, TS, R, T, NUMS, SIG, DS = G['GY'], G['TS'], G['R'], G['T'], G['NUMS'], G['SIG'], G['DS']
stat, CAND, START, STEPS, SELW = G['stat'], G['CAND'], G['START'], G['STEPS'], tuple(G['SELW'])
KC = PA.kepcap(GAME)

def chon_tai(b):
    """bộ cộng điểm từng cỡ, chọn chỉ bằng 100 kỳ trước b (đúng thuật toán pool_chon.py + điều kiện 10 kỳ)"""
    out = {}
    for K in PA.KS:
        res = []
        for start in ([], START):
            cur = [c for c in start if c[0] in NUMS[TS[0]]]; bs = stat(cur, K, b)
            for _ in range(STEPS):
                best = None
                for c in CAND:
                    if any(c[0] == x[0] for x in cur): continue
                    o = stat(cur + [c], K, b)
                    if any(o[W][j] < bs[W][j] for W in SELW + (10,) for j in (0, 1)): continue
                    gain = (sum(o[W][1] - bs[W][1] for W in SELW), sum(o[W][0] - bs[W][0] for W in SELW))
                    if gain > (0, 0) and (best is None or gain > best[0]): best = (gain, c, o)
                if not best: break
                cur.append(best[1]); bs = best[2]
            res.append(((sum(bs[W][1] for W in SELW), sum(bs[W][0] for W in SELW)), cur))
        out[str(K)] = [list(x) for x in max(res, key=lambda x: x[0])[1]]
    return out

TT = list(range(T - 100, T)); BLK = list(range(T - 100, T, 10))
PO = {}; P0 = {}; SETS = []
for b in BLK:
    C = chon_tai(b); SETS.append((DS[b], C))
    for t in range(b, b + 10):
        f, s = SIG[t]
        PO[t] = PA.make(GY, R, t, f, s, NUMS[t], GAME, C=C, KC=KC)
        P0[t] = PA.make(GY, R, t, f, s, NUMS[t], GAME, C={}, KC=KC)
    print(f'  khối {DS[b]}: đã chọn', file=sys.stderr, flush=True)
def st(P, K, W):
    hs = [len(set(P[t][K]) & R[t]) for t in TT[-W:]]
    return sum(hs) / W, sum(h >= 3 for h in hs) * 100 // W, sum(h >= 4 for h in hs) * 100 // W
print(f'## {GAME} — CHẤM TIẾN cách chọn pool, 100 kỳ đến {DS[-1]} (chọn lại mỗi 10 kỳ chỉ bằng 100 kỳ trước đó)\n')
print('Ô: TB số trúng · % kỳ ≥3 số · % kỳ ≥4 số\n')
print('| Pool | Cách app (chọn bộ cộng điểm) 10 / 50 / 100 kỳ | Không cộng điểm 10 / 50 / 100 kỳ |\n|---|---|---|')
f = lambda x: f'{x[0]:.2f} · {x[1]}% · {x[2]}%'
OUT = {}
for K in PA.KS:
    a = [st(PO, K, W) for W in (10, 50, 100)]; z = [st(P0, K, W) for W in (10, 50, 100)]
    OUT[str(K)] = dict(app=a, khong=z)
    print(f"| {K} | {' / '.join(f(x) for x in a)} | {' / '.join(f(x) for x in z)} |")
# độ ổn định bộ chọn
print('\n### Bộ cộng điểm pool 18 qua các khối\n')
for d, C in SETS:
    lab = ', '.join(nm.replace('TL: ', '') + ' ' + format(w, '+g') for nm, w in C.get('18', [])) or 'không cộng gì'
    print(f'- từ {d}: {lab}')
P = os.path.join(B, 'pool_tien.json'); allc = json.load(open(P, encoding='utf-8')) if os.path.exists(P) else {}
allc[GAME] = dict(den=DS[-1], stat=OUT, sets=SETS); json.dump(allc, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
