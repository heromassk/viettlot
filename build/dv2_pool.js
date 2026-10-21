const fs=require('fs');globalThis.window={};const {poolAt}=require(process.env.BANG||'./bang_t.js');
for(const g of ['loto','mega','power']){
 const J=JSON.parse(fs.readFileSync('/home/user/viettlot/build/goiy_latest/'+g+'.json'));const RA=J.res201,DA=J.dates201,NB=J.nb,n=RA.length;
 const F=[];
 for(let t=n-100;t<n;t++){const A=poolAt(J,'',t);const MS={};A.rows.forEach(([k,,a])=>{if(a)MS[k]=new Set(a);});
  const RK=(J.rkHist||{})[DA[t]];if(!RK){console.log('thiếu',DA[t]);continue;}
  const Aa=new Set(RA[t-1]),Bb=new Set(RA[t-2]),U=[...new Set([...Aa,...Bb])].sort((a,b)=>a-b);
  const tong=new Set(),hieu=new Set(),fib=new Set(),ban=new Set();
  for(const a of Aa)for(const b of Bb){if(a+b<=NB)tong.add(a+b);if(a!==b)hieu.add(Math.abs(a-b));}
  for(let i=0;i<U.length;i++)for(let j=i+1;j<U.length;j++){const a=U[i],b=U[j];for(const v of [a+b,a+2*b,2*a+3*b])if(v<=NB)fib.add(v);}
  const co={};for(let u=Math.max(0,t-101);u<t-1;u++)for(const a of RA[u])for(const b of RA[u])if(a!==b)co[a+','+b]=(co[a+','+b]||0)+1;
  for(const a of Aa){let m=0;for(let b=1;b<=NB;b++)if(b!==a)m=Math.max(m,co[a+','+b]||0);for(let b=1;b<=NB;b++)if(b!==a&&(co[a+','+b]||0)===m)ban.add(b);}
  for(const S of [tong,hieu,fib,ban])for(const a of Aa)S.delete(a);
  const P={};[9,12,15].forEach(K=>{const r=A.rows.find(z=>z[0]==='p'+K);P[K]=r&&r[2];});
  F.push({RK,MS,C:A.C,TS:MS.tl||new Set(),G:{tong,hieu,fib,ban},R:new Set(RA[t]),P});}
 const hs=(f,k,x)=>!!(f.MS[k]&&f.MS[k].has(x));const up=(ks,b)=>(f,x,i)=>i-ks.reduce((z,k)=>z+(hs(f,k,x)?b:0),0);
 const RULE={loto:{9:up(['t2','kp'],2),12:up(['v','t'],4),15:up(['t2','tl'],2)},mega:{9:up(['v','tl'],4),12:up(['t','tl'],2),15:up(['t2','tl'],4)},power:{9:up(['k1'],2),12:up(['tr'],6),15:(f,x,i)=>i-((f.C[x]||0)>=2?4:0)}}[g];
 const pick=(f,K,d)=>f.RK.map((x,i)=>[RULE[K](f,x,i)+d(f,x),i,x]).sort((a,b)=>a[0]-b[0]||a[1]-b[1]).slice(0,K).map(z=>z[2]);
 // kiểm khớp app
 let mis=0;F.forEach(f=>[9,12,15].forEach(K=>{const a=pick(f,K,()=>0).sort((a,b)=>a-b).join();if(f.P[K]&&a!==f.P[K].join())mis++;}));
 const ev=(K,d)=>[20,50,100].map(W=>{let h=0,g3=0;for(const f of F.slice(-W)){const x=pick(f,K,d).filter(z=>f.R.has(z)).length;h+=x;g3+=x>=3;}return [h,g3];});
 const V=[['hiện tại',()=>0]];
 for(const k of ['tong','hieu','fib','ban'])for(const b of [2,4,-2,-4])V.push([`${k}${b>0?'−':'+'}${Math.abs(b)}`,(f,x)=>f.G[k].has(x)?b:0]);
 for(const b of [2,4])V.push([`tong+fib −${b}`,(f,x)=>(f.G.tong.has(x)?b:0)+(f.G.fib.has(x)?b:0)]);
 for(const b of [2,4])V.push([`hieu+ban +${b}`,(f,x)=>-(f.G.hieu.has(x)?b:0)-(f.G.ban.has(x)?b:0)]);
 for(const [a,b] of [[2,2],[4,2],[2,4],[4,4]])V.push([`tong+${a}&ban−${b}`,(f,x)=>-(f.G.tong.has(x)?a:0)+(f.G.ban.has(x)?b:0)]);
 console.log(`\n=== ${g} (${F.length} kỳ, lệch app ${mis}) — tổng số trúng·kỳ≥3 ở 20/50/100`);
 for(const K of [9,12,15]){const res=V.map(([nm,d])=>[nm,ev(K,d)]);const b0=res[0][1];
  const sc=r=>r.reduce((z,[h],i)=>z+h-b0[i][0],0);
  console.log(`P${K} hiện tại: ${b0.map(z=>z.join('·')).join(' / ')}`);
  res.slice(1).map(r=>[...r,sc(r[1]),r[1].every((z,i)=>z[0]>=b0[i][0])]).sort((a,b)=>b[2]-a[2]).slice(0,4).forEach(([nm,r,s,ok])=>console.log(`   ${nm.padEnd(12)} ${r.map(z=>z.join('·')).join(' / ')}  ${s>0?'+':''}${s}${ok?' ✓đủ3khung':''}`));}}
