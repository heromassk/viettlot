const fs=require('fs');globalThis.window={};const {poolAt}=(()=>{const src=require('fs').readFileSync(__dirname+'/bang.js','utf8')+';module.exports.poolAt=poolAt;';const m={exports:{}};new Function('module','exports','require','window',src)(m,m.exports,require,globalThis.window);return m.exports;})();
const AD=JSON.parse(fs.readFileSync('/home/user/viettlot/build/all_data.json','utf8'));const K=['v','t','h','k1','k2','tr','t2','kp','nh'];
for(const [key,nb,g] of [['loto535',35,'loto'],['mega645',45,'mega'],['power655',55,'power']]){const D=AD[key],RA=D.res,J={res201:RA,dates201:D.dates,lk201:D.lk,nb,game:g,poolLog:{},poolThuc:{}};const n=RA.length;
 const st={};K.forEach(k=>st[k]={50:[0,0],100:[0,0],200:[0,0]});let all={50:[0,0],100:[0,0],200:[0,0]};
 for(let t=n-200;t<n;t++){const A=poolAt(J,'',t);const R=new Set(RA[t]);A.rows.forEach(([k,,a])=>{if(!K.includes(k)||!a)return;for(const W of [50,100,200])if(t>=n-W){st[k][W][0]+=a.length;st[k][W][1]+=a.filter(x=>R.has(x)).length;}});}
 console.log(g,'(%/số ở 50 / 100 / 200 kỳ)',K.map(k=>k+' '+[50,100,200].map(W=>(st[k][W][1]/st[k][W][0]*100).toFixed(1)).join('/')).join(' · '));}
