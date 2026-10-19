# Số May Mắn Loto — thử thêm dấu vết mới ngoài ±3 (anh 19/10/2026). Mỗi cách chọn 3 số, chỉ dùng dữ liệu trước kỳ đó.
# Chấm % kỳ trúng ở 10/20/50/100 kỳ và 3 đoạn 100 kỳ (gần → xa). Cách đang dùng: ±3 quanh MM kỳ trước, xếp nóng 10 kỳ.
import json
from collections import Counter
D=json.load(open('build/all_data.json'))['loto535'];LK=D['lk'];R=[set(r) for r in D['res']];DT=D['dates'];T=len(LK)
SES=['13' if d.endswith('13h') else '21' for d in DT]+['13' if DT[-1].endswith('21h') else '21']   # thêm phiên của kỳ tới
K12=range(1,13)
def c(t,w):return Counter(LK[max(0,t-w):t])
def gap(t,k):
    g=0
    while g<t and LK[t-1-g]!=k:g+=1
    return g
def near(t,d=3,ref=None):
    ref=LK[t-1] if ref is None else ref;return [k for k in K12 if abs(k-ref)<=d]
def top(ks,key):return sorted(ks,key=key)[:3]
def prev_ses(t):
    for i in range(t-1,-1,-1):
        if SES[i]==SES[t]:return i
def markov(t,W=300):
    m=Counter((LK[u-1],LK[u]) for u in range(max(1,t-W),t));p=LK[t-1];return {k:m[(p,k)] for k in K12}
def dmap(t,W=200):
    return Counter(LK[u]-LK[u-1] for u in range(max(1,t-W),t))
M={}
M['Đang dùng: ±3, nóng 10 kỳ']=lambda t:top(near(t),lambda k:(-c(t,10)[k],-c(t,50)[k],k))
M['±3, vắng lâu nhất']=lambda t:top(near(t),lambda k:(-gap(t,k),k))
M['±3, vắng ít nhất (vừa ra gần)']=lambda t:top([k for k in near(t) if k!=LK[t-1]],lambda k:(gap(t,k),k))
M['±3, nóng 20 kỳ']=lambda t:top(near(t),lambda k:(-c(t,20)[k],-c(t,50)[k],k))
M['±3, bỏ MM kỳ trước, nóng 10']=lambda t:top([k for k in near(t) if k!=LK[t-1]],lambda k:(-c(t,10)[k],-c(t,50)[k],k))
M['±3, sát MM trước nhất (±1, ±2)']=lambda t:top([k for k in near(t) if k!=LK[t-1]],lambda k:(abs(k-LK[t-1]),-c(t,10)[k],k))
M['±3, xa nhất (±3, ±2)']=lambda t:top([k for k in near(t) if k!=LK[t-1]],lambda k:(-abs(k-LK[t-1]),-c(t,10)[k],k))
M['Chênh lệch hay gặp 200 kỳ (Δ = MM sau − MM trước)']=lambda t:(lambda dm:top([k for k in K12],lambda k:(-dm[k-LK[t-1]],k)))(dmap(t))
M['Markov MM trước → MM sau (300 kỳ)']=lambda t:(lambda m:top(K12,lambda k:(-m[k],-c(t,50)[k],k)))(markov(t))
M['±3, xếp theo Markov']=lambda t:(lambda m:top(near(t),lambda k:(-m[k],-c(t,10)[k],k)))(markov(t))
M['±3 quanh MM kỳ CÙNG GIỜ trước, nóng 10']=lambda t:top(near(t,3,LK[prev_ses(t)]),lambda k:(-c(t,10)[k],-c(t,50)[k],k))
M['Giao ±3 kỳ trước và ±3 cùng giờ trước']=lambda t:(lambda a,b:top([k for k in a if k in b] or a,lambda k:(-c(t,10)[k],-c(t,50)[k],k)))(near(t),near(t,3,LK[prev_ses(t)]))
M['MM vắng 8 kỳ (không ra 8 kỳ), trong ±3']=lambda t:(lambda v:top([k for k in near(t) if k in v] or near(t),lambda k:(-c(t,10)[k],k)))(set(K12)-set(LK[t-8:t]))
M['MM vắng 4 kỳ, trong ±3']=lambda t:(lambda v:top([k for k in near(t) if k in v] or near(t),lambda k:(-c(t,10)[k],k)))(set(K12)-set(LK[t-4:t]))
M['Số chính kỳ trước ≤12 (trong ±3 trước)']=lambda t:top(sorted(set(near(t))&R[t-1]) or near(t),lambda k:(-c(t,10)[k],k)) if set(near(t))&R[t-1] else top(near(t),lambda k:(-c(t,10)[k],-c(t,50)[k],k))
M['Tổng 5 số chính kỳ trước mod 12 ±1']=lambda t:(lambda s:[((s+d-1)%12)+1 for d in (0,-1,1)])(sum(R[t-1]))
M['Đuôi tổng kỳ trước (1–12) ±1']=lambda t:(lambda s:[((s%10+d-1)%12)+1 for d in (0,-1,1)])(sum(R[t-1]))
M['Nóng 10 kỳ toàn bộ (không ±3)']=lambda t:top(K12,lambda k:(-c(t,10)[k],-c(t,50)[k],k))
M['Vắng lâu nhất toàn bộ']=lambda t:top(K12,lambda k:(-gap(t,k),k))
def rate(f,ts):return sum(LK[t] in f(t) for t in ts)/len(ts)
print('Cách | 10 | 20 | 50 | 100 | đoạn 1 / 2 / 3 (100 kỳ) | 500 kỳ | kỳ tới')
res=[]
for nm,f in M.items():
    r=[rate(f,range(T-w,T)) for w in (10,20,50,100)];s=[rate(f,range(T-100*(k+1),T-100*k)) for k in range(3)];a=rate(f,range(T-500,T))
    res.append((nm,r,s,a,f(T)))
for nm,r,s,a,nx in res:
    print(f'{nm} | '+' | '.join(f'{x:.0%}' for x in r)+' | '+' / '.join(f'{x:.0%}' for x in s)+f' | {a:.0%} | '+' '.join(f'{k:02d}' for k in nx))
print('Δ phân bố 200 kỳ:',sorted(dmap(T).items()))
print('±3 đúng: 100 kỳ', sum(abs(LK[t]-LK[t-1])<=3 for t in range(T-100,T)),'| 3 đoạn',[sum(abs(LK[t]-LK[t-1])<=3 for t in range(T-100*(k+1),T-100*k)) for k in range(3)])

# Kết hợp trong ±3: nóng 10 kỳ + chênh lệch hay gặp (Δ) với trọng số w
print('\nKết hợp trong ±3: điểm = số lần ra 10 kỳ + w × (tần suất Δ 200 kỳ / 10)')
for w in (0.5, 1, 2):
    f=lambda t,w=w:(lambda dm:top(near(t),lambda k:(-(c(t,10)[k]+w*dm[k-LK[t-1]]/10),-c(t,50)[k],k)))(dmap(t))
    r=[rate(f,range(T-x,T)) for x in (10,20,50,100)];s=[rate(f,range(T-100*(k+1),T-100*k)) for k in range(3)]
    print(f'w={w} | '+' | '.join(f'{x:.0%}' for x in r)+' | '+' / '.join(f'{x:.0%}' for x in s)+f' | {rate(f,range(T-500,T)):.0%} | '+' '.join(f'{k:02d}' for k in f(T)))
for W2 in (5,15):
    f=lambda t,W2=W2:top(near(t),lambda k:(-c(t,W2)[k],-c(t,50)[k],k))
    r=[rate(f,range(T-x,T)) for x in (10,20,50,100)];s=[rate(f,range(T-100*(k+1),T-100*k)) for k in range(3)]
    print(f'±3 nóng {W2} kỳ | '+' | '.join(f'{x:.0%}' for x in r)+' | '+' / '.join(f'{x:.0%}' for x in s)+f' | {rate(f,range(T-500,T)):.0%} | '+' '.join(f'{k:02d}' for k in f(T)))
