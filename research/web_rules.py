"""Các quy luật lấy từ web: bóng âm/dương, Cửu tinh ngày, giá trị Can Chi.
Dùng chung khung kiểm định (study.study) với các quy luật khác."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from study import study, date_info, root, DIG, SINH
from more_rules import sun_long_deg

BONG_DUONG = {0: 5, 5: 0, 1: 6, 6: 1, 2: 7, 7: 2, 3: 8, 8: 3, 4: 9, 9: 4}
BONG_AM = {0: 7, 7: 0, 1: 4, 4: 1, 2: 9, 9: 2, 3: 6, 6: 3, 5: 8, 8: 5}
STAR_EL = {1: 'Thủy', 2: 'Thổ', 3: 'Mộc', 4: 'Mộc', 5: 'Thổ', 6: 'Kim', 7: 'Kim', 8: 'Thổ', 9: 'Hỏa'}
CAN_VAL = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]          # Giáp Ất 1, Bính Đinh 2, Mậu Kỷ 3, Canh Tân 4, Nhâm Quý 5
CHI_VAL = [0, 0, 1, 1, 2, 2, 0, 0, 1, 1, 2, 2]    # Tý Sửu Ngọ Mùi 0, Dần Mão Thân Dậu 1, Thìn Tỵ Tuất Hợi 2

_SW = {}
def switch_points(year):
    """Ngày Giáp Tý gần Đông chí (bắt đầu dương độn, sao 1 tăng dần) và gần Hạ chí (âm độn, sao 9 giảm dần)."""
    if year in _SW: return _SW[year]
    from lunar import jd_from_date
    pts = []
    for y in (year-1, year):
        for target, kind in ((90, 'am'), (270, 'duong')):
            jd = jd_from_date(1, 6 if target == 90 else 12, y)
            while not (sun_long_deg(jd, 12) >= target and sun_long_deg(jd-1, 12) < target): jd += 1
            gt = min((j for j in range(jd-35, jd+35) if (j+9) % 10 == 0 and (j+1) % 12 == 0), key=lambda j: abs(j-jd))
            pts.append((gt, kind))
    _SW[year] = sorted(pts); return _SW[year]
def day_star(i):
    start, kind = [p for p in switch_points(i['y']) if p[0] <= i['jd']][-1]
    k = (i['jd'] - start) % 9
    return 1 + k if kind == 'duong' else 9 - k

def rules(mx):
    rng = range(1, mx+1)
    one = lambda f: (lambda i: {v for v in [f(i)] if 1 <= v <= mx})
    many = lambda f: (lambda i: {v for v in f(i) if 1 <= v <= mx})
    def bong(n, B):  # đổi từng chữ số của n sang bóng
        s = f'{n:02d}'; return int(''.join(str(B[int(c)]) for c in s))
    good = lambda E: {n for n in rng if DIG[n % 10] in (E, SINH[E])}
    return {
      'Bóng dương của ngày (26->71)': one(lambda i: bong(i['d'], BONG_DUONG)),
      'Bóng âm của ngày (26->93)': one(lambda i: bong(i['d'], BONG_AM)),
      'Bóng dương của tháng': one(lambda i: bong(i['m'], BONG_DUONG)),
      'Bóng dương của ngày âm': one(lambda i: bong(i['ld'], BONG_DUONG)),
      'Bóng âm của ngày âm': one(lambda i: bong(i['ld'], BONG_AM)),
      'Số tận cùng = bóng dương của d%10': many(lambda i: {n for n in rng if n % 10 == BONG_DUONG[i['d'] % 10]}),
      'Số tận cùng = bóng âm của d%10': many(lambda i: {n for n in rng if n % 10 == BONG_AM[i['d'] % 10]}),
      'Số tận cùng = bóng dương của daySum': many(lambda i: {n for n in rng if n % 10 == BONG_DUONG[i['ds'] % 10]}),
      'Cửu tinh ngày (1..9)': one(lambda i: day_star(i)),
      'Rút gọn = sao Cửu tinh ngày': many(lambda i: {n for n in rng if root(n) == day_star(i)}),
      'Tận cùng = sao Cửu tinh ngày': many(lambda i: {n for n in rng if n % 10 == day_star(i) % 10}),
      'Hành sao Cửu tinh: tỷ hòa/được sinh': many(lambda i: good(STAR_EL[day_star(i)])),
      'Giá trị Can+Chi ngày (1..7)': one(lambda i: CAN_VAL[i['can']] + CHI_VAL[i['chi']]),
      'Ghép giá trị Can, Chi (vd 51)': one(lambda i: CAN_VAL[i['can']]*10 + CHI_VAL[i['chi']]),
    }

if __name__ == '__main__':
    if sys.argv[1:2] == ['ex']:
        for dd in [(2026, 9, 26), (2026, 9, 27), (2026, 12, 25), (2026, 6, 25)]:
            i = date_info(*dd, 18); print(dd, 'Cửu tinh ngày', day_star(i), {k: sorted(f(i)) for k, f in rules(55).items() if 'Bóng' in k and 'Số' not in k})
        sys.exit()
    perms = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    for game in ['power655', 'mega645', 'loto535']:
        mx, c, n, cut, res, thr = study(game, perms, rules_fn=rules)
        print(f'\n=== {game}: {n} kỳ, {len(res)} quy luật từ web; ngưỡng may mắn |z| = {thr:.2f}')
        for name, zA, HA, EA, zT, zV in sorted(res, key=lambda r: -abs(r[1])):
            print(f"  {name:40s} trúng {HA:5.0f}/{EA:6.1f} ({(HA/EA-1)*100:+4.0f}%) z {zA:5.2f} p={math.erfc(abs(zA)/2**.5):.3f} | cũ {zT:5.2f} mới {zV:5.2f} {'cùng chiều' if zT*zV > 0 else 'ĐẢO'}")
