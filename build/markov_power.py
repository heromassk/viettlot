"""Chấm phương pháp bài FB 'Giải Mã Vietlott' trên Power 6/55 (anh 13/10/2026):
Markov bậc k (3, 5, …, 99) theo chuỗi có/không của từng số + hồi quy xu hướng tần suất.
Mỗi kỳ thử chỉ dùng 200 kỳ trước nó; chấm 100 kỳ gần, 2 nửa 50·50.
python3 build/markov_power.py"""
import json, os, numpy as np
B = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(B, 'all_data.json')))['power655']['res']
N, NB, W, T = len(R), 55, 200, 100
X = np.zeros((N, NB), int)
for i, r in enumerate(R):
    for n in r: X[i, n - 1] = 1

def markov(t, k, mode):
    H = X[t - W:t]                      # 200 kỳ trước
    sc = np.zeros(NB); used = np.zeros(NB)
    if mode == 'chung':                 # 55 số dùng chung bảng chuyển
        cnt = {}
        for j in range(k, W):
            for n in range(NB):
                s = tuple(H[j - k:j, n]); a = cnt.setdefault(s, [0, 0]); a[0] += H[j, n]; a[1] += 1
        for n in range(NB):
            a = cnt.get(tuple(H[W - k:W, n]))
            if a and a[1] >= 3: sc[n] = (a[0] + 0.11) / (a[1] + 1); used[n] = a[1]
            else: sc[n] = 6 / 55
    else:                               # mỗi số 1 bảng riêng
        for n in range(NB):
            col = H[:, n]; s = tuple(col[W - k:]); hit = tot = 0
            for j in range(k, W):
                if tuple(col[j - k:j]) == s: hit += col[j]; tot += 1
            sc[n] = (hit + 0.11) / (tot + 1) if tot else 6 / 55; used[n] = tot
    return sc + 1e-6 * H[-100:].sum(0), used

def hoiquy(t, w):                      # độ dốc tần suất cộng dồn w kỳ (xu hướng chạy)
    H = X[t - w:t]; c = H.cumsum(0); x = np.arange(w) - (w - 1) / 2
    return (x[:, None] * (c - c.mean(0))).sum(0) / (x ** 2).sum() + 1e-6 * H.sum(0)

def cham(fn, ks=(9, 12, 15, 20)):
    out = {}
    for k in ks:
        h = []
        for t in range(N - T, N):
            s = fn(t); top = np.argsort(-s)[:k]; h.append(int(X[t, top].sum()))
        h = np.array(h); a, b = h[:50], h[50:]
        out[k] = dict(tb=h.mean(), g2=(h >= 2).mean() * 100, g3=(h >= 3).mean() * 100, g4=(h >= 4).mean() * 100,
                      n1=(a >= 3).mean() * 100, n2=(b >= 3).mean() * 100)
    return out

KQ = {}
for k in (1, 2, 3, 5, 8, 10):
    KQ[f'Markov bậc {k} (chung 55 số)'] = cham(lambda t, k=k: markov(t, k, 'chung')[0])
for k in (3, 5, 10, 20, 50, 99):
    KQ[f'Markov bậc {k} (từng số)'] = cham(lambda t, k=k: markov(t, k, 'rieng')[0])
for w in (30, 50, 100, 200):
    KQ[f'Hồi quy xu hướng {w} kỳ'] = cham(lambda t, w=w: hoiquy(t, w))
def ket(t):                             # kết hợp: cộng hạng Markov 3 + 5 (chung) + hồi quy 50
    rk = lambda s: np.argsort(np.argsort(s))
    return rk(markov(t, 3, 'chung')[0]) + rk(markov(t, 5, 'chung')[0]) + rk(hoiquy(t, 50))
KQ['Kết hợp Markov 3+5 + hồi quy 50'] = cham(ket)
# số mẫu khớp trạng thái ở bậc cao (từng số) tại kỳ mới nhất
dem = {k: float(np.median(markov(N, k, 'rieng')[1])) for k in (3, 5, 10, 20, 50, 99)}
json.dump(dict(kq=KQ, mau=dem), open(os.path.join(B, 'markov_power.json'), 'w'), ensure_ascii=False, default=float)
for m, v in KQ.items():
    print(m, ' | '.join(f"p{k}: {d['tb']:.2f} ≥3 {d['g3']:.0f}% ≥4 {d['g4']:.0f}% (nửa {d['n1']:.0f}·{d['n2']:.0f})" for k, d in v.items()))
print('mẫu khớp trung vị (từng số):', dem)
