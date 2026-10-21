# Nhịp bước nhảy số May Mắn Loto (anh 21/10/2026): +3 → −3 (quay lại), −4 +3 −1 (ngắn dần), +3 −4 +2 (zic-zắc)
import json
d = json.load(open('build/all_data.json'))['loto535']; LK = d['lk']; D = d['dates']
def seq(g): return [LK[i] for i in range(len(LK)) if g is None or D[i].endswith(g)]
for g, nm in ((None, 'Liền 2 buổi'), (' 13h', 'Chỉ 13h'), (' 21h', 'Chỉ 21h')):
    s = seq(g)
    for W in (20, 50, 100):
        z = s[-(W + 3):]; dd = [z[i] - z[i - 1] for i in range(1, len(z))]
        # chỉ xét các kỳ trong khung (W kỳ cuối), cần 2 bước trước
        quay = gan = ngan = dai = bang = zz = tot = 0
        for i in range(len(dd) - W, len(dd)):
            a, b = dd[i - 1], dd[i]
            if a == 0: continue
            tot += 1
            quay += (b == -a)                       # quay lại đúng số 2 kỳ trước
            gan += (abs(b + a) <= 1)                # quay lại gần (±1) số 2 kỳ trước
            ngan += (abs(b) < abs(a))               # bước ngắn lại
            dai += (abs(b) > abs(a)); bang += (abs(b) == abs(a))
            zz += (b * a < 0)                       # đổi chiều (zic-zắc)
        # chuỗi 3 bước: đổi chiều 2 lần liền và ngắn dần
        z3 = n3 = 0
        for i in range(len(dd) - W, len(dd)):
            a0, a, b = dd[i - 2], dd[i - 1], dd[i]
            if a0 * a < 0:   # đã zic-zắc 1 lần
                n3 += 1; z3 += (a * b < 0)
        print(f'{nm} {W}: kỳ xét {tot} · quay lại đúng số 2 kỳ trước {quay} · quay lại ±1 {gan} · bước ngắn lại {ngan} · dài ra {dai} · bằng {bang} · đổi chiều {zz} | đã zic-zắc → zic-zắc tiếp {z3}/{n3}')
