const fs=require('fs');globalThis.window={};const {poolAt}=require(process.argv[2]);
const ND=JSON.parse(fs.readFileSync('/tmp/claude-0/-home-user-viettlot/6e75ae3d-96cf-5250-96a3-3d305a41f786/scratchpad/ngay_sets.json'));const LUC=new Set([1,2,3,4,7,11,18,29,47]),FBN=new Set([1,2,3,5,8,13,21,34,55]),NGF=new Set([5,8,13,21,34]);
for(const g of ['loto','mega','power']){
 const J=JSON.parse(fs.readFileSync('build/goiy_latest/'+g+'.json'));const RA=J.res201,DA=J.dates201,NB=J.nb,n=RA.length;const F=[];
 for(let t=n-100;t<n;t++){const A=poolAt(J,'',t);const MS={};A.rows.forEach(([k,,a])=>{if(a)MS[k]=new Set(a);});const RK=(J.rkHist||{})[DA[t]];if(!RK)continue;
  const pv=RA[t-1],pv2=RA[t-2],P=new Set(pv);const tg=new Set(),hi=new Set(),bn=new Set();
  for(const a of pv)for(const b of pv2){if(a+b<=NB)tg.add(a+b);if(a!==b)hi.add(Math.abs(a-b));}
  const co={};for(let u=Math.max(0,t-101);u<t-1;u++)for(const a of RA[u])for(const b of RA[u])if(a!==b)co[a*100+b]=(co[a*100+b]||0)+1;
  for(const a of pv){let m=0;for(let b=1;b<=NB;b++)if(b!==a)m=Math.max(m,co[a*100+b]||0);for(let b=1;b<=NB;b++)if(b!==a&&(co[a*100+b]||0)===m)bn.add(b);}
  [tg,hi,bn].forEach(S=>pv.forEach(a=>S.delete(a)));
  const s=[...pv].sort((a,b)=>a-b),ftq=new Set();for(let i=0;i<s.length;i++)for(let j=i+1;j<s.length;j++)for(const v of [s[i]+s[j],s[i]+2*s[j],2*s[i]+3*s[j]])if(v<=NB)ftq.add(v);pv.forEach(a=>ftq.delete(a));
  const ch=k=>{const U=new Set();for(let u=t-k;u<t;u++)RA[u].forEach(x=>U.add(x));const su=[...U].sort((a,b)=>a-b),nx=new Set();for(let i=0;i<su.length;i++)for(let j=i+1;j<su.length;j++){const a=su[i],b=su[j];if(U.has(a+b)&&a+2*b<=NB)nx.add(a+2*b);}U.forEach(x=>nx.delete(x));return nx;};
  const ng=new Set();for(let x=1;x<=NB;x++){let u=t-1;while(u>=0&&!RA[u].includes(x))u--;if(NGF.has(t-u))ng.add(x);}
  F.push({RK,MS,C:A.C,HK:{tg,hi,bn},G:Object.fromEntries(Object.entries(ND[g][DA[t]]).map(([k,v])=>[k,new Set(v)])),R:new Set(RA[t])});}
 const hs=(f,k,x)=>!!(f.MS[k]&&f.MS[k].has(x));const up=(ks,b)=>(f,x,i)=>i-ks.reduce((z,k)=>z+(hs(f,k,x)?b:0),0);
 const RULE={loto:{9:up(['t2','kp'],2),12:up(['v','t'],4),15:up(['t2','tl'],2)},mega:{9:(f,x,i)=>up(['v','tl'],4)(f,x,i)-(f.HK.tg.has(x)?2:0)+(f.HK.bn.has(x)?4:0),12:up(['t','tl'],2),15:up(['t2','tl'],4)},power:{9:(f,x,i)=>up(['k1'],2)(f,x,i)-(f.HK.hi.has(x)?4:0)-(f.HK.bn.has(x)?4:0),12:(f,x,i)=>up(['tr'],6)(f,x,i)-(f.HK.bn.has(x)?2:0),15:(f,x,i)=>i-((f.C[x]||0)>=2?4:0)}}[g];
 const pick=(f,K,d)=>f.RK.map((x,i)=>[RULE[K](f,x,i)+d(f,x),i,x]).sort((a,b)=>a[0]-b[0]||a[1]-b[1]).slice(0,K).map(z=>z[2]);
 const ev=(K,d)=>[20,50,100].map(W=>{let h=0,g3=0;for(const f of F.slice(-W)){const x=pick(f,K,d).filter(z=>f.R.has(z)).length;h+=x;g3+=x>=3;}return [h,g3];});
 const V=[['hiện tại',()=>0]];
 for(const k of Object.keys(F[0].G))for(const b of [2,4,-2,-4])V.push([`${k}${b>0?'−':'+'}${Math.abs(b)}`,(f,x)=>f.G[k].has(x)?b:0]);
 console.log(`\n=== ${g} (${F.length} kỳ) — tổng số trúng·kỳ≥3 ở 20/50/100`);
 for(const K of [9,12,15]){const res=V.map(([nm,d])=>[nm,ev(K,d)]);const b0=res[0][1];const sc=r=>r.reduce((z,[h],i)=>z+h-b0[i][0],0);
  console.log(`P${K} hiện tại: ${b0.map(z=>z.join('·')).join(' / ')}`);
  res.slice(1).map(r=>[...r,sc(r[1]),r[1].every((z,i)=>z[0]>=b0[i][0])&&sc(r[1])>0]).sort((a,b)=>b[2]-a[2]).slice(0,6).forEach(([nm,r,s,ok])=>console.log(`   ${nm.padEnd(9)} ${r.map(z=>z.join('·')).join(' / ')}  ${s>0?'+':''}${s}${ok?' ✓đủ3khung':''}`));}}
