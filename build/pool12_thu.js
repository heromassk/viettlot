// Thử dựng pool 12 / 15 từ pool app + các pool (vắng, tổng, hiệu, ±1, trùng, cách 1 kỳ, kẹp) + luật loại (anh 21/10/2026)
// Cần thứ hạng app từng kỳ: GOIY_RKDUMP=<thư mục>/rk_<game>.json GOIY_RKW=200 python3 build/goiy.py <game> --app tl.json ; rồi: node build/pool12_thu.js <thư mục>
const fs=require('fs');globalThis.window={};const {poolAt}=(()=>{const src=require('fs').readFileSync(__dirname+'/bang.js','utf8')+';module.exports.poolAt=poolAt;';const m={exports:{}};new Function('module','exports','require','window',src)(m,m.exports,require,globalThis.window);return m.exports;})();
const AD=JSON.parse(fs.readFileSync('/home/user/viettlot/build/all_data.json','utf8'));const S=process.argv[2];
const FEAT=['v','t','h','k1','k2','tr','t2','kp','r5','r10h','v20'];
for(const [key,nb,g] of [['loto535',35,'loto'],['mega645',45,'mega'],['power655',55,'power']]){
 const D=AD[key],RA=D.res,DA=D.dates,J={res201:RA,dates201:DA,lk201:D.lk,nb,game:g,poolLog:{},poolThuc:{}};const RK=JSON.parse(fs.readFileSync(S+'/rk_'+g+'.json'));const kb=RA[0].length;
 const n=RA.length,T0=n-200;const F=[];   // F[t]: {feat:Set} for t in [T0,n)
 for(let t=T0;t<n;t++){const A=poolAt(J,'',t);const f={};A.rows.forEach(([k,,a])=>{if(FEAT.includes(k))f[k]=new Set(a||[]);});
  const c5={},c10={};for(let u=t-10;u<t;u++)RA[u].forEach(x=>{c10[x]=(c10[x]||0)+1;if(u>=t-5)c5[x]=(c5[x]||0)+1;});
  f.r5=new Set(Object.keys(c5).map(Number).filter(x=>c5[x]>=2));f.r10h=new Set(Object.keys(c10).map(Number).filter(x=>c10[x]>=3));
  const seen=new Set();for(let u=t-20;u<t;u++)RA[u].forEach(x=>seen.add(x));f.v20=new Set([...Array(nb).keys()].map(x=>x+1).filter(x=>!seen.has(x)));
  const rk=RK[DA[t]]||[];f.rk=rk;F.push(f);}
 const at=t=>F[t-T0];
 // rate tables from past L kỳ
 const rate=(t,L)=>{const r={};for(const k of FEAT){let s=0,h=0;for(let u=t-L;u<t;u++){const a=at(u)[k];s+=a.size;a.forEach(x=>{if(RA[u].includes(x))h++;});}r[k]=s?(h+1)/(s+nb/kb):kb/nb;}
   const rb=[0,0,0,0,0];const rs=[0,0,0,0,0];for(let u=t-L;u<t;u++){const rk=at(u).rk;for(let i=0;i<nb;i++){const x=i<rk.length?rk[i]:null;const b=i<5?0:i<10?1:i<15?2:i<20?3:4;if(x==null){continue;}rs[b]++;if(RA[u].includes(x))rb[b]++;}}
   r.rk=rb.map((h,b)=>(h+1)/(rs[b]+nb/kb));const base=kb/nb;
   // out-of-top20 rate
   let so=0,ho=0;for(let u=t-L;u<t;u++){const st=new Set(at(u).rk);for(let x=1;x<=nb;x++)if(!st.has(x)){so++;if(RA[u].includes(x))ho++;}}r.rk[4]=(ho+1)/(so+nb/kb);r.base=base;return r;};
 const pickApp=(t,K)=>at(t).rk.slice(0,K);
 const pickScore=(t,K,L,useApp,wApp)=>{const r=rate(t,L),f=at(t),pos={};f.rk.forEach((x,i)=>pos[x]=i);const sc=[];
   for(let x=1;x<=nb;x++){let s=0;for(const k of FEAT){if(f[k].has(x))s+=Math.log(r[k]/r.base);}
     if(useApp){const i=pos[x];const b=i==null?4:i<5?0:i<10?1:i<15?2:3;s+=wApp*Math.log(r.rk[b]/r.base);}sc.push([s,x]);}
   sc.sort((a,b)=>b[0]-a[0]||a[1]-b[1]);return sc.slice(0,K).map(z=>z[1]);};
 const evalM=(name,fn)=>{const out=[];for(const K of [12,15]){const row=[];for(const W of [20,50,100]){let h=0,g2=0,g3=0,g4=0;for(let t=n-W;t<n;t++){const p=fn(t,K);const x=p.filter(z=>RA[t].includes(z)).length;h+=x;g2+=x>=2;g3+=x>=3;g4+=x>=4;}row.push(`${W}: ${(h/W).toFixed(2)} ≥3 ${g3} ≥4 ${g4}`);}out.push(`P${K} `+row.join(' | '));}console.log(g,name.padEnd(14),out.join('  ||  '));};
 const cnt=(f,x)=>['v','t','h','k1','k2','tr','t2','kp'].reduce((a,k)=>a+(f[k].has(x)?1:0),0);
 evalM('app',pickApp);
 for(const b of [2,4,6])evalM('app+≥2pool b'+b,(t,K)=>{const f=at(t);return f.rk.map((x,i)=>[i-(cnt(f,x)>=2?b:0),x]).sort((a,c)=>a[0]-c[0]).slice(0,K).map(z=>z[1]);});
 for(const b of [1,2,3])evalM('app+đếm pool b'+b,(t,K)=>{const f=at(t);return f.rk.map((x,i)=>[i-b*cnt(f,x),x]).sort((a,c)=>a[0]-c[0]).slice(0,K).map(z=>z[1]);});
 for(const ex of ['r5','v20','tr','r10h'])evalM('app bỏ '+ex,(t,K)=>{const f=at(t);return f.rk.filter(x=>!f[ex].has(x)).slice(0,K);});
 evalM('app bỏ r5+v20',(t,K)=>{const f=at(t);return f.rk.filter(x=>!f.r5.has(x)&&!f.v20.has(x)).slice(0,K);});
 for(const k of ['v','t2','h','k2'])evalM('app ưu '+k,(t,K)=>{const f=at(t);return f.rk.map((x,i)=>[i-(f[k].has(x)?3:0),x]).sort((a,c)=>a[0]-c[0]).slice(0,K).map(z=>z[1]);});

}
