"""Nghiên cứu: các cách "lấy số từ ngày quay" có liên hệ với dãy số trúng không?
Mỗi quy luật R(ngày) -> tập số S trong 1..max. So số trúng thật rơi vào S với kỳ vọng ngẫu nhiên.
- z-score theo phân phối siêu bội (mỗi kỳ bốc c số từ max số).
- Tách thời gian: 60% kỳ cũ để TÌM, 40% kỳ mới để KIỂM CHỨNG.
- Hoán vị: xáo ngày <-> kết quả 2000 lần, lấy max|z| trên mọi quy luật => ngưỡng "may mắn thuần túy"."""
import csv, datetime, random, math, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from lunar import solar_to_lunar, jd_from_date
ROOT = os.path.join(os.path.dirname(__file__), '..')
CAN_EL = ['Mộc','Mộc','Hỏa','Hỏa','Thổ','Thổ','Kim','Kim','Thủy','Thủy']
CHI_EL = ['Thủy','Thổ','Mộc','Mộc','Thổ','Hỏa','Hỏa','Thổ','Kim','Kim','Thổ','Thủy']
NAP = ['Kim','Hỏa','Mộc','Thổ','Kim','Hỏa','Thủy','Thổ','Kim','Mộc','Thủy','Thổ','Hỏa','Mộc','Thủy','Kim','Hỏa','Mộc','Thổ','Kim','Hỏa','Thủy','Thổ','Kim','Mộc','Thủy','Thổ','Hỏa','Mộc','Thủy']
DIG = {0:'Thổ',1:'Thủy',2:'Hỏa',3:'Mộc',4:'Kim',5:'Thổ',6:'Thủy',7:'Hỏa',8:'Mộc',9:'Kim'}
SINH = {'Mộc':'Hỏa','Hỏa':'Thổ','Thổ':'Kim','Kim':'Thủy','Thủy':'Mộc'}
KHAC = {'Mộc':'Thổ','Thổ':'Thủy','Thủy':'Hỏa','Hỏa':'Kim','Kim':'Mộc'}
def root(n):
    while n > 9: n = sum(map(int, str(n)))
    return n
def el_set(E, rel, mx):
    ok = {'tyhoa': lambda e: e == E, 'duocsinh': lambda e: SINH[E] == e, 'sinhra': lambda e: SINH[e] == E,
          'khac': lambda e: KHAC[E] == e, 'bikhac': lambda e: KHAC[e] == E}[rel]
    return {n for n in range(1, mx+1) if ok(DIG[n % 10])}

def date_info(y, m, d, h):
    jd = jd_from_date(d, m, y); can = (jd+9) % 10; chi = (jd+1) % 12
    k = next(k for k in range(60) if k % 10 == can and k % 12 == chi)
    ld, lm, ly, _ = solar_to_lunar(d, m, y)
    return dict(y=y, m=m, d=d, h=h, ly=ly, jd=jd, can=can, chi=chi, nap=NAP[k//2], ld=ld, lm=lm,
                wd=datetime.date(y, m, d).isoweekday(),  # 1=T2..7=CN
                doy=datetime.date(y, m, d).timetuple().tm_yday,
                ds=root(sum(map(int, f'{y}{m:02d}{d:02d}'))),
                dsum=sum(map(int, f'{y}{m:02d}{d:02d}')),
                lds=root(ld+lm), hchi=((h+1) % 24)//2 % 12)

def rules(mx):
    """Mỗi quy luật: tên -> hàm(info) -> tập số."""
    def one(f): return lambda i: {v for v in [f(i)] if 1 <= v <= mx}
    def many(f): return lambda i: {v for v in f(i) if 1 <= v <= mx}
    R = {
      'ngày dương d': one(lambda i: i['d']),
      'tháng dương m': one(lambda i: i['m']),
      'năm 2 số (26)': one(lambda i: i['y'] % 100),
      'd+m': one(lambda i: i['d']+i['m']),
      '|d-m|': one(lambda i: abs(i['d']-i['m'])),
      'd đảo (12->21)': one(lambda i: int(f"{i['d']:02d}"[::-1])),
      'd*m mod max': one(lambda i: (i['d']*i['m']-1) % mx + 1),
      'tổng chữ số ngày (chưa rút)': one(lambda i: i['dsum']),
      'daySum rút gọn': one(lambda i: i['ds']),
      'ngày âm': one(lambda i: i['ld']),
      'tháng âm': one(lambda i: i['lm']),
      'ngày+tháng âm': one(lambda i: i['ld']+i['lm']),
      'thứ (2..8)': one(lambda i: i['wd']+1),
      'ngày trong năm mod max': one(lambda i: (i['doy']-1) % mx + 1),
      'JD mod max': one(lambda i: i['jd'] % mx + 1),
      'Can (1..10)': one(lambda i: i['can']+1),
      'Chi (1..12)': one(lambda i: i['chi']+1),
      'Chi giờ (1..12)': one(lambda i: i['hchi']+1),
      'giờ quay': one(lambda i: i['h']),
      'số tận cùng = d%10': many(lambda i: {n for n in range(1, mx+1) if n % 10 == i['d'] % 10}),
      'số tận cùng = m%10': many(lambda i: {n for n in range(1, mx+1) if n % 10 == i['m'] % 10}),
      'số tận cùng = ngày âm%10': many(lambda i: {n for n in range(1, mx+1) if n % 10 == i['ld'] % 10}),
      'rút gọn = daySum': many(lambda i: {n for n in range(1, mx+1) if root(n) == i['ds']}),
      'rút gọn = rút gọn(ngày+tháng âm)': many(lambda i: {n for n in range(1, mx+1) if root(n) == i['lds']}),
      'rút gọn = rút gọn(d)': many(lambda i: {n for n in range(1, mx+1) if root(n) == root(i['d'])}),
      'bội số của daySum': many(lambda i: {n for n in range(1, mx+1) if i['ds'] > 1 and n % i['ds'] == 0}),
      'chứa chữ số của d': many(lambda i: {n for n in range(1, mx+1) if set(str(n)) & set(str(i['d']))}),
      'hàng chục = hàng chục của d': many(lambda i: {n for n in range(1, mx+1) if n//10 == i['d']//10}),
      'd±1': many(lambda i: {i['d']-1, i['d']+1}),
      'bội của d': many(lambda i: {i['d']*k for k in range(1, mx+1)}),
    }
    for src, key in [('Nạp Âm ngày', 'nap'), ('Can ngày', None), ('Chi ngày', None), ('Chi giờ', None)]:
        for rel in ['tyhoa', 'duocsinh', 'sinhra', 'khac', 'bikhac']:
            def f(i, src=src, rel=rel):
                E = {'Nạp Âm ngày': i['nap'], 'Can ngày': CAN_EL[i['can']], 'Chi ngày': CHI_EL[i['chi']], 'Chi giờ': CHI_EL[i['hchi']]}[src]
                return el_set(E, rel, mx)
            R[f'{src}: {rel}'] = f
    return R

def load(game):
    cfg = {'power655': (55, 6, None), 'mega645': (45, 6, None), 'loto535': (35, 5, 12)}[game]
    mx, c, lmx = cfg
    rows = list(csv.reader(open(os.path.join(ROOT, f'{game}_history.csv'))))
    seen = {}; draws = []
    for r in rows:  # file mới nhất trước; Loto: cột cuối = giờ quay, nếu thiếu thì dòng đầu của 1 ngày = 21h
        dd, mm, yy = map(int, r[0].split('/'))
        if game == 'loto535':
            h = int(r[2+c]) if len(r) > 2+c and r[2+c] else (21 if r[0] not in seen else 13); seen[r[0]] = 1
        else: h = 18
        draws.append(dict(info=date_info(yy, mm, dd, h), nums=set(map(int, r[1:1+c])),
                          lucky=int(r[1+c]) if lmx and len(r) > 1+c else None))
    draws.reverse()
    for k, d in enumerate(draws):  # kỳ trước (dùng làm nhóm đối chứng "không phải từ ngày")
        d['info']['prev'] = draws[k-1]['nums'] if k else set()
    return mx, c, lmx, draws

def zscore(sets, draws, c, mx, key='nums'):
    H = E = V = 0.0
    for S, dr in zip(sets, draws):
        K = len(S); p = K/mx
        W = dr[key] if key == 'nums' else {dr['lucky']}
        H += len(S & W); E += c*p
        V += c*p*(1-p)*(mx-c)/(mx-1) if mx > 1 else 0
    return (H-E)/math.sqrt(V) if V > 0 else 0.0, H, E

def study(game, perms=2000, seed=1, rules_fn=None):
    mx, c, lmx, draws = load(game)
    R = (rules_fn or rules)(mx)
    sets = {name: [f(d['info']) for d in draws] for name, f in R.items()}
    n = len(draws); cut = int(n*0.6)
    res = []
    for name, S in sets.items():
        if sum(map(len, S)) == 0: continue
        zA, HA, EA = zscore(S, draws, c, mx)
        zT, _, _ = zscore(S[:cut], draws[:cut], c, mx)
        zV, _, _ = zscore(S[cut:], draws[cut:], c, mx)
        res.append((name, zA, HA, EA, zT, zV))
    # hoán vị: giữ nguyên chuỗi ngày, xáo thứ tự kết quả
    rng = random.Random(seed); maxz = []
    nums = [d['nums'] for d in draws]
    names = [r[0] for r in res]
    for _ in range(perms):
        perm = nums[:]; rng.shuffle(perm)
        fake = [dict(nums=x) for x in perm]
        maxz.append(max(abs(zscore(sets[nm], fake, c, mx)[0]) for nm in names))
    maxz.sort()
    thr = maxz[int(0.95*perms)]
    return mx, c, n, cut, res, thr

if __name__ == '__main__':
    perms = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    for game in ['power655', 'mega645', 'loto535']:
        mx, c, n, cut, res, thr = study(game, perms)
        print(f'\n=== {game}: {n} kỳ (tìm {cut} kỳ đầu / kiểm {n-cut} kỳ sau), {len(res)} quy luật ===')
        print(f'Ngưỡng may mắn thuần túy (95% hoán vị, max|z| trên mọi quy luật): {thr:.2f}')
        res.sort(key=lambda r: -abs(r[4]))
        print(f"{'quy luật':38s} {'z_tìm':>6s} {'z_kiểm':>7s} {'z_toàn':>7s} {'trúng':>6s} {'kỳvọng':>7s}")
        for name, zA, HA, EA, zT, zV in res[:12]:
            same = '✓' if zT*zV > 0 and abs(zV) > 1.64 else ' '
            print(f'{name:38s} {zT:6.2f} {zV:7.2f}{same} {zA:6.2f} {HA:6.0f} {EA:7.1f}')
