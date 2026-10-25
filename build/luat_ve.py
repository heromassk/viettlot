#!/usr/bin/env python3
"""MỌI luật lọc vé kỳ T ở MỘT chỗ (anh 15/10/2026: "kiểm tra lại hết các luật"): goiy.py dùng để đổi vé, luat_ve.py chạy trực tiếp
để chấm lùi CẢ BỘ — mỗi kỳ t dựng lại bộ luật chỉ bằng dữ liệu trước t, xem kết quả thật có lọt hết không.
  build(R, LK, NB, KB, T, game) -> dict(rules, lienhe, cl, specs)      (R: các kỳ trước T; LK: số may mắn Loto hoặc None)
  ok(B, x, mm, prev, NB, KB) -> bool
  python build/luat_ve.py loto|mega|power [số kỳ chấm=100]"""
import json, os, sys
B_ = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B_)
import khuon as KH, lienhe_dang as LH, dauvet_ltkep as LT


_NF = ('ac', 'span', 'dmin', 'dmax', 'duoi', 'tduoi', 'm3max', 'm3min')
NEWF = {'mega': _NF, 'power': _NF, 'loto': _NF}   # thử trên Mega trước (anh 17/10/2026)


def _ev(x, mm): return sum(v % 2 == 0 for v in x) + ((mm % 2 == 0) if mm else 0)


def nhom(r, lienhe=False):
    """nhóm của một luật (để chấm & chọn theo nhóm)"""
    if lienhe: return 'liên hệ: ' + r['lab'].split(' →')[0].split(' kỳ trước')[0]
    g = r.get('id') or r['lab']
    if g.startswith(('hc', 'bh')): return 'hàng (' + g[:2] + ')'
    if g.startswith('comat'): return 'comat'
    return g.rstrip('0123456789') if g[:3] in ('ton', 'le7', 'le8', 'nho') else g


def _sel(game):
    P = os.path.join(B_, 'luat_ve.json')
    return (json.load(open(P, encoding='utf-8')).get(game) or {}).get('nhom') if os.path.exists(P) else None


def build(R, LK, NB, KB, T, game, all_rules=False):
    """all_rules=True: lấy mọi luật ứng viên (để chấm lùi); mặc định chỉ nhóm đã chọn trong luat_ve.json"""
    R = [set(r) for r in R[:T]]
    sums = [sum(r) + (LK[i] if LK else 0) for i, r in enumerate(R)]
    mid = KB * (NB + 1) / 2 + (6.5 if LK else 0)   # mốc giữa của đúng thứ đang cộng (Loto: dãy 6 số, MM 1–12 TB 6,5)
    K = KH.build(R, LK, NB, KB, T)
    rules = list(K['rules'])
    lienhe = LH.active(R, LK, NB, KB, T, game) + LT.active(R, NB, T)
    # Số kép nhiều nhất 1 số (anh 15/10: "11 22 33 gợi ý ngu như bò")
    kp = lambda t: sum(1 for v in R[t] if v % 11 == 0) <= 1
    a = [round(sum(kp(t) for t in range(T - W, T)) / W * 100) for W in (50, 100)]
    if min(a) >= 70 and not any(r.get('id') == 'kep1' for r in rules):
        rules.append(dict(id='kep1', lab='Số kép (11, 22, 33…) nhiều nhất 1 số', spec=dict(k='rng', f='kep', lo=0, hi=1, neg=False), a50=a[0], a100=a[1], n100=100))
    # Cặp lộn trong cùng kỳ (anh 15/10: "các số lộn trong 1 kỳ"): kỳ này không có cặp lộn (12–21, 13–31…)
    cl0 = lambda t: KH.check(dict(k='lon', max=0), sorted(R[t]), None, None, NB, KB)
    a = [round(sum(cl0(t) for t in range(T - W, T)) / W * 100) for W in (50, 100)]
    if min(a) >= 70:
        rules.append(dict(id='lon0', lab='Không có cặp số lộn trong kỳ (12–21, 13–31…)', spec=dict(k='lon', max=0), a50=a[0], a100=a[1], n100=100))
    # Nhịp riêng của số vừa ra (anh 15/10: "50 về 1 kỳ thì kỳ sau gần như nghỉ"): số kỳ trước mà 20 lần ra gần nhất của chính nó
    # chỉ ra lại ngay ≤1 lần (≥8 lần ra) → vé không chứa. Chấm cấp kỳ: kỳ không có số nào như vậy ra lại.
    def nr(t):
        o = set()
        for n in R[t - 1]:
            ap = [u for u in range(max(0, t - 100), t - 1) if n in R[u]][-20:]
            if len(ap) >= 8 and sum(n in R[u + 1] for u in ap) <= 1: o.add(n)
        return o
    a = [round(sum(not (nr(t) & R[t]) for t in range(T - W, T) if nr(t)) / max(1, sum(1 for t in range(T - W, T) if nr(t))) * 100) for W in (50, 100)]
    cur = nr(T)
    if cur and min(a) >= 70:
        rules.append(dict(id='nhiprieng', lab=f"Vé không chứa số vừa ra mà nhịp riêng hay nghỉ ({' '.join(f'{n:02d}' for n in sorted(cur))})",
                          spec=dict(k='tranh', nums=sorted(cur)), a50=a[0], a100=a[1], n100=100))
    # Tổng thường gặp (khoảng 80% giữa của 200 kỳ trước) — anh 15/10/2026: vé tổng 69 trong khi app ghi "thường gặp 70–124"
    def band(t):
        v = sorted(sums[t - 100:t]); return v[10], v[90]
    a = [round(sum(band(t)[0] <= sums[t] <= band(t)[1] for t in range(T - W, T)) / W * 100) for W in (50, 100)]
    lo80, hi80 = band(T)
    if min(a) >= 70:
        rules.append(dict(id='tongthuong', lab=f'Tổng trong khoảng thường gặp {lo80}–{hi80} (80% kỳ)', spec=dict(k='tong', lo=lo80, hi=hi80), a50=a[0], a100=a[1], n100=100))
    # Đặc điểm dạng mới (anh 17/10/2026, tra 15 ngôn ngữ): AC, biên độ, delta nhỏ/lớn nhất, số đuôi khác nhau, tổng đuôi, chia dư 3.
    # Khoảng hẹp nhất phủ ≥90% của 100 kỳ trước (chỉ dữ liệu trước kỳ t). Thử trước ở game trong NEWF.
    if game in NEWF:
        EX = [KH.ext(sorted(r)) for r in R]
        def bandf(f, t, p=0.9):
            v = sorted(EX[u][f] for u in range(t - 100, t)); n = len(v); m = int(n * p + 0.999); best = None
            for i in range(0, n - m + 1):
                w = v[i + m - 1] - v[i]
                if best is None or w < best[0]: best = (w, v[i], v[i + m - 1])
            return best[1], best[2]
        TEN = dict(ac='Độ rải AC', span='Biên độ (lớn nhất − nhỏ nhất)', dmin='Khoảng cách nhỏ nhất giữa 2 số liền', dmax='Khoảng cách lớn nhất giữa 2 số liền',
                   duoi='Số đuôi khác nhau', tduoi='Tổng đuôi', m3max='Nhóm chia 3 đông nhất', m3min='Nhóm chia 3 ít nhất')
        for f in NEWF[game]:
            a = [round(sum(bandf(f, t)[0] <= EX[t][f] <= bandf(f, t)[1] for t in range(T - W, T)) / W * 100) for W in (50, 100)]
            lo, hi = bandf(f, T)
            if min(a) >= 70:
                rules.append(dict(id='x' + f, lab=f'{TEN[f]} trong {lo}–{hi} (≥90% của 100 kỳ)', spec=dict(k='rng', f=f, lo=lo, hi=hi, neg=False), a50=a[0], a100=a[1], n100=100))
    # Nhịp tăng/giảm của tổng: đã đi cùng chiều k kỳ liền → kỳ sau đảo; ưu tiên "qua mốc giữa" (anh: "giảm là bé hơn 168")
    ud = lambda t: sums[t] > sums[t - 1]
    def run(t):
        k = 1
        while k < 10 and sums[t - 1 - k] != sums[t - 2 - k] and ud(t - 1 - k) == ud(t - 1): k += 1
        return min(k, 3)
    kn, up = run(T), ud(T - 1)
    rt = {}
    for nm, f in (('mid', lambda t: (sums[t] < mid) if up else (sums[t] > mid)), ('prev', lambda t: ud(t) != up)):
        rt[nm] = []
        for W in (50, 100):
            ts = [t for t in range(T - W, T) if run(t) == kn and sums[t - 1] != sums[t - 2] and ud(t - 1) == up]
            rt[nm].append((sum(f(t) for t in ts), len(ts)))
    pick = next((nm for nm in ('mid', 'prev') if kn >= 2 and all(n >= 4 and k * 100 >= 70 * n for k, n in rt[nm])), None)
    if pick:
        if pick == 'mid':
            lo, hi = (0, int(mid - 0.01)) if up else (int(mid) + 1, 9999); lab = f"{'<' if up else '>'} mốc giữa {mid:g}"
        else:
            lo, hi = (0, sums[-1] - 1) if up else (sums[-1] + 1, 9999); lab = f"{'<' if up else '>'} {sums[-1]}"
        rules.append(dict(id='nhiptong', lab=f"Tổng đã {'tăng' if up else 'giảm'} {kn if kn < 3 else '≥3'} kỳ liền → kỳ này {'giảm' if up else 'tăng'}: tổng {lab}",
                          spec=dict(k='tong', lo=lo, hi=hi), a50=round(rt[pick][0][0] * 100 / rt[pick][0][1]), a100=round(rt[pick][1][0] * 100 / rt[pick][1][1]), n100=rt[pick][1][1]))
    # Giới hạn tổng theo phía kỳ trước (anh: "có dấu vết giới hạn dưới không"): cao → ≥ 10% thấp nhất của các kỳ sau kỳ cao (200 kỳ); thấp → ≤ 90%
    def bd(t):
        h = sums[t - 1] > mid; v = sorted(sums[u] for u in range(t - 100, t) if (sums[u - 1] > mid) == h)
        return h, (v[len(v) // 10] if h else v[len(v) * 9 // 10])
    bk = []
    for W in (50, 100):
        bk.append(sum((sums[t] >= bd(t)[1]) if bd(t)[0] else (sums[t] <= bd(t)[1]) for t in range(T - W, T)) * 100 // W)
    h, L = bd(T)
    if min(bk) >= 70:
        rules.append(dict(id='bientong', lab=f"Kỳ trước tổng {'cao' if h else 'thấp'} ({sums[-1]}) → kỳ này tổng {'≥' if h else '≤'} {L}",
                          spec=dict(k='tong', lo=L, hi=9999) if h else dict(k='tong', lo=0, hi=L), a50=bk[0], a100=bk[1], n100=100))
    # Chẵn–lẻ cần tránh (anh 14/10): 3-3 sau 2 kỳ liền 3-3; Power tránh kiểu kỳ trước; toàn chẵn / toàn lẻ
    nd = KB + (1 if LK else 0); half = nd // 2
    e1, e2 = _ev(R[T - 1], LK[T - 1] if LK else None), _ev(R[T - 2], LK[T - 2] if LK else None)
    cl = {0, nd}
    if e1 == e2 == half: cl.add(half)
    if game == 'power': cl.add(e1)
    S = None if all_rules else _sel(game)
    if S is not None:
        rules = [r for r in rules if nhom(r) in S]; lienhe = [r for r in lienhe if nhom(r, True) in S]
        if 'chẵn–lẻ tránh' not in S: cl = set()
    return dict(rules=rules, lienhe=lienhe, cl=cl, specs=[r['spec'] for r in rules] + [r['spec'] for r in lienhe], khuon=K)


def chon_nhom(REC, PIN=(), ga=70, cb=85):
    """Chọn nhóm luật vé từ kết quả từng kỳ REC (list {nhóm: đúng?}). Nhóm đúng ≥ga% (≥5 lần), không sai từ một nửa ở 10 kỳ gần
    (khi áp ≥3 lần); thêm dần khi cả bộ vẫn lọt ≥cb% ở 10, 50, 100 kỳ. cb=85: chấm lùi cao hơn chấm tiến ~10–15 điểm (anh 15/10/2026)."""
    per = {}
    for g in REC:
        for k, v in g.items(): a = per.setdefault(k, [0, 0]); a[1] += 1; a[0] += v
    W2 = min(100, len(REC))
    pas = lambda S, W: sum(all(v for k, v in g.items() if k in S) for g in REC[-W:]) * 100 // W
    order = sorted(per, key=lambda k: (-per[k][0] / per[k][1], -per[k][1]))
    def r10(k):
        xs = [g[k] for g in REC[-10:] if k in g]; return sum(not v for v in xs), len(xs)
    bo = {k for k in per if r10(k)[1] >= 3 and r10(k)[0] * 2 >= r10(k)[1]}
    S = {k for k in PIN if k in per}
    for k in order:
        if per[k][1] < 5 or per[k][0] * 100 < ga * per[k][1] or k in bo: continue
        # 17/10/2026 (anh: "tỉ lệ đều tốt mà lại làm tổng thể yếu đi"): khung nào cả bộ đang ≥cb thì phải giữ ≥cb; khung nào đang dưới cb
        # (do luật ghim) thì luật mới chỉ cần KHÔNG làm tụt thêm — trước đây luật đúng 100% cũng bị loại khi bộ ghim đã dưới cb
        if all(pas(S | {k}, W) >= min(cb, pas(S, W)) for W in (10, 50, W2)): S.add(k)
    return S | set(PIN), bo, r10


def tien(REC, PIN=(), ga=70, cb=85):
    """CHẤM TIẾN cách chọn: chọn bằng REC[:i], thử 10 kỳ sau (i = 50, 60, …, 90). Trả (% lọt, số kỳ lọt trong 10 kỳ cuối)."""
    ok = []
    for i in range(50, len(REC), 10):
        S, _, _ = chon_nhom(REC[:i], PIN, ga, cb); ok += [all(v for k, v in g.items() if k in S) for g in REC[i:i + 10]]
    return (sum(ok) * 100 // len(ok) if ok else None), sum(ok[-10:])


def ok(B, x, mm, prev, NB, KB):
    return _ev(x, mm) not in B['cl'] and all(KH.check(sp, x, mm, prev, NB, KB) for sp in B['specs'])


if __name__ == '__main__':
    from collections import defaultdict
    GAME = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    key, NB, KB = {'power': ('power655', 55, 6), 'mega': ('mega645', 45, 6), 'loto': ('loto535', 35, 5)}[GAME]
    D = json.load(open(os.path.join(B_, 'all_data.json'), encoding='utf-8'))[key]
    R = [set(r) for r in D['res']]; LK = D.get('lk') if GAME == 'loto' else None; T = len(R)
    # Kết quả chấm từng kỳ lưu ra đĩa, kỳ cũ không chấm lại (anh 23/10/2026). Dấu vân tay kỳ t = toàn bộ dữ liệu đến hết kỳ t;
    # code luật (luat_ve, khuon, lienhe_dang, dauvet_ltkep) đổi thì xoá hết. Kết quả y hệt chấm lại từ đầu.
    import hashlib, pickle
    CP = os.path.join(B_, '_tmp', f'luat_ve_rec_{GAME}.pkl')
    VER = hashlib.md5(b''.join(open(os.path.join(B_, f), 'rb').read() for f in ('luat_ve.py', 'khuon.py', 'lienhe_dang.py', 'dauvet_ltkep.py'))).hexdigest()
    h = hashlib.md5(); FP = []
    for i in range(T): h.update(repr((sorted(R[i]), LK[i] if LK else None)).encode()); FP.append(h.hexdigest())
    try:
        _c = pickle.load(open(CP, 'rb')); OLD = _c['rec'] if _c.get('ver') == VER else {}
    except Exception: OLD = {}
    REC = []   # mỗi kỳ: {nhóm: đúng hết các luật của nhóm đó?}
    for t in range(T - N, T):
        if FP[t] in OLD: REC.append(OLD[FP[t]]); continue
        Bt = build(R, LK, NB, KB, t, GAME, all_rules=True); x = sorted(R[t]); mm = LK[t] if LK else None; prev = sorted(R[t - 1])
        g = {}
        for r, lh in [(r, False) for r in Bt['rules']] + [(r, True) for r in Bt['lienhe']]:
            k = nhom(r, lh); g[k] = g.get(k, True) and KH.check(r['spec'], x, mm, prev, NB, KB)
        g['chẵn–lẻ tránh'] = _ev(x, mm) not in Bt['cl']
        REC.append(g)
    OLD.update({FP[t]: g for t, g in zip(range(T - N, T), REC)}); keep = set(FP[-200:])
    pickle.dump(dict(ver=VER, rec={k: v for k, v in OLD.items() if k in keep}), open(CP + '.tmp', 'wb')); os.replace(CP + '.tmp', CP)
    per = defaultdict(lambda: [0, 0])
    for g in REC:
        for k, v in g.items(): per[k][1] += 1; per[k][0] += v
    pas = lambda S, W: sum(all(v for k, v in g.items() if k in S) for g in REC[-W:]) * 100 // W
    print(f'## {GAME} — chấm lùi CẢ BỘ luật lọc vé, {N} kỳ đến {D["dates"][-1]} (mỗi kỳ dựng luật chỉ bằng dữ liệu trước nó)\n')
    ALL = set(per)
    print(f'- Mọi luật ứng viên ghép lại: kết quả thật lọt hết {pas(ALL, 50)}% (50 kỳ) · {pas(ALL, 100)}% (100 kỳ)\n')
    print('| Nhóm luật | Đúng / số lần áp (áp tiến) | % |\n|---|---|---|')
    order = sorted(per, key=lambda k: (-per[k][0] / per[k][1], -per[k][1]))
    for k in order: print(f'| {k} | {per[k][0]}/{per[k][1]} | {per[k][0] * 100 // per[k][1]}% |')
    PIN = {x for x in os.environ.get('PIN', '').split(',') if x}   # nhóm anh chốt giữ (Power: nhiptong,bientong,nhiprieng — anh 15/10/2026)
    CB = int(os.environ.get('LV_CB', '85'))
    S, BO10, r10 = chon_nhom(REC, PIN, cb=CB)
    TIEN, TIEN10 = tien(REC, PIN, cb=CB)
    print(f'\n### Bộ chọn: {len(S)} nhóm — chấm lùi lọt {pas(S, 10)}% (10 kỳ) · {pas(S, 50)}% (50 kỳ) · {pas(S, 100)}% (100 kỳ) · **chấm tiến {TIEN}%** (50 kỳ, chọn lại mỗi 10 kỳ; 10 kỳ cuối {TIEN10}/10)\n')
    if BO10: print('Tạm bỏ vì sai nhiều ở 10 kỳ gần: ' + ', '.join(f'{k} (sai {r10(k)[0]}/{r10(k)[1]})' for k in sorted(BO10)) + '\n')
    for k in order:
        if k in S: print(f'- {k} ({per[k][0]}/{per[k][1]})')
    if os.environ.get('NOSAVE') != '1':
        P = os.path.join(B_, 'luat_ve.json'); allc = json.load(open(P, encoding='utf-8')) if os.path.exists(P) else {}
        allc[GAME] = dict(nhom=sorted(S | PIN), pin=sorted(PIN), pass10=pas(S, 10), pass50=pas(S, 50), pass100=pas(S, 100), tien=TIEN, tien10=TIEN10, bo10=sorted(BO10), rec=REC, dates=D['dates'][T - N:], den=D['dates'][-1],
                          per={k: per[k] for k in order}); json.dump(allc, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('\nĐã ghi luat_ve.json')
