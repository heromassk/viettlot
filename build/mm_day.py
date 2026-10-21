# Độ lớn bước nhảy số May Mắn (bỏ dấu) có nối tiếp thành dãy tự nhiên không (anh 21/10/2026):
# 2 bước trước |a|, |b| → bước kế đoán |c| = |b| + (|b| − |a|)  (4,3→2 · 3,4→5 · 3,3→3)
import json
d = json.load(open('build/all_data.json'))['loto535']; LK = d['lk']; D = d['dates']
def seq(g): return [LK[i] for i in range(len(LK)) if g is None or D[i].endswith(g)]
for g, nm in ((None, 'Liền 2 buổi'), (' 13h', 'Chỉ 13h'), (' 21h', 'Chỉ 21h')):
    s = seq(g)
    for W in (20, 50, 100):
        dung = gan = tot = v1 = v2 = n2 = 0
        for t in range(len(s) - W, len(s)):
            a, b, c = s[t - 2] - s[t - 3], s[t - 1] - s[t - 2], s[t] - s[t - 1]
            m = abs(b) + (abs(b) - abs(a))
            if m < 0: continue
            tot += 1; dung += abs(c) == m; gan += abs(abs(c) - m) <= 1
            # đoán số May Mắn: lùi/tiến m bước từ số kỳ trước, đổi chiều so với bước trước (zic-zắc); và cả 2 chiều
            sg = -1 if b > 0 else 1
            p1 = s[t - 1] + sg * m
            v1 += s[t] == p1
            cand = {x for x in (s[t - 1] + m, s[t - 1] - m) if 1 <= x <= 12}
            n2 += len(cand); v2 += s[t] in cand
        print(f'{nm} {W}: kỳ xét {tot} · độ lớn đúng {dung} · lệch ≤1 {gan} · đoán 1 số (đổi chiều) trúng {v1} · đoán 2 chiều trúng {v2} (TB {n2/tot:.1f} số)')
