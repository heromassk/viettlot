const fs=require('fs');globalThis.window={};const {poolAt}=require(process.argv[2]);
const PK=['v','t','h','k1','k2','tr','t2','kp','nd'];
for(const g of ['loto','mega','power']){const J=JSON.parse(fs.readFileSync('build/goiy_latest/'+g+'.json'));const RA=J.res201,DA=J.dates201,n=RA.length,NB=J.nb;const L=[];
 for(let t=n-100;t<n;t++){const A=poolAt(J,'',t);const rows={};A.rows.forEach(([k,,a])=>{if(a)rows[k]=new Set(a);});const RK=(J.rkHist||{})[DA[t]]||[];const TL=rows.tl||new Set();
  const X=[];for(let x=1;x<=NB;x++){const c=PK.reduce((z,k)=>z+(rows[k]&&rows[k].has(x)?1:0),0);if(c<2)continue;
   let gap=0;for(let u=t-1;u>=0&&!RA[u].includes(x);u--)gap++;let c10=0;for(let u=t-10;u<t;u++)if(RA[u].includes(x))c10++;const ri=RK.indexOf(x);
   const F={'đếm':c>=4?'≥4':String(c),'hạng app':ri<0?'ngoài 20':ri<10?'1–10':'11–20','tâm linh':TL.has(x)?'có':'không','vắng':gap===0?'0 (ra kỳ trước)':gap<=2?'1–2':gap<=5?'3–5':gap<=9?'6–9':'≥10','ra 10 kỳ':c10>=3?'≥3':String(c10)};
   PK.forEach(k=>F['có '+k]=rows[k]&&rows[k].has(x)?'có':'không');X.push({x,F,hit:RA[t].includes(x)});}
  L.push(X);}
 const base=[20,50,100].map(W=>{let a=0,b=0;L.slice(-W).forEach(X=>X.forEach(o=>{a++;b+=o.hit;}));return b/a*100;});
 const k34=W=>{let g3=0,g4=0;L.slice(-W).forEach(X=>{const h=X.filter(o=>o.hit).length;g3+=h>=3;g4+=h>=4;});return g3+'/'+g4;};
 console.log(`\n=== ${g} ≥2 pool: % mỗi số ${base.map(z=>z.toFixed(1)).join('/')} · kỳ ≥3/≥4: ${[20,50,100].map(k34).join(' | ')}`);
const RS={loto:[['vắng 3–5',o=>o.F['vắng']==='3–5'],['có tổng',o=>o.F['có t']==='có'],['đếm ≥4',o=>o.F['đếm']==='≥4'],['vắng 3–5 + tổng',o=>o.F['vắng']==='3–5'||o.F['có t']==='có'],['vắng 3–5 + tổng + ≥4',o=>o.F['vắng']==='3–5'||o.F['có t']==='có'||o.F['đếm']==='≥4']],
 mega:[['ngoài top 20 app',o=>o.F['hạng app']==='ngoài 20'],['ra kỳ trước',o=>o.F['có tr']==='có'],['ra 10 kỳ ≥3',o=>o.F['ra 10 kỳ']==='≥3'],['ra kỳ trước + ra 10 kỳ ≥3',o=>o.F['có tr']==='có'||o.F['ra 10 kỳ']==='≥3'],['ngoài top 20 + ra kỳ trước',o=>o.F['hạng app']==='ngoài 20'||o.F['có tr']==='có']],
 power:[['ngoài top 20 app',o=>o.F['hạng app']==='ngoài 20'],['ra kỳ trước',o=>o.F['có tr']==='có'],['ra 10 kỳ ≥3',o=>o.F['ra 10 kỳ']==='≥3']]}[g];
 const ev=fn=>[20,50,100].map(W=>{let sz=0,h=0,g3=0,g4=0;L.slice(-W).forEach(X=>{const Y=X.filter(o=>!fn(o));const k=Y.filter(o=>o.hit).length;sz+=Y.length;h+=k;g3+=k>=3;g4+=k>=4;});return `${(sz/W).toFixed(1)}·${(h/W).toFixed(2)}·${(h/sz*100).toFixed(1)}%·${g3}/${g4}`;});
 console.log('  cỡ·trúng/kỳ·%·kỳ≥3/≥4 (20 | 50 | 100)');console.log('  giữ nguyên'.padEnd(32),ev(()=>false).join(' | '));
 for(const [nm,fn] of RS)console.log(('  loại '+nm).padEnd(32),ev(fn).join(' | '));}

