# Loto: chữ số hàng đơn vị (đuôi) của 5 số trong 1 kỳ có tạo dãy liên tiếp không? (anh 08/11/2026). Đếm số kỳ ở 20/50/100/200.
import json
d = json.load(open('build/all_data.json'))['loto535']; R = d['res']; D = d['dates']
def run_len(tails, wrap):
    s = set(tails); best = 0
    for a in range(10):
        n = 0
        while (a + n < 10 or wrap) and ((a + n) % 10) in s: n += 1; best = max(best, n)
            
        if n >= 10: break
    return best
def inorder(r):  # đuôi theo thứ tự số tăng dần: có ≥3 số liền nhau mà đuôi tăng +1 / giảm −1 không
    t = [x % 10 for x in sorted(r)]; best = 1; up = dn = 1
    for i in range(1, len(t)):
        up = up + 1 if t[i] == t[i-1] + 1 else 1; dn = dn + 1 if t[i] == t[i-1] - 1 else 1; best = max(best, up, dn)
    return best
def stat(idx, label):
    print(f'\n== {label} ({len(idx)} kỳ)')
    for W in (20, 50, 100, 200):
        L = idx[-W:]; row = []
        for k in (2, 3, 4):
            a = sum(run_len([x % 10 for x in R[i]], False) >= k for i in L)
            b = sum(run_len([x % 10 for x in R[i]], True) >= k for i in L)
            row.append(f'đuôi liên tiếp ≥{k}: {a}/{W} (vòng 9→0: {b})')
        o = sum(inorder(R[i]) >= 3 for i in L)
        print(f'  {W:3d} kỳ: ' + ' · '.join(row) + f' · đuôi tăng/giảm đều theo thứ tự số ≥3: {o}')
n = len(R)
stat(list(range(n)), 'Loto liền 2 buổi')
stat([i for i in range(n) if D[i].endswith('13h')], 'Loto 13h')
stat([i for i in range(n) if D[i].endswith('21h')], 'Loto 21h')
# 3 đoạn 100 kỳ gần: ổn định?
print('\nỔn định (đuôi liên tiếp ≥3, không vòng) theo 3 đoạn 100 kỳ liền nhau:', [sum(run_len([x % 10 for x in R[i]], False) >= 3 for i in range(n - 100 * (j + 1), n - 100 * j)) for j in (2, 1, 0)])
# kỳ sau khi có đuôi liên tiếp ≥3: kỳ sau có không?
a = b = c = e = 0
for i in range(n - 201, n - 1):
    x = run_len([v % 10 for v in R[i]], False) >= 3; y = run_len([v % 10 for v in R[i+1]], False) >= 3
    if x: a += 1; b += y
    else: c += 1; e += y
print(f'200 kỳ: kỳ có đuôi liên tiếp ≥3 → kỳ sau cũng có: {b}/{a} · kỳ không có → kỳ sau có: {e}/{c}')
# số lần xuất hiện của từng dãy đuôi 3 liên tiếp (a,a+1,a+2) ở 200 kỳ
cnt = {}
for i in range(n - 200, n):
    t = {x % 10 for x in R[i]}
    for a in range(8):
        if {a, a+1, a+2} <= t: cnt[a] = cnt.get(a, 0) + 1
print('200 kỳ, dãy đuôi 3 liên tiếp bắt đầu từ chữ số:', dict(sorted(cnt.items())))
print('5 kỳ gần nhất:', [(D[i], sorted(R[i]), sorted({x % 10 for x in R[i]})) for i in range(n - 5, n)])
