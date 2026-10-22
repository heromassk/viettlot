const fs=require('fs');globalThis.window={};const {poolAt}=require(process.argv[2]);
for(const g of ['loto','mega']){const J=JSON.parse(fs.readFileSync('build/goiy_latest/'+g+'.json'));const RA=J.res201,n=RA.length;
 const ev=b=>{globalThis.X2B={9:b,12:b,15:b};const r={9:[],12:[],15:[]};for(let t=n-100;t<n;t++){const A=poolAt(J,'',t);const R=new Set(RA[t]);for(const K of [9,12,15]){const a=A.rows.find(z=>z[0]==='p'+K)[2];const h=a.filter(x=>R.has(x)).length;r[K].push(h);}}return r;};
 const fm=a=>[20,50,100].map(W=>{const b=a.slice(-W);return b.reduce((x,y)=>x+y,0)+'·'+b.filter(x=>x>=3).length;}).join(' / ');
 console.log('\n=== '+g+' (tổng trúng·kỳ≥3 ở 20/50/100)');const R0=ev(0);
 for(const K of [9,12,15]){console.log(`P${K} hiện tại ${fm(R0[K])}`);for(const b of [2,4,6,-2]){const r=ev(b)[K];console.log(`   ×2 ${b>0?'xuống':'lên'} ${Math.abs(b)}: ${fm(r)}`);}}}
