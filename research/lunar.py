# Chuyển dương lịch -> âm lịch Việt Nam (thuật toán Hồ Ngọc Đức, múi giờ +7)
from math import sin, pi, floor
def jd_from_date(dd, mm, yy):
    a = (14 - mm) // 12; y = yy + 4800 - a; m = mm + 12*a - 3
    return dd + (153*m + 2)//5 + 365*y + y//4 - y//100 + y//400 - 32045
def new_moon_day(k, tz=7):
    T = k/1236.85; T2 = T*T; T3 = T2*T; dr = pi/180
    Jd1 = 2415020.75933 + 29.53058868*k + 0.0001178*T2 - 0.000000155*T3
    Jd1 += 0.00033*sin((166.56 + 132.87*T - 0.009173*T2)*dr)
    M = 359.2242 + 29.10535608*k - 0.0000333*T2 - 0.00000347*T3
    Mpr = 306.0253 + 385.81691806*k + 0.0107306*T2 + 0.00001236*T3
    F = 21.2964 + 390.67050646*k - 0.0016528*T2 - 0.00000239*T3
    C1 = (0.1734 - 0.000393*T)*sin(M*dr) + 0.0021*sin(2*dr*M)
    C1 -= 0.4068*sin(Mpr*dr) + 0.0161*sin(dr*2*Mpr)
    C1 -= 0.0004*sin(dr*3*Mpr)
    C1 += 0.0104*sin(dr*2*F) - 0.0051*sin(dr*(M+Mpr))
    C1 -= 0.0074*sin(dr*(M-Mpr)) + 0.0004*sin(dr*(2*F+M))
    C1 -= 0.0004*sin(dr*(2*F-M)) - 0.0006*sin(dr*(2*F+Mpr))
    C1 += 0.0010*sin(dr*(2*F-Mpr)) + 0.0005*sin(dr*(2*Mpr+M))
    if T < -11: dt = 0.001 + 0.000839*T + 0.0002261*T2 - 0.00000845*T3 - 0.000000081*T*T3
    else: dt = -0.000278 + 0.000265*T + 0.000262*T2
    return floor(Jd1 + C1 - dt + 0.5 + tz/24)
def sun_longitude(jdn, tz=7):
    T = (jdn - 2451545.5 - tz/24)/36525; T2 = T*T; dr = pi/180
    M = 357.52910 + 35999.05030*T - 0.0001559*T2 - 0.00000048*T*T2
    L0 = 280.46645 + 36000.76983*T + 0.0003032*T2
    DL = (1.914600 - 0.004817*T - 0.000014*T2)*sin(dr*M)
    DL += (0.019993 - 0.000101*T)*sin(dr*2*M) + 0.000290*sin(dr*3*M)
    L = (L0 + DL)*dr; L -= pi*2*floor(L/(pi*2))
    return floor(L/pi*6)
def lunar_month11(yy, tz=7):
    k = floor((jd_from_date(31, 12, yy) - 2415021)/29.530588853)
    nm = new_moon_day(k, tz)
    return new_moon_day(k-1, tz) if sun_longitude(nm, tz) >= 9 else nm
def leap_month_offset(a11, tz=7):
    k = floor((a11 - 2415021.076998695)/29.530588853 + 0.5)
    i = 1; arc = sun_longitude(new_moon_day(k+i, tz), tz)
    while True:
        last = arc; i += 1; arc = sun_longitude(new_moon_day(k+i, tz), tz)
        if not (arc != last and i < 14): break
    return i - 1
def solar_to_lunar(dd, mm, yy, tz=7):
    dn = jd_from_date(dd, mm, yy)
    k = floor((dn - 2415021.076998695)/29.530588853)
    ms = new_moon_day(k+1, tz)
    if ms > dn: ms = new_moon_day(k, tz)
    a11 = lunar_month11(yy, tz); b11 = a11
    if a11 >= ms: ly = yy; a11 = lunar_month11(yy-1, tz)
    else: ly = yy+1; b11 = lunar_month11(yy+1, tz)
    ld = dn - ms + 1; diff = floor((ms - a11)/29); leap = 0; lm = diff + 11
    if b11 - a11 > 365:
        lo = leap_month_offset(a11, tz)
        if diff >= lo:
            lm = diff + 10
            if diff == lo: leap = 1
    if lm > 12: lm -= 12
    if lm >= 11 and diff < 4: ly -= 1
    return ld, lm, ly, leap
