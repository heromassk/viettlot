// Lay tu app (index_loto.html): phieu tam linh 20 phuong phap, pool app, phuong phap tot nhat 50 ky. In JSON.
// node build/tamlinh.js power|mega|loto
const {chromium}=require(require.resolve('playwright',{paths:['/opt/node-tools/node_modules',process.cwd()]}));const path=require('path');
const gi={loto:0,mega:1,power:2}[process.argv[2]];
(async()=>{const b=await chromium.launch();const p=await (await b.newContext({viewport:{width:1100,height:900}})).newPage();
await p.goto('file://'+path.join(__dirname,'..','index_loto.html'));await p.waitForTimeout(3000);await p.click('#sgCard > summary');await p.click(`#gameTabs .gtab >> nth=${gi}`);await p.waitForTimeout(4000);
await p.evaluate(()=>{$('tqCard').open=true;renderTarot();});await p.waitForFunction(()=>S.kx&&S.kx.nv,null,{timeout:120000});
const r=await p.evaluate(()=>{const {out:O,N}=S.PS,ids=PM.map(q=>q[0]).filter(id=>O[id]&&O[id][N]),hk=(id,t,K)=>{const rk=rankH(id,t);return rk?rk.filter(x=>x<K).length:null;};
  const best={};for(const K of [12,15,18]){let bi=null,bv=-1;for(const id of ids){let h=0,n=0;for(let t=N-50;t<N;t++){const x=hk(id,t,K);if(x==null)continue;h+=x;n++;}if(n&&h/n>bv){bv=h/n;bi=id;}}best[K]={id:bi,tb:+bv.toFixed(2),pool:topK(O[bi][N],K).sort((a,b)=>a-b)};}
  return {next:S.M.nd,votes:S.kx.nv,methods:KX_M.map((m,i)=>[m[1],S.kx.now[i]?S.kx.now[i].nums:[]]),appPool:S.sg.pool.slice().sort((a,b)=>a-b),appMethod:S.sg.sel,appTickets:(S.sg.G.ranked||S.sg.G.tickets).map(t=>t.x),best50:best};});
console.log(JSON.stringify(r));await b.close();})();
