# Các số trong cùng 1 kỳ có quan hệ Fibonacci không, dùng loại trừ vé được không (anh 21/10/2026). Đếm 20/50/100 kỳ.
import json
d = json.load(open('build/all_data.json')); FIB = {1, 2, 3, 5, 8, 13, 21, 34, 55}
def rules(r):
    s = sorted(r); S = set(s); gaps = [b - a for a, b in zip(s, s[1:])]
    nf = len(S & FIB)
    tri = [(a, b) for i, a in enumerate(s) for b in s[i + 1:] if a + b in S]          # a + b = c trong kỳ
    chain = any(a + b in S and b + (a + b) in S for a, b in tri)                       # chuỗi kiểu Fibonacci a, b, a+b, a+2b
    return {
        'Có ≤2 số Fibonacci': nf <= 2,
        'Có ≥1 số Fibonacci': nf >= 1,
        'Không có bộ a+b=c': not tri,
        'Không có chuỗi 4 số kiểu Fibonacci (a, b, a+b, a+2b)': not chain,
        'Không phải mọi khoảng cách đều là số Fib': not all(g in FIB for g in gaps),
        'Có ≥1 khoảng cách là số Fib': any(g in FIB for g in gaps),
        'Có ≤3 khoảng cách là số Fib': sum(g in FIB for g in gaps) <= 3,
    }
for key, nm in (('loto535', 'Loto'), ('mega645', 'Mega'), ('power655', 'Power')):
    R = d[key]['res']; print(f'\n{nm}')
    labs = list(rules(R[-1]).keys())
    for lab in labs:
        print(f'  {lab:55s}', ' / '.join(f'{sum(rules(r)[lab] for r in R[-W:])}/{W}' for W in (20, 50, 100)))
