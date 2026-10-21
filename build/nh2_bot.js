const fs=require('fs');globalThis.window={};const {poolAt}=require(process.argv[2]);
const ALL=['v','t','h','k1','k2','tr','t2','kp','nd'];
const DROP=[[],['k1'],['t'],['k2'],['kp'],['k1','t'],['k1','k2'],['k1','t','k2'],['k1','t','kp'],['k1','t','k2','kp'],['h'],['v'],['tr'],['t2']];
for(const g of ['loto','mega','power']){const J=JSON.parse(fs.readFileSync('build/goiy_latest/'+g+'.json'));const RA=J.res201,n=RA.length,NB=J.nb;const L=[];
 for(let t=n-100;t<n;t++){const A=poolAt(J,'',t);const rows={};A.rows.forEach(([k,,a])=>{if(a)rows[k]=new Set(a);});L.push({R:new Set(RA[t]),rows});}
 const ev=(ks,need)=>[20,50,100].map(W=>{let sz=0,h=0,g3=0;L.slice(-W).forEach(f=>{const nh=[];for(let x=1;x<=NB;x++){let c=0;ks.forEach(k=>{if(f.rows[k]&&f.rows[k].has(x))c++;});if(c>=need)nh.push(x);}const k=nh.filter(x=>f.R.has(x)).length;sz+=nh.length;h+=k;g3+=k>=3;});return `${(sz/W).toFixed(1)}·${(h/W).toFixed(2)}·${(h/Math.max(1,sz)*100).toFixed(1)}%·${g3}`;});
 console.log(`\n=== ${g} (cỡ · trúng/kỳ · % mỗi số · kỳ ≥3) 20 | 50 | 100`);
 for(const d of DROP){const ks=ALL.filter(k=>!d.includes(k));console.log(('bỏ '+(d.join(',')||'—')).padEnd(18),ev(ks,2).join(' | '));}}
