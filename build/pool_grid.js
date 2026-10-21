const fs=require('fs');globalThis.window={};const {poolAt}=(()=>{const src=require('fs').readFileSync(__dirname+'/bang.js','utf8')+';module.exports.poolAt=poolAt;';const m={exports:{}};new Function('module','exports','require','window',src)(m,m.exports,require,globalThis.window);return m.exports;})();const S=process.argv[2];
const AD=JSON.parse(fs.readFileSync('/home/user/viettlot/build/all_data.json','utf8'));const PK=['v','t','h','k1','k2','tr','t2','kp'];
for(const [key,nb,g] of [['loto535',35,'loto'],['mega645',45,'mega'],['power655',55,'power']]){
 const D=AD[key],RA=D.res,DA=D.dates;const RK=JSON.parse(fs.readFileSync(S+'/rk_'+g+'.json'));const TL=JSON.parse(fs.readFileSync(S+'/tl_'+g+'.json'));const TLH={};(TL.votesHist||[]).forEach(h=>TLH[h.d]=new Set(h.top));
 const J={res201:RA,dates201:DA,lk201:D.lk,nb,game:g,poolLog:{},poolThuc:{}};const n=RA.length;const F=[];
 for(let t=n-100;t<n;t++){const A=poolAt(J,'',t);const m={};A.rows.forEach(([k,,a])=>{if(PK.includes(k))m[k]=new Set(a||[]);});m.tl=TLH[DA[t]]||new Set();F.push({rk:RK[DA[t]]||[],m,C:A.C,R:new Set(RA[t])});}
 const ev=(fn,K)=>{const r=[];for(const W of [20,50,100]){let h=0,g3=0,g4=0;for(const f of F.slice(-W)){const p=fn(f,K);const x=p.filter(z=>f.R.has(z)).length;h+=x;g3+=x>=3;g4+=x>=4;}r.push([h/W,g3,g4]);}return r;};
 const fmt=r=>r.map(([a,b,c])=>`${a.toFixed(2)}·${b}·${c}`).join(' / ');
 const reorder=(sc)=>(f,K)=>f.rk.map((x,i)=>[i-sc(f,x),i,x]).sort((a,b)=>a[0]-b[0]||a[1]-b[1]).slice(0,K).map(z=>z[2]);
 const C=[];C.push(['app',(f,K)=>f.rk.slice(0,K)]);
 for(const X of [...PK,'tl'])for(const b of [2,4,6])C.push([`${X}+${b}`,reorder((f,x)=>f.m[X].has(x)?b:0)]);
 for(const [X,Y] of [['v','t'],['v','t2'],['t','t2'],['v','h'],['t2','kp'],['v','tl'],['t','tl'],['t2','tl']])for(const b of [2,4])C.push([`${X}&${Y}+${b}`,reorder((f,x)=>(f.m[X].has(x)?b:0)+(f.m[Y].has(x)?b:0))]);
 for(const b of [1,2,3])C.push([`đếm pool×${b}`,reorder((f,x)=>b*(f.C[x]||0))]);
 console.log('\n=== '+g+' (trúng TB·kỳ≥3·kỳ≥4 ở 20/50/100 kỳ)');
 for(const K of [9,12,15]){const res=C.map(([nm,fn])=>{const r=ev(fn,K);return [nm,r,r[1][0]+r[2][0]+ (r[1][1]+r[2][1])/50];});const app=res[0];res.sort((a,b)=>b[2]-a[2]);
  console.log(`P${K} app: ${fmt(app[1])}`);res.slice(0,5).forEach(([nm,r])=>console.log(`   ${nm.padEnd(14)} ${fmt(r)}`));}}
