// Tâm linh cho Max 3D / Pro: chạy các phương pháp tâm linh của app (KX_M) trên ngày quay Max 3D (18h), số trong khoảng 1..1000 (1000 = bộ 000).
// Category A/C/D (Lục Nhâm, Thái Ất, Huyền Không, Nhị thập bát tú, Hoàng đạo, Nạp âm, Thần số học, Tử vi, Xin xăm, Tarot, Mai Hoa, Kỳ Môn, Tứ trụ, Bát trạch)
// + Bóng âm dương, Lộn của 2 số ĐB kỳ trước (viết riêng cho 3 chữ số). Chấm từng phương pháp và theo số phiếu trên toàn lịch sử; in phiếu kỳ tới.
// node build/max3d_tl.js  → build/max3d_tl.json
const {chromium}=require(require.resolve('playwright',{paths:['/opt/node-tools/node_modules',process.cwd()]}));const path=require('path'),fs=require('fs');
const games={plus:JSON.parse(fs.readFileSync(path.join(__dirname,'max3d_data.json'))),pro:JSON.parse(fs.readFileSync(path.join(__dirname,'max3dpro_data.json')))};
const app=JSON.parse(fs.readFileSync(path.join(__dirname,'max3d_app.json')));
(async()=>{const b=await chromium.launch();const p=await (await b.newContext({viewport:{width:1100,height:900}})).newPage();
await p.goto('file://'+path.join(__dirname,'..','index_loto.html'));await p.waitForTimeout(3000);
await p.evaluate(()=>{$('toolsCard').open=true;$('tqCard').open=true;try{renderTarot();}catch(e){}});await p.waitForTimeout(1500);
const out={};
for(const k of ['plus','pro']){const G=games[k],nd=app[k].goiy.next;
  out[k]=await p.evaluate(({G,nd})=>{const N=1000,toV=s=>(+s)||1000,toS=v=>String(v%1000).padStart(3,'0');
    const P=kxPerson(),M=KX_M.filter(m=>m[2]!=='B');
    const B=[['bong3','Bóng âm dương 2 số ĐB kỳ trước',pv=>{const D=[5,6,7,8,9,0,1,2,3,4],A=[7,4,9,6,1,8,3,0,5,2],o=[];pv.slice(0,2).forEach(s=>{o.push(s.split('').map(c=>D[+c]).join(''),s.split('').map(c=>A[+c]).join(''));});return {why:'bóng dương, bóng âm của '+pv.slice(0,2).join(' '),nums:[...new Set(o.map(toV))]};}],
             ['lon3','Lộn 2 số ĐB kỳ trước',pv=>({why:'lộn '+pv.slice(0,2).join(' '),nums:[...new Set(pv.slice(0,2).map(s=>toV(s.split('').reverse().join(''))))]})]];
    const names=M.map(m=>m[1]).concat(B.map(x=>x[1])),nm=names.length;
    const run=(date,pv)=>{const c=kxCtx(date+' 18h'),o=M.map(m=>{try{return m[3](c,pv?pv.map(toV):null,{n:0},P,N);}catch(e){return null;}});B.forEach(x=>{o.push(pv?x[2](pv):null);});return o;};
    const segs=[[G.res.length-100,G.res.length],[G.res.length-200,G.res.length-100],[G.res.length-300,G.res.length-200],[1,G.res.length]];
    const acc=names.map(()=>segs.map(()=>({h:0,e:0}))),VL={};
    for(let t=1;t<G.res.length;t++){const o=run(G.dates[t],G.res[t-1]),R=G.res[t].map(toV),vt=new Int16Array(N+1);
      o.forEach((x,i)=>{if(!x||!x.nums||!x.nums.length)return;const S=new Set(x.nums.filter(v=>v>=1&&v<=N));S.forEach(v=>vt[v]++);const h=R.filter(v=>S.has(v)).length,e=20*S.size/N;segs.forEach((sg,j)=>{if(t>=sg[0]&&t<sg[1]){acc[i][j].h+=h;acc[i][j].e+=e;}});});
      const cnt={};for(let v=1;v<=N;v++){cnt[vt[v]]=(cnt[vt[v]]||0)+1;}const hit={};R.forEach(v=>{hit[vt[v]]=(hit[vt[v]]||0)+1;});
      for(const kk in cnt){const z=VL[kk]=VL[kk]||{n:0,h:0};z.n+=cnt[kk]*20/N;z.h+=hit[kk]||0;}}
    const now=run(nd,G.res[G.res.length-1]),vt=new Int16Array(N+1),src={};now.forEach((x,i)=>{if(!x||!x.nums)return;new Set(x.nums.filter(v=>v>=1&&v<=N)).forEach(v=>{vt[v]++;(src[v]=src[v]||[]).push(i);});});
    const ord=[...Array(N).keys()].map(i=>i+1).sort((a,b)=>vt[b]-vt[a]||a-b);
    return {names,acc:acc.map(a=>a.map(z=>z.e?+(z.h/z.e).toFixed(3):null)),VL,next:nd,
      methods:now.map((x,i)=>x?{name:names[i],why:(x.why||'').replace(/<[^>]+>/g,''),n:new Set(x.nums).size}:{name:names[i],why:'(không có)',n:0}),
      votes:ord.slice(0,300).map(v=>[toS(v),vt[v],src[v].map(i=>names[i])]),maxv:vt[ord[0]]};},{G,nd});}
fs.writeFileSync(path.join(__dirname,'max3d_tl.json'),JSON.stringify(out));
for(const k of ['plus','pro']){const o=out[k];console.log('\n##',k,'kỳ tới',o.next,'· phiếu cao nhất',o.maxv);
  console.log('| Phương pháp | 100 kỳ gần | giữa | xa | cả lịch sử |');o.names.forEach((n,i)=>console.log('|',n,'|',o.acc[i].map(x=>x==null?'—':'×'+x.toFixed(2)).join(' | '),'|'));
  console.log('Theo số phiếu (cả lịch sử):',Object.entries(o.VL).sort((a,b)=>a[0]-b[0]).map(([k2,z])=>`${k2} phiếu: ×${(z.h/z.n).toFixed(2)} (${z.h} lần)`).join(' · '));
  console.log('Top bộ:',o.votes.slice(0,12).map(([s,v])=>s+'('+v+')').join(' '));}
await b.close();})();
