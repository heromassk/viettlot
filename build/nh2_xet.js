const fs=require('fs');globalThis.window={};const {poolAt}=require(process.argv[2]);const g=process.argv[3]||'loto';
const J=JSON.parse(fs.readFileSync('build/goiy_latest/'+g+'.json'));const RA=J.res201,DA=J.dates201,n=RA.length,NB=J.nb;
const L=[];for(let t=n-100;t<n;t++){const A=poolAt(J,'',t);const R=new Set(RA[t]);const rows={};A.rows.forEach(([k,,a])=>{if(a)rows[k]=new Set(a);});L.push({t,C:A.C,R,rows});}
console.log('10 kỳ gần: ngày | cỡ ≥2 | trúng ≥2 | trúng P15');
L.slice(-10).forEach(f=>{const nh=Object.keys(f.C).map(Number).filter(x=>f.C[x]>=2);console.log(DA[f.t],nh.length,nh.filter(x=>f.R.has(x)).length,[...(f.rows.p15||[])].filter(x=>f.R.has(x)).length);});
console.log('\n% ra theo số pool chứa số đó (20 | 50 | 100):');
for(const c of [0,1,2,3,4]){const o=[20,50,100].map(W=>{let a=0,b=0;L.slice(-W).forEach(f=>{for(let x=1;x<=NB;x++){const k=Math.min(4,f.C[x]||0);if(k===c){a++;b+=f.R.has(x);}}});return `${(a/W).toFixed(1)} số ${(b/a*100).toFixed(1)}%`;});console.log(c===4?'≥4':c,o.join(' | '));}
const PK=['v','t','h','k1','k2','tr','t2','kp','nd'];
console.log('\n% ra từng pool thành phần (20 | 50 | 100):');
for(const k of PK){console.log(k.padEnd(3),[20,50,100].map(W=>{let a=0,b=0;L.slice(-W).forEach(f=>{const s=f.rows[k];if(s)s.forEach(x=>{a++;b+=f.R.has(x);});});return (b/Math.max(1,a)*100).toFixed(1)+'%';}).join(' | '));}
