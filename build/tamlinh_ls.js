// Phiếu tâm linh từng kỳ quá khứ (anh 10/10/2026: dùng tâm linh để loại). node build/tamlinh_ls.js power|mega > out.json
const {chromium}=require(require.resolve('playwright',{paths:['/opt/node-tools/node_modules',process.cwd()]}));const path=require('path');
const gi={loto:0,mega:1,power:2}[process.argv[2]];
(async()=>{const b=await chromium.launch();const p=await (await b.newContext({viewport:{width:1100,height:900}})).newPage();
await p.goto('file://'+path.join(__dirname,'..','index_loto.html'));await p.waitForTimeout(3000);await p.evaluate(()=>{$('toolsCard').open=true;});await p.click('#sgCard > summary');await p.click(`#gameTabs .gtab >> nth=${gi}`);await p.waitForTimeout(4000);
// cùng môi trường với tamlinh.js (mở thẻ Tarot để có người hỏi, chờ app tính xong tâm linh) → phiếu quá khứ khớp phiếu thật
await p.evaluate(()=>{$('tqCard').open=true;renderTarot();});await p.waitForFunction(()=>S.kx&&S.kx.nv,null,{timeout:120000});
const r=await p.evaluate(()=>{const all=S.M.all,L=all.length,N=NM,P=S.kx.P;const st={T:new Float64Array((N+1)*(N+1)),cnt:new Float64Array(N+1),f:new Float64Array(N+1),n:0};const out=[];
 for(let t=0;t<L;t++){const ctx=kxCtx(all[t].date),pv=t?all[t-1].r:null,r=all[t].r;
  if(t>=L-220){const vt=new Array(N+1).fill(0);KX_M.forEach(m=>{let o=null;try{o=m[3](ctx,pv,st,P,N);}catch(e){}if(o&&o.nums)o.nums.forEach(v=>vt[v]++);});out.push({date:all[t].date,r,vt});}
  if(pv){pv.forEach(x=>{st.cnt[x]++;r.forEach(y=>st.T[x*(N+1)+y]++);});}r.forEach(y=>st.f[y]++);st.n++;}
 const lv=S.kx.lastV;if(lv&&out.length&&out[out.length-1].vt.join()!==lv.vt.join())out.push({lech:true});return out;});
console.log(JSON.stringify(r));await b.close();})();
