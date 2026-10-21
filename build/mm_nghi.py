# Xu hướng nghỉ của số May Mắn Loto (anh 21/10/2026): ra liên tục hay nghỉ x kỳ rồi mới ra
import json
d = json.load(open('build/all_data.json'))['loto535']; LK = d['lk']; D = d['dates']; N = len(LK)
B = [(1, 1), (2, 2), (3, 5), (6, 10), (11, 15), (16, 25), (26, 999)]
lab = lambda a, b: f'{a}' if a == b else (f'{a}–{b}' if b < 999 else f'≥{a}')
for g, nm in ((None, 'Liền 2 buổi'), (' 13h', 'Chỉ 13h'), (' 21h', 'Chỉ 21h')):
    s = [LK[i] for i in range(N) if g is None or D[i].endswith(g)]; L = len(s)
    for W in (100, 200):
        # 1) khoảng nghỉ của lần ra trong W kỳ gần: số kỳ từ lần ra trước của chính số đó
        gaps = []
        for t in range(L - W, L):
            u = t - 1
            while u >= 0 and s[u] != s[t]: u -= 1
            if u >= 0: gaps.append(t - u)
        dist = [sum(a <= x <= b for x in gaps) for a, b in B]
        # 2) khi một số đang nghỉ x kỳ: kỳ sau ra bao nhiêu lần / bao nhiêu lần ở mức đó
        hz = []
        for a, b in B:
            n_ = h_ = 0
            for t in range(L - W, L):
                for k in range(1, 13):
                    u = t - 1
                    while u >= 0 and s[u] != k: u -= 1
                    x = t - u
                    if a <= x <= b: n_ += 1; h_ += s[t] == k
            hz.append(f'{h_}/{n_}')
        print(f'{nm} {W} kỳ | nghỉ trước khi ra: ' + ' · '.join(f'{lab(a,b)}: {c}' for (a, b), c in zip(B, dist)))
        print(f'{" " * len(nm)}        | đang nghỉ x kỳ → ra ngay kỳ sau: ' + ' · '.join(f'{lab(a,b)}: {h}' for (a, b), h in zip(B, hz)))
