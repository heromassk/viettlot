"""Kinh Dịch — lập quẻ Mai Hoa Dịch Số theo ngày giờ quay, rút số, kiểm định trên lịch sử.
Quẻ thượng = (Chi năm âm + tháng âm + ngày âm) mod 8; quẻ hạ = (tổng + Chi giờ) mod 8; hào động = tổng mod 6.
Chi đánh số Tý=1..Hợi=12. Số quẻ Tiên Thiên: Càn1 Đoài2 Ly3 Chấn4 Tốn5 Khảm6 Cấn7 Khôn8."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from study import study, date_info, SINH, KHAC, DIG

NAME = {1:'Càn', 2:'Đoài', 3:'Ly', 4:'Chấn', 5:'Tốn', 6:'Khảm', 7:'Cấn', 8:'Khôn'}
LINES = {1:(1,1,1), 2:(1,1,0), 3:(1,0,1), 4:(1,0,0), 5:(0,1,1), 6:(0,1,0), 7:(0,0,1), 8:(0,0,0)}  # hào dưới -> trên
BY_LINES = {v: k for k, v in LINES.items()}
ELEM = {1:'Kim', 2:'Kim', 3:'Hỏa', 4:'Mộc', 5:'Mộc', 6:'Thủy', 7:'Thổ', 8:'Thổ'}
HAU_THIEN = {6:1, 8:2, 4:3, 5:4, 1:6, 2:7, 7:8, 3:9}  # số Lạc Thư (Hậu Thiên) của quẻ đơn
# Số thứ tự Văn Vương: KW[thượng][hạ], cột hạ theo thứ tự Càn Chấn Khảm Cấn Khôn Tốn Ly Đoài
_ORD = [1, 4, 6, 7, 8, 5, 3, 2]
_TBL = {1:[1,25,6,33,12,44,13,10], 4:[34,51,40,62,16,32,55,54], 6:[5,3,29,39,8,48,63,60],
        7:[26,27,4,52,23,18,22,41], 8:[11,24,7,15,2,46,36,19], 5:[9,42,59,53,20,57,37,61],
        3:[14,21,64,56,35,50,30,38], 2:[43,17,47,31,45,28,49,58]}
KW = {(u, l): _TBL[u][_ORD.index(l)] for u in _TBL for l in _ORD}
assert sorted(KW.values()) == list(range(1, 65))

def m8(x): return x % 8 or 8
def m6(x): return x % 6 or 6

def mai_hoa(i, solar=False):
    if solar: base = (i['y'] % 100) + i['m'] + i['d']
    else: base = ((i['ly'] + 8) % 12 + 1) + i['lm'] + i['ld']
    hour = i['hchi'] + 1
    up, lo = m8(base), m8(base + hour); mv = m6(base + hour)
    six = list(LINES[lo]) + list(LINES[up])
    ch = six[:]; ch[mv-1] ^= 1
    bup, blo = BY_LINES[tuple(ch[3:])], BY_LINES[tuple(ch[:3])]
    hup, hlo = BY_LINES[tuple(six[2:5])], BY_LINES[tuple(six[1:4])]
    the, dung = (lo, up) if mv > 3 else (up, lo)   # quẻ có hào động là Dụng
    return dict(up=up, lo=lo, mv=mv, kw=KW[(up, lo)], bkw=KW[(bup, blo)], hkw=KW[(hup, hlo)],
                the=the, dung=dung, bin=int(''.join(map(str, six[::-1])), 2))

def rules(mx):
    R = {}
    for tag, solar in [('MH âm', False), ('MH dương', True)]:
        g = lambda i, s=solar: mai_hoa(i, s)
        def one(f): return lambda i: {v for v in [f(i)] if 1 <= v <= mx}
        def many(f): return lambda i: {v for v in f(i) if 1 <= v <= mx}
        R[f'{tag}: số quẻ chủ (Văn Vương)'] = one(lambda i, g=g: g(i)['kw'])
        R[f'{tag}: số quẻ chủ mod max'] = one(lambda i, g=g: (g(i)['kw']-1) % mx + 1)
        R[f'{tag}: số quẻ biến'] = one(lambda i, g=g: g(i)['bkw'])
        R[f'{tag}: số quẻ hỗ'] = one(lambda i, g=g: g(i)['hkw'])
        R[f'{tag}: ghép thượng-hạ (vd 36)'] = one(lambda i, g=g: g(i)['up']*10 + g(i)['lo'])
        R[f'{tag}: ghép hạ-thượng (vd 63)'] = one(lambda i, g=g: g(i)['lo']*10 + g(i)['up'])
        R[f'{tag}: số Tiên Thiên thượng+hạ'] = many(lambda i, g=g: {g(i)['up'], g(i)['lo']})
        R[f'{tag}: số Hậu Thiên thượng+hạ'] = many(lambda i, g=g: {HAU_THIEN[g(i)['up']], HAU_THIEN[g(i)['lo']]})
        R[f'{tag}: hào động'] = one(lambda i, g=g: g(i)['mv'])
        R[f'{tag}: nhị phân quẻ +1'] = one(lambda i, g=g: g(i)['bin'] + 1)
        R[f'{tag}: tất cả số đơn gộp'] = many(lambda i, g=g: {g(i)[k] for k in ('kw','bkw','hkw','up','lo','mv')} | {g(i)['up']*10+g(i)['lo']})
        for rel, test in [('tỷ hòa Thể', lambda E, e: e == E), ('sinh Thể', lambda E, e: SINH[e] == E),
                          ('Thể sinh', lambda E, e: SINH[E] == e), ('khắc Thể', lambda E, e: KHAC[e] == E),
                          ('Thể khắc', lambda E, e: KHAC[E] == e)]:
            R[f'{tag}: hành số {rel}'] = many(lambda i, g=g, test=test: {n for n in range(1, mx+1) if test(ELEM[g(i)['the']], DIG[n % 10])})
        R[f'{tag}: tận cùng = số quẻ Thể/Dụng'] = many(lambda i, g=g: {n for n in range(1, mx+1) if n % 10 in (g(i)['the'] % 10, g(i)['dung'] % 10)})
    return R

if __name__ == '__main__':
    if sys.argv[1:2] == ['ex']:
        i = date_info(2026, 9, 26, 18); q = mai_hoa(i)
        print(f"26/09/2026 18h = âm {i['ld']}/{i['lm']}; quẻ {NAME[q['up']]}/{NAME[q['lo']]} (số {q['kw']}), hào động {q['mv']}, "
              f"biến {q['bkw']}, hỗ {q['hkw']}, Thể {NAME[q['the']]} ({ELEM[q['the']]}), Dụng {NAME[q['dung']]} ({ELEM[q['dung']]})")
        W = {14,18,21,38,48,52}
        for n, f in rules(55).items():
            if n.startswith('MH âm'): print(f'  {n}: {sorted(f(i))}  trúng {sorted(f(i) & W)}')
        sys.exit()
    perms = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    for game in ['power655', 'mega645', 'loto535']:
        mx, c, n, cut, res, thr = study(game, perms, rules_fn=rules)
        print(f'\n=== {game}: {n} kỳ (tìm {cut} / kiểm {n-cut}), {len(res)} quy luật Kinh Dịch; ngưỡng may mắn |z| = {thr:.2f}')
        res.sort(key=lambda r: -abs(r[4]))
        for name, zA, HA, EA, zT, zV in res[:8]:
            same = '✓' if zT*zV > 0 and abs(zV) > 1.64 else ' '
            print(f'{name:40s} tìm {zT:6.2f}  kiểm {zV:6.2f}{same}  toàn {zA:6.2f}  trúng {HA:5.0f} / kỳ vọng {EA:6.1f}')
