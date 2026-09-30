"""Kiểm chứng độc lập: tín hiệu "hy vọng nhỏ" tìm trên 2025–2026 có còn đúng trên dữ liệu 2020–2024 (chưa từng dùng để tìm) không?"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(__file__))
from study import load, zscore
from report import all_rules
from community import methods
from recency import pick
from collections import Counter
from itertools import permutations
def zp(z): return math.erfc(abs(z)/math.sqrt(2))
S = sys.argv[1]
old_rules = json.load(open(f'{S}/old_results.json'))['games']
old_comm = json.load(open(f'{S}/old_community.json')); old_rec = json.load(open(f'{S}/old_recency.json'))
for game in ['power655', 'mega645']:
    mx, c, _, dr = load(game)
    idx = [i for i, d in enumerate(dr) if d['info']['y'] <= 2024]           # 2020–2024
    D = [set(d['nums']) for d in dr]
    print(f'\n######## {game}: kiểm chứng trên {len(idx)} kỳ 2020–2024')
    tot_ok = tot = 0
    def show(name, H, E, V, lift0):
        global tot_ok, tot
        z = (H-E)/math.sqrt(V) if V else 0; same = (H/E-1)*(lift0-1) > 0
        tot += 1; tot_ok += same
        print(f"  {'✅' if same and abs(z)>=1.5 else ('✓' if same else '✗')} {name:46s} 2025–26: {(lift0-1)*100:+4.0f}% → 2020–24: {(H/E-1)*100:+4.0f}% (z {z:+.2f}, p={zp(z):.3f})")
    R = all_rules(mx)
    for r in [r for r in old_rules[game]['rules'] if r['consistent'] and abs(r['z']) >= 1.5]:
        sets = [R[r['rule']](dr[i]['info']) for i in idx]; z, H, E = zscore(sets, [dr[i] for i in idx], c, mx)
        V = ((H-E)/z)**2 if z else 1; show(r['rule'], H, E, V, r['lift'])
    M = methods(mx, c); st = {'follow': Counter(), 'cnt': Counter(), 'pos': list(permutations(range(2*c), 2))}
    hope_c = [r for r in old_comm[game] if r['consistent'] and abs(r['z']) >= 1.5]
    acc = {r['rule']: [0, 0.0, 0.0] for r in hope_c}
    for i in range(1, len(D)):
        if i in idx and i >= 30:
            for r in hope_c:
                S_ = M[r['rule']](D[:i], st); K = len(S_); q = K/mx
                acc[r['rule']][0] += len(S_ & D[i]); acc[r['rule']][1] += c*q; acc[r['rule']][2] += c*q*(1-q)*(mx-c)/(mx-1)
        for x in D[i-1]:
            st['cnt'][x] += 1
            for y in D[i]: st['follow'][(x, y)] += 1
    for r in hope_c: show('Cộng đồng: ' + r['rule'], *acc[r['rule']], r['lift'])
    for r in [r for r in old_rec[game] if r['consistent'] and abs(r['z']) >= 1.5]:
        H = E = 0.0; pr = (1/math.comb(mx, 2)*math.comb(c, 2)) if r['mode'] == 'pair' else c/mx
        for i in idx:
            if i < 50: continue
            past = D[max(0, i-r['window']):i] if r['window'] else D[:i]
            best = pick(past, mx, r['mode'], r['k'])
            H += sum(a in D[i] and b in D[i] for a, b in best) if r['mode'] == 'pair' else len(set(best) & D[i]); E += len(best)*pr
        show('Gần đây: ' + r['rule'], H, E, E*(1-pr), r['lift'])
    print(f'  → {tot_ok}/{tot} tín hiệu giữ cùng chiều trên dữ liệu 2020–2024 (nếu chỉ là ngẫu nhiên: ~{tot/2:.0f}/{tot})')
