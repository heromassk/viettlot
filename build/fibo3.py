# Số kỳ nghỉ giữa 2 lần ra của cùng 1 số: mức nghỉ là số Fib (1 2 3 5 8 13 21) có gặp nhiều hơn mức nghỉ liền bên không (anh 21/10/2026)
# Chỉ so trong dữ liệu thật (anh: không so với ngẫu nhiên).
import json
d = json.load(open('build/all_data.json')); FIB = {1, 2, 3, 5, 8, 13, 21}
for key, nm, NB, WS in (('loto535', 'Loto', 35, (100, 200)), ('mega645', 'Mega', 45, (50, 100)), ('power655', 'Power', 55, (50, 100))):
    for W in WS:
        R = [set(x) for x in d[key]['res']][-W:]; rest = []
        for x in range(1, NB + 1):
            idx = [i for i, r in enumerate(R) if x in r]; rest += [b - a for a, b in zip(idx, idx[1:])]
        c = {g: sum(1 for x in rest if x == g) for g in range(1, 23)}
        print(f'{nm} {W} kỳ:', ' '.join(f'{g}{"*" if g in FIB else ""}:{c[g]}' for g in range(1, 23)))
