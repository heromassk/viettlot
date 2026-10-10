# Học cách loại trong Pool 25 Power (anh 10/10/2026): 291 điểm của pool25_quet làm đặc trưng cho từng số TRONG pool,
# hồi quy logistic học trên 100 kỳ trước (cuốn chiếu mỗi 10 kỳ), bỏ k số có xác suất ra thấp nhất. Chuẩn: ≥4 tụt ≤5 điểm.
exec(open('build/pool25_loaitiep.py').read().split("POOL=POOLX")[0])
R=P25.R; T=P25.T
tsall=list(range(T-200,T)); POOL={t:P25.pool(t) for t in tsall}
names=list(M); F={t:np.array([M[k](t) for k in names]).T for t in tsall}   # t -> NB×291
def XY(t):
    idx=np.array(POOL[t])-1; return F[t][idx], np.array([n in R[t] for n in POOL[t]],float)
def fit(tt,l2=50,it=400,lr=0.1):
    X=np.vstack([XY(t)[0] for t in tt]); y=np.concatenate([XY(t)[1] for t in tt])
    mu,sd=X.mean(0),X.std(0)+1e-9; Z=(X-mu)/sd; w=np.zeros(Z.shape[1]); b=0.
    for _ in range(it):
        p=1/(1+np.exp(-(Z@w+b))); e=p-y; w-=lr*(Z.T@e/len(y)+l2*w/len(y)); b-=lr*e.mean()
    return w,b,mu,sd
te=tsall[100:]; f4=lambda h:np.mean(np.array(h)>=4)*100
for l2 in (10,50,300):
  for k in (1,2,3,5):
    H=[];C=[]
    for i,t in enumerate(te):
        if i%10==0: m=fit(tsall[i:i+100],l2=l2)
        X,y=XY(t); s=((X-m[2])/m[3])@m[0]+m[1]; rm=np.argsort(s)[:k]
        H.append(int(y.sum()-y[rm].sum())); C.append(y[rm].sum()==0)
    H=np.array(H);C=np.array(C)
    print(f'l2={l2} bỏ {k}: ≥4 {f4(H):.0f}% (nửa {f4(H[:50]):.0f}·{f4(H[50:]):.0f}) | bỏ sạch {C.mean()*100:.0f}% (nửa {C[:50].mean()*100:.0f}·{C[50:].mean()*100:.0f})',flush=True)
