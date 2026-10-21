# 3 kỳ liên tiếp của số May Mắn: có số nào = tổng hoặc hiệu (bỏ dấu) của 2 số kia không (anh 21/10/2026)
import json
d = json.load(open('build/all_data.json'))['loto535']; LK = d['lk']; D = d['dates']
def seq(g): return [LK[i] for i in range(len(LK)) if g is None or D[i].endswith(g)]
def rel(a, b, c):   # bất kỳ số nào = tổng / hiệu 2 số còn lại
    for x, y, z in ((a, b, c), (a, c, b), (b, c, a)):
        if z == x + y or (z == abs(x - y) and z > 0): return True
    return False
for g, nm in ((None, 'Liền 2 buổi'), (' 13h', 'Chỉ 13h'), (' 21h', 'Chỉ 21h')):
    s = seq(g)
    for W in (20, 50, 100):
        bo = sum(rel(s[t - 2], s[t - 1], s[t]) for t in range(len(s) - W, len(s)))
        # đoán kỳ tới: số kỳ này = tổng hoặc hiệu 2 kỳ trước
        tg = hi = th = nc = 0
        for t in range(len(s) - W, len(s)):
            a, b = s[t - 2], s[t - 1]; T = a + b; H = abs(a - b)
            cand = {x for x in (T, H) if 1 <= x <= 12}; nc += len(cand)
            tg += s[t] == T; hi += s[t] == H and H > 0; th += s[t] in cand
        print(f'{nm} {W}: bộ 3 có quan hệ {bo}/{W} · kỳ sau = tổng 2 kỳ trước {tg} · = hiệu {hi} · tổng hoặc hiệu {th} (TB {nc/W:.1f} số/kỳ)')
