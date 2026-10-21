# Loto: số đang nghỉ đúng 5/8/13/21/34 kỳ ra ít hơn? Tách liền 2 buổi / chỉ 13h / chỉ 21h (anh 21/10/2026)
import json
d = json.load(open('build/all_data.json'))['loto535']; RA = [set(x) for x in d['res']]; D = d['dates']
FB = {5, 8, 13, 21, 34}
for g, nm in ((None, 'Liền 2 buổi'), ('13h', 'Chỉ 13h'), ('21h', 'Chỉ 21h')):
    R = [RA[i] for i in range(len(RA)) if g is None or D[i].endswith(g)]; n = len(R)
    for W in (20, 50, 100, 150):
        a = [0, 0]; b = [0, 0]
        for t in range(n - W, n):
            for x in range(1, 36):
                u = t - 1
                while u >= 0 and x not in R[u]: u -= 1
                z = a if (t - u) in FB else b; z[0] += 1; z[1] += x in R[t]
        print(f'{nm} {W} kỳ: nghỉ 5/8/13/21/34 → {a[0]/W:.1f} số/kỳ, ra {a[1]}/{a[0]} ({a[1]/a[0]*100:.1f}%) · số còn lại ra {b[1]}/{b[0]} ({b[1]/b[0]*100:.1f}%)')
