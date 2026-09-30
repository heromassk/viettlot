"""Báo cáo: các số liên hệ với ngày quay so với kết quả thật của từng loại vé.
python3 research/report.py [power655|mega645|loto535|all] [số hoán vị] [--json out.json]"""
import math, random, sys, os, json, datetime
sys.path.insert(0, os.path.dirname(__file__))
from study import load, zscore, rules as r1
from kinhdich import rules as r2
from more_rules import rules as r3
from web_rules import rules as r4
from astro import rules as r5
LABEL = {'power655': 'Power 6/55', 'mega645': 'Mega 6/45', 'loto535': 'Loto 5/35', 'loto535_lucky': 'Loto – số may mắn'}
def p(z): return math.erfc(abs(z)/math.sqrt(2))

def all_rules(mx):
    R = {**r1(mx), **r2(mx), **r3(mx), **r4(mx), **r5(mx)}
    return {k: v for k, v in R.items() if not k.startswith('ĐỐI CHỨNG')}

def analyse(game, perms=500, seed=7):
    if game.endswith('_lucky'):   # số may mắn của Loto: bốc 1 số trong 1..12
        _, _, mx, draws = load(game[:-6]); c = 1
        draws = [dict(d, nums={d['lucky']}) for d in draws if d['lucky']]
    else:
        mx, c, _, draws = load(game)
    n = len(draws); cut = int(n*0.6)
    R = all_rules(mx)
    sets = {k: [f(d['info']) for d in draws] for k, f in R.items()}
    rows = []
    for k, S in sets.items():
        if not sum(map(len, S)): continue
        zA, H, E = zscore(S, draws, c, mx)
        zT = zscore(S[:cut], draws[:cut], c, mx)[0]; zV = zscore(S[cut:], draws[cut:], c, mx)[0]
        rows.append(dict(rule=k, size=round(sum(map(len, S))/n, 1), hits=int(H), expected=round(E, 1),
                         lift=round(H/E, 3), z=round(zA, 2), p=round(p(zA), 4), z_old=round(zT, 2), z_new=round(zV, 2),
                         consistent=zT*zV > 0))
    rng = random.Random(seed); nums = [d['nums'] for d in draws]; mz = []
    for _ in range(perms):
        perm = nums[:]; rng.shuffle(perm); fake = [dict(nums=x) for x in perm]
        mz.append(max(abs(zscore(sets[r['rule']], fake, c, mx)[0]) for r in rows))
    mz.sort(); thr = mz[int(0.95*len(mz))]
    single = [k for k in sets if max(len(s) for s in sets[k]) <= 2]
    U = [set().union(*(sets[k][i] for k in single)) for i in range(n)]
    zU, HU, EU = zscore(U, draws, c, mx)
    fmt = lambda I: f"{I['d']:02d}/{I['m']:02d}/{I['y']}"
    recent = []
    for i in range(n-5, n):
        d = draws[i]
        recent.append(dict(date=fmt(d['info']), hour=d['info']['h'], nums=sorted(d['nums']),
                           links={x: [k for k in single if x in sets[k][i]] for x in sorted(d['nums'])}))
    zs = [r['z'] for r in rows]
    return dict(game=game, label=LABEL[game], draws=n, first=fmt(draws[0]['info']), last=fmt(draws[-1]['info']),
                threshold=round(thr, 2), sig=sum(abs(z) > 1.96 for z in zs), sig_expected=round(0.05*len(zs), 1),
                up=sum(z > 0 for z in zs), down=sum(z < 0 for z in zs),
                union=dict(rules=len(single), size=round(sum(map(len, U))/n, 1), hits=round(HU/n, 2), expected=round(EU/n, 2), z=round(zU, 2)),
                rules=sorted(rows, key=lambda r: -r['z']), recent=recent)

def show(a):
    print(f"\n######## {a['label']}: {a['draws']} kỳ ({a['first']} → {a['last']}), {len(a['rules'])} quy luật. Ngưỡng may mắn (95%): |z| = {a['threshold']}")
    line = lambda r: (f"  {r['rule']:44s} ~{r['size']:4.1f} số/kỳ | trúng {r['hits']:4d} / kỳ vọng {r['expected']:6.1f} ({(r['lift']-1)*100:+4.0f}%) "
                      f"| z {r['z']:5.2f} p={r['p']:.3f} | 2 giai đoạn {'cùng chiều' if r['consistent'] else 'ĐẢO'}")
    print('TRÚNG NHIỀU HƠN NGẪU NHIÊN (top 10)'); [print(line(r)) for r in a['rules'][:10]]
    print('TRÚNG ÍT HƠN NGẪU NHIÊN (top 10)'); [print(line(r)) for r in a['rules'][::-1][:10]]
    print(f"Phân bố: {a['sig']} / {len(a['rules'])} quy luật có |z|>1.96 (ngẫu nhiên kỳ vọng ~{a['sig_expected']:.0f}); {a['up']} lệch lên, {a['down']} lệch xuống")
    u = a['union']
    print(f"Gộp {u['rules']} cách ra số đơn: phủ ~{u['size']} số/kỳ; trúng TB {u['hits']} số/kỳ, ngẫu nhiên {u['expected']} → z {u['z']}")
    print('5 kỳ gần nhất: số trúng liên hệ với ngày')
    for k in a['recent']:
        print(f"  {k['date']} {k['hour']}h {' '.join(f'{x:02d}' for x in k['nums'])}: " +
              '; '.join(f"{x}←{', '.join(v[:3])}{'…' if len(v) > 3 else ''}" for x, v in k['links'].items() if v))

if __name__ == '__main__':
    args = [x for x in sys.argv[1:] if not x.startswith('--')]
    games = ['power655', 'mega645', 'loto535', 'loto535_lucky'] if not args or args[0] == 'all' else [args[0]]
    perms = int(args[1]) if len(args) > 1 else 500
    res = [analyse(g, perms) for g in games]
    for a in res: show(a)
    if '--json' in sys.argv:
        out = sys.argv[sys.argv.index('--json')+1]
        json.dump(dict(generated=datetime.date.today().isoformat(), games={a['game']: a for a in res}), open(out, 'w'), ensure_ascii=False)
        print('\nĐã ghi', out)
