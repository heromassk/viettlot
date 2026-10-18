#!/usr/bin/env python3
"""Chạy code của app (index_loto.html) trong Chromium, xuất từng kỳ của W kỳ gần nhất ra build/kiemtra_app.json
(cho kiemtra_pp.py chấm). Mỗi kỳ chỉ dùng dữ liệu trước kỳ đó, đúng như app tính:
  - 16 phương pháp pool PM (PP15…PP27): thứ tự xếp hạng toàn bộ số (mảng dài W+1, phần tử cuối = kỳ tới)
  - 20 phương pháp tâm linh KX_M: dãy số mỗi phương pháp chọn (chạy tiến như kxRun)
  python build/kiemtra_app.py [W=400]          (cần: pip install playwright; playwright install chromium)"""
import json, sys, pathlib
from playwright.sync_api import sync_playwright
B = pathlib.Path(__file__).resolve().parent; ROOT = B.parent
W = int(sys.argv[1]) if len(sys.argv) > 1 else 400
JS = r"""(W)=>{const all=S.M.all,L=all.length,N=NM,P=kxPerson();
 S.PS=poolScores();S.rkC={};poolEval();const {out}=S.PS;
 const pm={};PM.forEach(([id,nm])=>{pm[id]={nm,ord:[]};for(let t=L-W;t<=L;t++)pm[id].ord.push(out[id]&&out[id][t]?topK(out[id][t],N):null);});
 const st={T:new Float64Array((N+1)*(N+1)),cnt:new Float64Array(N+1),f:new Float64Array(N+1),n:0};
 const kx=KX_M.map(m=>({id:m[0],nm:m[1],g:m[2],nums:[]}));
 for(let t=0;t<L;t++){const ctx=kxCtx(all[t].date),pv=t?all[t-1].r:null,r=all[t].r;
   if(t>=L-W)KX_M.forEach((m,i)=>{let o=null;try{o=m[3](ctx,pv,st,P,N);}catch(e){}kx[i].nums.push(o&&o.nums?o.nums.slice():null);});
   if(pv){pv.forEach(x=>{st.cnt[x]++;r.forEach(y=>st.T[x*(N+1)+y]++);});}r.forEach(y=>st.f[y]++);st.n++;}
 const nx=kxCtx(S.M.nd);KX_M.forEach((m,i)=>{let o=null;try{o=m[3](nx,all[L-1].r,st,P,N);}catch(e){}kx[i].nums.push(o&&o.nums?o.nums.slice():null);});
 return {key:GAME,N,C:CC,L,dates:all.slice(L-W).map(d=>d.date),res:all.slice(L-W).map(d=>d.r),pm,kx,person:P?{sol:P.sol,name:P.name}:null};}"""
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1100, 'height': 900})
    pg.goto((ROOT / 'index_loto.html').as_uri()); pg.wait_for_timeout(3000)
    pg.evaluate("()=>{$('toolsCard').open=true;}"); pg.click('#sgCard > summary')
    for gi, g in enumerate(['loto', 'mega', 'power']):
        pg.click(f'#gameTabs .gtab >> nth={gi}'); pg.wait_for_timeout(4000)
        pg.evaluate("()=>{$('tqCard').open=true;try{renderTarot();}catch(e){}}"); pg.wait_for_timeout(1500)
        res[g] = pg.evaluate(JS, W); print(g, res[g]['key'], res[g]['L'], 'kỳ, cuối', res[g]['dates'][-1])
    b.close()
(B / 'kiemtra_app.json').write_text(json.dumps(res, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
