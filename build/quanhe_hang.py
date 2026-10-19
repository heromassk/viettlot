# Quan hệ các số trong cùng 1 kỳ (anh 19/10/2026): a+b=c, a+b=c+d, gấp đôi (b=2a), cấp số 3 số (a,b,c cách đều).
# Đếm số kỳ có dạng đó (anh: không so với ngẫu nhiên). Phần 'mức tự nhiên' bên dưới chỉ là bản cũ, không dùng khi báo anh.
import json,itertools,random
ALL=json.load(open('build/all_data.json'))
def rel(s):
    s=sorted(s);S=set(s);o={}
    o['a+b=c']=any(a+b in S for a,b in itertools.combinations(s,2))
    o['a+b=c+d']=any(a+b==c+d for a,b,c,d in itertools.permutations(s,4) if a<b and c<d and a<c and len({a,b,c,d})==4)
    o['gấp đôi (b=2a)']=any(2*a in S for a in s)
    o['3 số cách đều']=any(b-a==c-b for a,b,c in itertools.combinations(s,3))
    return o
KEYS=['a+b=c','a+b=c+d','gấp đôi (b=2a)','3 số cách đều']
random.seed(1)
for key,NB,KB,nm in [('loto535',35,5,'Loto 5/35'),('mega645',45,6,'Mega 6/45'),('power655',55,6,'Power 6/55')]:
    R=[set(r) for r in ALL[key]['res']];T=len(R)
    if nm.startswith('Loto'):base=[rel(c) for c in itertools.combinations(range(1,NB+1),KB)]
    else:base=[rel(random.sample(range(1,NB+1),KB)) for _ in range(200000)]
    segs=[('100 kỳ gần',T-100,T),('đoạn 2',T-200,T-100),('đoạn 3',T-300,T-200)]
    if nm.startswith('Loto'):segs+=[('toàn bộ',0,T)]
    print(f'\n## {nm}')
    print('| Quan hệ | '+' | '.join(s[0] for s in segs)+' | mức tự nhiên | kỳ gần nhất |')
    rl=rel(R[-1])
    for k in KEYS:
        print(f'| {k} | '+' | '.join(f'{sum(rel(R[t])[k] for t in range(a,b))/(b-a):.0%}' for _,a,b in segs)+f' | {sum(x[k] for x in base)/len(base):.0%} | {"có" if rl[k] else "không"} |')
