# Thu hẹp trong ±3 quanh số May Mắn kỳ trước, nhận định riêng từng buổi (anh 21/10/2026)
# Đếm độ lệch MM kỳ này − MM kỳ trước (liền 2 buổi) theo buổi của kỳ này; tách thêm theo chiều (đi ngược / cùng chiều bước trước cùng buổi)
import json
d = json.load(open('build/all_data.json'))['loto535']; LK = d['lk']; D = d['dates']; N = len(LK)
SP = {t: [u for u in range(t - 1, -1, -1) if D[u].endswith(D[t][-3:])][:2] for t in range(N)}
for g in ('13h', '21h'):
    idx = [t for t in range(N) if D[t].endswith(g)]
    for W in (50, 100, 150):
        T = idx[-W:]; c = {k: 0 for k in range(-3, 4)}; out = 0
        for t in T:
            x = LK[t] - LK[t - 1]
            if -3 <= x <= 3: c[x] += 1
            else: out += 1
        print(f'{g} {W} kỳ: ' + ' · '.join(f'{k:+d}: {c[k]}' for k in range(-3, 4)) + f' · ngoài ±3: {out}')
    # theo chiều gợi ý của buổi (13h: đảo chiều bước trước cùng buổi; 21h: chiều nghiêng)
    for W in (50, 100, 150):
        T = idx[-W:]; theo = nguoc = 0; c = {k: 0 for k in range(1, 4)}; n0 = 0
        for t in T:
            s1, s2 = SP[t]; m1, m2 = LK[s1], LK[s2]; p = LK[t - 1]
            if g == '13h': up = m1 < m2 if m1 != m2 else None
            else: up = m1 <= 6
            if up is None: continue
            n0 += 1; x = LK[t] - p
            if x == 0: continue
            if (x > 0) == up:
                theo += 1
                if abs(x) <= 3: c[abs(x)] += 1
            else: nguoc += 1
        print(f'   {g} {W} kỳ chiều gợi ý: đúng chiều {theo}/{n0} (trong đó cách 1: {c[1]} · cách 2: {c[2]} · cách 3: {c[3]}) · ngược chiều {nguoc}')
