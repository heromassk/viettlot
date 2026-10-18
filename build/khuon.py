"""Khuôn DẠNG kỳ tới (anh 14/10/2026): ghép các luật dạng đã chấm lùi thành một khuôn cho kỳ tới, RIÊNG từng game.
Luật ứng viên (mỗi kỳ t chỉ dùng dữ liệu trước t):
  - Chuyển hàng: kỳ trước hàng i ra c số → kỳ này hàng i ≤1 / ≥1 số
  - Bù/hãm: hàng ra ít (≤ mức thấp 10 kỳ, so 200 kỳ trước) → ≥1; ra nhiều (≥ mức cao) → ≤1
  - Khoảng tổng / số lẻ / số nhỏ hay gặp (200 kỳ trước), không hàng nào ≥4 số, dạng hàng khác kỳ trước,
    trùng kỳ trước ≤1, ≤1 cặp liền nhau, ≥m hàng có mặt
Luật đạt: đúng ≥70% ở cả khung 50 và 100 kỳ gần. Ghép dần (luật nào thu hẹp nhiều nhất lấy trước) khi dạng thật vẫn lọt
khuôn ≥ NGUONG ở cả 50 và 100 kỳ. Loto: tổng, lẻ, nhỏ tính trên dãy 6 số (5 số + số may mắn, MM nhỏ = 1–6).
  build(R, LK, NB, KB, T) -> dict(rules=[...], pass50, pass100, keep)   (R: list set/list các kỳ; LK: số may mắn hoặc None)
  check(spec, x, mm, prev, NB, KB) -> bool"""
import random
NGUONG = 75

def feat(x, mm, prev, NB, KB):
    s = sorted(x); d6 = s + ([mm] if mm else [])
    H = NB // 10 + 1; hang = [0] * H
    for v in s: hang[v // 10] += 1
    return dict(hang=hang, tong=sum(d6), le=sum(v % 2 for v in d6),
                nho=sum(v <= NB // 2 for v in s) + (1 if mm and mm <= 6 else 0),
                trung=len(set(s) & set(prev or [])), lt=sum(1 for a, b in zip(s, s[1:]) if b == a + 1),
                maxh=max(hang), comat=sum(1 for v in hang if v), dang='-'.join(map(str, hang)))

def ext(x):
    """đặc điểm thêm từ tra cứu 15 ngôn ngữ (anh 17/10/2026): AC, biên độ, delta, đuôi, chia dư 3 — chỉ tính trên số chính"""
    s = sorted(x); d = [b - a for a, b in zip(s, s[1:])]
    r3 = [sum(v % 3 == i for v in s) for i in range(3)]
    return dict(ac=len({b - a for i, a in enumerate(s) for b in s[i + 1:]}) - (len(s) - 1), span=s[-1] - s[0], dmin=min(d), dmax=max(d),
                duoi=len({v % 10 for v in s}), tduoi=sum(v % 10 for v in s), m3max=max(r3), m3min=min(r3))


def check(sp, x, mm, prev, NB, KB):
    f = feat(x, mm, prev, NB, KB); k = sp['k']
    if k == 'hang': return f['hang'][sp['i']] <= sp['v'] if sp['op'] == 'le' else f['hang'][sp['i']] >= sp['v']
    if k in ('tong', 'le', 'nho'): return sp['lo'] <= f[k] <= sp['hi']
    if k in ('trung', 'lt', 'maxh'): return f[k] <= sp['max']
    if k == 'comat': return f['comat'] >= sp['min']
    if k == 'khac': return f['dang'] != sp['dang']
    if k == 'tranh': return not (set(x) & set(sp['nums']))   # vé không chứa các số này
    if k == 'lon': return sum(1 for v in x if (v % 10) * 10 + v // 10 != v and (v % 10) * 10 + v // 10 in set(x)) // 2 <= sp['max']   # cặp lộn trong kỳ
    if k == 'rng':
        f['kep'] = sum(1 for v in x if v % 11 == 0)
        if sp['f'] not in f: f.update(ext(x))
        v = f[sp['f']]; inn = sp['lo'] <= v <= sp['hi']
        return (not inn) if sp.get('neg') else inn
    return True

def build(R, LK, NB, KB, T, full=False, bh=False):
    R = [sorted(r) for r in R]; H = NB // 10 + 1
    LKv = lambda t: (LK[t] if LK else None)
    F = {t: feat(R[t], LKv(t), R[t - 1], NB, KB) for t in range(T - 320, T)}
    hc = lambda t, i: F[t]['hang'][i]
    def inst(t):
        """các luật (id, nhãn, spec) đang có hiệu lực ở kỳ t — chỉ dùng kỳ < t"""
        out = [('maxh', 'Không hàng nào ≥4 số', dict(k='maxh', max=3)),
               ('khac', f"Dạng hàng khác kỳ trước ({F[t - 1]['dang']})", dict(k='khac', dang=F[t - 1]['dang'])),
               ('trung', 'Trùng kỳ trước ≤1 số', dict(k='trung', max=1)),
               ('lt', '≤1 cặp số liền nhau', dict(k='lt', max=1)),
               ('kep1', 'Số kép (11, 22, 33…) nhiều nhất 1 số', dict(k='rng', f='kep', lo=0, hi=1, neg=False))]
        for m in range(3, H):
            out.append((f'comat{m}', f'≥{m} hàng có mặt', dict(k='comat', min=m)))
        for i in range(H):
            s = min(hc(t - 1, i), 3)
            out.append((f'hc{i}le{s}', f'{i}x kỳ trước ra {s if s < 3 else "≥3"} số → kỳ này {i}x ≤1 số', dict(k='hang', i=i, op='le', v=1)))
            out.append((f'hc{i}ge{s}', f'{i}x kỳ trước ra {s if s < 3 else "≥3"} số → kỳ này {i}x có ≥1 số', dict(k='hang', i=i, op='ge', v=1)))
            c10 = lambda u: sum(hc(w, i) for w in range(u - 10, u))
            xs = sorted(c10(u) for u in range(t - 100, t)); lo, hi = xs[len(xs) // 5], xs[len(xs) * 4 // 5]
            if c10(t) <= lo: out.append((f'bh{i}it', f'{i}x ra ít 10 kỳ ({c10(t)}) → kỳ này có ≥1 số', dict(k='hang', i=i, op='ge', v=1)))
            if c10(t) >= hi: out.append((f'bh{i}nh', f'{i}x ra nhiều 10 kỳ ({c10(t)}) → kỳ này ≤1 số', dict(k='hang', i=i, op='le', v=1)))
        for key, lab in (('tong', 'Tổng'), ('le', 'Số lẻ'), ('nho', 'Số nhỏ')):
            xs = sorted(F[u][key] for u in range(t - 100, t))   # tối đa 100 kỳ
            for q in (80, 70):
                if key == 'tong':
                    a = (100 - q) // 2; lo, hi = xs[len(xs) * a // 100], xs[len(xs) * (100 - a) // 100 - 1]
                else:   # khoảng liền ngắn nhất phủ ≥q% kỳ
                    vals = sorted(set(xs)); best = None
                    for i0 in range(len(vals)):
                        for j0 in range(i0, len(vals)):
                            c = sum(vals[i0] <= v <= vals[j0] for v in xs)
                            if c * 100 >= q * len(xs) and (best is None or vals[j0] - vals[i0] < best[1] - best[0]): best = (vals[i0], vals[j0]); break
                    lo, hi = best
                out.append((f'{key}{q}', f'{lab} {lo}–{hi}', dict(k=key, lo=lo, hi=hi)))
        return out
    TS = range(T - 100, T)
    I = {t: inst(t) for t in TS}
    ok = {t: {rid: check(sp, R[t], LKv(t), R[t - 1], NB, KB) for rid, _, sp in I[t]} for t in TS}
    def acc(rid, W):
        ts = [t for t in range(T - W, T) if rid in ok[t]]
        return (sum(ok[t][rid] for t in ts) / len(ts) * 100, len(ts)) if ts else (None, 0)
    ids = {rid for t in TS for rid in ok[t]}
    A = {rid: (acc(rid, 50), acc(rid, 100)) for rid in ids}
    good = {rid for rid, ((a50, n50), (a100, n100)) in A.items() if a50 is not None and a100 is not None and a50 >= 70 and a100 >= 70 and n100 >= 8}
    if bh:   # chỉ giữ luật qua Benjamini–Hochberg (q=0,10) trên mọi luật ứng viên; H0: đúng ≤70% (khung 100 kỳ)
        from scipy.stats import binomtest
        cand = [r for r in ids if r in A and A[r][1][1] >= 8]
        pv = {r: binomtest(round(A[r][1][0] * A[r][1][1] / 100), A[r][1][1], 0.70, alternative='greater').pvalue for r in cand}
        od = sorted(cand, key=lambda r: pv[r]); cut = max([i for i, r in enumerate(od, 1) if pv[r] <= 0.10 * i / len(od)] or [0])
        good &= set(od[:cut])
    famk = lambda rid: next((p for p in ('tong', 'le', 'nho') if rid.startswith(p) and rid[len(p):].isdigit()), rid)
    # đo độ thu hẹp ở kỳ tới bằng mẫu dãy
    NOW = {rid: (lab, sp) for rid, lab, sp in inst(T)}
    rnd = random.Random(1); S = [(sorted(rnd.sample(range(1, NB + 1), KB)), rnd.randint(1, 12) if LK else None) for _ in range(3000)]
    def pas(sel, W): return sum(all(ok[t].get(r, True) for r in sel) for t in range(T - W, T)) / W * 100
    def keep(sel):
        sps = [NOW[r][1] for r in sel if r in NOW]
        return sum(all(check(sp, x, mm, R[T - 1], NB, KB) for sp in sps) for x, mm in S) / len(S) * 100
    sel = []
    while True:
        best = None
        for rid in sorted(good):   # cố định thứ tự (trước đây duyệt set → mỗi lần chạy có thể chọn luật khác khi ngang điểm)
            if rid in sel or rid not in NOW or any(famk(rid) == famk(r) for r in sel): continue
            c = sel + [rid]
            if pas(c, 50) < NGUONG or pas(c, 100) < NGUONG: continue
            kp = keep(c)
            if best is None or kp < best[0]: best = (kp, rid)
        if not best or (sel and best[0] >= keep(sel) - 0.5): break
        sel.append(best[1])
    rules = [dict(id=r, lab=NOW[r][0], spec=NOW[r][1], a50=round(A[r][0][0]), a100=round(A[r][1][0]), n100=A[r][1][1]) for r in sel]
    # bảng từng hàng (anh 14/10: "2x, 1x không nói gì"): kỳ trước ra c số → kỳ sau 0 / 1 / ≥2 số (200 kỳ) + luật đạt của hàng
    hang = []
    for i in range(H):
        c = min(hc(T - 1, i), 3); ts = [t for t in range(T - 100, T) if min(hc(t - 1, i), 3) == c]
        dist = [round(sum(min(hc(t, i), 2) == k for t in ts) / len(ts) * 100) if ts else None for k in range(3)]
        lu = [dict(lab=NOW[r][0], a50=round(A[r][0][0]), a100=round(A[r][1][0]), trong=r in sel) for r in good if r in NOW and NOW[r][1].get('k') == 'hang' and NOW[r][1].get('i') == i]
        hang.append(dict(h=i, truoc=c, n=len(ts), dist=dist, luat=lu))
    out = dict(rules=rules, pass50=round(pas(sel, 50)), pass100=round(pas(sel, 100)), keep=round(keep(sel)), nguong=NGUONG, hang=hang)
    if full:   # khuon_fdr.py: số lần đúng / số lần áp dụng của MỌI luật ứng viên (đếm thô, để kiểm định nhiều phép thử)
        cnt = lambda rid, W: (sum(ok[t][rid] for t in range(T - W, T) if rid in ok[t]), sum(rid in ok[t] for t in range(T - W, T)))
        out['all'] = [dict(id=r, lab=NOW[r][0] if r in NOW else None, k50=cnt(r, 50)[0], n50=cnt(r, 50)[1], k100=cnt(r, 100)[0], n100=cnt(r, 100)[1],
                           good=r in good, sel=r in sel) for r in sorted(ids)]
    return out
