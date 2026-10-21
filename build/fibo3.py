# So với bốc ngẫu nhiên (anh 21/10/2026 hỏi thẳng): (1) tỉ lệ khoảng cách Fib trong kỳ; (2) số kỳ nghỉ của 1 số có hay đúng số Fib không
import json, random
d = json.load(open('build/all_data.json')); FIB = {1, 2, 3, 5, 8, 13, 21, 34, 55}; random.seed(1)
for key, nm, NB, KB, W in (('loto535', 'Loto', 35, 5, 200), ('mega645', 'Mega', 45, 6, 100), ('power655', 'Power', 55, 6, 100)):
    RS = [sorted(x) for x in d[key]['res']][-W:]
    gaps = [b - a for t in RS for a, b in zip(t, t[1:])]; real = sum(g in FIB for g in gaps) / len(gaps)
    sim = []
    for _ in range(20000):
        t = sorted(random.sample(range(1, NB + 1), KB)); sim += [b - a for a, b in zip(t, t[1:])]
    rnd = sum(g in FIB for g in sim) / len(sim)
    # số kỳ nghỉ giữa 2 lần ra của cùng 1 số (dùng toàn bộ dữ liệu W kỳ)
    R = [set(x) for x in d[key]['res']][-W:]; rest = []
    for x in range(1, NB + 1):
        idx = [i for i, r in enumerate(R) if x in r]
        rest += [b - a for a, b in zip(idx, idx[1:])]
    p = KB / NB; N = len(rest)
    exp = lambda g: N * (1 - p) ** (g - 1) * p   # nếu ngẫu nhiên: phân bố hình học
    fib_real = sum(1 for g in rest if g in FIB); fib_exp = sum(exp(g) for g in FIB if g < 200)
    print(f'{nm} ({W} kỳ): khoảng cách trong kỳ là Fib — thực {real*100:.1f}% · ngẫu nhiên {rnd*100:.1f}%')
    print(f'   số kỳ nghỉ giữa 2 lần ra ({N} lần): đúng số Fib thực {fib_real} · ngẫu nhiên kỳ vọng {fib_exp:.0f}')
    print('   từng độ dài nghỉ (thực / ngẫu nhiên):', ' '.join(f'{g}{"*" if g in FIB else ""}:{sum(1 for x in rest if x == g)}/{exp(g):.0f}' for g in range(1, 22)))
