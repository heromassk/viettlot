const fs=require('fs');globalThis.window={};const {poolAt}=require(process.argv[2]);
const ALL=['v','t','h','k1','k2','tr','t2','kp','nd'];const WK={loto:['t','k1'],mega:['k2'],power:['v','h','k1','k2']};
for(const g of ['loto','mega','power']){const J=JSON.parse(fs.readFileSync('build/goiy_latest/'+g+'.json'));const RA=J.res201,n=RA.length,NB=J.nb;const L=[];
 for(let t=n-100;t<n;t++){const A=poolAt(J,'',t);const rows={};A.rows.forEach(([k,,a])=>{if(a)rows[k]=new Set(a);});L.push({R:new Set(RA[t]),rows});}
 const ev=w=>[20,50,100].map(W=>{let sz=0,h=0,g3=0;L.slice(-W).forEach(f=>{let k=0,c=0;for(let x=1;x<=NB;x++){const s=ALL.reduce((z,p)=>z+(f.rows[p]&&f.rows[p].has(x)?(WK[g].includes(p)?w:1):0),0);if(s>=2){c++;k+=f.R.has(x);}}sz+=c;h+=k;g3+=k>=3;});return `${(sz/W).toFixed(1)}·${(h/W).toFixed(2)}·${(h/sz*100).toFixed(1)}%·${g3}`;});
 console.log(`\n=== ${g} pool yếu: ${WK[g].join(',')}`);for(const w of [1,0.75,0.5,0])console.log(`  pool yếu tính ${w}`.padEnd(22),ev(w).join(' | '));}
