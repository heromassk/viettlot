#!/usr/bin/env python3
"""Max 3D / Pro — DẠNG bộ số (111, 112, 121, 211, 123, 321…) có hay ra không. Tỉ lệ = số lần ra / (số bộ của dạng × 20 lần quay × số kỳ),
so với chia đều 0,1%/lần quay. Chấm cả lịch sử và 3 đoạn 100 kỳ gần.
  python3 build/max3d_dang.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
def dang(s):
    a, b, c = s
    if a == b == c: return 'Tam hoa (000, 111…)'
    if a == b: return 'Kép đầu (112, 330…)'
    if b == c: return 'Kép cuối (211, 033…)'
    if a == c: return 'Kép kẹp (121, 303…)'
    x, y, z = map(int, s)
    if y - x == z - y == 1: return 'Tiến liên tiếp (123, 789)'
    if x - y == y - z == 1: return 'Lùi liên tiếp (321, 987)'
    return 'Ba chữ số khác nhau, còn lại'
ALL = [f'{i:03d}' for i in range(1000)]; SZ = {}
for s in ALL: SZ[dang(s)] = SZ.get(dang(s), 0) + 1
for f, nm in (('max3d_data.json', 'Max 3D (3D+)'), ('max3dpro_data.json', 'Max 3D Pro')):
    D = json.load(open(os.path.join(HERE, f))); R = D['res']; T = len(R)
    def rate(a, b):
        c = {}
        for r in R[a:b]:
            for s in r: c[dang(s)] = c.get(dang(s), 0) + 1
        return {k: c.get(k, 0) / (SZ[k] * 20 * (b - a)) * 1000 for k in SZ}   # ×1000 → đơn vị "lần chia đều"
    full = rate(0, T); seg = [rate(T - 100, T), rate(T - 200, T - 100), rate(T - 300, T - 200)]
    cnt = {}
    for r in R:
        for s in r: cnt[dang(s)] = cnt.get(dang(s), 0) + 1
    print(f'\n## {nm} — {T} kỳ ({D["dates"][0]} → {D["dates"][-1]}), {T * 20} lần quay\n')
    print('| Dạng | Số bộ | Lần ra (cả lịch sử) | Kỳ vọng | Tỉ lệ so với chia đều: cả lịch sử | 3 đoạn 100 kỳ gần → xa |\n|---|---|---|---|---|---|')
    for k in sorted(SZ, key=lambda k: SZ[k]):
        print(f'| {k} | {SZ[k]} | {cnt.get(k, 0)} | {SZ[k] * 20 * T / 1000:.0f} | ×{full[k]:.2f} | ' + ' · '.join(f'×{x[k]:.2f}' for x in seg) + ' |')
    th = sum(any(dang(s).startswith('Tam hoa') for s in r) for r in R[-300:]) / 3
    print(f'\n- Kỳ có ≥1 tam hoa (300 kỳ gần): {th:.0f}% (kỳ vọng {(1 - 0.99 ** 20) * 100:.0f}%) → luật "loại tam hoa" đúng {100 - th:.0f}% số kỳ')
