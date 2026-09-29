"""Xuất tập số của mọi quy luật cho nhiều ngày mẫu — dùng để kiểm tra bản JavaScript trong app khớp với Python."""
import sys, os, json, random, datetime
sys.path.insert(0, os.path.dirname(__file__))
from study import date_info
from report import all_rules
rng = random.Random(5); days = []
d0 = datetime.date(2024, 1, 1)
for k in range(150): days.append(d0 + datetime.timedelta(rng.randrange(0, 365*5)))
for y in (2025, 2026, 2027):   # quanh Tết, Đông chí, Hạ chí, Lập xuân
    for md in ((1, 28), (1, 29), (2, 3), (2, 4), (2, 5), (2, 16), (2, 17), (2, 18), (6, 20), (6, 21), (6, 22), (12, 20), (12, 21), (12, 22), (12, 31), (1, 1)):
        days.append(datetime.date(y, *md))
out = {}
for mx in (55, 45, 35, 12):
    R = all_rules(mx)
    for dd in days:
        for h in (13, 18, 21):
            i = date_info(dd.year, dd.month, dd.day, h)
            out[f'{mx}|{dd.isoformat()}|{h}'] = {k: sorted(f(i)) for k, f in R.items()}
json.dump(out, open(sys.argv[1], 'w'), ensure_ascii=False)
print(len(out), 'mẫu x', len(R), 'quy luật')
