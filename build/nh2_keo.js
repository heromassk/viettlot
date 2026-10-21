const fs=require('fs');globalThis.window={};const {poolAt}=require(process.argv[2]);
const ALL=['v','t','h','k1','k2','tr','t2','kp','nd'],NM={v:'Vắng x kỳ',t:'Tổng',h:'Hiệu',k1:'±1 kỳ trước',k2:'±1 kỳ cách 1',tr:'Trùng kỳ trước',t2:'Số kỳ cách 1',kp:'Số kẹp',nd:'Ngày quay'};
for(const g of ['loto','mega','power']){const J=JSON.parse(fs.readFileSync('build/goiy_latest/'+g+'.json'));const RA=J.res201,n=RA.length,NB=J.nb;const L=[];
 for(let t=n-100;t<n;t++){const A=poolAt(J,'',t);const rows={};A.rows.forEach(([k,,a])=>{if(a)rows[k]=new Set(a);});L.push({R:new Set(RA[t]),rows});}
 const cnt=(f,ks,x)=>ks.reduce((c,k)=>c+(f.rows[k]&&f.rows[k].has(x)?1:0),0);
 const st=W=>{let a=0,b=0,o=0,ob=0;L.slice(-W).forEach(f=>{for(let x=1;x<=NB;x++){if(cnt(f,ALL,x)>=2){a++;b+=f.R.has(x);}else{o++;ob+=f.R.has(x);}}});return [a/W,b/a*100,ob/o*100];};
 const base=[20,50,100].map(st);
 console.log(`\n=== ${g}: ≥2 pool ${base.map(([s,r,o])=>`${s.toFixed(1)} số ${r.toFixed(1)}% (ngoài ${o.toFixed(1)}%)`).join(' | ')}`);
 console.log('Pool kéo thêm: số kéo thêm/kỳ · % ra của số kéo thêm  (20 | 50 | 100)');
 for(const k of ALL){const ks=ALL.filter(z=>z!==k);const o=[20,50,100].map(W=>{let a=0,b=0;L.slice(-W).forEach(f=>{for(let x=1;x<=NB;x++)if(cnt(f,ALL,x)>=2&&cnt(f,ks,x)<2){a++;b+=f.R.has(x);}});return [a/W,a?b/a*100:0];});
  const bad=o.every(([,r],i)=>r<base[i][1]);console.log(`  ${NM[k].padEnd(15)} ${o.map(([s,r])=>`${s.toFixed(1)}·${r.toFixed(1)}%`).join(' | ')}${bad?'  ← kém ≥2 cả 3 khung':''}`);}}
