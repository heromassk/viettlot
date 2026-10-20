# Số kẹp (a và a+2 cùng ra, a+1 không ra) — ra ở kỳ +1, +2, +3… sau đó? (anh 21/10/2026)
import json
d=json.load(open('build/all_data.json'))
def run(res,W,K=5):
    n=len(res);rows=[]
    for t in range(n-W-K,n-K) if False else range(max(0,n-W),n):
        S=set(res[t]);kp=[m for m in S if m+2 in S and m+1 not in S]
        for a in kp:
            m=a+1;seq=[(m in set(res[t+j])) if t+j<n else None for j in range(1,K+1)]
            rows.append(seq)
    return rows
def rep(rows,K=5):
    out=[]
    for j in range(K):
        # chỉ xét số chưa ra ở các kỳ trước j, và đã có kết quả kỳ j
        base=[r for r in rows if r[j] is not None and not any(r[:j])]
        hit=sum(1 for r in base if r[j])
        out.append(f"{hit}/{len(base)} ({hit/len(base)*100:.0f}%)" if base else "-")
    return out
for key,nm,gios in [('loto535','Loto',[None,' 13h',' 21h']),('mega645','Mega',[None]),('power655','Power',[None])]:
    R=d[key]['res'];D=d[key]['dates']
    for g in gios:
        res=[R[i] for i in range(len(R)) if g is None or D[i].endswith(g)]
        for W in ([20,50,100,300] if key=='loto535' else [20,50,100]):
            rows=run(res,W);print(nm,(g or 'cả 2 buổi' if key=='loto535' else ''),W,'kỳ | số kẹp',len(rows),'| ra kỳ +1..+5 (chưa ra trước đó):',' · '.join(rep(rows)))
