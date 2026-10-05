#!/usr/bin/env python3
"""Max 3D / Pro — quan hệ 20 bộ số TRONG 1 KỲ: bi có nghiêng về phía nào không (anh, 05/10/2026).
Mỗi kỳ lọc riêng 20 chữ số hàng trăm, 20 chữ số hàng chục, 20 chữ số hàng đơn vị → so sánh; rồi so với các kỳ trước (ngắn hạn ≤50 kỳ).
Đối chứng: cùng phép tính trên 200 bộ dữ liệu quay ngẫu nhiên đều (cùng số kỳ) → khoảng 90%.
  python3 build/max3d_trongky.py [--file build/max3dpro_data.json]"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
f = sys.argv[sys.argv.index('--file') + 1] if '--file' in sys.argv else os.path.join(HERE, 'max3d_data.json')
D = json.load(open(f)); N = 300
X = np.array([[[int(c) for c in s] for s in r] for r in D['res'][-N:]])          # (kỳ, 20 bộ, 3 hàng)
HANG = ['trăm', 'chục', 'đơn vị']; rng = np.random.default_rng(7)
def cr(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    return np.nan if a.std() == 0 or b.std() == 0 else np.corrcoef(a, b)[0, 1]
def feats(X):
    """Trả về dict chỉ số; X (n,20,3)"""
    n = X.shape[0]; out = {}
    C = np.stack([(X == d).sum(1) for d in range(10)], -1)                          # (n,3,10) số lần chữ số d ở mỗi hàng trong kỳ
    low = (X <= 4).sum(1); even = (X % 2 == 0).sum(1)                                # (n,3)
    # 1. độ dồn trong kỳ: chữ số ra nhiều nhất mỗi hàng (TB)
    out['Chữ số ra nhiều nhất trong 20 (TB, mỗi hàng)'] = C.max(-1).mean()
    # 2. phân tán nhỏ/lớn giữa các kỳ (nếu từng kỳ bi nghiêng → phân tán lớn hơn ngẫu nhiên)
    out['Độ dao động số chữ số nhỏ 0–4 giữa các kỳ (độ lệch chuẩn)'] = low.std(0).mean()
    # 3. hàng trăm/chục/đơn vị cùng kỳ nghiêng cùng phía?
    out['Tương quan nhỏ/lớn giữa 3 hàng cùng kỳ'] = np.mean([np.corrcoef(low[:, a], low[:, b])[0, 1] for a, b in ((0, 1), (1, 2), (0, 2))])
    # 4. trong kỳ: 10 bộ đầu (ĐB, Nhất, Nhì) vs 10 bộ sau — cùng nghiêng?
    c1 = np.stack([(X[:, :10] == d).sum(1) for d in range(10)], -1); c2 = np.stack([(X[:, 10:] == d).sum(1) for d in range(10)], -1)
    out['Trong kỳ: 10 bộ đầu ↔ 10 bộ sau (tương quan chữ số)'] = np.nanmean([cr(c1[t, h], c2[t, h]) for t in range(n) for h in range(3)])
    # 5. nối tiếp kỳ: tần suất chữ số kỳ t ↔ TB W kỳ trước (W = 1, 5, 10, 20, 50)
    for W in (1, 5, 10, 20, 50):
        v = []
        for t in range(50, n):
            prev = C[t - W:t].mean(0)
            v += [cr(prev[h], C[t, h]) for h in range(3)]
        out[f'Kỳ này ↔ TB {W} kỳ trước (tương quan chữ số mỗi hàng)'] = np.nanmean(v)
    # 6. nhỏ/lớn nối tiếp
    out['Nhỏ/lớn: kỳ này ↔ kỳ trước (tương quan)'] = np.mean([np.corrcoef(low[1:, h], low[:-1, h])[0, 1] for h in range(3)])
    out['Chẵn/lẻ: kỳ này ↔ kỳ trước (tương quan)'] = np.mean([np.corrcoef(even[1:, h], even[:-1, h])[0, 1] for h in range(3)])
    return out
real = feats(X)
sims = [feats(rng.integers(0, 10, X.shape)) for _ in range(100)]
print(f'## {os.path.basename(f)} — quan hệ 20 bộ trong kỳ, {N} kỳ gần ({D["dates"][-N]} → {D["dates"][-1]})\n')
print('| Chỉ số | Thực tế | Quay ngẫu nhiên: TB (khoảng 90%) | Nhận xét |\n|---|---|---|---|')
for k, v in real.items():
    s = np.array([x[k] for x in sims]); lo, hi = np.percentile(s, [5, 95])
    nx = '**cao hơn ngẫu nhiên**' if v > hi else '**thấp hơn ngẫu nhiên**' if v < lo else 'trong vùng ngẫu nhiên'
    print(f'| {k} | {v:+.3f} | {s.mean():+.3f} ({lo:+.3f} … {hi:+.3f}) | {nx} |')
# bảng ngắn hạn: tỉ lệ ra từng chữ số mỗi hàng — kỳ gần nhất vs 5 / 10 / 20 / 50 kỳ
C = np.stack([(X == d).sum(1) for d in range(10)], -1)
print(f'\n### Tỉ lệ ra từng chữ số theo hàng: kỳ gần nhất ({D["dates"][-1]}) so với các kỳ trước (chia đều 10%)\n')
for h in range(3):
    print(f'**Hàng {HANG[h]}**\n\n| Khung | ' + ' | '.join(str(d) for d in range(10)) + ' |\n|---|' + '---|' * 10)
    for nm, a in (('Kỳ gần nhất', 1), ('5 kỳ', 5), ('10 kỳ', 10), ('20 kỳ', 20), ('50 kỳ', 50)):
        p = C[-a:, h].sum(0) / (20 * a) * 100
        print(f'| {nm} | ' + ' | '.join(f'**{x:.0f}**' if x >= 13 else f'{x:.0f}' for x in p) + ' |')
    print()
