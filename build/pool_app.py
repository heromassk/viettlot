#!/usr/bin/env python3
"""Pool từng cỡ ĐÚNG như app chọn (anh 15/10/2026: "rà xem cách app chọn pool có vấn đề gì"). goiy.py và phần chấm lùi dùng chung hàm này:
  1. điểm tín hiệu + bộ cộng/trừ điểm RIÊNG của cỡ đó (pool_chon.json: 'chon' hoặc 'chon50' — bộ nào hơn ở ≥4 rồi ≥3 số, 50 & 100 kỳ)
  2. Power pool 10/15: hàng đang "ra nhiều 10 kỳ" chỉ giữ 1 số (hang_chuky.py)
  3. giới hạn số kép trong pool ở cỡ đã chấm có tăng (kep_pool.json)
  make(GY, R, t, f, s, cand, game, extra0=None) -> {K: [số theo thứ hạng]}
  python build/pool_app.py loto|mega|power     # chấm lùi 100 kỳ, ghi pool_thuc.json (app hiện ở "Pool trúng bao nhiêu")"""
import json, os, sys
B = os.path.dirname(os.path.abspath(__file__))
KS = (10, 12, 15, 18, 20, 25)


def ks_of(game):
    """cỡ pool theo game: Loto tối đa 25 (anh 16/10/2026); Power, Mega thêm 30, 35 để xem tỉ lệ trúng 5/6 số"""
    return KS if game == 'loto' else KS + (30, 35)
HANGCAP = {'power': ((5, 1, 2, 4), (10, 15))}
# "Khó ra" (100 kỳ) KHÔNG trừ với số đang nóng lại (≥2/10 hoặc ≥3/20 kỳ) — anh 15/10/2026 ("sao lại loại 05"). Chỉ cỡ đã chấm tăng
# ≥3 / ≥4 số ở 50 & 100 kỳ mà không giảm (Loto 10: ≥3 13→14 /50 kỳ; 12: ≥4 8→9 /50, 15→16 /100). Cỡ lớn hơn giảm → giữ trừ.
KHO_NONG = {'loto': {10, 12}}
# Luật ghim cứng theo cỡ pool (anh 15/10/2026: "vẫn thấy có 50"): luôn cộng thêm vào bộ cộng điểm đã chọn; đã chấm không làm giảm ≥3 / ≥4
# số ở 50 & 100 kỳ (Power 10, 15 giữ nguyên; 12 tăng). Pool 18/20/25 không ghim vì loại vào thì mất kỳ ≥4.
GHIM = {}   # 16/10/2026: anh chọn bỏ hẳn luật nhịp riêng khỏi pool Power (chấm 10/50 kỳ thua nhẹ); vé vẫn không chứa các số này


# Chỉ giữ bộ cộng điểm ở cỡ CHẤM TIẾN có lợi (pool_tien.py, anh 15/10/2026: "pool dạo này lệch"): chọn lại mỗi 10 kỳ bằng 100 kỳ trước,
# chấm 10 kỳ sau. Loto, Power: không cỡ nào hơn pool không cộng điểm → bỏ. Mega: pool 18 và 25 hơn ở cả 10/50/100 kỳ → giữ.
# Trộn Markov RIÊNG theo cỡ pool (anh 15/10/2026: "markov đang dùng nhỉ"): Loto không trộn Markov chung; riêng pool 15 trộn Markov bộ số
# bậc 4 (mk4) — tăng kỳ ≥3 / ≥4 số ở cả 10 / 50 / 100 kỳ (2·0→5·2, 21·7→25·9, 43·17→49·19). Cỡ khác giảm ≥4 → không trộn.
MIXK = {'loto': {15: ['mk4'], 18: ['mk4']}}   # 18: anh chọn áp 16/10/2026 (≥3 số 55→64 / 100 kỳ, ≥4 29→28)
TIEN_GIU = {'loto': set(), 'power': set(), 'mega': {'18', '25'}}


def chon(game):
    """bộ cộng/trừ điểm của từng cỡ + nhãn chọn theo"""
    P = os.path.join(B, 'pool_chon.json')
    J = json.load(open(P, encoding='utf-8')).get(game, {}) if os.path.exists(P) else {}
    C = dict(J.get('chon') or {}); theo = {}
    sc = lambda st: (st['50'][1] * 2 + st['100'][1], st['50'][0] * 2 + st['100'][0])
    for K in list(C):
        a, b = (J.get('stat') or {}).get(K), (J.get('stat50') or {}).get(K)
        theo[K] = '50 & 100 kỳ'
        if a and b and sc(b) > sc(a): C[K] = J['chon50'][K]; theo[K] = '50 kỳ'
    if game in TIEN_GIU:
        for K in list(C):
            if K not in TIEN_GIU[game]: C[K] = []; theo[K] = 'không cộng (chấm tiến không lợi)'
    return C, theo


def kepcap(game):
    P = os.path.join(B, 'kep_pool.json')
    return (json.load(open(P, encoding='utf-8')).get(game) or {}).get('cap', {}) if os.path.exists(P) else {}


def hang_on(R, t, NB, game):
    hc = HANGCAP.get(game)
    if not hc: return []
    R = [set(r) for r in R]
    NH = lambda h: {n for n in range(1, NB + 1) if n // 10 == h}
    c10 = lambda h, u: sum(len(R[w] & NH(h)) for w in range(u - 10, u))
    on = []
    for h in hc[0]:
        xs = sorted(c10(h, u) for u in range(t - 100, t))
        if c10(h, t) >= xs[len(xs) * 4 // 5]: on.append(h)
    return on


def make(GY, R, t, f, s, cand, game, extra0=None, C=None, KC=None):
    """cand: {tên ứng viên: tập số} ở kỳ t (dauvet_ngay.cand_nums + 'TL: …'); extra0: điểm cộng sẵn (linh cảm anh)"""
    NB = GY['NB']; C = C if C is not None else chon(game)[0]; KC = KC if KC is not None else kepcap(game)
    hc = HANGCAP.get(game); on = hang_on(R, t, NB, game) if hc else []
    out = {}
    for K in ks_of(game):
        e = dict(extra0 or {})
        have = {nm for nm, _ in C.get(str(K), [])}
        ex = set()   # trọng số ≤ −20 = LOẠI HẲN khỏi pool (trừ điểm không đủ khi điểm trộn với Markov — Power, Mega)
        for nm, w in C.get(str(K), []) + [g for g in GHIM.get(game, {}).get(K, []) if g[0] not in have]:
            if w <= -20: ex |= set(cand.get(nm, ())); continue
            for n in cand.get(nm, ()): e[n] = e.get(n, 0) + w
        sK = s
        if K in MIXK.get(game, {}) and 'MIXF' in GY: sK = dict(s); sK['_mix'] = list(s.get('_mix') or []) + [GY['MIXF'][m](t) for m in MIXK[game][K]]
        if K in KHO_NONG.get(game, ()): sK = dict(sK); sK['kho'] = {n for n in s['kho'] if f[n]['c10'] < 2 and f[n]['c20'] < 3}
        order = [n for n in GY['pool_of'](GY['score'](f, sK, e), sK, NB) if n not in ex]
        cap = KC.get(str(K)); hcap = bool(hc and K in hc[1])
        if cap is None and not hcap:
            out[K] = order[:min(K, NB - len(s['vang']))]; continue
        o, cnt, nk = [], {}, 0
        for n in order:
            if hcap and n // 10 in on and cnt.get(n // 10, 0) >= 1: continue
            if cap is not None and n % 11 == 0:
                if nk >= cap: continue
                nk += 1
            cnt[n // 10] = cnt.get(n // 10, 0) + 1; o.append(n)
            if len(o) == K: break
        out[K] = o
    return out


if __name__ == '__main__':
    GAME = sys.argv[1]
    src = open(os.path.join(B, 'pool_chon.py'), encoding='utf-8').read(); src = src[:src.index('CHON = {}; STAT = {}')]
    sys.argv = ['pool_chon.py', GAME]; G = {'__file__': os.path.join(B, 'pool_chon.py'), '__name__': 'x'}
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()): exec(compile(src, 'pool_chon.py', 'exec'), G)
    GY, TS, R, T, NUMS, SIG, DS = G['GY'], G['TS'], G['R'], G['T'], G['NUMS'], G['SIG'], G['DS']
    C, theo = chon(GAME); KC = kepcap(GAME)
    PT = {t: make(GY, R, t, SIG[t][0], SIG[t][1], NUMS[t], GAME, C=C, KC=KC) for t in TS}
    res = {}
    print(f'## {GAME} — pool ĐÚNG như app chọn, chấm lùi 100 kỳ đến {DS[-1]} (mỗi kỳ chỉ dùng dữ liệu trước nó)\n')
    print('| Pool | TB số trúng 50 / 100 kỳ | ≥2 số | ≥3 số | ≥4 số (10 / 20 / 50 / 100 kỳ) |\n|---|---|---|---|---|')
    for K in ks_of(GAME):
        r = {}
        for W in (10, 20, 50, 100):
            hs = [len(set(PT[t][K]) & R[t]) for t in range(T - W, T)]
            r[W] = [round(sum(hs) / W, 2)] + [round(sum(h >= j for h in hs) * 100 / W) for j in (2, 3, 4, 5, 6)]
        res[str(K)] = r
        f3 = lambda j: ' / '.join(f'{r[W][j]}%' for W in (10, 20, 50, 100))
        print(f"| {K} | {r[50][0]} / {r[100][0]} | {f3(1)} | {f3(2)} | {f3(3)} |")
    P = os.path.join(B, 'pool_thuc.json'); allc = json.load(open(P, encoding='utf-8')) if os.path.exists(P) else {}
    LKs = G['GY']['D'].get('lk') or []
    hist = [dict(d=DS[t], r=sorted(R[t]), lk=(LKs[t] if GAME == 'loto' and t < len(LKs) else None), pools={str(K): PT[t][K] for K in ks_of(GAME)}) for t in range(T - 20, T)][::-1]
    hits = {str(K): [len(set(PT[t][K]) & R[t]) for t in range(T - 100, T)] for K in ks_of(GAME)}   # số trúng từng kỳ (100 kỳ) — app tự tính lại khung 10/20/50/100 khi anh nhập kết quả tay (17/10/2026)
    allc[GAME] = dict(den=DS[-1], stat=res, theo=theo, hist=hist, hits=hits)   # hist: pool THẬT 20 kỳ gần (anh 15/10/2026), mới nhất trước
    json.dump(allc, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'\nĐã ghi pool_thuc.json [{GAME}]')
