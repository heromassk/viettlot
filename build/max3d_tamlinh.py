#!/usr/bin/env python3
"""Max 3D / Pro — TÂM LINH: các quẻ theo ngày quay (âm lịch, can chi, ngũ hành, thần số học) và theo kỳ trước (bóng, lộn, tổng chạm).
Chấm trên dữ liệu thật: bộ quẻ chọn ra bao nhiêu % (chia đều 1,98%/bộ), chữ số quẻ chọn chiếm bao nhiêu % lần quay (chia đều = số chữ số × 10%).
3 đoạn 100 kỳ gần → xa + cả lịch sử. Cuối cùng in quẻ cho kỳ tới.
  python3 build/max3d_tamlinh.py"""
import json, os, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
LUN = json.load(open(os.path.join(HERE, 'max3d_lunar.json')))
P = 1 - 0.999 ** 20
CAN = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
HANH_CAN = ['Mộc', 'Mộc', 'Hỏa', 'Hỏa', 'Thổ', 'Thổ', 'Kim', 'Kim', 'Thủy', 'Thủy']
HADO = {'Thủy': (1, 6), 'Hỏa': (2, 7), 'Mộc': (3, 8), 'Kim': (4, 9), 'Thổ': (5, 0)}      # Hà Đồ
jdn = lambda d: d.toordinal() + 1721425
def info(ds):
    d = datetime.datetime.strptime(ds, '%d/%m/%Y').date(); ld, lm, ly = LUN[ds]
    can = (jdn(d) + 9) % 10; hanh = HANH_CAN[can]
    red = lambda n: n if n < 10 else red(sum(map(int, str(n))))
    tsh = red(sum(map(int, d.strftime('%d%m%Y'))))
    return dict(d=d, ld=ld, lm=lm, can=can, hanh=hanh, tsh=tsh % 10)
bong = lambda s: ''.join(str((int(c) + 5) % 10) for c in s)
def bo_methods(ds, prev):
    I = info(ds); d = I['d']; ld, lm = I['ld'], I['lm']
    return {
        'Ngày + tháng âm (25/8 → 258, 825)': {f'{ld:02d}{lm % 10}', f'{lm % 10}{ld:02d}'},
        'Ngày + tháng dương (05/10 → 050, 005…)': {f'{d.day:02d}{d.month % 10}', f'{d.month % 10}{d.day:02d}'},
        'Bóng âm dương 2 số ĐB kỳ trước': {bong(s) for s in prev[:2]},
        'Lộn 2 số ĐB kỳ trước': {s[::-1] for s in prev[:2]} - set(prev[:2]),
        'Tam hoa theo thần số học ngày': {str(I['tsh']) * 3},
    }
def digit_methods(ds, prev):
    I = info(ds)
    s = sum(int(c) for c in prev[0]) % 10
    return {
        'Ngũ hành ngày (Hà Đồ, 2 chữ số)': set(HADO[I['hanh']]),
        'Can ngày (chữ số đuôi năm can: Canh 0…Kỷ 9)': {(I['can'] + 4) % 10},
        'Thần số học ngày (1 chữ số)': {I['tsh']},
        'Ngày âm (chữ số đuôi + đầu)': {I['ld'] % 10, I['ld'] // 10},
        'Tổng chạm ĐB1 kỳ trước (1 chữ số)': {s},
    }
for f, nm in (('max3d_data.json', 'Max 3D (3D+)'), ('max3dpro_data.json', 'Max 3D Pro')):
    D = json.load(open(os.path.join(HERE, f))); R = D['res']; DT = D['dates']; T = len(R)
    segs = [('100 kỳ gần', T - 100, T), ('100 kỳ giữa', T - 200, T - 100), ('100 kỳ xa', T - 300, T - 200), ('Cả lịch sử', 1, T)]
    print(f'\n## {nm} — {T} kỳ\n\n### Quẻ chọn BỘ SỐ — mỗi bộ ra kỳ đó (chia đều {P * 100:.2f}%)\n')
    print('| Quẻ | ' + ' | '.join(s[0] for s in segs) + ' |\n|---|' + '---|' * len(segs))
    for k in bo_methods(DT[-1], R[-1]):
        cells = []
        for _, a, b in segs:
            h = n = 0
            for t in range(a, b):
                g = bo_methods(DT[t], R[t - 1])[k]; h += len(g & set(R[t])); n += len(g)
            cells.append(f'{h / max(n, 1) * 100:.2f}% (×{h / max(n, 1) / P:.2f})')
        print(f'| {k} | ' + ' | '.join(cells) + ' |')
    print('\n### Quẻ chọn CHỮ SỐ — tỉ lệ chiếm trong 60 lần quay chữ số của kỳ (so với chia đều)\n')
    print('| Quẻ | ' + ' | '.join(s[0] for s in segs) + ' |\n|---|' + '---|' * len(segs))
    for k in digit_methods(DT[-1], R[-1]):
        cells = []
        for _, a, b in segs:
            h = e = 0
            for t in range(a, b):
                g = digit_methods(DT[t], R[t - 1])[k]; h += sum(int(c) in g for s in R[t] for c in s); e += 60 * len(g) / 10
            cells.append(f'×{h / e:.2f}')
        print(f'| {k} | ' + ' | '.join(cells) + ' |')
# quẻ kỳ tới
print('\n## Quẻ kỳ tới\n')
for f, nm, nd in (('max3d_data.json', 'Max 3D+', '05/10/2026'), ('max3dpro_data.json', 'Max 3D Pro', '06/10/2026')):
    D = json.load(open(os.path.join(HERE, f))); prev = D['res'][-1]; I = info(nd)
    print(f'**{nm} {nd}** (âm {I["ld"]}/{I["lm"]}, ngày {CAN[I["can"]]} – hành {I["hanh"]}, thần số học {I["tsh"]}; ĐB kỳ trước {" ".join(prev[:2])})')
    for k, v in bo_methods(nd, prev).items(): print(f'- {k}: {" ".join(sorted(v))}')
    for k, v in digit_methods(nd, prev).items(): print(f'- {k}: {" ".join(map(str, sorted(v)))}')
    print()
