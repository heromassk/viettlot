# Kỳ sau có số = 2× hoặc ÷2 một số kỳ trước? (anh 22/10/2026). % ra mỗi số trong nhóm vs số còn lại; kỳ có ≥1 số; 20/50/100 kỳ.
import json
d = json.load(open('build/all_data.json'))
G = {'×2': lambda P, NB: {2 * a for a in P if 2 * a <= NB},
     '÷2': lambda P, NB: {a // 2 for a in P if a % 2 == 0},
     '×2 hoặc ÷2': lambda P, NB: {2 * a for a in P if 2 * a <= NB} | {a // 2 for a in P if a % 2 == 0}}
def run(key, nm, NB, gio=None):
    R = d[key]['res']; D = d[key]['dates']
    S = [set(R[i]) for i in range(len(R)) if gio is None or D[i].endswith(gio)]; n = len(S)
    print(f'\n=== {nm}')
    for lab, f in G.items():
        row = []
        for W in (20, 50, 100):
            a = [0, 0]; b = [0, 0]; k = 0
            for t in range(n - W, n):
                g = f(S[t - 1], NB) - S[t - 1]; k += bool(g & S[t])
                for x in range(1, NB + 1):
                    z = a if x in g else b; z[0] += 1; z[1] += x in S[t]
            row.append(f'{a[0]/W:.1f} số · {a[1]/a[0]*100:.1f}% vs {b[1]/b[0]*100:.1f}% · có ≥1: {k}/{W}')
        print(f'  {lab:11s}', ' | '.join(row))
run('loto535', 'Loto liền 2 buổi', 35)
run('loto535', 'Loto 13h (so kỳ 13h trước)', 35, '13h')
run('loto535', 'Loto 21h (so kỳ 21h trước)', 35, '21h')
run('mega645', 'Mega', 45)
run('power655', 'Power', 55)
