#!/usr/bin/env python3
"""Max 3D / Max 3D+ / Max 3D Pro — tính CHÍNH XÁC xác suất từng hạng giải và % hoàn tiền (vé 10.000đ),
theo cơ cấu giải công bố. Mỗi kỳ quay 20 bộ số 000–999 (mỗi lần quay độc lập):
ĐB 2 bộ (D1, D2 theo thứ tự quay), Nhất 4, Nhì 6, Ba 8.
  python3 build/max3d.py"""
from itertools import product
GR = ['D1'] * 1 + ['D2'] * 1 + ['N'] * 4 + ['H'] * 6 + ['B'] * 8
G = ['D1', 'D2', 'N', 'H', 'B']
p = 1 / 1000
# DP: trạng thái = (tập nhóm a xuất hiện, tập nhóm b xuất hiện) — a ≠ b
st = {(0, 0): 1.0}
for g in GR:
    bit = 1 << G.index(g); nx = {}
    for (ma, mb), pr in st.items():
        for k, q in ((0, 1 - 2 * p), (1, p), (2, p)):
            key = (ma | bit, mb) if k == 1 else (ma, mb | bit) if k == 2 else (ma, mb)
            nx[key] = nx.get(key, 0) + pr * q
    st = nx
B = {g: 1 << G.index(g) for g in G}; D = B['D1'] | B['D2']; NHB = B['N'] | B['H'] | B['B']
def tier_plus(ma, mb, pro):
    if pro and ma & B['D1'] and mb & B['D2']: return 'ĐB (đúng thứ tự)'
    if pro and ma & B['D2'] and mb & B['D1']: return 'Phụ ĐB (ngược thứ tự)'
    if not pro and ma & D and mb & D: return 'ĐB'
    for g, n in (('N', 'Nhất'), ('H', 'Nhì'), ('B', 'Ba')):
        if ma & B[g] and mb & B[g]: return n
    if ma and mb: return 'Tư'
    if ma & D or mb & D: return 'Năm'
    if ma or mb: return 'Sáu'
    return None
PZ = {'plus': {'ĐB': 1e9, 'Nhất': 40e6, 'Nhì': 10e6, 'Ba': 5e6, 'Tư': 1e6, 'Năm': 150e3, 'Sáu': 40e3},
      'pro': {'ĐB (đúng thứ tự)': 2e9, 'Phụ ĐB (ngược thứ tự)': 400e6, 'Nhất': 30e6, 'Nhì': 10e6, 'Ba': 4e6, 'Tư': 1e6, 'Năm': 100e3, 'Sáu': 40e3}}
def show(name, pro):
    pt = {}
    for (ma, mb), pr in st.items():
        t = tier_plus(ma, mb, pro)
        if t: pt[t] = pt.get(t, 0) + pr
    z = PZ['pro' if pro else 'plus']; ev = 0
    print(f'\n## {name} — chọn 2 bộ số, vé 10.000đ\n\n| Hạng | Điều kiện | Giải | Xác suất/kỳ | Khoảng 1 lần / | Đóng góp hoàn tiền |\n|---|---|---|---|---|---|')
    COND = {'ĐB': 'cả 2 bộ trùng 2 số ĐB', 'ĐB (đúng thứ tự)': '2 bộ trùng 2 số ĐB đúng thứ tự quay', 'Phụ ĐB (ngược thứ tự)': '2 bộ trùng 2 số ĐB ngược thứ tự',
            'Nhất': 'cả 2 bộ nằm trong 4 số giải Nhất', 'Nhì': 'cả 2 bộ trong 6 số giải Nhì', 'Ba': 'cả 2 bộ trong 8 số giải Ba',
            'Tư': 'cả 2 bộ nằm trong 20 số (khác nhóm)', 'Năm': '1 bộ trùng 1 số ĐB', 'Sáu': '1 bộ trùng 1 số Nhất/Nhì/Ba'}
    for t, v in z.items():
        pr = pt.get(t, 0); ev += pr * v
        print(f'| {t} | {COND[t]} | {v:,.0f}đ | {pr * 100:.5f}% | {1 / pr:,.0f} kỳ | {pr * v / 10000 * 100:.1f}% |')
    print(f'| **Tổng** | | | **{sum(pt.values()) * 100:.2f}% có giải** | {1 / sum(pt.values()):.0f} kỳ | **{ev / 10000 * 100:.1f}%** |')
# Max 3D cơ bản: 1 bộ số
print('## Max 3D — chọn 1 bộ số, vé 10.000đ\n\n| Hạng | Số bộ | Giải | Xác suất/kỳ | Đóng góp hoàn tiền |\n|---|---|---|---|---|')
ev = 0; pw = 0
for n, k, v in (('ĐB', 2, 1e6), ('Nhất', 4, 350e3), ('Nhì', 6, 210e3), ('Ba', 8, 100e3)):
    pr = 1 - (1 - p) ** k; ev += k * p * v; pw += pr
    print(f'| {n} | {k} | {v:,.0f}đ | {pr * 100:.2f}% | {k * p * v / 10000 * 100:.1f}% |')
print(f'| **Tổng** | 20 | | **{(1 - (1 - p) ** 20) * 100:.2f}% có giải** (≈1/{1 / (1 - (1 - p) ** 20):.0f} kỳ) | **{ev / 10000 * 100:.1f}%** |')
show('Max 3D+', False)
show('Max 3D Pro', True)
