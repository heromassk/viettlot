import json,math,random
d=json.load(open('/home/user/viettlot/build/all_data.json'))['loto535']
R=[set(r) for r in d['res']];L=d['lk'];D=d['dates'];T=len(R)
ses=['13' if '13h' in x else '21' for x in D]
def corr(a,b):
    ma,mb=sum(a)/len(a),sum(b)/len(b);n=sum((x-ma)*(y-mb) for x,y in zip(a,b));q=math.sqrt(sum((x-ma)**2 for x in a)*sum((y-mb)**2 for y in b));return n/q if q else 0
random.seed(7)
# significance of session-stability & MM anticorr via sims (internal check)
def sim(nsim=300):
    a13=[];amm=[]
    for _ in range(nsim):
        RR=[set(random.sample(range(1,36),5)) for _ in range(T)];LL=[random.randint(1,12) for _ in range(T)]
        s13=[t for t in range(T) if ses[t]=='13'];h=len(s13)//2
        g=lambda ix:[sum(n in RR[t] for t in ix) for n in range(1,36)]
        a13.append(corr(g(s13[:h]),g(s13[h:])))
        th=[range(0,T//3),range(T//3,2*T//3),range(2*T//3,T)]
        mm=lambda ix:[sum(1 for t in ix if LL[t]==k) for k in range(1,13)]
        amm.append(sum(corr(mm(th[i]),mm(th[j])) for i,j in ((0,1),(1,2),(0,2)))/3)
    return a13,amm
a13,amm=sim()
print('p(sess13 corr>=0.326)',sum(x>=0.326 for x in a13)/len(a13),' p(MM avg corr<=-0.314)',sum(x<=-0.314 for x in amm)/len(amm))
# walk-forward methods: own hit rate per third
def wf(choose,start=200):
    hits={}
    for t in range(start,T):
        p=choose(t);hits[t]=len(p&R[t])
    th=[(start,start+(T-start)//3),(start+(T-start)//3,start+2*(T-start)//3),(start+2*(T-start)//3,T)]
    blk=[sum(hits[t] for t in range(a,b))/(b-a) for a,b in th]
    p3=sum(h>=3 for h in hits.values())/len(hits)
    last50=sum(hits[t] for t in range(T-50,T))/50
    return [round(x,2) for x in blk],round(last50,2),round(p3*100,1)
def topk(cnt,k,rev=True):
    return set(sorted(range(1,36),key=lambda n:((-cnt[n]) if rev else cnt[n],n))[:k])
def freq(ix):
    c={n:0 for n in range(1,36)}
    for t in ix:
        for n in R[t]: c[n]+=1
    return c
K=15
for W in (50,100,200):
    print(f'M1 nóng cùng phiên W{W}',wf(lambda t:topk(freq([u for u in range(max(0,t-2*W),t) if ses[u]==ses[t]]),K)))
    print(f'M2 nóng mọi phiên W{W}',wf(lambda t:topk(freq(range(max(0,t-W),t)),K)))
    print(f'M3 lạnh cùng phiên W{W}',wf(lambda t:topk(freq([u for u in range(max(0,t-2*W),t) if ses[u]==ses[t]]),K,False)))
    print(f'M3b lạnh mọi phiên W{W}',wf(lambda t:topk(freq(range(max(0,t-W),t)),K,False)))
# transition learned
def trans_choose(t,lag=1):
    c={n:0 for n in range(1,36)}
    for u in range(lag,t):
        for a in R[u-lag]&R[t-lag]:
            for b in R[u]: c[b]+=1
    return topk(c,K)
print('M4 chuyển kỳ (học từ đầu) lag1',wf(trans_choose))
print('M4 chuyển cùng phiên lag2',wf(lambda t:trans_choose(t,2)))
# MM methods: top3 MM
def mmwf(choose,start=200):
    h=[L[t] in choose(t) for t in range(start,T)];n=len(h);b=n//3
    return [round(sum(h[i*b:(i+1)*b])/b*100,1) for i in range(3)],round(sum(h[-50:])/50*100,1)
mmc=lambda ix:{k:sum(1 for t in ix if L[t]==k) for k in range(1,13)}
tk=lambda c,k,rev:set(sorted(c,key=lambda x:((-c[x]) if rev else c[x],x))[:k])
for W in (30,60,120,300):
    print(f'MM nóng W{W} top3',mmwf(lambda t:tk(mmc(range(max(0,t-W),t)),3,True)),f' lạnh W{W} top3',mmwf(lambda t:tk(mmc(range(max(0,t-W),t)),3,False)))
print('MM lặp/±1 kỳ trước (3 số)',mmwf(lambda t:{L[t-1],L[t-1]-1,L[t-1]+1}))
print('MM vắng lâu nhất top3',mmwf(lambda t:set(sorted(range(1,13),key=lambda k:-next((g for g in range(t) if L[t-1-g]==k),t))[:3])))
