// Keno — tâm linh: chạy 20 phương pháp tâm linh của app (KX_M) với dải 1–80 cho 1 kỳ Keno.
// node build/keno_tamlinh.js "dd/mm/yyyy" giờ "<20 số kỳ trước>"   → JSON {votes, methods}
// Bạc nhớ dựng từ 5000 kỳ gần trong kho (keno.jsonl). Người chơi: mặc định của app (ngày sinh, tên lưu trong app).
const {chromium}=require(require.resolve('playwright',{paths:['/opt/node-tools/node_modules',process.cwd()]}));const path=require('path'),fs=require('fs');
const [ds,hh,prevS]=process.argv.slice(2);const prev=prevS.trim().split(/\s+/).map(Number);
const rows=fs.readFileSync('/home/user/vietvudanh/vietlott-data/data/keno.jsonl','utf8').trim().split('\n').map(JSON.parse);
const uniq=Object.values(Object.fromEntries(rows.map(r=>[r.id,r]))).sort((a,b)=>+a.id.slice(1)-+b.id.slice(1)).slice(-5000).map(r=>r.result);
(async()=>{const b=await chromium.launch();const p=await (await b.newContext()).newPage();
await p.goto('file://'+path.join(__dirname,'..','index_loto.html'));await p.waitForTimeout(3000);
const r=await p.evaluate(([ds,hh,prev,H])=>{const N=80,[dd,mm,yy]=ds.split('/').map(Number);
  const cc=canChi(dd,mm,yy,hh,0),L=solar2lunar(dd,mm,yy);let Y=yy;if(mm<=2&&cc.lam<315&&cc.lam>=270)Y--;const c={dd,mm,yy,hh,cc,L,jdn:cc.jdn,Y};
  const st={T:new Float64Array((N+1)*(N+1)),cnt:new Float64Array(N+1),f:new Float64Array(N+1),n:0};
  for(let t=0;t<H.length;t++){const r=H[t],pv=t?H[t-1]:null;if(pv)pv.forEach(x=>{st.cnt[x]++;r.forEach(y=>st.T[x*(N+1)+y]++);});r.forEach(y=>st.f[y]++);st.n++;}
  const P=kxPerson(),votes=new Array(N+1).fill(0),methods=[];
  KX_M.forEach(m=>{let o=null;try{o=m[3](c,prev,st,P,N);}catch(e){}if(o&&o.nums&&o.nums.length){o.nums.forEach(v=>votes[v]++);methods.push([m[1],o.why.replace(/<[^>]+>/g,''),o.nums]);}});
  return {votes,methods,person:P&&{sol:P.sol,name:P.name}};},[ds,+hh,prev,uniq]);
console.log(JSON.stringify(r));await b.close();})();
