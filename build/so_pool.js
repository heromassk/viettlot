const fs=require('fs');globalThis.window={};const {poolAt}=require(process.argv[2]);
for(const g of ['loto','mega','power']){const J=JSON.parse(fs.readFileSync('build/goiy_latest/'+g+'.json'));const RA=J.res201,n=RA.length;const st={};
 for(let t=n-100;t<n;t++){const A=poolAt(J,'',t);if(!A)continue;const R=new Set(RA[t]);
  const rows=A.rows.filter(([k,,a])=>a&&a.length);const nh=Object.keys(A.C).map(Number).filter(x=>A.C[x]>=2);rows.push(['nh2','≥2',nh]);
  for(const [k,,a] of rows){const h=a.filter(x=>R.has(x)).length;(st[k]=st[k]||[]).push([a.length,h]);}}
 console.log('\n=== '+g+'  (cỡ TB · trúng TB/kỳ · % mỗi số · kỳ ≥2 · kỳ ≥3)  20 | 50 | 100');
 for(const k in st){if(k==='mm')continue;const a=st[k];const f=W=>{const b=a.slice(-W);const sz=b.reduce((z,x)=>z+x[0],0)/b.length,h=b.reduce((z,x)=>z+x[1],0)/b.length;return `${sz.toFixed(0)}·${h.toFixed(2)}·${(h/sz*100).toFixed(1)}%·${b.filter(x=>x[1]>=2).length}·${b.filter(x=>x[1]>=3).length}`;};
  console.log(k.padEnd(4),[20,50,100].map(f).join(' | '),a.length<100?'(n='+a.length+')':'');}}
