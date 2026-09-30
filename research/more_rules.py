"""Thêm các hệ lấy số từ ngày: Tiết khí, Can Chi tháng/năm, Trực, Lục thập hoa giáp, Nhị thập bát tú,
Khổng Minh Lục Diệu, Tam hợp/Lục hợp/Xung, Can hợp, cặp số trong chuỗi ngày, cung hoàng đạo, tuần ISO,
và nhóm đối chứng từ kỳ trước."""
import sys, os, datetime, math
sys.path.insert(0, os.path.dirname(__file__))
from study import study, date_info, root, NAP, SINH, DIG

def sun_long_deg(jd, h=0, tz=7):
    T = (jd - 0.5 + h/24 - tz/24 - 2451545.0)/36525; dr = math.pi/180
    M = 357.52910 + 35999.05030*T - 0.0001559*T*T
    L0 = 280.46645 + 36000.76983*T + 0.0003032*T*T
    C = (1.914600 - 0.004817*T)*math.sin(dr*M) + 0.019993*math.sin(2*dr*M) + 0.000290*math.sin(3*dr*M)
    return (L0 + C) % 360

def extra(i):
    L = sun_long_deg(i['jd'], i['h'])
    tiet = int(L//15)                                  # 0 = Xuân phân ... 21 = Lập xuân
    tiet_from_lx = (tiet - 21) % 24                    # 0 = Lập xuân .. 23 = Đại hàn
    days_in = next(k for k in range(0, 20) if int(sun_long_deg(i['jd']-k-1, 0)//15) != tiet) + 1
    mon = int(((L - 315) % 360)//30)                   # 0 = tháng Dần
    mchi = (2 + mon) % 12
    Y = i['y'] if not (i['m'] <= 2 and mon >= 10) else i['y'] - 1   # năm tiết khí (đổi ở Lập xuân)
    ycan, ychi = (Y + 6) % 10, (Y + 8) % 12
    mcan = (ycan*2 + 2 + mon) % 10
    kk = lambda c, z: next(k for k in range(60) if k % 10 == c and k % 12 == z)
    return dict(tiet=tiet_from_lx, tday=days_in, mcan=mcan, mchi=mchi, ycan=ycan, ychi=ychi,
                mnap=NAP[kk(mcan, mchi)//2], ynap=NAP[kk(ycan, ychi)//2],
                truc=(i['chi'] - mchi) % 12, hoagiap=kk(i['can'], i['chi']),
                tu28=(i['jd'] + 11) % 28, lucdieu=(i['lm']-1 + i['ld']-1 + i['hchi']) % 6)

ZOD = [(1,20),(2,19),(3,21),(4,20),(5,21),(6,21),(7,23),(8,23),(9,23),(10,23),(11,22),(12,22)]
def zodiac(m, d):  # 1 = Bảo Bình (20/1) .. 12 = Ma Kết
    k = 0
    for idx, (mm, dd) in enumerate(ZOD):
        if (m, d) >= (mm, dd): k = idx
    return k + 1 if (m, d) >= ZOD[0] else 12

def rules(mx):
    X = {}
    def ex(i):
        key = (i['jd'], i['h'])
        if key not in X: X[key] = extra(i)
        return X[key]
    one = lambda f: (lambda i: {v for v in [f(i)] if 1 <= v <= mx})
    many = lambda f: (lambda i: {v for v in f(i) if 1 <= v <= mx})
    rng = range(1, mx+1)
    good = lambda E: {n for n in rng if DIG[n % 10] in (E, SINH[E])}
    TAM = lambda z: {z, (z+4) % 12, (z+8) % 12}
    LUC = lambda z: (1 - z) % 12                       # Tý-Sửu, Dần-Hợi, Mão-Tuất, ...
    nchi = lambda n: (n - 1) % 12                      # số 1 = Tý, 2 = Sửu, ...
    ncan = lambda n: (n - 1) % 10                      # số 1 = Giáp, ...
    def pairs(s):
        return {int(s[k:k+2]) for k in range(len(s)-1)}
    return {
      'Tiết khí thứ (1..24, từ Lập xuân)': one(lambda i: ex(i)['tiet'] + 1),
      'Ngày thứ mấy trong tiết': one(lambda i: ex(i)['tday']),
      'Can tháng (1..10)': one(lambda i: ex(i)['mcan'] + 1),
      'Chi tháng (1..12)': one(lambda i: ex(i)['mchi'] + 1),
      'Can năm / Chi năm': many(lambda i: {ex(i)['ycan'] + 1, ex(i)['ychi'] + 1}),
      'Nạp Âm tháng: tỷ hòa/được sinh': many(lambda i: good(ex(i)['mnap'])),
      'Nạp Âm năm: tỷ hòa/được sinh': many(lambda i: good(ex(i)['ynap'])),
      'Trực (1=Kiến..12=Bế)': one(lambda i: ex(i)['truc'] + 1),
      'Lục thập hoa giáp (1..60)': one(lambda i: ex(i)['hoagiap'] + 1),
      'Nhị thập bát tú (1..28, mốc chưa xác minh)': one(lambda i: ex(i)['tu28'] + 1),
      'Khổng Minh Lục Diệu (1..6)': one(lambda i: ex(i)['lucdieu'] + 1),
      'Số có Chi tam hợp Chi ngày': many(lambda i: {n for n in rng if nchi(n) in TAM(i['chi'])}),
      'Số có Chi lục hợp Chi ngày': many(lambda i: {n for n in rng if nchi(n) == LUC(i['chi'])}),
      'Số có Chi xung Chi ngày': many(lambda i: {n for n in rng if nchi(n) == (i['chi'] + 6) % 12}),
      'Số có Chi = Chi ngày': many(lambda i: {n for n in rng if nchi(n) == i['chi']}),
      'Số có Can hợp Can ngày': many(lambda i: {n for n in rng if ncan(n) == (i['can'] + 5) % 10}),
      'Số có Can = Can ngày': many(lambda i: {n for n in rng if ncan(n) == i['can']}),
      'Cặp số liền trong ddmmyyyy': many(lambda i: pairs(f"{i['d']:02d}{i['m']:02d}{i['y']}")),
      'Cặp số liền trong ngày-tháng âm': many(lambda i: pairs(f"{i['ld']:02d}{i['lm']:02d}")),
      'Ghép ngày âm đảo (16->61)': one(lambda i: int(f"{i['ld']:02d}"[::-1])),
      'Cung hoàng đạo (1..12)': one(lambda i: zodiac(i['m'], i['d'])),
      'Tuần ISO trong năm': one(lambda i: datetime.date(i['y'], i['m'], i['d']).isocalendar()[1]),
      'Life path (không rút 11/22/33)': one(lambda i: (lambda s: s if s in (11, 22, 33) else root(s))(i['dsum'])),
      'ĐỐI CHỨNG: số kỳ trước': many(lambda i: i['prev']),
      'ĐỐI CHỨNG: kỳ trước ±1': many(lambda i: {n+k for n in i['prev'] for k in (-1, 1)} - i['prev']),
    }

if __name__ == '__main__':
    if sys.argv[1:2] == ['ex']:
        i = date_info(2026, 9, 26, 18); i['prev'] = set(); print(extra(i))
        for n, f in rules(55).items(): print(f'  {n}: {sorted(f(i))}')
        sys.exit()
    perms = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    for game in ['power655', 'mega645', 'loto535']:
        mx, c, n, cut, res, thr = study(game, perms, rules_fn=rules)
        print(f'\n=== {game}: {len(res)} quy luật mới; ngưỡng may mắn |z| = {thr:.2f}')
        res.sort(key=lambda r: -abs(r[1]))
        for name, zA, HA, EA, zT, zV in res[:8]:
            same = '✓' if zT*zV > 0 else '✗'
            print(f'{name:44s} tìm {zT:6.2f} kiểm {zV:6.2f} {same} toàn {zA:6.2f}  trúng {HA:5.0f}/{EA:6.1f}')
