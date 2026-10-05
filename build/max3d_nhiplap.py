#!/usr/bin/env python3
"""Max 3D / Pro — mỗi lần 1 bộ số ra, bao lâu sau nó RA LẠI (khoảng nghỉ lặp lại). So với quay đều (p = 1,98%/kỳ).
  python3 build/max3d_nhiplap.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = 1 - 0.999 ** 20
CUT = [1, 5, 10, 20, 50, 100, 200]
for f, nm in (('max3d_data.json', 'Max 3D (3D+)'), ('max3dpro_data.json', 'Max 3D Pro')):
    D = json.load(open(os.path.join(HERE, f))); L = [set(r) for r in D['res']]; T = len(L)
    def gaps(a, b):
        """lần ra ở kỳ t ∈ [a,b): khoảng tới lần ra lại (None nếu chưa ra lại trước khi hết dữ liệu)"""
        out = []
        for t in range(a, b):
            for s in L[t]:
                g = next((u - t for u in range(t + 1, T) if s in L[u]), None)
                out.append((g, T - 1 - t))
        return out
    print(f'\n## {nm} — {T} kỳ ({D["dates"][0]} → {D["dates"][-1]})\n')
    print('| Ra lại trong vòng | ' + ' | '.join(f'{c} kỳ' for c in CUT) + ' |\n|---|' + '---|' * len(CUT))
    for lab, a, b in (('Lần ra ở 300 kỳ trước khúc 200 kỳ cuối', T - 500, T - 200), ('Lần ra ở các kỳ cũ hơn', 0, T - 500)):
        G = gaps(max(0, a), b)
        cells = []
        for c in CUT:
            el = [(g, rest) for g, rest in G if rest >= c]
            cells.append(f'{sum(g is not None and g <= c for g, _ in el) / max(len(el), 1) * 100:.1f}%')
        print(f'| {lab} | ' + ' | '.join(cells) + ' |')
    print('| **Quay đều (lý thuyết)** | ' + ' | '.join(f'{(1 - (1 - P) ** c) * 100:.1f}%' for c in CUT) + ' |')
    G = [g for g, _ in gaps(0, T) if g is not None]; G.sort()
    print(f'\n- Khoảng nghỉ lặp lại: trung bình **{sum(G) / len(G):.0f} kỳ**, trung vị **{G[len(G) // 2]} kỳ** (quay đều: TB {1 / P:.0f}, trung vị {round(0.693 / P)} kỳ); dài nhất {G[-1]} kỳ')
    # bộ ra lại ngay kỳ sau, cách 1 kỳ
    for c in (1, 2, 3):
        n = sum(1 for g in G if g == c); tot = len(G)
        print(f'- Ra lại đúng sau {c} kỳ: {n} lần ({n / tot * 100:.2f}% số lần lặp; quay đều {P * (1 - P) ** (c - 1) / (1 - (1 - P) ** 600) * 100:.2f}%)')
