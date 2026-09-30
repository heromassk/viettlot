"""Chiêm tinh (phương Tây + Ấn Độ) cho thời điểm quay số, tính bằng công thức thiên văn (không cần mạng):
- Mặt Trời, Mặt Trăng (Meeus, sai ~0,01–0,3°), 5 hành tinh Thủy/Kim/Hỏa/Mộc/Thổ (phần tử quỹ đạo JPL 1800–2050, sai < 1°).
- Cung hoàng đạo (nhiệt đới), pha trăng, tuổi trăng, Nakshatra (thiên văn Ấn, ayanamsa Lahiri gần đúng),
  hành tinh chủ ngày, giờ hành tinh lúc quay (theo mặt trời mọc/lặn ở Hà Nội), hành tinh nghịch hành.
Mỗi quy luật: info (study.date_info) → tập số trong 1..mx. Số của hành tinh theo thần số học Cheiro:
Mặt Trời 1, Mặt Trăng 2, Mộc 3, Thủy 5, Kim 6, Thổ 8, Hỏa 9."""
import math
D2R = math.pi/180
def _n(x): return x % 360
def jd_ut(i):  # giờ Việt Nam (UTC+7) → Julian Day UT
    return i['jd'] - 0.5 + (i['h'] - 7)/24

def sun_lon(jd):
    T = (jd - 2451545.0)/36525
    M = 357.52911 + 35999.05029*T; L0 = 280.46646 + 36000.76983*T
    C = (1.914602 - 0.004817*T)*math.sin(D2R*M) + (0.019993 - 0.000101*T)*math.sin(2*D2R*M) + 0.000289*math.sin(3*D2R*M)
    return _n(L0 + C)

MOON_TERMS = [  # (hệ số, D, M, M', F) — các số hạng lớn nhất của kinh độ Mặt Trăng (Meeus ch.47)
    (6.288774, 0, 0, 1, 0), (1.274027, 2, 0, -1, 0), (0.658314, 2, 0, 0, 0), (0.213618, 0, 0, 2, 0),
    (-0.185116, 0, 1, 0, 0), (-0.114332, 0, 0, 0, 2), (0.058793, 2, 0, -2, 0), (0.057066, 2, -1, -1, 0),
    (0.053322, 2, 0, 1, 0), (0.045758, 2, -1, 0, 0), (-0.040923, 0, 1, -1, 0), (-0.034720, 1, 0, 0, 0),
    (-0.030383, 0, 1, 1, 0), (0.015327, 2, 0, 0, -2), (-0.012528, 0, 0, 1, 2), (0.010980, 0, 0, 1, -2),
    (0.010675, 4, 0, -1, 0), (0.010034, 0, 0, 3, 0), (0.008548, 4, 0, -2, 0), (-0.007888, 2, 1, -1, 0),
    (-0.006766, 2, 1, 0, 0), (-0.005163, 1, 0, -1, 0), (0.004987, 1, 1, 0, 0), (0.004036, 2, -1, 1, 0)]
def moon_lon(jd):
    T = (jd - 2451545.0)/36525
    Lp = 218.3164477 + 481267.88123421*T; D = 297.8501921 + 445267.1114034*T
    M = 357.5291092 + 35999.0502909*T; Mp = 134.9633964 + 477198.8675055*T; F = 93.2720950 + 483202.0175233*T
    s = sum(k*math.sin(D2R*(a*D + b*M + c*Mp + d*F)) for k, a, b, c, d in MOON_TERMS)
    return _n(Lp + s)

# phần tử quỹ đạo (a, e, I, L, ϖ, Ω) và tốc độ mỗi thế kỷ — JPL "Approximate Positions of the Planets", 1800–2050
PLANETS = {
    'Thủy': ((0.38709927, 0.20563593, 7.00497902, 252.25032350, 77.45779628, 48.33076593),
             (0.00000037, 0.00001906, -0.00594749, 149472.67411175, 0.16047689, -0.12534081)),
    'Kim':  ((0.72333566, 0.00677672, 3.39467605, 181.97909950, 131.60246718, 76.67984255),
             (0.00000390, -0.00004107, -0.00078890, 58517.81538729, 0.00268329, -0.27769418)),
    'Đất':  ((1.00000261, 0.01671123, -0.00001531, 100.46457166, 102.93768193, 0.0),
             (0.00000562, -0.00004392, -0.01294668, 35999.37244981, 0.32327364, 0.0)),
    'Hỏa':  ((1.52371034, 0.09339410, 1.84969142, -4.55343205, -23.94362959, 49.55953891),
             (0.00001847, 0.00007882, -0.00813131, 19140.30268499, 0.44441088, -0.29257343)),
    'Mộc':  ((5.20288700, 0.04838624, 1.30439695, 34.39644051, 14.72847983, 100.47390909),
             (-0.00011607, -0.00013253, -0.00183714, 3034.74612775, 0.21252668, 0.20469106)),
    'Thổ':  ((9.53667594, 0.05386179, 2.48599187, 49.95424423, 92.59887831, 113.66242448),
             (-0.00125060, -0.00050991, 0.00193609, 1222.49362201, -0.41897216, -0.28867794))}
def helio(name, jd):
    T = (jd - 2451545.0)/36525
    (a, e, I, L, w, O), (da, de, dI, dL, dw, dO) = PLANETS[name]
    a += da*T; e += de*T; I += dI*T; L += dL*T; w += dw*T; O += dO*T
    M = math.radians(_n(L - w)); om = math.radians(w - O); O = math.radians(O); I = math.radians(I)
    E = M
    for _ in range(12): E = E - (E - e*math.sin(E) - M)/(1 - e*math.cos(E))
    xp = a*(math.cos(E) - e); yp = a*math.sqrt(1 - e*e)*math.sin(E)
    x = (math.cos(om)*math.cos(O) - math.sin(om)*math.sin(O)*math.cos(I))*xp + (-math.sin(om)*math.cos(O) - math.cos(om)*math.sin(O)*math.cos(I))*yp
    y = (math.cos(om)*math.sin(O) + math.sin(om)*math.cos(O)*math.cos(I))*xp + (-math.sin(om)*math.sin(O) + math.cos(om)*math.cos(O)*math.cos(I))*yp
    return x, y
def planet_lon(name, jd):
    px, py = helio(name, jd); ex, ey = helio('Đất', jd)
    return _n(math.degrees(math.atan2(py - ey, px - ex)))

LAT, LON = 21.0285, 105.8542   # Hà Nội
def sun_times(i):
    """giờ mặt trời mọc / lặn (giờ VN) trong ngày quay."""
    lam = sun_lon(i['jd'] - 0.5 + (12 - 7)/24)
    dec = math.asin(math.sin(D2R*23.44)*math.sin(D2R*lam))
    B = D2R*360*(i['doy'] - 81)/364
    eot = 9.87*math.sin(2*B) - 7.53*math.cos(B) - 1.5*math.sin(B)      # phút
    noon = 12 - (LON - 105)/15 - eot/60
    H0 = math.degrees(math.acos((math.sin(D2R*-0.833) - math.sin(D2R*LAT)*math.sin(dec))/(math.cos(D2R*LAT)*math.cos(dec))))
    return noon - H0/15, noon + H0/15
CHALDEAN = ['Thổ', 'Mộc', 'Hỏa', 'Mặt Trời', 'Kim', 'Thủy', 'Mặt Trăng']
DAY_RULER = {1: 'Mặt Trăng', 2: 'Hỏa', 3: 'Thủy', 4: 'Mộc', 5: 'Kim', 6: 'Thổ', 7: 'Mặt Trời'}   # wd: 1 = Thứ 2 .. 7 = CN
CHEIRO = {'Mặt Trời': 1, 'Mặt Trăng': 2, 'Mộc': 3, 'Thủy': 5, 'Kim': 6, 'Thổ': 8, 'Hỏa': 9}
def planetary_hour(i):
    rise, set_ = sun_times(i); h = i['h']
    if rise <= h < set_: k = int((h - rise)/((set_ - rise)/12))
    elif h >= set_: k = 12 + int((h - set_)/((24 - (set_ - rise))/12))
    else: k = 12 + int((h + 24 - set_)/((24 - (set_ - rise))/12))   # trước bình minh: thuộc đêm hôm trước (hiếm với giờ quay)
    day = DAY_RULER[i['wd']]
    return CHALDEAN[(CHALDEAN.index(day) + min(k, 23)) % 7]

def astro(i):
    if '_astro' in i: return i['_astro']
    jd = jd_ut(i); s = sun_lon(jd); m = moon_lon(jd); el = _n(m - s)
    ayan = 23.853 + (i['y'] - 2000)*0.013972           # Lahiri gần đúng
    pl = {p: planet_lon(p, jd) for p in ('Thủy', 'Kim', 'Hỏa', 'Mộc', 'Thổ')}
    retro = {p: _n(planet_lon(p, jd + 0.5) - planet_lon(p, jd - 0.5) + 180) - 180 < 0 for p in pl}
    sign = lambda lon: int(lon//30) + 1                # 1 = Bạch Dương .. 12 = Song Ngư
    A = dict(sun=s, moon=m, msign=sign(m), ssign=sign(s), phase=int(_n(el + 22.5)//45) + 1, age=int(el/360*29.530589) + 1,
             nak=int(_n(m - ayan)//(360/27)) + 1, mdeg=int(m % 30) + 1, sdeg=int(s % 30) + 1,
             psign={p: sign(v) for p, v in pl.items()}, retro=retro, nretro=sum(retro.values()),
             dayr=DAY_RULER[i['wd']], hourr=planetary_hour(i))
    i['_astro'] = A; return A

def _root(n):
    while n > 9: n = sum(map(int, str(n)))
    return n
def rules(mx):
    one = lambda f: (lambda i: {v for v in [f(i)] if 1 <= v <= mx})
    grp = lambda f, mod: (lambda i: {n for n in range(1, mx+1) if n % mod == f(i) % mod})
    R = {
      'Chiêm tinh: cung Mặt Trăng (1..12)': one(lambda i: astro(i)['msign']),
      'Chiêm tinh: số ≡ cung Mặt Trăng (mod 12)': grp(lambda i: astro(i)['msign'], 12),
      'Chiêm tinh: cung Mặt Trời thiên văn (1..12)': one(lambda i: astro(i)['ssign']),
      'Chiêm tinh: pha Mặt Trăng (1..8)': one(lambda i: astro(i)['phase']),
      'Chiêm tinh: số ≡ pha Mặt Trăng (mod 8)': grp(lambda i: astro(i)['phase'], 8),
      'Chiêm tinh: tuổi trăng (1..30)': one(lambda i: astro(i)['age']),
      'Chiêm tinh: Nakshatra (1..27)': one(lambda i: astro(i)['nak']),
      'Chiêm tinh: số ≡ Nakshatra (mod 27)': grp(lambda i: astro(i)['nak'], 27),
      'Chiêm tinh: nguyên tố cung Mặt Trăng (mod 4)': grp(lambda i: astro(i)['msign'], 4),
      'Chiêm tinh: độ Mặt Trăng trong cung (1..30)': one(lambda i: astro(i)['mdeg']),
      'Chiêm tinh: độ Mặt Trời trong cung (1..30)': one(lambda i: astro(i)['sdeg']),
      'Chiêm tinh: hành tinh chủ ngày (số rút gọn Cheiro)': lambda i: {n for n in range(1, mx+1) if _root(n) == CHEIRO[astro(i)['dayr']]},
      'Chiêm tinh: giờ hành tinh lúc quay (số rút gọn Cheiro)': lambda i: {n for n in range(1, mx+1) if _root(n) == CHEIRO[astro(i)['hourr']]},
      'Chiêm tinh: Thủy Tinh nghịch hành → số rút gọn 5': lambda i: {n for n in range(1, mx+1) if _root(n) == 5} if astro(i)['retro']['Thủy'] else set(),
      'Chiêm tinh: số hành tinh đang nghịch hành (1..5)': one(lambda i: astro(i)['nretro']),
      'Chiêm tinh: tổng cung 7 thiên thể mod max': one(lambda i: (astro(i)['msign'] + astro(i)['ssign'] + sum(astro(i)['psign'].values()) - 1) % mx + 1),
    }
    for p in ('Thủy', 'Kim', 'Hỏa', 'Mộc', 'Thổ'):
        R[f'Chiêm tinh: cung {p} Tinh (1..12)'] = one(lambda i, p=p: astro(i)['psign'][p])
    return R

if __name__ == '__main__':
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from study import date_info
    for y, m, d, h in [(2026, 9, 30, 21), (2026, 9, 25, 18), (2024, 4, 8, 18), (2000, 1, 6, 12)]:
        i = date_info(y, m, d, h); A = astro(i)
        print(f'{d:02d}/{m:02d}/{y} {h}h: Mặt Trời {A["sun"]:.2f}° (cung {A["ssign"]}), Mặt Trăng {A["moon"]:.2f}° (cung {A["msign"]}), pha {A["phase"]}, tuổi trăng {A["age"]}, nakshatra {A["nak"]}, '
              f'cung hành tinh {A["psign"]}, nghịch hành {[p for p, v in A["retro"].items() if v]}, chủ ngày {A["dayr"]}, giờ {A["hourr"]}, mọc/lặn {tuple(round(x, 2) for x in sun_times(i))}')
