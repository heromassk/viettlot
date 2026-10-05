#!/usr/bin/env python3
"""Dữ liệu cho ô "Max 3D+ / Max 3D Pro" trong app → build/max3d_app.json (assemble.py nhúng vào /*MAX3D*/).
Max 3D+ dùng kết quả Max 3D (thứ 2, 4, 6); Max 3D Pro có kết quả riêng (thứ 3, 5, 7).
  python3 build/max3d_app.py   (chạy sau khi cập nhật build/max3d_data.json, max3dpro_data.json)"""
import json, os, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import max3d_tamlinh as TL
ALL = [f'{i:03d}' for i in range(1000)]
TIEN = {'012', '123', '234', '345', '456', '567', '678', '789'}
def next_day(last, days):   # days: weekday() của ngày quay (T2=0)
    d = datetime.datetime.strptime(last, '%d/%m/%Y').date() + datetime.timedelta(days=1)
    while d.weekday() not in days: d += datetime.timedelta(days=1)
    return d.strftime('%d/%m/%Y')
def goiy(f, kind):
    """Pool + 3 cặp gợi ý kèm lý do (luật đã nghiên cứu 05/10/2026, xem ghi-chu-quy-luat.md)."""
    D = json.load(open(os.path.join(HERE, f))); R = D['res']; T = len(R)
    nd = next_day(D['dates'][-1], (0, 2, 4) if kind == 'plus' else (1, 3, 5))
    NG = 5 if kind == 'plus' else 20
    nghi = {s for r in R[-NG:] for s in r}
    c = [[1] * 10 for _ in range(3)]
    for r in R[-50:]:
        for s in r:
            for i, ch in enumerate(s): c[i][int(ch)] += 1
    tot = [sum(x) for x in c]
    w = lambda s: (c[0][int(s[0])] / tot[0]) * (c[1][int(s[1])] / tot[1]) * (c[2][int(s[2])] / tot[2]) * 1000
    def sc(s): return w(s) * (0.95 if s[0] == s[2] and s[0] != s[1] else 1)   # kép kẹp trừ điểm nhẹ
    loai = {'nghi': nghi, 'tien': TIEN, 'tamhoa': {d * 3 for d in '0123456789'}}
    con = [s for s in ALL if not any(s in v for v in loai.values())]
    con.sort(key=lambda s: -sc(s))
    pool = con[:340] if kind == 'plus' else con
    P = set(pool)
    top = lambda i: sorted(range(10), key=lambda d: -c[i][d])[:3]
    def why(s):
        r = [f'chữ số nặng 50 kỳ: trăm {s[0]} ({c[0][int(s[0])] - 1} lần), chục {s[1]} ({c[1][int(s[1])] - 1}), đơn vị {s[2]} ({c[2][int(s[2])] - 1}); kỳ vọng 100 lần']
        r.append(f'không nằm trong {len(nghi)} bộ đang nghỉ ({NG} kỳ gần)')
        return r
    prev = R[-1]; I = TL.info(nd); Q = TL.bo_methods(nd, prev); QD = TL.digit_methods(nd, prev)
    pairs = []
    a, b = pool[0], pool[1]
    pairs.append(dict(x=[a, b], kind='Dấu vết' if kind == 'plus' else 'Chữ số nặng 50 kỳ (tham khảo — Pro chưa có dấu vết chữ số ổn định)', why=[f'{a}: ' + '; '.join(why(a)), f'{b}: ' + '; '.join(why(b)),
                      'Cặp điểm cao nhất của pool' + (' 340 bộ (giữ nhóm chữ số nặng nhất)' if kind == 'plus' else '')]))
    tld = set(QD['Ngũ hành ngày (Hà Đồ, 2 chữ số)']) | set(QD['Thần số học ngày (1 chữ số)'])
    mix = [s for s in pool if sum(int(ch) in tld for ch in s) >= 2 and s not in (a, b)][:2]
    if len(mix) == 2:
        pairs.append(dict(x=mix, kind=('Dấu vết' if kind == 'plus' else 'Pool') + ' + chữ số hợp ngày', why=[f'Chữ số hợp ngày {nd}: ngũ hành {I["hanh"]} (Hà Đồ ' + ', '.join(map(str, sorted(QD["Ngũ hành ngày (Hà Đồ, 2 chữ số)"]))) + f'), thần số học {I["tsh"]}',
                      f'{mix[0]}, {mix[1]}: có ≥2 chữ số hợp ngày, vẫn trong pool (điểm hạng {pool.index(mix[0]) + 1}, {pool.index(mix[1]) + 1})']))
    TLF = os.path.join(HERE, 'max3d_tl.json')
    TLJ = json.load(open(TLF)).get(kind) if os.path.exists(TLF) else None
    tl = None
    if TLJ and TLJ.get('next') == nd:
        cand = [v for v in TLJ['votes'] if v[0] in P][:2]
        if len(cand) == 2:
            tl = dict(methods=TLJ['methods'], top=TLJ['votes'][:12])
            pairs.append(dict(x=[cand[0][0], cand[1][0]], kind=f'Tâm linh {len(TLJ["methods"])} phương pháp (phiếu nhiều nhất trong pool)',
                              why=[f'{v[0]}: {v[1]} phiếu — ' + ', '.join(v[2]) for v in cand] +
                                  ['Kiểm cả lịch sử: bộ nhiều phiếu ra ngang mức chia đều (×0,93–1,03) — không thiệt, chọn theo duyên']))
    if kind == 'pro':
        lon = [prev[0][::-1], prev[1][::-1]]
        pairs.append(dict(x=lon, kind='Tâm linh: lộn ĐB kỳ trước', why=[f'ĐB kỳ trước {prev[0]} – {prev[1]} → lộn giữ thứ tự: {lon[0]} – {lon[1]}',
                          'Pro: quẻ này ra ×1,33 cả lịch sử, ×1,97 · 1,39 · 1,95 ở 3 đoạn 100 kỳ gần (đang theo dõi trong sổ)'] +
                          [f'{x}: ' + ('trong pool' if x in P else 'ngoài pool (' + ', '.join(n for k, n in (('nghi', 'đang nghỉ'), ('tien', 'tiến liên tiếp'), ('tamhoa', 'tam hoa')) if x in loai[k]) + ') — cân nhắc') for x in lon]))
    else:
        am = sorted(Q['Ngày + tháng âm (25/8 → 258, 825)'])
        pairs.append(dict(x=am, kind='Tâm linh: ngày tháng âm', why=[f'{nd} là ngày {I["ld"]}/{I["lm"]} âm → {am[0]}, {am[1]}', 'Quẻ ra đúng mức chia đều (×1,01 cả lịch sử): không thiệt, chọn theo duyên'] +
                          [f'{x}: ' + ('trong pool' if x in P else 'ngoài pool — cân nhắc') for x in am]))
    return dict(next=nd, am=f'{I["ld"]}/{I["lm"]}', can=TL.CAN[I['can']], hanh=I['hanh'], pool_n=len(pool),
                loai_n={k: len(v) for k, v in loai.items()}, ng=NG, pool=pool[:40], pool_all=sorted(pool), pairs=pairs, tl=tl,
                rule=('Loại bộ ra trong 5 kỳ gần, tiến liên tiếp, tam hoa; trừ điểm nhẹ kép kẹp; giữ 340 bộ chữ số nặng nhất theo hàng (50 kỳ). Kiểm 300 kỳ: cặp ĐB rơi vào pool 13–14% số kỳ (chia đều 12%).' if kind == 'plus'
                      else 'Loại bộ ra trong 20 kỳ gần, tiến liên tiếp, tam hoa. Pro chưa có dấu vết chữ số ổn định → pool rộng, chọn trong pool theo tâm linh.'))
def stats(f):
    D = json.load(open(os.path.join(HERE, f))); R = D['res']; T = len(R)
    pos = []
    for i in range(3):
        c = [0] * 10
        for r in R[-100:]:
            for s in r: c[int(s[i])] += 1
        light = sorted(range(10), key=lambda d: (c[d], d))[:3]
        pos.append(dict(c=c, light=light))
    return dict(n=T, first=D['dates'][0], last=D['dates'][-1], recent=[dict(d=d, r=r) for d, r in zip(D['dates'][-12:], R[-12:])], pos=pos)
out = {
    'plus': dict(stats('max3d_data.json'), goiy=goiy('max3d_data.json', 'plus'), name='Max 3D+', days='Thứ 2, 4, 6 lúc 18h (chung kết quả với Max 3D)',
                 prizes=[['Đặc biệt', 'Cả 2 bộ trùng 2 số Đặc biệt (không xét thứ tự)', 1e9, 500000],
                         ['Nhất', 'Cả 2 bộ nằm trong 4 số giải Nhất', 40e6, 83500], ['Nhì', 'Cả 2 bộ nằm trong 6 số giải Nhì', 10e6, 33467],
                         ['Ba', 'Cả 2 bộ nằm trong 8 số giải Ba', 5e6, 17965], ['Tư', 'Cả 2 bộ nằm trong 20 số', 1e6, 2679],
                         ['Năm', 'Mỗi bộ trùng 1 số Đặc biệt', 150e3, 250], ['Sáu', 'Mỗi bộ trùng 1 số Nhất/Nhì/Ba', 40e3, 28]],
                 rtp=54.6, win=3.92,
                 trace='Dấu vết đang theo dõi: chữ số nhẹ nhất 100 kỳ của mỗi hàng ra ít hơn ở cả 3 đoạn 100 kỳ (29,3% · 27,9% · 29,2%, chia đều 30%). Nghiêng nhẹ, chưa áp dụng; cần sổ kiểm chứng xác nhận.'),
    'pro': dict(stats('max3dpro_data.json'), goiy=goiy('max3dpro_data.json', 'pro'), name='Max 3D Pro', days='Thứ 3, 5, 7 (kết quả riêng)',
                prizes=[['Đặc biệt', '2 bộ trùng 2 số Đặc biệt ĐÚNG thứ tự quay', 2e9, 1000000],
                        ['Phụ Đặc biệt', '2 bộ trùng 2 số Đặc biệt NGƯỢC thứ tự', 400e6, 1000000],
                        ['Nhất', 'Cả 2 bộ nằm trong 4 số giải Nhất', 30e6, 83500], ['Nhì', 'Cả 2 bộ nằm trong 6 số giải Nhì', 10e6, 33467],
                        ['Ba', 'Cả 2 bộ nằm trong 8 số giải Ba', 4e6, 17965], ['Tư', 'Cả 2 bộ nằm trong 20 số', 1e6, 2679],
                        ['Năm', 'Mỗi bộ trùng 1 số Đặc biệt', 100e3, 250], ['Sáu', 'Mỗi bộ trùng 1 số Nhất/Nhì/Ba', 40e3, 28]],
                rtp=54.8, win=3.92,
                trace='Chưa có dấu vết bi ổn định: chữ số nặng hay nhẹ theo mọi khung 10/20/50/100 kỳ đều quanh 30% (28,5–31,4%).'),
}
json.dump(out, open(os.path.join(HERE, 'max3d_app.json'), 'w'), ensure_ascii=False)
# lưu gợi ý đã đưa (để chấm sổ khi có kết quả); không ghi trùng kỳ
lg = os.path.join(HERE, 'max3d_goiy_log.jsonl'); seen = set()
if os.path.exists(lg): seen = {(j['game'], j['next']) for j in map(json.loads, open(lg, encoding='utf-8')) if j}
with open(lg, 'a', encoding='utf-8') as fo:
    for k in ('plus', 'pro'):
        g = out[k]['goiy']
        if (k, g['next']) not in seen: fo.write(json.dumps(dict(game=k, next=g['next'], pairs=[p['x'] for p in g['pairs']], kinds=[p['kind'] for p in g['pairs']], pool_n=g['pool_n'], pool=g['pool_all']), ensure_ascii=False) + '\n')
for k in ('plus', 'pro'):
    g = out[k]['goiy']; print(out[k]['name'], g['next'], 'pool', g['pool_n'], [ (p['kind'], p['x']) for p in g['pairs']])
print('ok max3d_app.json', out['plus']['last'], out['pro']['last'])
