#!/usr/bin/env python3
"""Dữ liệu cho ô "Max 3D+ / Max 3D Pro" trong app → build/max3d_app.json (assemble.py nhúng vào /*MAX3D*/).
Max 3D+ dùng kết quả Max 3D (thứ 2, 4, 6); Max 3D Pro có kết quả riêng (thứ 3, 5, 7).
  python3 build/max3d_app.py   (chạy sau khi cập nhật build/max3d_data.json, max3dpro_data.json)"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
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
    'plus': dict(stats('max3d_data.json'), name='Max 3D+', days='Thứ 2, 4, 6 lúc 18h (chung kết quả với Max 3D)',
                 prizes=[['Đặc biệt', 'Cả 2 bộ trùng 2 số Đặc biệt (không xét thứ tự)', 1e9, 500000],
                         ['Nhất', 'Cả 2 bộ nằm trong 4 số giải Nhất', 40e6, 83500], ['Nhì', 'Cả 2 bộ nằm trong 6 số giải Nhì', 10e6, 33467],
                         ['Ba', 'Cả 2 bộ nằm trong 8 số giải Ba', 5e6, 17965], ['Tư', 'Cả 2 bộ nằm trong 20 số', 1e6, 2679],
                         ['Năm', 'Mỗi bộ trùng 1 số Đặc biệt', 150e3, 250], ['Sáu', 'Mỗi bộ trùng 1 số Nhất/Nhì/Ba', 40e3, 28]],
                 rtp=54.6, win=3.92,
                 trace='Dấu vết đang theo dõi: chữ số nhẹ nhất 100 kỳ của mỗi hàng ra ít hơn ở cả 3 đoạn 100 kỳ (29,3% · 27,9% · 29,2%, chia đều 30%). Nghiêng nhẹ, chưa áp dụng; cần sổ kiểm chứng xác nhận.'),
    'pro': dict(stats('max3dpro_data.json'), name='Max 3D Pro', days='Thứ 3, 5, 7 (kết quả riêng)',
                prizes=[['Đặc biệt', '2 bộ trùng 2 số Đặc biệt ĐÚNG thứ tự quay', 2e9, 1000000],
                        ['Phụ Đặc biệt', '2 bộ trùng 2 số Đặc biệt NGƯỢC thứ tự', 400e6, 1000000],
                        ['Nhất', 'Cả 2 bộ nằm trong 4 số giải Nhất', 30e6, 83500], ['Nhì', 'Cả 2 bộ nằm trong 6 số giải Nhì', 10e6, 33467],
                        ['Ba', 'Cả 2 bộ nằm trong 8 số giải Ba', 4e6, 17965], ['Tư', 'Cả 2 bộ nằm trong 20 số', 1e6, 2679],
                        ['Năm', 'Mỗi bộ trùng 1 số Đặc biệt', 100e3, 250], ['Sáu', 'Mỗi bộ trùng 1 số Nhất/Nhì/Ba', 40e3, 28]],
                rtp=54.8, win=3.92,
                trace='Chưa có dấu vết bi ổn định: chữ số nặng hay nhẹ theo mọi khung 10/20/50/100 kỳ đều quanh 30% (28,5–31,4%).'),
}
json.dump(out, open(os.path.join(HERE, 'max3d_app.json'), 'w'), ensure_ascii=False)
print('ok max3d_app.json', out['plus']['last'], out['pro']['last'])
