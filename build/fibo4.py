# Kiểm thêm (anh 21/10/2026): dãy Lucas, Fibonacci tổng quát từ kỳ trước, chuỗi kiểu Fibonacci trên 2 / 3 kỳ gần nhất, chu kỳ Pisano (đuôi tổng)
# Mỗi nhóm: bao nhiêu số/kỳ, 1 số trong nhóm ra bao nhiêu % kỳ, so với các số còn lại cùng kỳ. Đếm 20 / 50 / 100 kỳ.
import json
d = json.load(open('build/all_data.json')); LUC = {1, 2, 3, 4, 7, 11, 18, 29, 47}
def groups(R, t, NB):
    P = R[t - 1]; s = sorted(P); G = {}
    G['Dãy Lucas (1 2 3 4 7 11 18 29 47)'] = {x for x in LUC if x <= NB}
    gen = set()
    for i, a in enumerate(s):
        for b in s[i + 1:]:
            for v in (a + b, a + 2 * b, 2 * a + 3 * b): 
                if v <= NB: gen.add(v)
    G['Fib tổng quát từ kỳ trước (a+b, a+2b, 2a+3b)'] = gen - P
    for k in (2, 3):
        U = set().union(*R[t - k:t]); su = sorted(U); nx = set()
        for i, a in enumerate(su):
            for b in su[i + 1:]:
                if a + b in U and a + 2 * b <= NB: nx.add(a + 2 * b)   # chuỗi a, b, a+b đã có trong k kỳ → số kế tiếp a+2b
        G[f'Số kế tiếp chuỗi kiểu Fib trên {k} kỳ gần (a,b,a+b → a+2b)'] = nx - U
    return G
for key, nm, NB in (('loto535', 'Loto', 35), ('mega645', 'Mega', 45), ('power655', 'Power', 55)):
    R = [set(x) for x in d[key]['res']]; n = len(R); print(f'\n=== {nm}')
    labs = list(groups(R, n - 1, NB).keys())
    for lab in labs:
        row = []
        for W in (20, 50, 100):
            a = [0, 0]; b = [0, 0]
            for t in range(n - W, n):
                Gs = groups(R, t, NB)[lab]
                for x in range(1, NB + 1):
                    z = a if x in Gs else b; z[0] += 1; z[1] += x in R[t]
            row.append(f'{a[0]/W:.1f} số · {a[1]/max(1,a[0])*100:.1f}% vs {b[1]/b[0]*100:.1f}%')
        print(f'  {lab}:\n     ' + ' | '.join(f'{W} kỳ: {r}' for W, r in zip((20, 50, 100), row)))
    sm = [sum(r) for r in d[key]['res']]
    print('  Đuôi tổng kỳ = đuôi (tổng 2 kỳ trước cộng lại) [kiểu Pisano]:', ' / '.join(f'{sum(sm[t] % 10 == (sm[t-1] + sm[t-2]) % 10 for t in range(n - W, n))}/{W}' for W in (20, 50, 100)),
          '· đuôi tổng kỳ = đuôi tổng kỳ trước:', ' / '.join(f'{sum(sm[t] % 10 == sm[t-1] % 10 for t in range(n - W, n))}/{W}' for W in (20, 50, 100)))
