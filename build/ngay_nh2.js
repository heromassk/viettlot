const fs=require('fs');globalThis.window={};const {poolAt}=require(process.argv[2]);const ND=JSON.parse(fs.readFileSync(process.argv[3]));
const CAND={loto:[['gop'],['gop','ghep'],['gop','ghep','tam'],['gop','ghep','tam','nlon'],['thang','nlon','ghep','tam']],mega:[['nlon'],['nlon','ncong']],power:[['thu'],['thu','n1'],['thu','n1','namlon'],['gop'],['gop','n1']]};
for(const g of ['loto','mega','power']){const J=JSON.parse(fs.readFileSync('build/goiy_latest/'+g+'.json'));const RA=J.res201,DA=J.dates201,n=RA.length;const F=[];
 for(let t=n-100;t<n;t++){const A=poolAt(J,'',t);F.push({C:A.C,N:ND[g][DA[t]],R:new Set(RA[t])});}
 const ev=ks=>[20,50,100].map(W=>{let sz=0,h=0,g3=0;for(const f of F.slice(-W)){const S=new Set(ks.flatMap(k=>f.N[k]));const nh=[];for(let x=1;x<=J.nb;x++)if((f.C[x]||0)+(S.has(x)?1:0)>=2)nh.push(x);const k=nh.filter(x=>f.R.has(x)).length;sz+=nh.length;h+=k;g3+=k>=3;}return `${(sz/W).toFixed(1)}·${(h/W).toFixed(2)}·${(h/sz*100).toFixed(1)}%·${g3}`;});
 console.log(`\n=== ${g} ≥2 pool (cỡ · trúng/kỳ · % mỗi số · kỳ ≥3) 20 | 50 | 100`);console.log('hiện tại      ',ev([]).join(' | '));
 for(const ks of CAND[g])console.log(('+'+ks.join('+')).padEnd(14),ev(ks).join(' | '));}
