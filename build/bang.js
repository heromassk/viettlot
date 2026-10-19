// Bảng gợi ý trực quan — dùng chung cho app (thẻ đầu trang) và ảnh gửi trong chat.
// renderBang(J) -> HTML. J = dữ liệu từ `goiy.py --json`.
// 20 kỳ gần: pool (chạy lại từng kỳ, chỉ dùng dữ liệu trước kỳ đó) trúng bao nhiêu số. Chọn cỡ pool → tính lại.
// Số liền nhau trong 1 dãy (vd 05 06): khoanh chung bằng viền chấm trắng (anh 15/10/2026). nums: dãy số, rb: n -> HTML quả bóng
function ltWrap(nums,rb){const s=[...nums].sort((a,b)=>a-b),out=[];let i=0;
  const st=new Set(s),lon=n=>(n%10)*10+Math.floor(n/10);   // cặp lộn trong cùng dãy (01–10, 12–21…): vuông nét đứt (anh 15/10/2026)
  const kb=n=>n%11===0&&n>0?`<span class="bg-kep">${rb(n)}</span>`:(lon(n)!==n&&st.has(lon(n))?`<span class="bg-lon">${rb(n)}</span>`:rb(n));   // số kép: khoanh vuông nhẹ
  while(i<s.length){let j=i;while(j+1<s.length&&s[j+1]===s[j]+1)j++;const g=s.slice(i,j+1).map(kb).join('');out.push(j>i?`<span class="bg-lt">${g}</span>`:g);i=j+1;}
  return out.join('');}
const H20K=[10,12,15,18,20];
function hist20HTML(J,K){
  // Pool THẬT của từng kỳ (pool_app.py, anh 15/10/2026); thiếu thì dùng pool thô cũ
  const PH=J.poolThuc&&J.poolThuc.hist,H=PH?PH.map(h=>({d:h.d,r:h.r,lk:h.lk,rk:h.pools[K]||h.pools[String(K)]||[]})):(J.hist20||[]);if(!H.length)return '';
  const p2=n=>String(n).padStart(2,'0'),MMH=new Map((J.mmHist||[]).map(m=>[m.d,m]));
  const rows=H.map(h=>{const pool=h.rk.slice(0,K),pos=new Map(pool.map((n,i)=>[n,i])),res=new Set(h.r),mg=MMH.get(h.d);
    const cls=n=>{const i=pos.get(n);return i==null?'':(i<10?'t10':i<15?'t15':'t20')+' hit';};
    const hit=h.r.filter(n=>pos.has(n)).length;
    return {hit,html:`<details class="bg-h20r"><summary><span class="bg-h20d">${h.d}</span>${ltWrap(h.r,n=>`<span class="bg-b ${cls(n)||'miss'}">${p2(n)}</span>`)}${h.lk?`<span class="bg-b mm">${p2(h.lk)}</span>`:''}${mg?`<small class="bg-mmg" style="margin-left:6px;">MM gợi ý ${mg.goi.map(p2).join(' ')} ${mg.dung?'<b class="bg-ok">✔</b>':'✘'}</small>`:''}<span class="bg-h20n${hit>=4?' g4':hit>=3?' g3':''}">trúng ${hit}${hit>=4?' ★':''}</span></summary>
      <div class="bg-row bg-h20p"><small>Pool ${K} kỳ này:</small>${pool.map(n=>`<span class="bg-b ${res.has(n)?cls(n):(pos.get(n)<10?'t10':pos.get(n)<15?'t15':'t20')+' dim'}">${p2(n)}</span>`).join('')}</div></details>`};});
  const n=rows.length,tb=rows.reduce((a,r)=>a+r.hit,0)/n,g=j=>rows.filter(r=>r.hit>=j).length;
  return `<div class="bg-row bg-chips">${H20K.map(k=>`<span class="bg-h20k${k===K?' on':''}" onclick="h20Set(${k})">Pool ${k}</span>`).join('')}</div>
  <div class="bg-h20s">Pool ${K}: TB <b>${tb.toFixed(1)}</b> số/kỳ · ≥2 số <b>${g(2)}/${n}</b> · ≥3 số <b>${g(3)}/${n}</b> · ≥4 số <b>${g(4)}/${n}</b> kỳ</div>
  ${rows.map(r=>r.html).join('')}
  <div class="bg-foot">Số khoanh màu = nằm trong pool và trùng kết quả (vàng đậm: top 10 · viền: 11–15 · nét đứt: 16–20). Bấm 1 kỳ để xem pool kỳ đó. ${PH?'Pool đúng như app đang chọn (bộ cộng điểm từng cỡ, luật hàng, giới hạn kép), mỗi kỳ chỉ dùng dữ liệu trước nó.':'Pool tín hiệu thô, chưa cộng điểm từng cỡ.'}${J.mmHist&&J.mmHist.length?' MM gợi ý = 3 số may mắn app gợi ý cho kỳ đó, ✔ = có số trúng.':''}</div>`;}
function h20Set(k){if(typeof window==='undefined')return;window.__h20K=k;const el=document.getElementById('h20');if(el&&window.__h20J)el.innerHTML=hist20HTML(window.__h20J,k);}
const POOLK=[10,12,15,18,20,25,30,35];
function k10Set(n){if(typeof window==='undefined')return;window.__k10N=n;window.__k10Open=true;rgOff('k');if(typeof renderBangCard==='function')renderBangCard();}
// Chọn kỳ theo khoảng ngày (anh 19/10/2026): blk 'k' = bảng x kỳ gần nhất, 'p' = pool. Loto chọn được 13h/21h ở đầu và cuối khoảng.
function rgKeep(blk){if(blk==='k')window.__k10Open=true;if(blk==='q')window.__qhOpen=true;}   // đang dùng bảng thì giữ mở sau khi tính lại
function k10Tog(el){if(typeof window!=='undefined')window.__k10Open=el.open;}
function qhTog(el){if(typeof window!=='undefined')window.__qhOpen=el.open;}
function qhSet(n){if(typeof window==='undefined')return;window.__qhN=n;window.__qhOpen=true;rgOff('q');rgRe();}
function qhGio(g){if(typeof window==='undefined')return;window.__qhG=g;window.__qhOpen=true;rgRe();}
function rgGet(blk){if(typeof window==='undefined')return null;const r=(window.__rg||{})[blk];return r&&r.on?r:null;}
function rgRe(){if(typeof renderBangCard==='function')renderBangCard();}
function rgTog(blk){if(typeof window==='undefined')return;rgKeep(blk);window.__rg=window.__rg||{};const r=window.__rg[blk]||{};r.on=!r.on;window.__rg[blk]=r;rgRe();}
function rgSet(blk,k,v){if(typeof window==='undefined')return;rgKeep(blk);window.__rg=window.__rg||{};const r=window.__rg[blk]||{on:true};r[k]=v;window.__rg[blk]=r;rgRe();}
function rgOff(blk){if(typeof window!=='undefined'&&window.__rg&&window.__rg[blk])window.__rg[blk].on=false;}
function rgKey(s){const m=String(s).match(/(\d+)\/(\d+)\/(\d+)(?:\s*(\d+)h)?/);return m?(+m[3])*1e6+(+m[2])*1e4+(+m[1])*100+(m[4]?+m[4]:50):0;}
function rgIso(s){const m=String(s).match(/(\d+)\/(\d+)\/(\d+)/);return m?`${m[3]}-${m[2].padStart(2,'0')}-${m[1].padStart(2,'0')}`:'';}
function rgIsoKey(iso,h,def){const m=String(iso||'').match(/(\d+)-(\d+)-(\d+)/);if(!m)return null;return (+m[1])*1e6+(+m[2])*1e4+(+m[3])*100+(h==='13h'?13:h==='21h'?21:def);}
// chỉ số các kỳ trong res201: theo khoảng ngày nếu đang bật, không thì n kỳ gần nhất; gio = '' | '13h' | '21h' (Loto)
function rgPick(J,blk,n,gio){const DA=J.dates201||[],ok=i=>!gio||String(DA[i]).endsWith(gio),r=rgGet(blk),out=[];
  if(r){const lo=J.game==='loto',f=rgDef(J,blk,n,gio),a=rgIsoKey(r.f||f.f,lo?(r.fh||f.fh):'',0),b=rgIsoKey(r.t||f.t,lo?(r.th||f.th):'',99);
    for(let i=0;i<DA.length;i++){const k=rgKey(DA[i]);if(k>=a&&k<=b&&ok(i))out.push(i);}return out;}
  for(let i=DA.length-1;i>=0&&out.length<n;i--)if(ok(i))out.unshift(i);return out;}
// mặc định khi mới bật: đến = kỳ mới nhất, từ = kỳ đầu của n kỳ đang xem
function rgDef(J,blk,n,gio){const DA=J.dates201||[];const ix=[];for(let i=DA.length-1;i>=0&&ix.length<n;i--)if(!gio||String(DA[i]).endsWith(gio))ix.unshift(i);
  const a=DA[ix.length?ix[0]:0]||'',b=DA[DA.length-1]||'';return {f:rgIso(a),fh:/21h/.test(a)?'21h':'13h',t:rgIso(b),th:/13h/.test(b)?'13h':'21h'};}
function rgUI(J,blk,n,gio){const r=rgGet(blk),lo=J.game==='loto',DA=J.dates201||[];
  const chip=`<span class="bg-h20k${r?' on':''}" onclick="rgTog('${blk}')">Chọn ngày</span>`;if(!r)return chip;
  const f=rgDef(J,blk,n,gio),mn=rgIso(DA[0]),mx=rgIso(DA[DA.length-1]),st='background:var(--panel2,#212a40);color:var(--text,#e8ecf5);border:1px solid var(--border,#2c3550);border-radius:8px;padding:3px 4px;font-size:.8rem;';
  const d=(k,v)=>`<input type="date" style="${st}" min="${mn}" max="${mx}" value="${v}" onchange="rgSet('${blk}','${k}',this.value)">`;
  const h=(k,v)=>lo?`<select style="${st}" onchange="rgSet('${blk}','${k}',this.value)">${['13h','21h'].map(x=>`<option${x===v?' selected':''}>${x}</option>`).join('')}</select>`:'';
  return `${chip}<span style="display:inline-flex;flex-wrap:wrap;gap:4px;align-items:center;font-size:.8rem;">Từ ${h('fh',r.fh||f.fh)}${d('f',r.f||f.f)} đến ${h('th',r.th||f.th)}${d('t',r.t||f.t)}</span>`;}
function rgLabel(J,ix){const DA=J.dates201||[];if(!ix.length)return 'không có kỳ nào';const s=d=>{const m=String(d).match(/(\d+\/\d+)\/\d+(?:\s*(\d+h))?/);return m?(m[2]?m[2]+' ':'')+m[1]:d;};return `từ ${s(DA[ix[0]])} đến ${s(DA[ix[ix.length-1]])}`;}
function ppGio(g){if(typeof window==='undefined')return;window.__ppH=g;rgRe();}   // Loto: pool chỉ lấy kỳ 13h / 21h / cả 2 (anh 19/10/2026)
// Kiểm pool vắng x kỳ (anh 19/10/2026): mỗi kỳ trong 10 kỳ gần, pool = số không ra trong x kỳ liền trước kỳ đó → cỡ pool, số trúng.
function vxSet(g,v){if(typeof window==='undefined')return;const x=parseInt(v,10);window.__vxX=window.__vxX||{};if(x>=1&&x<=50)window.__vxX[g]=x;window.__vxOpen=true;rgRe();}
function vxGio(v){if(typeof window==='undefined')return;window.__vxG=v;window.__vxOpen=true;rgRe();}
function vxN(n){if(typeof window==='undefined')return;window.__vxN=n;window.__vxOpen=true;rgRe();}   // số kỳ hiện: 10 / 20 / 50
function vxTog(el){if(typeof window!=='undefined')window.__vxOpen=el.open;}
function vxBlock(J){const RA=J.res201||[],DA=J.dates201||[],NB=J.nb,g=J.game,p2=n=>String(n).padStart(2,'0');if(RA.length<12)return '';
  const def={loto:8,mega:8,power:12}[g]||8,X=(typeof window!=='undefined'&&window.__vxX&&window.__vxX[g])||def,open=typeof window!=='undefined'&&window.__vxOpen;
  const NK=typeof window!=='undefined'&&[10,20,50].includes(window.__vxN)?window.__vxN:20;
  const lo=g==='loto',G=lo&&typeof window!=='undefined'&&['13h','21h'].includes(window.__vxG)?window.__vxG:'',okG=i=>!G||String(DA[i]).endsWith(G);
  // Loto chọn giờ: pool = x kỳ CÙNG GIỜ liền trước, bảng = 10 kỳ giờ đó
  const vang=t=>{const seen=new Set();let c=0;for(let i=t-1;i>=0&&c<X;i--){if(!okG(i))continue;RA[i].forEach(n=>seen.add(n));c++;}if(c<X)return null;const v=[];for(let n=1;n<=NB;n++)if(!seen.has(n))v.push(n);return v;};
  // đánh dấu số trong pool kề ±1 với số của kỳ trước (anh 19/10/2026); lọc giờ thì "kỳ trước" = kỳ cùng giờ liền trước
  // anh 19/10/2026: vòng đỏ = số kỳ trước −1 · vòng xanh lá = số kỳ trước +1 · vòng xanh dương = kề cả hai phía
  const keOf=t=>{for(let i=t-1;i>=0;i--)if(okG(i)){const P=new Set(RA[i]),k=new Map();for(let n=1;n<=NB;n++){if(P.has(n))continue;const up=P.has(n-1),dn=P.has(n+1);if(up||dn)k.set(n,up&&dn?'b':up?'p':'m');}return k;}return new Map();};
  const TV='border:1.5px solid #f0b429;border-radius:50%;padding:0 3px;';   // trùng kỳ trước: khoanh tròn nét liền vàng (anh 19/10/2026)
  const KC={m:'#ff4d4f',p:'#3fb950',b:'#4aa3ff'},KS=c=>`border:1.5px dashed ${c};border-radius:5px;padding:0 2px;`;
  const fmtV=(v,h,K)=>v.map(n=>{const st=(h.includes(n)?'color:var(--ac);font-weight:700;':'')+(K.has(n)?KS(KC[K.get(n)]):'');return st?`<span style="${st}">${p2(n)}</span>`:p2(n);}).join(' ');
  const rows=[];let sz=0,ht=0,ks=0,kh=0;const ge=[0,0,0,0];
  for(let t=RA.length-1;t>=0&&rows.length<NK;t--){if(!okG(t))continue;const v0=vang(t);if(!v0)break;const v=v0,h=RA[t].filter(n=>v.includes(n)).sort((a,b)=>a-b),K=keOf(t),vk=v.filter(n=>K.has(n));ks+=vk.length;kh+=vk.filter(n=>h.includes(n)).length;sz+=v.length;ht+=h.length;for(let k=1;k<=3;k++)if(h.length>=k)ge[k]++;
    rows.push(`<tr><td class="l" style="white-space:nowrap">${String(DA[t]).replace(/\/\d{4}/,'')}</td><td class="l" style="white-space:nowrap">${(()=>{let pi=t-1;while(pi>=0&&!okG(pi))pi--;const PV=new Set(pi>=0?RA[pi]:[]);return [...RA[t]].sort((a,b)=>a-b).map(n=>PV.has(n)?`<span style="${TV}">${p2(n)}</span>`:p2(n)).join(' ');})()}${lo&&(J.lk201||[])[t]!=null?` <b style="color:#ff9f43">${p2(J.lk201[t])}</b>${mmDelta(J,t,G)}`:''}</td><td>${v.length}</td><td><b>${h.length}</b></td></tr><tr><td></td><td class="l" colspan="3" style="white-space:normal;line-height:1.5;padding-top:0;color:var(--muted,#8b93a7);">${fmtV(v,h,K)}</td></tr>`);}
  const n=rows.length;if(!n)return '';const nxt=String(J.next||''),nxG=!G||nxt.endsWith(G),nx=vang(RA.length)||[],pc=k=>`${ge[k]}/${n}`;
  return `<details class="bg-wh" style="margin:6px 0;"${open?' open':''} ontoggle="vxTog(this)"><summary><b>Kiểm pool vắng x kỳ</b> <small>— 10 / 20 / 50 kỳ gần, pool = số không ra trong x kỳ liền trước mỗi kỳ</small></summary>
   <div class="bg-row" style="margin:6px 0;"><small>x =</small><input type="number" min="1" max="50" inputmode="numeric" value="${X}" onchange="vxSet('${g}',this.value)" style="width:64px;background:var(--panel2,#212a40);color:var(--text,#e8ecf5);border:1px solid var(--border,#2c3550);border-radius:8px;padding:4px 6px;font-size:.9rem;"><small>kỳ (gõ số rồi bấm ra ngoài / Enter)</small></div><div class="bg-row bg-chips"><small>Xem:</small>${[10,20,50].map(k=>`<span class="bg-h20k${k===NK?' on':''}" onclick="vxN(${k})">${k} kỳ</span>`).join('')}</div>${lo?`<div class="bg-row bg-chips">${[['','13h &amp; 21h'],['13h','Chỉ 13h'],['21h','Chỉ 21h']].map(([v,t])=>`<span class="bg-h20k${v===G?' on':''}" onclick="vxGio('${v}')">${t}</span>`).join('')}</div>`:''}
   <div style="overflow-x:auto;"><table class="bg-g10" style="font-size:.72rem;"><thead><tr><th>Kỳ</th><th>Kết quả</th><th>Cỡ pool</th><th>Trúng</th></tr></thead><tbody>${rows.join('')}</tbody></table></div>
   <div class="bg-foot" style="margin:4px 0 0;">${lo?'<b style="color:#ff9f43">Số cam</b> = số may mắn (không tính vào pool). ':''}Dòng nhỏ dưới mỗi kỳ = pool vắng ${X} kỳ${G?' '+G:''} trước kỳ đó, <b style="color:var(--ac)">số tô màu</b> = số trúng, <span style="${TV}">vòng tròn vàng</span> (cột kết quả) = trùng số kỳ${G?' '+G:''} trước; khung trong pool = kề số kỳ${G?' '+G:''} trước: <span style="${KS(KC.m)}">−1</span> <span style="${KS(KC.p)}">+1</span> <span style="${KS(KC.b)}">±1</span>.<br>${n} kỳ: pool TB <b>${(sz/n).toFixed(1)}</b> số · trúng TB <b>${(ht/n).toFixed(1)}</b> số/kỳ · ≥1 số <b>${pc(1)}</b> · ≥2 số <b>${pc(2)}</b> · ≥3 số <b>${pc(3)}</b> kỳ.<br>Số có khung (vắng + kề ±1): TB <b>${(ks/n).toFixed(1)}</b> số/kỳ, trúng <b>${kh}/${ks}</b>${ks?` (${Math.round(kh/ks*100)}% mỗi số; cả pool ${sz?Math.round(ht/sz*100):0}%)`:''}.</div>
   <div class="bg-foot" style="margin:2px 0 0;">Pool vắng ${X} kỳ${G?' '+G:''} cho ${nxG?'kỳ '+nxt:'kỳ '+G+' tới'}: <b>${nx.length} số</b> — ${nx.length?fmtV(nx,[],keOf(RA.length)):'—'}</div></details>`;}
// Số may mắn Loto: chênh so với MM kỳ liền trước (anh 19/10/2026) — nhỏ ở góc dưới bên phải: −3 đỏ, +1 xanh lá, 0 xám
function mmDelta(J,i,gio){const L=J.lk201||[],DA=J.dates201||[];let j=i-1;if(gio)while(j>=0&&!String(DA[j]).endsWith(gio))j--;   // lọc giờ: so với kỳ cùng giờ trước
  if(i<1||j<0||L[i]==null||L[j]==null)return '';const d=L[i]-L[j];return `<sub style="font-size:.6rem;font-weight:700;margin-left:1px;color:${d<0?'#ff4d4f':d>0?'#3fb950':'#8b93a7'};">${d>0?'+':d<0?'−':''}${Math.abs(d)}</sub>`;}
// tô màu số lặp (≥2 lần) cho một danh sách dòng (cũ → mới) — dùng chung bảng x kỳ và bảng Quan hệ trong kỳ
function lapMau(ROWS){const C10={};ROWS.forEach(r=>r.forEach(n=>C10[n]=(C10[n]||0)+1));
  const LAP=Object.keys(C10).map(Number).filter(n=>C10[n]>=2).sort((x,y)=>x-y),MAU={},CHU={};
  // 17/10/2026 (anh: "thiếu màu, màu trùng lại còn cạnh nhau"): mỗi số lặp một màu RIÊNG sinh theo góc vàng — số liền nhau lệch ~137° màu,
  // xen 3 độ sáng; bỏ vùng cam (màu số may mắn). Không lặp màu dù nhiều số.
  { // bảng màu N màu riêng (không xám, bỏ vùng cam); rồi gán màu sao cho số đứng cạnh nhau trong cùng dòng có màu khác xa nhất
    const N=LAP.length,pal=[...Array(N).keys()].map(i=>{let h=(i*137.508)%312;if(h>=6)h+=48;let L=[48,66,34][i%3];const S=i%2?90:76;if((h<6||h>335)&&L>50)L=40;return {h,S,L};});
    const rgb=c=>{const s=c.S/100,l=c.L/100,k=n=>(n+c.h/30)%12,a=s*Math.min(l,1-l),f=n=>l-a*Math.max(-1,Math.min(k(n)-3,9-k(n),1));return [f(0)*255,f(8)*255,f(4)*255];};
    pal.forEach(c=>c.rgb=rgb(c));const chuOf=c=>{const l=c.rgb.map(v=>{v/=255;return v<=.03928?v/12.92:((v+.055)/1.055)**2.4;});return .2126*l[0]+.7152*l[1]+.0722*l[2]>.179?'#111':'#fff';};const dist=(p,q)=>{const x=p.rgb,y=q.rgb,r=(x[0]+y[0])/2;return Math.sqrt((2+r/256)*(x[0]-y[0])**2+4*(x[1]-y[1])**2+(2+(255-r)/256)*(x[2]-y[2])**2);};
    const nb={};LAP.forEach(n=>nb[n]=new Set());
    const link=(a,c)=>{if(a!==c&&nb[a]&&nb[c]){nb[a].add(c);nb[c].add(a);}},RS=ROWS.map(r=>[...r].sort((x,y)=>x-y));
    RS.forEach((s,k)=>{for(let i=0;i<s.length;i++){for(let j=i+1;j<=i+2&&j<s.length;j++)link(s[i],s[j]);   // cùng dòng: liền kề và cách 1 ô
      const t=RS[k+1];if(t)for(let j=i-1;j<=i+1;j++)if(j>=0&&j<t.length)link(s[i],t[j]);}});   // dòng trên – dưới: cùng cột và chéo 1 ô (anh 17/10/2026)
    const used=new Set(),ord=[...LAP].sort((x,y)=>nb[y].size-nb[x].size||x-y);
    ord.forEach(n=>{let best=-1,bv=-1;pal.forEach((c,i)=>{if(used.has(i))return;const ds=[...nb[n]].filter(m=>MAU[m]).map(m=>dist(c,pal[MAU[m].i]));const v=ds.length?Math.min(...ds):999;if(v>bv){bv=v;best=i;}});
      used.add(best);const c=pal[best];MAU[n]={i:best,css:`hsl(${c.h.toFixed(1)} ${c.S}% ${c.L}%)`};CHU[n]=chuOf(c);});
    // tinh chỉnh: đổi chéo màu giữa 2 số nếu làm các cặp kề (ngang, trên–dưới) bớt giống nhau (phạt khi khoảng cách màu < 220)
    const pen=(n,ci)=>[...nb[n]].reduce((s,m)=>s+Math.max(0,240-dist(pal[ci],pal[MAU[m].i]))**2,0);
    for(let pass=0;pass<10;pass++){let better=false;
      for(let x=0;x<LAP.length;x++)for(let y=x+1;y<LAP.length;y++){const u=LAP[x],v=LAP[y],cu=MAU[u].i,cv=MAU[v].i;
        const before=pen(u,cu)+pen(v,cv);MAU[u].i=cv;MAU[v].i=cu;const after=pen(u,cv)+pen(v,cu);
        if(after+1e-6<before)better=true;else{MAU[u].i=cu;MAU[v].i=cv;}}
      if(!better)break;}
    LAP.forEach(n=>{const c=pal[MAU[n].i];MAU[n]=`hsl(${c.h.toFixed(1)} ${c.S}% ${c.L}%)`;CHU[n]=chuOf(c);});}
  return {MAU,CHU};}
// Bảng "Quan hệ trong kỳ" (anh 19/10/2026): như bảng x kỳ gần nhất nhưng không khoanh kép / liên tiếp / ±1; thay bằng
// cặp kẹp (a, a+2 thiếu a+1: gạch chân tím) · số kẹp về trong 2 kỳ sau (vòng tím) · tổng a+b=c (Σ trên phải) · nhân đôi 2a=b (×2 dưới phải).
// Lọc 13h / 21h: "2 kỳ sau" = 2 kỳ cùng giờ tiếp theo.
function qhBlock(J,ball,p2,HCOL){const RA=J.res201||[],DA=J.dates201||[],L=J.lk201||[],lo=J.game==='loto';if(RA.length<5)return '';
  const W=typeof window!=='undefined'?window:{},N0=[5,10,15,20,25,30,50].includes(W.__qhN)?W.__qhN:20,G=lo&&['13h','21h'].includes(W.__qhG)?W.__qhG:'',okG=i=>!G||String(DA[i]).endsWith(G);
  const QR=rgGet('q'),IX=rgPick(J,'q',N0,G),N=IX.length;if(!N)return '';
  const prevI=(i,n)=>{let j=i;for(let c=0;c<n;c++){j--;while(j>=0&&!okG(j))j--;if(j<0)return -1;}return j;};
  const kep=S=>{const s=new Set(S),o=[];s.forEach(a=>{if(s.has(a+2)&&!s.has(a+1))o.push(a+1);});return o.sort((x,y)=>x-y);};
  const {MAU,CHU}=lapMau(IX.map(i=>RA[i]));
  const rows=[];let nS=0,nD=0,nK=0,kv=0,kt=0;
  IX.forEach(i=>{const r=[...RA[i]].sort((a,b)=>a-b),S=new Set(r);
    const sums=[],dbl=[],SUMC=new Set(),DBLC=new Set();
    for(let x=0;x<r.length;x++)for(let y=x+1;y<r.length;y++){const c=r[x]+r[y];if(S.has(c)){sums.push(`${p2(r[x])}+${p2(r[y])}=${p2(c)}`);SUMC.add(c);}}
    r.forEach(a=>{if(S.has(2*a)){dbl.push(`${p2(a)}×2=${p2(2*a)}`);DBLC.add(2*a);}});
    const kp=kep(r),KS=new Set();kp.forEach(m=>{KS.add(m-1);KS.add(m+1);});
    const p1=prevI(i,1),p2i=prevI(i,2),VE=new Set([...(p1>=0?kep(RA[p1]):[]),...(p2i>=0?kep(RA[p2i]):[])].filter(n=>S.has(n)));
    if(sums.length)nS++;if(dbl.length)nD++;if(kp.length)nK++;
    rows.push({i,r,sums,dbl,kp,KS,VE,SUMC,DBLC});});
  // số kẹp về trong 2 kỳ: chấm các kỳ có kẹp mà đã có đủ 2 kỳ sau
  const nextI=(i,n)=>{let j=i,c=0;while(c<n){j++;while(j<RA.length&&!okG(j))j++;if(j>=RA.length)return -1;c++;}return j;};
  const wait=[];rows.forEach(o=>{o.kp.forEach(m=>{const a=nextI(o.i,1),b=nextI(o.i,2);if(b>=0){kt++;if(RA[a].includes(m)||RA[b].includes(m))kv++;}else if(!(a>=0&&RA[a].includes(m)))wait.push(`${p2(m)} (kẹp ${String(DA[o.i]).replace(/\/\d{4}/,'')}, còn ${a>=0?1:2} kỳ)`);});});
  const qb=(n,o)=>{let cls='';if(o.KS.has(n))cls+=' qk';if(o.VE.has(n))cls+=' qv';if(o.SUMC.has(n))cls+=' qs';if(o.DBLC.has(n))cls+=' qd';
    return MAU[n]?`<span class="bg-b${cls}" style="background:${MAU[n]};border-color:${MAU[n]};color:${CHU[n]};">${p2(n)}</span>`:ball(n,cls.trim());};
  const body=rows.slice().reverse().map(o=>{const a=o.r,c=a.filter(n=>n%2===0).length,i=o.i;
    const tags=[o.kp.length?`<span style="color:#c58bff">kẹp ${o.kp.map(p2).join(' ')}</span>`:'',o.VE.size?`<span style="color:#c58bff">về ${[...o.VE].map(p2).join(' ')}</span>`:'',...o.sums.map(x=>`<span style="color:#ffb347">${x}</span>`),...o.dbl.map(x=>`<span style="color:#4dd0c8">${x}</span>`)].filter(Boolean);
    return `<div class="bg-row bg-pool bg-k10"><small class="bg-k10d">${String(DA[i]).replace(/\/\d{4}/,'')}</small>${a.map(n=>qb(n,o)).join('')}${lo&&L[i]!=null?ball(L[i],'mm')+mmDelta(J,i,G):''}<small class="bg-k10i">${a.map(n=>{const h=Math.floor(n/10);return `<i style="color:${HCOL[h%HCOL.length]};">${h}</i>`;}).join('-')} <b>${a.reduce((x,y)=>x+y,0)}</b> ${c}C:${a.length-c}L</small></div>${tags.length?`<div class="bg-foot" style="margin:-2px 0 4px 44px;font-size:.68rem;">${tags.join(' · ')}</div>`:''}`;}).join('');
  const open=W.__qhOpen;
  return `<details class="bg-wh" style="margin:6px 0;"${open?' open':''} ontoggle="qhTog(this)"><summary><b>Quan hệ trong kỳ</b> <small>— cặp kẹp, số kẹp về trong 2 kỳ, tổng, nhân đôi</small></summary>
   <div class="bg-row bg-chips">${[5,10,15,20,25,30,50].map(n=>`<span class="bg-h20k${!QR&&n===N0?' on':''}" onclick="qhSet(${n})">${n} kỳ</span>`).join('')}</div>
   <div class="bg-row bg-chips">${rgUI(J,'q',N0,G)}</div>
   ${lo?`<div class="bg-row bg-chips">${[['','13h &amp; 21h'],['13h','Chỉ 13h'],['21h','Chỉ 21h']].map(([g,t])=>`<span class="bg-h20k${g===G?' on':''}" onclick="qhGio('${g}')">${t}</span>`).join('')}</div>`:''}
   <div class="bg-dgh" style="margin-top:4px;"><b>${QR?rgLabel(J,IX)+' · ':''}${N} kỳ${G?' · chỉ '+G:''}</b></div>
   ${body}
   <div class="bg-foot" style="margin:4px 0 0;"><span style="text-decoration:underline 2px #b46cff;text-underline-offset:3px;">gạch chân tím</span> = cặp kẹp (a, a+2 thiếu a+1) · <span style="border:2px solid #b46cff;border-radius:50%;padding:0 3px;">vòng tím</span> = số kẹp về trong 2 kỳ${G?' '+G:''} sau · <b style="color:#ffb347">Σ</b> = bằng tổng 2 số khác cùng kỳ · <b style="color:#4dd0c8">×2</b> = gấp đôi 1 số khác cùng kỳ.</div>
   <div class="bg-foot" style="margin:2px 0 0;">${N} kỳ: có tổng <b>${nS}</b> kỳ · nhân đôi <b>${nD}</b> kỳ · cặp kẹp <b>${nK}</b> kỳ · số kẹp về trong 2 kỳ <b>${kv}/${kt}</b> lần.${wait.length?`<br>Số kẹp đang chờ: <b>${wait.join(' · ')}</b>`:''}</div></details>`;}
function k10Gio(g){if(typeof window==='undefined')return;window.__k10G=g;window.__k10Open=true;if(typeof renderBangCard==='function')renderBangCard();}   // Loto: lọc x kỳ gần nhất theo giờ quay '' (cả 2) / 13h / 21h (anh 19/10/2026)
// Sổ pool của anh (16/10/2026): MỖI KỲ, MỖI GAME chỉ MỘT pool được dùng — lưu lại thì thay bản cũ của kỳ đó. Chỉ nằm trong trình duyệt.
function kyKey(k){const m=String(k).match(/(\d+)\/(\d+)\/(\d+)(?:\s+(\d+)h)?/);return m?(+m[3])*1e8+(+m[2])*1e6+(+m[1])*1e4+(+(m[4]||0)):0;}   // kỳ mới nhất = số lớn nhất
function ppBook(g){try{const v=JSON.parse(localStorage.getItem('vl_sopool_'+g)||'{}');return v&&typeof v==='object'?v:{};}catch(e){return {};}}
function ppPut(g,bk){try{localStorage.setItem('vl_sopool_'+g,JSON.stringify(bk));return true;}catch(e){return false;}}
function ppGet(g,ky){const e=ppBook(g)[ky];return e&&Array.isArray(e.n)&&e.n.length?e.n:null;}
function ppRe(){if(typeof renderBangCard==='function')renderBangCard();}
function ppStart(){const g=window.__ppG;window.__ppW=(ppGet(g,window.__ppK)||window.__ppX||[]).slice();window.__ppEd=true;ppRe();}
function ppTog(n){const w=window.__ppW,i=w.indexOf(n);if(i>=0)w.splice(i,1);else w.push(n);ppRe();}
function ppSave(){const g=window.__ppG,bk=ppBook(g);if(bk[window.__ppK]&&bk[window.__ppK].lock){alert('Kỳ này đã có kết quả và đã khóa, không lưu lại được');window.__ppEd=false;ppRe();return;}bk[window.__ppK]={n:window.__ppW.slice().sort((a,b)=>a-b),t:Date.now()};if(!ppPut(g,bk))alert('Không lưu được trên trình duyệt này');window.__ppEd=false;ppRe();if(typeof bkAuto==='function')bkAuto(false);}
function ppCancel(){window.__ppEd=false;ppRe();}
function ppFromX(){window.__ppW=(window.__ppX||[]).slice();ppRe();}
function ppDel(){if(!confirm('Xóa pool đã lưu của kỳ này?'))return;const g=window.__ppG,bk=ppBook(g);if(bk[window.__ppK]&&bk[window.__ppK].lock)return;delete bk[window.__ppK];ppPut(g,bk);ppRe();if(typeof bkAuto==='function')bkAuto(false);}
function ppCopy(){const t=JSON.stringify({game:window.__ppG,so:ppBook(window.__ppG)});try{navigator.clipboard.writeText(t).then(()=>alert('Đã sao chép sổ pool'),()=>prompt('Sao chép:',t));}catch(e){prompt('Sao chép:',t);}}
// ---- Vé bốc ngẫu nhiên từ pool của anh, chỉ giữ vé vừa dạng kỳ tới của app (anh 16/10/2026) ----
function vlFeat(x,mm,prev,NB){const s=[...x].sort((a,b)=>a-b),d6=mm?s.concat([mm]):s,H=Math.floor(NB/10)+1,hang=Array(H).fill(0);s.forEach(v=>hang[Math.floor(v/10)]++);
  return {hang,tong:d6.reduce((a,b)=>a+b,0),le:d6.reduce((a,v)=>a+v%2,0),nho:s.filter(v=>v<=Math.floor(NB/2)).length+(mm&&mm<=6?1:0),
    trung:s.filter(v=>(prev||[]).includes(v)).length,lt:s.slice(1).filter((b,i)=>b===s[i]+1).length,maxh:Math.max(...hang),comat:hang.filter(v=>v).length,dang:hang.join('-')};}
function vlCheck(sp,x,mm,prev,NB){const f=vlFeat(x,mm,prev,NB),k=sp.k;
  if(k==='hang')return sp.op==='le'?f.hang[sp.i]<=sp.v:f.hang[sp.i]>=sp.v;
  if(k==='tong'||k==='le'||k==='nho')return sp.lo<=f[k]&&f[k]<=sp.hi;
  if(k==='trung'||k==='lt'||k==='maxh')return f[k]<=sp.max;
  if(k==='comat')return f.comat>=sp.min;
  if(k==='khac')return f.dang!==sp.dang;
  if(k==='tranh')return !x.some(v=>sp.nums.includes(v));
  if(k==='lon'){const S=new Set(x);return Math.floor(x.filter(v=>{const r=(v%10)*10+Math.floor(v/10);return r!==v&&S.has(r);}).length/2)<=sp.max;}
  if(k==='rng'){f.kep=x.filter(v=>v%11===0).length;if(!(sp.f in f)){const s=[...x].sort((a,b)=>a-b),d=s.slice(1).map((v,i)=>v-s[i]),r3=[0,1,2].map(i=>s.filter(v=>v%3===i).length),df=new Set();s.forEach((a,i)=>s.slice(i+1).forEach(c=>df.add(c-a)));
    Object.assign(f,{ac:df.size-(s.length-1),span:s[s.length-1]-s[0],dmin:Math.min(...d),dmax:Math.max(...d),duoi:new Set(s.map(v=>v%10)).size,tduoi:s.reduce((a,v)=>a+v%10,0),m3max:Math.max(...r3),m3min:Math.min(...r3)});}   // đặc điểm mới (khuon.ext)
const inn=sp.lo<=f[sp.f]&&f[sp.f]<=sp.hi;return sp.neg?!inn:inn;}
  return true;}
function vlOk(x,mm,V,NB){const ev=x.filter(v=>v%2===0).length+(mm&&mm%2===0?1:0);return !V.cl.includes(ev)&&V.specs.every(sp=>vlCheck(sp,x,mm,V.prev,NB));}
function vlEv(x,mm){return x.filter(v=>v%2===0).length+(mm&&mm%2===0?1:0);}
// Chia số vé theo dạng chẵn:lẻ — dạng nào ra ≥20% trong 100 kỳ gần mới được nhận vé, số vé tỉ lệ với tần suất (anh 16/10/2026)
function vlPlan(J,n){const R=(J.res201||[]).slice(-20),L=(J.lk201||[]).slice(-20),c={};   // xét 20 kỳ gần nhất (anh 16/10/2026)
  R.forEach((r,i)=>{const e=vlEv(r,J.game==='loto'?L[i]:null);c[e]=(c[e]||0)+1;});
  const tot=R.length||1,cl=(J.veLuat&&J.veLuat.cl)||[],pats=Object.keys(c).map(Number).filter(e=>c[e]*100/tot>=20&&!cl.includes(e)).sort((a,b)=>c[b]-c[a]);
  const nh=R.map(r=>new Set(r.map(v=>Math.floor(v/10))).size),ch={};nh.forEach(v=>ch[v]=(ch[v]||0)+1);const mxh=Math.max(0,...Object.values(ch)),hset=Object.keys(ch).map(Number).filter(v=>ch[v]===mxh);
  const ts=R.map(r=>r.reduce((a,b)=>a+b,0)).sort((a,b)=>a-b),tlo=ts[Math.floor(ts.length*.25)],thi=ts[Math.ceil(ts.length*.75)-1];
  const ex={hset,hpct:Math.round(mxh*100/tot),tlo,thi,ch};
  if(!pats.length)return Object.assign({pats:[],q:{},c,tot},ex);
  const sum=pats.reduce((a,e)=>a+c[e],0),q={},fr=[];let used=0;
  pats.forEach(e=>{const v=n*c[e]/sum;q[e]=Math.floor(v);used+=q[e];fr.push([e,v-Math.floor(v)]);});
  fr.sort((a,b)=>b[1]-a[1]||c[b[0]]-c[a[0]]);for(let i=0;used<n;i=(i+1)%fr.length){q[fr[i][0]]++;used++;}
  return Object.assign({pats,q,c,tot},ex);}
function vlGen(J,P,n){const V=J.veLuat,KB=J.kb,NB=J.nb,out=[],seen=new Set((J.tickets||[]).map(t=>t.x.join()));
  const plan=vlPlan(J,n);if(!V||P.length<KB||!plan.pats.length)return {out,tries:0,plan};
  const mms=J.game==='loto'&&J.mm&&J.mm.length?J.mm:[null];let tries=0;
  const draw=ev=>{const a=P.slice();for(let i=0;i<KB;i++){const j=i+Math.floor(Math.random()*(a.length-i));[a[i],a[j]]=[a[j],a[i]];}
    const x=a.slice(0,KB).sort((p,q)=>p-q),key=x.join();if(seen.has(key))return null;
    if(window.__vlH!==false&&!plan.hset.includes(new Set(x.map(v=>Math.floor(v/10))).size))return null;
    if(window.__vlS!==false){const sm=x.reduce((p,q)=>p+q,0);if(sm<plan.tlo||sm>plan.thi)return null;}
    const order=mms.slice().sort(()=>Math.random()-.5),mm=order.find(m=>vlEv(x,m)===ev&&vlOk(x,m,V,NB));if(mm===undefined)return null;
    seen.add(key);return {x,mm,ev};};
  const left={};plan.pats.forEach(e=>left[e]=plan.q[e]);
  plan.pats.forEach(e=>{let t=0;while(left[e]>0&&t<15000){t++;tries++;const v=draw(e);if(v){out.push(v);left[e]--;}}});
  // dạng nào không bốc đủ → dồn phần thiếu sang dạng còn lại theo thứ tự tần suất
  let miss=plan.pats.reduce((a,e)=>a+left[e],0);
  for(const e of plan.pats){let t=0;while(miss>0&&t<15000){t++;tries++;const v=draw(e);if(v){out.push(v);miss--;}}}
  const ord=Object.fromEntries(plan.pats.map((e,i)=>[e,i]));out.sort((a,b)=>ord[a.ev]-ord[b.ev]||a.x.join().localeCompare(b.x.join()));
  return {out,tries,plan};}
function vlBlock(J,P,label,SUB){
  if(!J||!J.veLuat)return '';if(J.stale)return `<div class="bg-foot" style="margin-top:10px;">Vé bốc ngẫu nhiên cần luật dạng của app cho kỳ ${J.next}; luật này chưa có (app mới tính đến kỳ ${J.nextBase}). Chạy cập nhật xong sẽ bốc được.</div>`+svBlock(J,SUB);const X=[3,5,6,8,10],n=X.includes(window.__vlX)?window.__vlX:5,p2=v=>String(v).padStart(2,'0');
  window.__vlG=J.game;window.__vlK=J.next;window.__vlLabel=label;
  const sig=J.game+'|'+J.next+'|'+P.join()+'|'+n+'|'+(window.__vlN||0)+'|'+(window.__vlH!==false)+(window.__vlS!==false);
  if(!window.__vlT||window.__vlT.sig!==sig)window.__vlT=Object.assign({sig},vlGen(J,P,n));
  const HC=['#ff6b6b','#ffd93d','#6bcb77','#4d96ff','#c77dff','#ff9f43'],T=window.__vlT,mmB=m=>m?`<span class="bg-b mm">${p2(m)}</span>`:'';
  const rows=T.out.map((t,i)=>`<div class="bg-row bg-pool bg-k10"><small class="bg-k10d" style="flex:0 0 30px;">Vé ${i+1}</small>${t.x.map(v=>`<span class="bg-b">${p2(v)}</span>`).join('')}${mmB(t.mm)}<small class="bg-k10i">${t.x.map(v=>{const h=Math.floor(v/10);return `<i style="color:${HC[h%HC.length]};">${h}</i>`;}).join('-')} <b>${t.x.reduce((a,b)=>a+b,0)}</b> ${t.ev}C:${J.kb+(J.game==='loto'?1:0)-t.ev}L</small></div>`).join('');
  return `<div class="bg-dgh" style="margin-top:2px;"><b>Vé bốc ngẫu nhiên từ ${label}</b> <small>— vé chia theo dạng chẵn:lẻ của 20 kỳ gần nhất, tỉ lệ với khả năng ra, mỗi vé vừa mọi luật dạng kỳ ${J.next} của app, không trùng 7 vé của app</small></div>
  <div class="bg-row bg-chips"><small>Số vé:</small>${X.map(v=>`<span class="bg-h20k${v===n?' on':''}" onclick="vlSet(${v})">${v}</span>`).join('')}<span class="bg-h20k" onclick="vlAgain()">Bốc lại</span><span class="bg-h20k${(svBook(J.game)[J.next]||{}).tk?' on':''}" onclick="svSave()">${(svBook(J.game)[J.next]||{}).tk?'Đã chốt · chốt lại':'Chốt bộ vé này'}</span></div>
  <div class="bg-row bg-chips"><small>Lọc thêm (20 kỳ gần):</small><span class="bg-h20k${window.__vlH!==false?' on':''}" onclick="vlTog('H')">Số hàng có mặt</span><span class="bg-h20k${window.__vlS!==false?' on':''}" onclick="vlTog('S')">Tổng</span></div>
  ${(()=>{const pl=T.plan,d=J.kb+(J.game==='loto'?1:0);return pl&&pl.pats.length?`<div class="bg-foot" style="margin:2px 0;">Chia vé theo chẵn:lẻ (20 kỳ gần): ${pl.pats.map(e=>`<b>${e}C:${d-e}L</b> ${Math.round(pl.c[e]*100/pl.tot)}% → ${pl.q[e]} vé`).join(' · ')}. Dạng ra dưới 20% (dưới 4/20 kỳ) bị bỏ.</div>`:'';})()}${(()=>{const pl=T.plan;if(!pl||!pl.hset)return '';return `<div class="bg-foot" style="margin:2px 0;">Lọc 20 kỳ gần: ${window.__vlH!==false?`số hàng có mặt = <b>${pl.hset.join(' hoặc ')}</b> (${pl.hpct}% số kỳ)`:'<s>số hàng</s>'} · ${window.__vlS!==false?`tổng <b>${pl.tlo}–${pl.thi}</b> (khoảng giữa, ~50% số kỳ)`:'<s>tổng</s>'}.</div>`;})()}${rows||'<div class="bg-foot">Pool chưa đủ số hoặc không bốc được vé nào vừa dạng.</div>'}
  <div class="bg-foot">${T.out.length<n?`Chỉ bốc được ${T.out.length}/${n} vé vừa dạng từ pool này (đã thử ${T.tries} lần) — mở rộng pool nếu muốn thêm vé. `:''}Bên phải mỗi vé: hàng chục từng số · tổng${J.game==='loto'?' 5 số chính':''} · chẵn:lẻ. ${J.game==='loto'?'Bóng cam = số may mắn, lấy trong ±3 quanh số kỳ trước.':''}</div>`+svBlock(J,SUB);}
// ---- Sổ vé đã chốt: mỗi kỳ 1 bộ (bản chốt cuối), có kết quả thì tự chấm và khóa (anh 16/10/2026) ----
function svBook(g){try{const v=JSON.parse(localStorage.getItem('vl_sove_'+g)||'{}');return v&&typeof v==='object'?v:{};}catch(e){return {};}}
function svPut(g,bk){try{localStorage.setItem('vl_sove_'+g,JSON.stringify(bk));return true;}catch(e){return false;}}
function svSave(){const T=window.__vlT,g=window.__vlG,k=window.__vlK;if(!T||!T.out||!T.out.length){alert('Chưa có vé để chốt');return;}
  const bk=svBook(g);if(bk[k]&&bk[k].lock){alert('Kỳ này đã có kết quả và đã khóa');return;}
  const pl=T.plan;bk[k]={tk:T.out.map(t=>({x:t.x,mm:t.mm,ev:t.ev})),t:Date.now(),pool:window.__vlLabel||'',f:{H:window.__vlH!==false,S:window.__vlS!==false,hset:pl.hset,tlo:pl.tlo,thi:pl.thi,pats:pl.pats}};
  if(!svPut(g,bk))alert('Không lưu được trên trình duyệt này');ppRe();if(typeof bkAuto==='function')bkAuto(false);}
function svCopy(){const t=JSON.stringify({game:window.__vlG,sove:svBook(window.__vlG)});try{navigator.clipboard.writeText(t).then(()=>alert('Đã sao chép sổ vé'),()=>prompt('Sao chép:',t));}catch(e){prompt('Sao chép:',t);}}
function svBlock(J,sub){
  const bk=svBook(J.game),ks=Object.keys(bk);if(!ks.length)return '';
  const idx={};(J.dates201||[]).forEach((d,i)=>idx[d]=i);const lo=J.game==='loto',d6=J.kb+(lo?1:0);let dirty=false;
  ks.forEach(k=>{const e=bk[k],i=idx[k];if(i==null||e.lock)return;
    const r=J.res201[i],lk=lo&&J.lk201?J.lk201[i]:null;
    e.res=e.tk.map(t=>t.x.filter(v=>r.includes(v)).length);e.mmh=e.tk.map(t=>!!(lo&&t.mm&&t.mm===lk));
    const real={ev:vlEv(r,lo?lk:null),nh:new Set(r.map(v=>Math.floor(v/10))).size,tong:r.reduce((a,b)=>a+b,0)};e.real=real;
    e.ok={cl:e.f.pats.includes(real.ev),h:e.f.H?e.f.hset.includes(real.nh):null,s:e.f.S?(real.tong>=e.f.tlo&&real.tong<=e.f.thi):null};e.lock=true;dirty=true;});
  if(dirty)svPut(J.game,bk);
  const L=ks.map(k=>({k,e:bk[k]})).sort((a,b)=>kyKey(b.k)-kyKey(a.k)).slice(0,12),sc=L.filter(x=>x.e.lock&&x.e.res);
  const mk=v=>v==null?'–':v?'✔':'✘',pc=(a,b)=>b?Math.round(a*100/b)+'%':'—';
  const rows=L.map(({k,e})=>`<tr><td class="l">${k}${e.lock?' <small>🔒</small>':''}</td><td>${e.tk.length}</td><td class="l">${e.res?e.res.join('·')+` <small>(tốt nhất ${Math.max(...e.res)})</small>`:'<small>chờ kết quả</small>'}</td><td class="l">${e.real?`${e.real.ev}C:${d6-e.real.ev}L · ${e.real.nh} hàng · ${e.real.tong} <small>${mk(e.ok.cl)}${mk(e.ok.h)}${mk(e.ok.s)}</small>`:''}</td></tr>`).join('');
  const b3=sc.filter(x=>Math.max(...x.e.res)>=3).length,b4=sc.filter(x=>Math.max(...x.e.res)>=4).length;
  const fr=(f)=>{const a=sc.filter(x=>x.e.ok[f]!=null);return pc(a.filter(x=>x.e.ok[f]).length,a.length);};
  return sub(`Sổ vé đã chốt (${ks.length} kỳ) — mỗi kỳ 1 bộ, có kết quả thì tự chấm và khóa`,`<div class="tw"><table><thead><tr><th class="l">Kỳ</th><th>Vé</th><th class="l">Trúng từng vé</th><th class="l">Dạng thật <small>(✔✘: chẵn:lẻ · hàng · tổng)</small></th></tr></thead><tbody>${rows}</tbody></table></div>
  <div class="bg-foot">${sc.length?`Đã chấm ${sc.length} kỳ: bộ vé có vé trúng ≥3 số ${pc(b3,sc.length)} · ≥4 số ${pc(b4,sc.length)} · dạng thật lọt chẵn:lẻ ${fr('cl')} · số hàng ${fr('h')} · tổng ${fr('s')}`:'Chưa có kỳ nào có kết quả để chấm.'} · <span class="bg-h20k" onclick="svCopy()">Sao chép sổ vé</span></div>`);}
function vlSet(n){window.__vlX=n;window.__vlN=(window.__vlN||0)+1;ppRe();}
function vlTog(k){window['__vl'+k]=window['__vl'+k]===false;window.__vlN=(window.__vlN||0)+1;ppRe();}
function vlAgain(){window.__vlN=(window.__vlN||0)+1;ppRe();}
function ppSet(n){if(typeof window==='undefined')return;window.__ppN=n;rgOff('p');if(typeof renderBangCard==='function')renderBangCard();}
function poolSet(k){if(typeof window==='undefined')return;window.__poolK=k;if(typeof renderBangCard==='function')renderBangCard();}

// ---- Check dạng (anh 14/10/2026): % các dạng trong 50/100 kỳ đã qua + kiểm 1 dãy ----
// Loto: tổng, chẵn-lẻ, nhỏ-lớn tính trên DÃY 6 SỐ (5 số + số may mắn, MM nhỏ = 1–6); liên tiếp, trùng kỳ trước, chia hàng: 5 số chính.
function dangOf(J,r,mm,prev){
  const NB=J.nb,lo=J.game==='loto',s=[...r].sort((a,b)=>a-b),d6=lo&&mm?[...s,mm]:s;
  const sum=d6.reduce((a,b)=>a+b,0),odd=d6.filter(v=>v%2).length;
  const small=s.filter(v=>v<=Math.floor(NB/2)).length+(lo&&mm?(mm<=6?1:0):0);
  let cons=0;for(let i=1;i<s.length;i++)if(s[i]===s[i-1]+1)cons++;
  const rep=prev?s.filter(v=>prev.includes(v)).length:0,hang=Array(Math.floor(NB/10)+1).fill(0);s.forEach(v=>hang[Math.floor(v/10)]++);
  const BW={loto:15,mega:20,power:25}[J.game]||20,b=Math.floor(sum/BW)*BW;
  return {tong:`${b}–${b+BW-1}`,tongN:b,sum,cl:`${d6.length-odd} chẵn – ${odd} lẻ`,nl:`${small} nhỏ – ${d6.length-small} lớn`,
    lt:cons===0?'không có cặp liền nhau':cons===1?'1 cặp liền nhau':'≥2 cặp liền nhau',tr:rep>=3?'trùng ≥3 số':`trùng ${rep} số`,hang:hang.join('-')};
}
function khuonOk(sp,J,x,mm){const f=dangF(J,x,mm);
  if(sp.k==='hang')return sp.op==='le'?f.hang[sp.i]<=sp.v:f.hang[sp.i]>=sp.v;
  if(sp.k==='tong'||sp.k==='le'||sp.k==='nho')return f[sp.k]>=sp.lo&&f[sp.k]<=sp.hi;
  if(sp.k==='trung'||sp.k==='lt'||sp.k==='maxh')return f[sp.k]<=sp.max;
  if(sp.k==='comat')return f.comat>=sp.min; if(sp.k==='khac')return f.dang!==sp.dang;
  if(sp.k==='rng'){const v=f[sp.f],inn=v>=sp.lo&&v<=sp.hi;return sp.neg?!inn:inn;} return true;}
function dangF(J,x,mm){const NB=J.nb,s=[...x].sort((a,b)=>a-b),d6=mm&&J.game==='loto'?[...s,mm]:s,hang=Array(Math.floor(NB/10)+1).fill(0);s.forEach(v=>hang[Math.floor(v/10)]++);
  let lt=0;for(let i=1;i<s.length;i++)if(s[i]===s[i-1]+1)lt++;
  return {hang,tong:d6.reduce((a,b)=>a+b,0),le:d6.filter(v=>v%2).length,nho:s.filter(v=>v<=Math.floor(NB/2)).length+(mm&&J.game==='loto'&&mm<=6?1:0),
    trung:s.filter(v=>J.lastRes.includes(v)).length,lt,kep:s.filter(v=>v%11===0).length,maxh:Math.max(...hang),comat:hang.filter(v=>v).length,dang:hang.join('-')};}
function g10HTML(J){const R=J.res201,DT=J.dates201,L=J.lk201||[];if(!R||!DT)return '';
  const p2=n=>String(n).padStart(2,'0'),lo=J.game==='loto',NB=J.nb;
  const nextSes=lo?(String(J.next).includes('13h')?'13h':'21h'):null,mode=(typeof window!=='undefined'&&window.__g10)||'gan',N=(typeof window!=='undefined'&&window.__g10n)||10,gio=lo&&mode==='gio';
  const idx=[];for(let i=R.length-1;i>=1&&idx.length<N;i--){if(gio&&!String(DT[i]).includes(nextSes))continue;idx.push(i);}
  const rows=idx.map(i=>{const s=[...R[i]].sort((a,b)=>a-b),mm=lo?L[i]:null,d6=mm?[...s,mm]:s,prev=R[i-1];
    const tong=d6.reduce((a,b)=>a+b,0),le=d6.filter(v=>v%2).length,nho=s.filter(v=>v<=Math.floor(NB/2)).length+(mm&&mm<=6?1:0);
    const lt=[];for(let j=1;j<s.length;j++)if(s[j]===s[j-1]+1)lt.push(p2(s[j-1])+'-'+p2(s[j]));
    return {d:DT[i],s,mm,tong,cl:`${d6.length-le}C-${le}L`,nl:`${nho}N-${d6.length-nho}L`,dau:s.map(v=>Math.floor(v/10)).join('-'),lt,kep:s.filter(v=>v%11===0),tr:s.filter(v=>prev.includes(v))};});
  const n=rows.length;if(!n)return '';const avg=Math.round(rows.reduce((a,r)=>a+r.tong,0)/n),mn=Math.min(...rows.map(r=>r.tong)),mx=Math.max(...rows.map(r=>r.tong));
  const top=k=>{const c={};rows.forEach(r=>c[r[k]]=(c[r[k]]||0)+1);return Object.entries(c).sort((a,b)=>b[1]-a[1]).slice(0,2).map(([v,x])=>`${v} (${x})`).join(', ');};
  const sw=[10,20].map(k=>`<span class="bg-h20k${!gio&&N===k?' on':''}" onclick="g10Set('gan',${k})">${k} kỳ gần nhất</span>`).join('')+(lo?[10,20].map(k=>`<span class="bg-h20k${gio&&N===k?' on':''}" onclick="g10Set('gio',${k})">${k} kỳ cùng giờ ${nextSes}</span>`).join(''):'');
  return `<div class="bg-dg" style="margin-top:6px;"><div class="bg-dgh bg-chips">${sw} <small>${lo?'tổng, chẵn–lẻ, nhỏ–lớn tính cả số may mắn (dãy 6 số); trùng = so với kỳ liền trước nó':''}</small></div>
   <div style="overflow-x:auto;"><table class="bg-g10"><thead><tr><th>Kỳ</th><th>Kết quả</th><th>Tổng</th><th>Chẵn–lẻ</th><th>Nhỏ–lớn</th><th>Đầu số</th><th>Liên tiếp</th><th>Kép</th><th>Trùng kỳ trước</th></tr></thead><tbody>
   ${rows.map(r=>`<tr><td>${r.d}</td><td>${r.s.map(p2).join(' ')}${r.mm?` <b style="color:#ff9f43">${p2(r.mm)}</b>`:''}</td><td>${r.tong}</td><td>${r.cl}</td><td>${r.nl}</td><td>${r.dau}</td><td>${r.lt.join(' ')||'—'}</td><td>${r.kep.map(p2).join(' ')||'—'}</td><td>${r.tr.length?r.tr.map(p2).join(' '):'—'}</td></tr>`).join('')}
   </tbody></table></div>
   <div class="bg-foot">Tóm tắt ${n} kỳ: tổng TB <b>${avg}</b> (thấp ${mn} – cao ${mx}) · chẵn–lẻ hay gặp: <b>${top('cl')}</b> · nhỏ–lớn: <b>${top('nl')}</b> · có số liên tiếp <b>${rows.filter(r=>r.lt.length).length}/${n}</b> kỳ · có số kép <b>${rows.filter(r=>r.kep.length).length}/${n}</b> kỳ · trùng kỳ trước <b>${rows.filter(r=>r.tr.length).length}/${n}</b> kỳ.</div></div>`;}
function g10Set(m,n){window.__g10=m;window.__g10n=n||10;dangRe();}
function duHTML(J){const K=J.khuon;if(!K||!K.du)return '';
  return `<div class="bg-dg" style="margin-top:6px;border-color:var(--ac);"><div class="bg-dgh"><b>Dạng gợi ý kỳ ${J.nextBase||J.next}</b> <small>(theo dữ liệu: sau trạng thái của kỳ vừa quay, kỳ sau hay ra gì — đã trừ các dạng trái luật)</small></div>
   ${[...K.du].sort((a,b)=>Math.min(b.a50,b.a100)-Math.min(a.a50,a.a100)).map(d=>{const m=Math.min(d.a50,d.a100),lv=m>=70?'chắc':m>=55?'vừa':'yếu';return `<div class="bg-dgr${m>=70?' on':''}" style="grid-template-columns:110px 1fr auto;${m<55?'opacity:.45;':''}"><span>${d.mat} <small>(${lv})</small></span><b>${d.du}${d.cach&&d.cach!=='theo 200 kỳ (kỳ trước giống)'?` <small style="font-weight:400">· ${d.cach}</small>`:''}</b><em>${d.p}% <small>· chấm lùi ${d.a50}% / ${d.a100}%</small></em></div>`;}).join('')}
   <div class="bg-foot">% = trong 100 kỳ qua, những lần kỳ trước giống kỳ vừa quay thì kỳ sau rơi vào dạng này bao nhiêu %. "Chấm lùi" = cách chọn này đoán trúng bao nhiêu % kỳ ở 50 / 100 kỳ gần (chắc ≥70%, vừa 55–69%, yếu <55% — mờ).</div></div>`;}
function khuonHTML(J,tk){const K=J.khuon;if(!K||!K.rules)return '';
  const all=tk?[...K.rules,...(K.lienhe||[])].every(r=>khuonOk(r.spec,J,tk.x,tk.lk)):null;
  return `<div class="bg-dg" style="margin-top:6px;"><div class="bg-dgh"><b>Dạng kỳ tới — khuôn</b> <span class="bg-dgm ok">dạng thật lọt khuôn ${K.pass50}% / ${K.pass100}% (50 / 100 kỳ qua${K.tien?", chấm tiến cả bộ luật lọc vé":""})</span>${tk?` <span class="bg-dgm ${all?'ok':'bad'}">dãy này: ${all?'✔ vừa khuôn':'✘ ngoài khuôn'}</span>`:''}</div>
    ${K.rules.length?K.rules.map(r=>{const o=tk?khuonOk(r.spec,J,tk.x,tk.lk):null;return `<div class="bg-dgr${o===false?'':' on'}" style="grid-template-columns:1fr auto auto;"><span>${tk?(o?'✔ ':'✘ '):''}${r.lab}</span><em>đúng ${r.a50}% / ${r.a100}%</em><small>${r.n100} lần/100 kỳ</small></div>`;}).join(''):'<div class="bg-foot">Kỳ này chưa có luật dạng nào đạt.</div>'}
    ${K.hang?`<div class="bg-dgh" style="margin-top:6px;"><b>Từng hàng kỳ tới</b> <small>(100 kỳ qua: những lần kỳ trước hàng đó ra như kỳ vừa quay → kỳ sau ra mấy số)</small></div>
     <table class="bg-g10"><thead><tr><th>Hàng</th><th>Kỳ trước</th><th>Kỳ sau vắng</th><th>1 số</th><th>≥2 số</th><th>Luật đạt (đúng 50 / 100 kỳ)</th>${tk?'<th>Dãy này</th>':''}</tr></thead><tbody>
     ${K.hang.map(h=>{const mx=Math.max(...h.dist.map(v=>v||0)),c=tk?dangF(J,tk.x,tk.lk).hang[h.h]:null;return `<tr><td><b>${h.h}x</b></td><td>${h.truoc>=3?'≥3':h.truoc} số</td>${h.dist.map(v=>`<td${v===mx?' style="font-weight:700;color:var(--ac)"':''}>${v==null?'—':v+'%'}</td>`).join('')}<td style="text-align:left;white-space:normal;">${h.luat.length?h.luat.map(l=>`${l.trong?'<b>':''}${l.lab.replace(/^.*→ kỳ này /,'')} (${l.a50}/${l.a100}%)${l.trong?' · trong khuôn</b>':''}`).join('<br>'):'<small>chưa có luật đạt — xem % bên trái</small>'}</td>${tk?`<td>${c} số</td>`:''}</tr>`;}).join('')}</tbody></table>`:''}
    ${(K.lienhe||[]).length?`<div class="bg-dgh" style="margin-top:6px;"><b>Liên hệ với kỳ trước (đang hiệu lực)</b></div>`+K.lienhe.map(r=>{const o=tk?khuonOk(r.spec,J,tk.x,tk.lk):null;return `<div class="bg-dgr${o===false?'':' on'}" style="grid-template-columns:1fr auto auto;"><span>${tk?(o?'✔ ':'✘ '):''}${r.lab}</span><em>đúng ${r.a50}% / ${r.a100}%</em><small>${r.n200} lần/100 kỳ</small></div>`;}).join(''):''}
    <div class="bg-foot">Vé gợi ý đã được đối chiếu: vé nào trái khuôn hoặc trái liên hệ đều được đổi 1–2 số trong pool cho vừa. Mỗi luật đúng ≥70% ở 50 và 100 kỳ gần (riêng game này). Ghép thêm luật cho tới khi dạng thật vẫn lọt khuôn ≥${K.nguong}%. Khuôn giữ lại khoảng ${K.keep}% số dãy.</div></div>`;}
function dangHTML(J){
  if(!J||!J.res201)return '';
  const W=(typeof window!=='undefined'&&window.__dangW)||100,p2=n=>String(n).padStart(2,'0'),R=J.res201,L=J.lk201||[];
  const F=[];for(let i=R.length-W;i<R.length;i++)F.push(dangOf(J,R[i],L[i],R[i-1]));
  const tk=(typeof window!=='undefined'&&window.__dangTk)||(J.tickets&&J.tickets[0]?{x:J.tickets[0].x,lk:J.tickets[0].lk}:null);
  const me=tk?dangOf(J,tk.x,tk.lk,J.lastRes):null;
  const DIM=[['tong','Tổng'+(J.game==='loto'?' (cả số may mắn)':''),true],['cl','Chẵn – lẻ'+(J.game==='loto'?' (dãy 6 số)':'')],['nl','Nhỏ – lớn'+(J.game==='loto'?` (≤${Math.floor(J.nb/2)}, MM ≤6)`:` (≤${Math.floor(J.nb/2)})`)],['lt','Số liên tiếp'],['tr','Trùng kỳ trước']];
  const tab=([k,lab,num])=>{const c={};F.forEach(f=>{c[f[k]]=(c[f[k]]||0)+1;});
    let rows=Object.entries(c);rows.sort(num?(a,b)=>parseInt(a[0])-parseInt(b[0]):(a,b)=>b[1]-a[1]);
    if(k==='hang'){const top=rows.slice(0,10);if(me&&!top.find(r=>r[0]===me.hang))top.push([me.hang,c[me.hang]||0]);rows=top;}
    const mine=me?me[k]:null,pm=mine!=null?Math.round((c[mine]||0)/W*100):null,rkm=Object.entries(c).sort((a,b)=>b[1]-a[1]).findIndex(r=>r[0]===mine);
    return `<div class="bg-dg"><div class="bg-dgh"><b>${lab}</b>${me?` <span class="bg-dgm${rkm>=0&&rkm<3?' ok':pm<=3?' bad':''}">dãy này: ${mine} → ${pm}%${rkm>=0?` · hạng ${rkm+1}`:' · chưa gặp'}</span>`:''}</div>
      ${rows.map(([v,n])=>`<div class="bg-dgr${v===mine?' on':''}"><span>${v}</span><i style="width:${Math.round(n/W*100)}%"></i><em>${Math.round(n/W*100)}% <small>(${n})</small></em></div>`).join('')}</div>`;};
  const tks=(J.tickets||[]).map((t,i)=>`<span class="bg-h20k${tk&&t.x.join()===tk.x.join()?' on':''}" onclick="dangTk(${i})">Vé ${i+1}${J.khuon&&J.khuon.ve?(J.khuon.ve[i]?' ✔':' ✘'):''}</span>`).join('');
  return `<div class="bg-row bg-chips">${DANGW.map(w=>`<span class="bg-h20k${w===W?' on':''}" onclick="dangSet(${w})">${w} kỳ</span>`).join('')}</div>
   <div class="bg-row bg-chips" style="margin-top:4px;"><small>Kiểm dãy:</small> ${tks}
     <input id="dangIn" placeholder="${J.game==='loto'?'5 số + số may mắn, vd 03 11 19 24 31 07':'vd 05 12 19 27 33 41'}" style="min-width:220px;padding:3px 6px;" value="${tk&&typeof window!=='undefined'&&window.__dangTk?tk.x.map(p2).join(' ')+(tk.lk?' '+p2(tk.lk):''):''}">
     <span class="bg-h20k" onclick="dangIn()">Kiểm</span></div>
   ${me?`<div class="bg-foot" style="margin:4px 0;">Đang kiểm: <b>${tk.x.map(p2).join(' ')}${tk.lk?' + '+p2(tk.lk):''}</b> · tổng ${me.sum}. Ô xanh = dạng của dãy, % = số kỳ trong ${W} kỳ qua có dạng đó.</div>`:''}
   ${duHTML(J)}
   ${g10HTML(J)}
   ${khuonHTML(J,tk)}
   <div class="bg-dgw">${DIM.map(tab).join('')}</div>`;
}
const DANGW=[50,100];   // tối đa 100 kỳ (anh 15/10/2026)
function dangRe(){if(typeof window==='undefined')return;const el=document.getElementById('dang');if(el&&window.__dangJ)el.innerHTML=dangHTML(window.__dangJ);}
function dangSet(w){window.__dangW=w;dangRe();}
function dangTk(i){const t=window.__dangJ.tickets[i];window.__dangTk={x:t.x,lk:t.lk};dangRe();}
function dangIn(){const J=window.__dangJ,v=(document.getElementById('dangIn').value.match(/\d+/g)||[]).map(Number);
  if(v.length<J.kb){alert('Cần '+J.kb+' số');return;}const x=v.slice(0,J.kb),lk=J.game==='loto'&&v.length>J.kb?v[J.kb]:null;window.__dangTk={x,lk};dangRe();}

// Thu gọn mặc định mọi khối lớn của bảng gợi ý (anh 14/10/2026: "mặc định thu hết các khối lớn cho đỡ rối").
// Khối nào anh mở thì giữ trạng thái mở khi bảng vẽ lại (đổi cỡ pool…).
function bgFold(root){if(!root||typeof document==='undefined')return;window.__bgOpen=window.__bgOpen||new Set();
  root.querySelectorAll('.bg > div.bg-sec').forEach(sec=>{const h=sec.querySelector(':scope > h4');if(!h)return;
    const d=document.createElement('details');d.className='bg-sec bg-h20w';const sm=document.createElement('summary');sm.appendChild(h);d.appendChild(sm);
    while(sec.firstChild)d.appendChild(sec.firstChild);const key=h.textContent.trim().slice(0,30);if(window.__bgOpen.has(key))d.open=true;
    d.addEventListener('toggle',()=>{d.open?window.__bgOpen.add(key):window.__bgOpen.delete(key);});
    if(sec.id)d.id=sec.id;sec.replaceWith(d);});
  root.querySelectorAll('details.bg-main').forEach(d=>{const k=d.dataset.k;d.addEventListener('toggle',()=>{window.__bgShut=window.__bgShut||new Set();
    if(d.open){window.__bgShut.delete(k);window.__bgOpen.add('m:'+k);}else{window.__bgShut.add(k);window.__bgOpen.delete('m:'+k);}});});
  root.querySelectorAll('details.bg-h20w').forEach(d=>{if(d.dataset.fk)return;d.dataset.fk=1;const h=d.querySelector('summary h4');if(!h)return;const key=h.textContent.trim().slice(0,30);
    if(window.__bgOpen.has(key))d.open=true;d.addEventListener('toggle',()=>{d.open?window.__bgOpen.add(key):window.__bgOpen.delete(key);});});}
function renderBang(J){
  if(!J)return '<div class="bg-foot">Chưa có bảng gợi ý cho trò này.</div>';
  const COL={power:'#f0b429',mega:'#c8204f',loto:'#3fb950'},ac=COL[J.game]||'#f0b429';
  const p2=n=>String(n).padStart(2,'0'),pct=v=>v==null?'—':Math.round(v)+'%';
  const rk=J.rank,t10=new Set(rk.slice(0,10)),t15=new Set(rk.slice(0,15)),t20=new Set(rk.slice(0,20));
  const vang=new Set(J.vang),hot=new Set(J.hot),tl=J.tl||{},strong=new Set(tl.strong||[]),top=new Set(tl.top||[]),linh=new Set(J.linh||[]),last=new Set(J.lastRes);
  const core=new Set(J.core);
  const ball=(n,cls,extra)=>`<span class="bg-b ${cls||''}"${extra||''}>${p2(n)}</span>`;
  const PK=(typeof window!=='undefined'&&window.__poolK)||18,PL=(J.pools&&J.pools[PK])||rk.slice(0,PK),inP=new Set(PL);   // anh 14/10: tích chọn cỡ pool, chỉ tô số trong pool
  const tierCls=n=>inP.has(n)?'t10':vang.has(n)?'tx':'';
  // 1. Lưới số
  const cols=J.nb===35?7:J.nb===45?9:11;
  let grid='';for(let n=1;n<=J.nb;n++){
    const mk=(strong.has(n)?'<i class="bg-st">★</i>':top.has(n)?'<i class="bg-st2">☆</i>':'')+(hot.has(n)?'<i class="bg-hot"></i>':'')+(linh.has(n)?'<i class="bg-li">✦</i>':'');
    grid+=`<div class="bg-c ${tierCls(n)}${last.has(n)?' lastd':''}" title="${(J.why[n]||'').replace(/"/g,'')}"><b>${p2(n)}</b>${mk}</div>`;}
  // 2. Thang pool
  const tierRow=(k,lab)=>{const a=J.tiers[k];if(!a)return '';const b=(J.tiers50||J.tiers100)[k]||[],bl=J.tiers50?'50 kỳ':'100 kỳ';return `<div class="bg-tr"><div class="bg-tl"><span class="bg-sw ${k<=10?'t10':k<=15?'t15':'t20'}"></span>${lab}<small>TB ${a[4].toFixed(2)} số/kỳ</small></div>
    <div class="bg-bars">${[1,2,3].map(j=>`<div class="bg-bar"><span style="width:${a[j]}%;"></span><em>≥${j+1} số: <b>${pct(a[j])}</b> <small>(${bl} ${pct(b[j])})</small></em></div>`).join('')}</div></div>`;};
  // 2b. Rải vé bao phủ (bao_phu.py): nếu ≥k số về nằm trong pool thì chắc chắn có vé trúng ≥m số
  const vnd=x=>Math.round(x).toLocaleString('vi-VN')+'đ';
  const wh=(J.wheel||[]).map((w,i)=>{const a=w.r100,b=w.r200;return `<details class="bg-wh"><summary><b>Pool ${w.v} · ${w.m} nếu ${w.k}</b> — ${w.nve} vé (${vnd(w.cost)}) · kỳ có vé ≥3 số <b>${pct(b.g3)}</b> <small>(50 kỳ) · 100 kỳ ${pct(a.g3)}</small> · ≥4 số <b>${pct(b.g4)}</b>${b.thuong!=null?` · thưởng TB ${vnd(b.thuong)}/kỳ`:''}</summary>
    <div class="bg-foot">Nếu ≥${w.k} số về nằm trong pool ${w.v} thì chắc chắn có vé trúng ≥${w.m} số. Đủ điều kiện ${pct(b.dk)} số kỳ (100 kỳ ${pct(a.dk)}). Số liệu chạy lại đúng pool thô của từng kỳ trong 100 kỳ (số đậm = 50 kỳ).</div>
    ${w.tickets.map((t,k)=>`<div class="bg-tk"><span class="bg-ti">${k+1}</span>${t.map(n=>ball(n,t10.has(n)?'t10':t15.has(n)?'t15':'t20')).join('')}</div>`).join('')}</details>`;}).join('');
  // 3. Khẳng định
  const cl=J.claims.filter(c=>c.r200>=70).sort((a,b)=>b.r200-a.r200).map(c=>`<div class="bg-cl${c.trace?' tr':''}">
    <div class="bg-clh"><span>${c.lab}</span><b>${pct(c.r200)}</b></div>
    <div class="bg-bar big"><span style="width:${c.r200}%;"></span><i style="left:${c.keep}%;" title="vé giữ lại"></i></div>
    <div class="bg-cls">50 kỳ gần ${pct(c.r50)} · vé giữ lại ${pct(c.keep)}${c.trace?' · <b class="bg-ok">✔ có dấu vết (đúng > giữ)</b>':''}</div></div>`).join('');
  // 4. Vé
  const tk=J.tickets.map((t,i)=>`<div class="bg-tk${t.kind.startsWith('cân nhắc')?' alt':''}"><span class="bg-ti">${i+1}</span>${t.x.map(n=>ball(n,(core.has(n)?'core ':'')+(strong.has(n)?'tl ':'')+(t20.has(n)?'':'out'))).join('')}${t.lk?ball(t.lk,'mm'):''}<small>${t.kind}${t.lv>0&&t.lv<3?' · nới ràng buộc':''} · tổng ${t.sum}</small></div>`).join('');
  // 5. 10 kỳ gần
  const mx=Math.max(4,...J.last10);
  const spark=J.last10.map(h=>`<div class="bg-sp" title="${h} số"><span style="height:${h/mx*100}%;"></span><small>${h}</small></div>`).join('');
  // 6. Tâm linh
  const tlH=J.tl?`<div class="bg-sec"><h4>Tâm linh · ${tl.nm} quẻ</h4>${tl.dung?`<div class="bg-foot">Cộng điểm vào pool chỉ từ phương pháp đã chứng minh giúp pool: <b>${tl.dung.join(', ')}</b> (+1 mỗi số). Phiếu các quẻ khác chỉ để tham khảo.</div>`:''}
    <div class="bg-row">Dãy tâm linh: ${tl.day.map(n=>ball(n,'tl')).join('')}</div>
    <div class="bg-row bg-chips">${tl.top.map(n=>`<span class="bg-chip${strong.has(n)?' s':''}">${p2(n)} <small>${tl.votes[n]} phiếu${inP.has(n)?'':' · ngoài pool '+PK}</small></span>`).join('')}</div>
    ${tl.out&&tl.out.length?`<div class="bg-warn">⚠ Tâm linh mạnh ngoài pool 18: <b>${tl.out.map(p2).join(' ')}</b> — xem vé "cân nhắc tâm linh".</div>`:''}
    ${tl.rescued&&tl.rescued.length?`<div class="bg-foot">Được cứu khỏi luật vắng: ${tl.rescued.map(p2).join(' ')}</div>`:''}</div>`:'';
  const mmR=J.mmRate,mmH=J.mmHist||[];
  const mmK=J.mmRank||{};
  const mm=J.mm&&J.mm.length?`<div class="bg-sec"><h4>Số May Mắn (${J.mm.length} số theo thứ tự ưu tiên — nóng 10 kỳ, trong ±3 quanh số kỳ trước)</h4><div class="bg-row">${J.mm.map((k,i)=>`<div style="display:flex;align-items:center;gap:6px;width:100%;"><small class="bg-mmg"><b>ưu tiên ${i+1}</b></small>`+ball(k,'mm')+`<small class="bg-mmg">vắng ${J.mmGap[k]} kỳ${mmK['100']?` · về ${mmK['50'][i]}% / ${mmK['100'][i]}% (50/100 kỳ)`:''}</small></div>`).join('')}</div>
    <div class="bg-foot">Chia vé (không tính vé thay thế): ${J.mm.map((k,i)=>`ưu tiên ${i+1} (${p2(k)}) ${J.tickets.filter(t=>t.lk===k&&!t.kind.startsWith('cân nhắc')).length} vé`).join(', ')}.</div>
    ${mmR?`<div class="bg-h20s">Tỉ lệ đoán đúng: 10 kỳ <b>${mmR[10]}%</b> · 20 kỳ <b>${mmR[20]}%</b> · 50 kỳ <b>${mmR[50]}%</b> · 100 kỳ <b>${mmR[100]}%</b></div>`:''}
    ${mmH.length?`<details class="bg-wh"><summary><b>${mmH.length} kỳ gần</b> — đúng ${mmH.filter(h=>h.dung).length}/${mmH.length} kỳ</summary>${mmH.map(h=>`<div class="bg-tk"><span class="bg-h20d">${h.d}</span>${h.goi.map(k=>`<span class="bg-b${k===h.ra?' mm hit':''}">${p2(k)}</span>`).join('')}<small style="flex-basis:auto;padding-left:6px;">về <b>${p2(h.ra)}</b> ${h.dung?'<b class="bg-ok">✔</b>':'✘'}</small></div>`).join('')}</details>`:''}
    <div class="bg-foot">Chạy lại đúng cách này ở từng kỳ (chỉ dùng số may mắn các kỳ trước). Số khoanh = số gợi ý trùng số về.</div></div>`:'';
  const h20K=(typeof window!=='undefined'&&window.__h20K)||18;if(typeof window!=='undefined'){if(window.__dangJ&&window.__dangJ.game!==J.game)window.__dangTk=null;window.__h20J=J;window.__dangJ=J;}
  const h20=hist20HTML(J,h20K);
  // Bố cục 4 khối (anh 15/10/2026: "mỗi block đều rối và khó hiểu"): Mua gì → Dạng → Pool → Vì sao; phần nâng cao gom cuối.
  const shut=(typeof window!=='undefined'&&(window.__bgShut=window.__bgShut||new Set()))||new Set();
  const STW=J.stale?`<div class="bg-warn" style="margin:4px 0 8px;">Phần này là gợi ý của app cho kỳ ${J.nextBase} (đã có kết quả). Gợi ý cho kỳ ${J.next} có sau khi chạy cập nhật.</div>`:'';
  const TKH=(()=>{if(!J.stale||!J.tickets)return '';const i=J.dates201.indexOf(J.nextBase);if(i<0)return '';const r=J.res201[i],lk=J.lk201?J.lk201[i]:null;
    return `<div class="bg-foot" style="margin:0 0 8px;">Vé app kỳ ${J.nextBase} trúng: ${J.tickets.map((t,q)=>`V${q+1} <b>${t.x.filter(n=>r.includes(n)).length}</b>${J.game==='loto'&&t.lk!=null&&t.lk===lk?' +MM':''}`).join(' · ')}</div>`;})();
  const sec=(key,title,sub,body,open)=>`<details class="bg-sec bg-main" data-k="${key}"${(open&&!shut.has(key))||(typeof window!=='undefined'&&window.__bgOpen&&window.__bgOpen.has('m:'+key))?' open':''}><summary><h4>${title}</h4>${sub?`<small class="bg-subt">${sub}</small>`:''}</summary>${(['mua','dang','visao'].includes(key)?STW:'')}${key==='mua'?TKH:''}${body}</details>`;
  const sub=(title,body)=>body?`<details class="bg-wh bg-sub"><summary><b>${title}</b></summary>${body}</details>`:'';
  const unwrap=h=>{const m=(h||'').match(/^<div class="bg-sec"><h4>([\s\S]*?)<\/h4>([\s\S]*)<\/div>$/);return m?sub(m[1],m[2]):'';};
  // 1. Mua gì
  const TKS=(PK!==18&&J.ticketsK&&J.ticketsK[PK])||J.tickets;   // vé theo cỡ pool đang chọn (anh 16/10/2026)
  const veRows=TKS.map((t,i)=>`<div class="bg-tk${t.kind.startsWith('cân nhắc')?' alt':''}"><span class="bg-ti">${i+1}</span>${ltWrap(t.x,n=>ball(n,(strong.has(n)?'tl ':'')+(t20.has(n)?'':'out')))}${t.lk?ball(t.lk,'mm'):''}<small>tổng ${t.sum}${t.kind.startsWith('cân nhắc')?' · vé tâm linh':''}</small></div>`).join('');
  const mmLine=J.mm&&J.mm.length?`<div class="bg-row" style="margin-top:6px;">Số may mắn ưu tiên: ${J.mm.map(k=>ball(k,'mm')).join('')}${mmR?`<small style="margin-left:6px;">cả ${J.mm.length} số đoán đúng ${mmR[50]}% (50 kỳ) · ${mmR[100]}% (100 kỳ)</small>`:''}</div>`:'';
  const S1=sec('mua','3. Mua gì kỳ này',`${TKS.length} vé rải trên pool ${PK>25?18:PK}${PK>25?' (pool '+PK+' chỉ để xem tỉ lệ trúng)':''}, đã vừa dạng ở mục 2`,`<div class="bg-row bg-chips">${POOLK.filter(k=>(J.pools&&J.pools[k])||k<=rk.length).map(k=>`<span class="bg-h20k${k===PK?' on':''}" onclick="poolSet(${k})">Pool ${k}</span>`).join('')}</div>${veRows}${mmLine}
    <div class="bg-foot">Vé rải đều trên pool ${PK} (chọn cỡ pool ở trên — đổi cả khối Pool), rồi đổi ít số nhất cho vừa mọi luật dạng. Sổ theo dõi chấm bộ vé pool 18. Nền tím = số tâm linh mạnh · gạch chân = ngoài pool 20.</div>`,false);
  // 2. Dạng
  const K=J.khuon||{},du=(K.du||[]),mn=d=>Math.min(d.a50,d.a100);
  const line=(lab,a,b)=>`<div class="bg-dgr on" style="grid-template-columns:1fr auto;"><span>${lab}</span><em>${a}% / ${b}%</em></div>`;
  const chac=[...(K.rules||[]),...(K.lienhe||[])].map(r=>line(r.lab,r.a50,r.a100)).join('');
  const kha=du.filter(d=>mn(d)>=70).sort((x,y)=>mn(y)-mn(x)).map(d=>line(`${d.mat}: <b>${d.du}</b>`,d.a50,d.a100)).join('');
  const yeu=du.filter(d=>mn(d)<70).sort((x,y)=>mn(y)-mn(x)).map(d=>`<div class="bg-dgr" style="grid-template-columns:1fr auto;opacity:.6;"><span>${d.mat}: ${d.du}</span><em>${d.a50}% / ${d.a100}%</em></div>`).join('');
  const tongL=`<div class="bg-foot">Tổng thường gặp (80% kỳ): ${J.sumRange[0]}–${J.sumRange[1]}${J.day6?' (tính cả số may mắn)':''}${(K.rules||[]).some(r=>r.id==='tongthuong')?'':' — chưa ép vào vé (ghép vào làm cả bộ luật tụt dưới 70%)'}${J.da&&J.da.n?` · đà tổng đang bật: nghiêng tổng ${J.da.cao?'>'+J.da.mid:'≤'+J.da.mid} (đúng ${J.da.k}/${J.da.n} lần đà bật)`:''}.</div>`;
  const S2=sec('dang','2. Dạng kỳ tới',K.tien!=null?`kết quả thật lọt cả bộ luật (chấm tiến): ${K.tien}% ở 50 kỳ · ${K.tien10}/10 kỳ gần${K.tien<70?' — dưới 70%':''}`:'',
    `<div class="bg-dgh"><b>Chắc</b> <small>— luật vé đang áp, % đúng 50 / 100 kỳ</small></div>${chac||'<div class="bg-foot">Kỳ này không có luật nào đạt.</div>'}
     ${kha?`<div class="bg-dgh" style="margin-top:8px;"><b>Khá</b> <small>— dạng gợi ý đúng ≥70%, chưa ép vào vé</small></div>${kha}`:''}
     ${tongL}
     ${sub('Yếu (dưới 70%, chỉ tham khảo)',yeu)}
     ${J.res201?sub('Kiểm 1 dãy · bảng % từng mặt',`<div id="dang">${dangHTML(J)}</div>`):''}`,false);
  // 3. Pool
  const ptS=J.poolThuc&&J.poolThuc.stat&&J.poolThuc.stat[PK];
  const ptTab=J.poolThuc?`<div class="tw"><table><thead><tr><th class="l">Pool</th><th>TB số trúng<br><small>50 / 100 kỳ</small></th><th>% số trúng nằm trong pool<br><small>50 / 100 kỳ</small></th><th>≥3 số<br><small>10 / 20 / 50 / 100 kỳ</small></th><th>≥4 số<br><small>10 / 20 / 50 / 100 kỳ</small>${J.kb>=5?'<th>≥5 số<br><small>10 / 20 / 50 / 100 kỳ</small></th>':''}${J.kb>=6?'<th>≥6 số<br><small>10 / 20 / 50 / 100 kỳ</small></th>':''}</tr></thead><tbody>${Object.entries(J.poolThuc.stat).sort((a,b)=>a[0]-b[0]).map(([k,r])=>`<tr${+k===PK?' style="background:rgba(255,255,255,.06)"':''}><td class="l"><b>${k}</b></td><td>${r['50'][0]} / ${r['100'][0]}</td><td>${Math.round(r['50'][0]/J.kb*100)}% / ${Math.round(r['100'][0]/J.kb*100)}%</td><td>${['10','20','50','100'].map(w=>r[w][2]+'%').join(' / ')}</td><td>${['10','20','50','100'].map(w=>r[w][3]+'%').join(' / ')}</td>${J.kb>=5?`<td>${['10','20','50','100'].map(w=>(r[w][4]??'–')+'%').join(' / ')}</td>`:''}${J.kb>=6?`<td>${['10','20','50','100'].map(w=>(r[w][5]??'–')+'%').join(' / ')}</td>`:''}</tr>`).join('')}</tbody></table></div><div class="bg-foot">Mỗi kỳ dựng lại pool đúng cách app đang dùng, chỉ bằng dữ liệu trước kỳ đó (đến ${J.poolThuc.den}).</div>`:'';
  const cach=[J.poolChon&&J.poolChon[PK]?`Cộng / trừ điểm riêng pool ${PK}: ${J.poolChon[PK].length?J.poolChon[PK].map(([nm,w])=>`${nm.replace('TL: ','')} ${w>0?'+':''}${w}`).join(' · '):'không cộng gì'}`:'',
    J.hangOn&&J.hangOn.length&&(PK===10||PK===15)?`Hàng ${J.hangOn.map(h=>h+'x').join(', ')} ra nhiều 10 kỳ → pool ${PK} chỉ giữ 1 số mỗi hàng đó`:'',
    J.poolCach?`Thứ tự gộp 50/50 với ${J.poolCach}`:''].filter(Boolean).map(x=>`<div class="bg-foot">${x}</div>`).join('');
  // 10 kỳ gần trên pool (anh 15/10/2026): số ra ≥2 lần trong 10 kỳ tô màu theo số lần lặp (2 / 3 / 4 / ≥5), ra 1 lần không tô
  const KN0=(typeof window!=='undefined'&&[5,10,15,20,25,30,50].includes(window.__k10N))?window.__k10N:20;
  const KG=J.game==='loto'&&typeof window!=='undefined'&&['13h','21h'].includes(window.__k10G)?window.__k10G:'';   // lọc giờ quay (chỉ Loto)
  const KR=rgGet('k'),IX=KR?rgPick(J,'k',KN0,KG):rgPick(J,'k',50,KG),KN=KR?IX.length:KN0;   // khoảng ngày đang bật → hiện đủ các kỳ trong khoảng
  const sesPrev=(i,n)=>{let j=i;for(let c=0;c<n;c++){j--;if(KG)while(j>=0&&!String(J.dates201[j]).endsWith(KG))j--;if(j<0)return null;}return J.res201[j];},P2=IX.map(i=>sesPrev(i,2));   // kỳ cách 1 kỳ (anh 19/10/2026)
  const R10=IX.map(i=>J.res201[i]),D10=IX.map(i=>J.dates201[i]),L10=IX.map(i=>(J.lk201||[])[i]),P10=IX.map((i,k)=>KG?(k?J.res201[IX[k-1]]:(()=>{for(let j=i-1;j>=0;j--)if(String(J.dates201[j]).endsWith(KG))return J.res201[j];})()):J.res201[i-1]),C10={};   // P10 = kỳ liền trước trong danh sách đang xem (lọc giờ thì so với kỳ cùng giờ trước)   // hiển thị 20 kỳ (anh 16/10/2026); màu lặp tính theo đúng số kỳ đang chọn (5/10/15/20/25/30/50)
  R10.slice(-KN).forEach(r=>r.forEach(n=>C10[n]=(C10[n]||0)+1));
  // MỖI số lặp (≥2 lần) một màu riêng (anh 15/10/2026: "sao lại dùng chung màu cho nhiều số") — tránh màu cam của số may mắn
  const PAL=['#e6194b','#4363d8','#3cb44b','#ffe119','#911eb4','#42d4f4','#f032e6','#bfef45','#469990','#dcbeff','#9a6324','#fabed4','#800000','#aaffc3','#808000','#000075','#a9a9a9','#e6beff','#00ced1','#b8860b','#ff69b4','#7fffd4'];
  const SANG=new Set(['#ffe119','#42d4f4','#bfef45','#dcbeff','#fabed4','#aaffc3','#a9a9a9','#e6beff','#00ced1','#7fffd4']);
  const LAP=Object.keys(C10).map(Number).filter(n=>C10[n]>=2).sort((x,y)=>x-y),MAU={},CHU={};
  // 17/10/2026 (anh: "thiếu màu, màu trùng lại còn cạnh nhau"): mỗi số lặp một màu RIÊNG sinh theo góc vàng — số liền nhau lệch ~137° màu,
  // xen 3 độ sáng; bỏ vùng cam (màu số may mắn). Không lặp màu dù nhiều số.
  { // bảng màu N màu riêng (không xám, bỏ vùng cam); rồi gán màu sao cho số đứng cạnh nhau trong cùng dòng có màu khác xa nhất
    const N=LAP.length,pal=[...Array(N).keys()].map(i=>{let h=(i*137.508)%312;if(h>=6)h+=48;let L=[48,66,34][i%3];const S=i%2?90:76;if((h<6||h>335)&&L>50)L=40;return {h,S,L};});
    const rgb=c=>{const s=c.S/100,l=c.L/100,k=n=>(n+c.h/30)%12,a=s*Math.min(l,1-l),f=n=>l-a*Math.max(-1,Math.min(k(n)-3,9-k(n),1));return [f(0)*255,f(8)*255,f(4)*255];};
    pal.forEach(c=>c.rgb=rgb(c));const chuOf=c=>{const l=c.rgb.map(v=>{v/=255;return v<=.03928?v/12.92:((v+.055)/1.055)**2.4;});return .2126*l[0]+.7152*l[1]+.0722*l[2]>.179?'#111':'#fff';};const dist=(p,q)=>{const x=p.rgb,y=q.rgb,r=(x[0]+y[0])/2;return Math.sqrt((2+r/256)*(x[0]-y[0])**2+4*(x[1]-y[1])**2+(2+(255-r)/256)*(x[2]-y[2])**2);};
    const nb={};LAP.forEach(n=>nb[n]=new Set());
    const link=(a,c)=>{if(a!==c&&nb[a]&&nb[c]){nb[a].add(c);nb[c].add(a);}},RS=R10.slice(-KN).map(r=>[...r].sort((x,y)=>x-y));
    RS.forEach((s,k)=>{for(let i=0;i<s.length;i++){for(let j=i+1;j<=i+2&&j<s.length;j++)link(s[i],s[j]);   // cùng dòng: liền kề và cách 1 ô
      const t=RS[k+1];if(t)for(let j=i-1;j<=i+1;j++)if(j>=0&&j<t.length)link(s[i],t[j]);}});   // dòng trên – dưới: cùng cột và chéo 1 ô (anh 17/10/2026)
    const used=new Set(),ord=[...LAP].sort((x,y)=>nb[y].size-nb[x].size||x-y);
    ord.forEach(n=>{let best=-1,bv=-1;pal.forEach((c,i)=>{if(used.has(i))return;const ds=[...nb[n]].filter(m=>MAU[m]).map(m=>dist(c,pal[MAU[m].i]));const v=ds.length?Math.min(...ds):999;if(v>bv){bv=v;best=i;}});
      used.add(best);const c=pal[best];MAU[n]={i:best,css:`hsl(${c.h.toFixed(1)} ${c.S}% ${c.L}%)`};CHU[n]=chuOf(c);});
    // tinh chỉnh: đổi chéo màu giữa 2 số nếu làm các cặp kề (ngang, trên–dưới) bớt giống nhau (phạt khi khoảng cách màu < 220)
    const pen=(n,ci)=>[...nb[n]].reduce((s,m)=>s+Math.max(0,240-dist(pal[ci],pal[MAU[m].i]))**2,0);
    for(let pass=0;pass<10;pass++){let better=false;
      for(let x=0;x<LAP.length;x++)for(let y=x+1;y<LAP.length;y++){const u=LAP[x],v=LAP[y],cu=MAU[u].i,cv=MAU[v].i;
        const before=pen(u,cu)+pen(v,cv);MAU[u].i=cv;MAU[v].i=cu;const after=pen(u,cv)+pen(v,cu);
        if(after+1e-6<before)better=true;else{MAU[u].i=cu;MAU[v].i=cv;}}
      if(!better)break;}
    LAP.forEach(n=>{const c=pal[MAU[n].i];MAU[n]=`hsl(${c.h.toFixed(1)} ${c.S}% ${c.L}%)`;CHU[n]=chuOf(c);});}
  const lball=n=>MAU[n]?`<span class="bg-b" style="background:${MAU[n]};border-color:${MAU[n]};color:${CHU[n]};">${p2(n)}</span>`:null;
  const pm1=(h,n,pv,cl=['pm1','pm2','pm3'])=>{if(!pv||!h)return h;const P=new Set(pv);if(P.has(n))return h;const u=P.has(n-1),d=P.has(n+1);const c=u&&d?cl[2]:u?cl[0]:d?cl[1]:'';return c?h.replace('class="bg-b','class="bg-b '+c):h;};   // +1: n = số kỳ trước +1 · −1: n = số kỳ trước −1 (anh 18/10/2026)
  const HCOL=['#ff6b6b','#ffd93d','#6bcb77','#4d96ff','#c77dff','#ff9f43'];   // mỗi hàng chục một màu: 0 đỏ · 1 vàng · 2 xanh lá · 3 xanh dương · 4 tím · 5 cam
  const k10H=R10.length?`${vxBlock(J)}<details class="bg-wh" style="margin:6px 0;"${typeof window!=='undefined'&&window.__k10Open?' open':''} ontoggle="k10Tog(this)"><summary><b>${KR?`${rgLabel(J,IX)} · ${KN} kỳ`:`${KN} kỳ gần nhất`}${KG?' · chỉ '+KG:''}</b> <small>— màu tính trong ${KN} kỳ đang xem: số ra ≥2 lần có một màu riêng, ra 1 lần không tô</small></summary>
    <div class="bg-row bg-chips">${[5,10,15,20,25,30,50].map(n=>`<span class="bg-h20k${!KR&&n===KN?' on':''}" onclick="k10Set(${n})">${n} kỳ</span>`).join('')}</div>
    <div class="bg-row bg-chips">${rgUI(J,'k',KN0,KG)}</div>
    ${J.game==='loto'?`<div class="bg-row bg-chips">${[['','13h &amp; 21h'],['13h','Chỉ 13h'],['21h','Chỉ 21h']].map(([g,t])=>`<span class="bg-h20k${g===KG?' on':''}" onclick="k10Gio('${g}')">${t}</span>`).join('')}</div>`:''}
    ${R10.map((r,i)=>[r,D10[i],L10[i],P10[i],IX[i],P2[i]]).slice(-KN).reverse().map(([r,d,lk,pv,ix,p2k])=>`<div class="bg-row bg-pool bg-k10"><small class="bg-k10d">${String(d).replace(/\/\d{4}/,'')}</small>${ltWrap(r,n=>pm1(pm1(lball(n)||ball(n,''),n,pv),n,p2k,['qm1','qm2','qm3']))}${J.game==='loto'&&lk!=null?ball(lk,'mm')+mmDelta(J,ix,KG):''}${(()=>{const a=[...r].sort((x,y)=>x-y),c=a.filter(n=>n%2===0).length;return `<small class="bg-k10i">${a.map(n=>{const h=Math.floor(n/10);return `<i style="color:${HCOL[h%HCOL.length]};">${h}</i>`;}).join('-')} <b>${a.reduce((x,y)=>x+y,0)}</b> ${c}C:${a.length-c}L</small>`;})()}</div>`).join('')}
    <div class="bg-foot" style="margin:2px 0 0;">Dấu đen +1 / −1 / ±1 góc dưới phải = số đó hơn / kém / kề hai phía một số của kỳ liền trước; <b style="background:#d62828;color:#fff;border-radius:4px;padding:0 3px;">dấu đỏ</b> góc trên trái = so với kỳ cách 1 kỳ (số lặp không dấu). Bên phải mỗi kỳ: hàng chục từng số · tổng · số chẵn (C) / lẻ (L), tính 5 số chính.${KG?` Đang lọc chỉ kỳ ${KG}: màu lặp và dấu ±1 so với kỳ ${KG} liền trước.`:''}${J.game==='loto'?' Bóng cam = số may mắn; số nhỏ bên phải = hơn / kém số may mắn kỳ liền trước'+(KG?' cùng giờ '+KG:'')+' (<b style="color:#3fb950">+ xanh</b>, <b style="color:#ff4d4f">− đỏ</b>).':''}</div></details>${qhBlock(J,ball,p2,HCOL)}`:'';
  const secP=(sub,body)=>`<div class="bg-poolblk">${sub?`<div class="bg-subt" style="display:block;margin-bottom:6px;">${sub}</div>`:''}${body}</div>`;   // Pool = block lớn riêng, nằm trên 'Gợi ý kỳ tới' (anh 16/10/2026)
  const BAN=J.stale?`<div class="bg-foot" style="margin:0 0 6px;color:var(--ac);">Pool đang áp dụng cho kỳ <b>${J.next}</b>${(()=>{const i=J.dates201.indexOf(J.nextBase);if(i<0||!J.pools)return '';const r=J.res201[i];return `<br><span style="color:var(--text,#e8ecf5);">Pool app kỳ ${J.nextBase} trúng: ${Object.keys(J.pools).map(Number).sort((x,y)=>x-y).map(k=>`P${k} <b>${J.pools[k].filter(n=>r.includes(n)).length}</b>`).join(' · ')}</span>`;})()}</div>`:'';
  const S3=secP(ptS?`pool ${PK}: kỳ trúng ≥3 số ${ptS['100'][2]}% · ≥4 số ${ptS['100'][3]}% (100 kỳ)`:'',
    `${BAN}${(()=>{
    // Pool từ x kỳ gần nhất, lưới cố định 0x…(anh 16/10/2026): số trong pool sáng màu game, chạm để bỏ/chọn, Lưu = pool của anh
    const PN=(typeof window!=='undefined'&&[5,10,15,20,25,30,50].includes(window.__ppN))?window.__ppN:10;
    const PH=J.game==='loto'&&typeof window!=='undefined'&&['13h','21h'].includes(window.__ppH)?window.__ppH:'',PR=rgGet('p'),PIX=rgPick(J,'p',PN,PH);
    const RR=PIX.map(i=>J.res201[i]),PLB=PR?`${rgLabel(J,PIX)} (${PIX.length} kỳ${PH?', chỉ '+PH:''})`:`${PN} kỳ gần nhất${PH?' (chỉ '+PH+')':''}`;if(!RR.length&&!PR)return '';
    const cnt={};RR.forEach(r=>r.forEach(n=>cnt[n]=(cnt[n]||0)+1));
    const ns=Object.keys(cnt).map(Number).sort((a,b)=>a-b);if(typeof window!=='undefined')window.__ppX=ns;window.__ppG=J.game;window.__ppK=J.next;
    const sv=ppGet(J.game,J.next),ed=!!window.__ppEd&&Array.isArray(window.__ppW),lit=new Set(ed?window.__ppW:(sv||ns));
    // dấu ngay trên số (anh 17/10/2026): ✕ = app loại hẳn kỳ này, chấm tím = tâm linh mạnh — để cân nhắc số có thêm cơ sở
    const WL=((J.poolWhy&&(J.poolWhy['18']||Object.values(J.poolWhy)[0]))||{}).loai||[],PLO=new Map(WL.filter(x=>x.loai==='hẳn').map(x=>[x.n,x.why])),PTL=new Set((J.tl&&J.tl.strong)||[]);
    // số tình nghi (anh 17/10/2026): số của luật loại có tỉ lệ ra thấp hơn các số còn lại (50 & 100 kỳ) + nhóm hạng cuối nếu nhóm đó ra ít nhất
    const NG=J.nghi,PNG=new Map();if(NG&&!J.stale){(NG.luat||[]).forEach(l=>l.nums.forEach(n=>{if(PLO.has(n))return;const a=PNG.get(n)||[];a.push(`${l.lab.replace(/</g,'&lt;').replace(/>/g,'&gt;')}: ra ${l.r100}% số kỳ, số khác ${l.o100}%`);PNG.set(n,a);}));
      const nh=NG.nhom||{};if(nh.cuoi&&nh.dau&&nh.giua&&nh.cuoi.pct<nh.dau.pct&&nh.cuoi.pct<nh.giua.pct)(NG.cuoi||[]).forEach(n=>{if(PLO.has(n))return;const a=PNG.get(n)||[];a.push(`nhóm ${NG.bg} số điểm thấp nhất: ra ${nh.cuoi.pct}% số kỳ, nhóm đầu ${nh.dau.pct}%`);PNG.set(n,a);});}
    const cell=n=>{const on=lit.has(n),c=cnt[n]||0;
      const b=`<span class="bg-b bg-ppc${on?' on':''}${PLO.has(n)?' lo':PNG.has(n)?' ng':''}"${ed?` onclick="ppTog(${n})"`:''}>${p2(n)}</span>`;
      const x=`<span class="bg-ppx">${b}${c>=2?`<sup>${c}</sup>`:''}${PTL.has(n)?'<i class="pp-t"></i>':''}</span>`;return n%11===0&&on?`<span class="bg-kep">${x}</span>`:x;};
    const rows=[...Array(Math.floor(J.nb/10)+1).keys()].map(d=>`<div class="bg-row bg-pool bg-hang bg-ppr"><b>${d}x:</b>${[...Array(10).keys()].map(u=>{const n=d*10+u;return n<1||n>J.nb?'<span class="bg-ppe"></span>':cell(n);}).join('')}</div>`).join('');
    const btn=(t,f)=>`<span class="bg-h20k" onclick="${f}">${t}</span>`;
    const tools=ed?btn('Lưu pool','ppSave()')+btn('Hủy','ppCancel()')+btn(`Lấy lại pool ${PR?'theo ngày đã chọn':PN+' kỳ'}`,'ppFromX()'):btn('Sửa pool','ppStart()')+(sv?btn('Xóa pool kỳ này','ppDel()'):'');
    const ttl=ed?`Đang sửa — ${lit.size} số`:sv?`Pool của anh cho kỳ ${J.next} (đã lưu) — ${lit.size} số`:`Pool số đã ra ${PR?PLB:'trong '+PLB} — ${ns.length} số`;
    return `${vlBlock(J,[...lit].sort((a,b)=>a-b),sv||ed?'pool của anh':`pool ${PLB}`,sub)}<div class="bg-dgh" style="margin-top:12px;"><b>${ttl}</b> <small>${ed?'— chạm số sáng để bỏ, chạm số tối để chọn, xong bấm Lưu pool':'— số sáng = trong pool, số xám = ngoài pool; số nhỏ ở góc = số lần ra trong khoảng đang chọn (từ 2 lần)'}</small></div>
    <div class="bg-row bg-chips"><small>Lấy từ:</small>${[5,10,15,20,25,30,50].map(n=>`<span class="bg-h20k${!PR&&n===PN?' on':''}" onclick="ppSet(${n})">${n} kỳ</span>`).join('')}</div>
    <div class="bg-row bg-chips">${rgUI(J,'p',PN,PH)}</div>${J.game==='loto'?`<div class="bg-row bg-chips">${[['','13h &amp; 21h'],['13h','Chỉ 13h'],['21h','Chỉ 21h']].map(([g,t])=>`<span class="bg-h20k${g===PH?' on':''}" onclick="ppGio('${g}')">${t}</span>`).join('')}</div>`:''}${rows}${PLO.size||PTL.size||PNG.size?sub(`Giải thích`,`<div class="bg-foot" style="margin:4px 0 0;">${PLO.size?`<b style="background:#111;color:#fff;border-radius:6px;padding:0 4px;">số đen</b> = app loại${J.stale?` (kỳ ${J.nextBase})`:''}: ${[...PLO].sort((a,b)=>a[0]-b[0]).map(([n,w])=>`<b>${p2(n)}</b>: ${w.replace(/ · /g,', ')}`).join(' | ')}`:''}${PLO.size&&PTL.size?'<br>':''}${PTL.size?`<b>●</b> chấm trắng = tâm linh mạnh: ${[...PTL].sort((a,b)=>a-b).map(p2).join(' ')}`:''}${PNG.size?`<br><b style="color:#b46cff;">chữ tím</b> = tình nghi: ${[...PNG].sort((a,b)=>a[0]-b[0]).map(([n,w])=>`<b>${p2(n)}</b>: ${w.join('; ')}`).join(' | ')}`:''}</div>`):''}<div class="bg-row bg-chips" style="margin-top:6px;">${tools}</div>${(()=>{
      const bk=ppBook(J.game),ks=Object.keys(bk);if(!ks.length)return '';
      const idx={};(J.dates201||[]).forEach((d,i)=>idx[d]=i);
      let dirty=false;
      const L=ks.map(k=>{const e=bk[k],p=e.n,i=idx[k];
        // kỳ đã có kết quả → chấm luôn và KHÓA (anh 16/10/2026): lưu số trúng cố định, không sửa lại được
        if(i!=null&&!e.lock){e.lock=true;e.hit=p.filter(n=>(J.res201[i]||[]).includes(n));dirty=true;}
        return {k,p,hit:e.lock?e.hit:null,lock:!!e.lock,t:e.t||0,i};}).sort((a,b)=>kyKey(b.k)-kyKey(a.k)).slice(0,12);
      if(dirty)ppPut(J.game,bk);const sc=L.filter(x=>x.hit);const rt=m=>sc.length?Math.round(sc.filter(x=>x.hit.length>=m).length*100/sc.length)+'%':'—';
      const rowsT=L.map(x=>`<tr><td class="l">${x.k}${x.lock?' <small title="đã chấm, đã khóa">🔒</small>':''}</td><td>${x.p.length}</td><td>${x.hit?`<b>${x.hit.length}/${J.kb}</b>`:'<small>chờ kết quả</small>'}</td><td class="l">${x.hit?(x.hit.length?x.hit.map(p2).join(' '):'—'):''}</td></tr>`).join('');
      return sub(`Sổ pool của anh (${L.length} kỳ gần nhất) — mỗi kỳ 1 pool, lưu lại thì thay bản cũ`,`      <div class="tw"><table><thead><tr><th class="l">Kỳ</th><th>Cỡ</th><th>Trúng</th><th class="l">Số trúng</th></tr></thead><tbody>${rowsT}</tbody></table></div>
      <div class="bg-foot">${sc.length?`Đã chấm và khóa ${sc.length} kỳ: ≥3 số ${rt(3)} · ≥4 số ${rt(4)} · ≥5 số ${rt(5)}`:'Chưa có kỳ nào có kết quả để chấm.'} · ${btn('Sao chép sổ','ppCopy()')}</div>`);})()}`;})()}${k10H}<div class="bg-dgh" style="margin-top:8px;"><b>Pool gợi ý</b> <small>— số có màu riêng = đã lặp trong 10 kỳ gần (cùng màu với bảng trên)</small></div><div class="bg-row bg-chips">${POOLK.filter(k=>(J.pools&&J.pools[k])||k<=rk.length).map(k=>`<span class="bg-h20k${k===PK?' on':''}" onclick="poolSet(${k})">Pool ${k}</span>`).join('')}</div>
    ${[...Array(Math.floor(J.nb/10)+1).keys()].map(d=>{const ns=PL.filter(n=>Math.floor(n/10)===d).sort((x,y)=>x-y);return `<div class="bg-row bg-pool bg-hang"><b>${d}x:</b>${ns.length?ns.map(n=>{const h=lball(n)||ball(n,'');return n%11===0?`<span class="bg-kep">${h}</span>`:h;}).join(''):'<small>—</small>'}</div>`;}).join('')}
    ${(()=>{const W=J.poolWhy&&J.poolWhy[PK];if(!W)return '';
      const lo=W.loai,han=lo.filter(x=>x.loai==='hẳn'),co=lo.filter(x=>x.loai==='luật cỡ'),di=lo.filter(x=>x.loai==='điểm').sort((a,b)=>b.d-a.d);
      const row=(x,extra)=>`<div class="bg-row" style="align-items:flex-start;gap:6px;">${lball(x.n)||ball(x.n,'')}<small style="flex:1;">${extra||''}${x.why||'—'}${x.them&&x.them.length?' · cộng riêng pool '+PK+': '+x.them.join(', '):''}${x.mix&&x.mix.length?' · <i>'+x.mix.join(', ')+'</i>':''}</small></div>`;
      return `<div class="bg-dgh" style="margin-top:8px;"><b>Vì sao chọn ${W.chon.length} số này</b> <small>— xếp theo thứ hạng; điểm = tổng tín hiệu cộng / trừ${W.note.length?' · '+W.note.join(' · '):''}</small></div>
      ${W.chon.map(x=>row(x,`<b>điểm ${x.d}</b> · `)).join('')}
      <div class="bg-dgh" style="margin-top:8px;"><b>Vì sao không chọn ${lo.length} số còn lại</b></div>
      ${han.length?`<div class="bg-foot" style="margin:2px 0;"><b>Bị loại hẳn</b> (luật loại, mọi cỡ pool):</div>${han.map(x=>row(x)).join('')}`:''}
      ${co.length?`<div class="bg-foot" style="margin:2px 0;"><b>Luật riêng của pool ${PK}</b>:</div>${co.map(x=>row(x)).join('')}`:''}
      ${di.length?sub(`Điểm thấp, xếp dưới ngưỡng pool ${PK} (${di.length} số)`,di.map(x=>row(x,`<b>điểm ${x.d}</b> · `)).join('')):''}`;})()}
    ${sub('Độ trúng của mọi cỡ pool',ptTab)}
    ${h20?sub(`Pool trúng mấy số ở ${(J.hist20||[]).length} kỳ gần`,`<div id="h20">${h20}</div>`):''}
    ${sub('Pool này chọn thế nào',cach)}`,false);
  // 4. Vì sao
  const lui=(J.chay&&J.chay.length)?`${J.chay.map(c=>`<div class="bg-row bg-pool"><b style="min-width:150px;">${c.nm}</b> <small style="min-width:120px;">về ${c.h10}/10 · ${c.h20}/20 kỳ</small> ${c.nums.map(n=>ball(n,inP.has(n)?'t10':'')).join('')}</div>`).join('')}<div class="bg-foot">Thứ, ngày, tháng (dương và âm) đã về trúng ≥3 trong 10 kỳ hoặc ≥4 trong 20 kỳ gần. Số tô màu = đang trong pool ${PK}.</div>`:'';
  const vlH=J.vl&&J.vl.length?`<div style="overflow-x:auto;"><table class="bg-vl"><thead><tr><th>Số</th><th>Vắng</th><th>Ra 50/100 kỳ</th><th>Mức ra</th><th>Hay nghỉ ≥15</th><th>Dài nhất</th><th>Ra ngay kỳ kế*</th><th>Nhận định</th></tr></thead><tbody>${J.vl.map(v=>`<tr><td><b>${p2(v.n)}</b></td><td>${v.gap}</td><td>${v.c100}/${v.c200}</td><td>${v.thua}%</td><td>${v.long15}%</td><td>${v.maxg}</td><td>${v.po==null?'—':v.po+'%'} <small>(${v.pn})</small></td><td class="${v.verdict==='Loại'?'vlx':v.verdict.startsWith('Nghiêng')?'vln':'vlt'}">${v.verdict}</td></tr>`).join('')}</tbody></table></div><div class="bg-foot">*Những lần chính số đó đã vắng tới mức hiện tại thì bao nhiêu % ra ngay kỳ kế.</div>`:'';
  const ngH=J.nong&&J.nong.length?`<div style="overflow-x:auto;"><table class="bg-vl"><thead><tr><th>Số</th><th>10 kỳ</th><th>20 kỳ</th><th>50/100</th><th>Kỳ kế*</th><th>Trạng thái</th></tr></thead><tbody>${J.nong.map(v=>`<tr><td><b>${p2(v.n)}</b></td><td>${v.c10}</td><td>${v.c20}</td><td>${v.c100}/${v.c200}</td><td>${v.nx==null?'—':v.nx+'%'}</td><td>${v.state}</td></tr>`).join('')}</tbody></table></div><div class="bg-foot">*Trong 300 kỳ, những lần số đó nóng tương tự thì kỳ kế ra bao nhiêu %.</div>`:'';
  const S4=sec('visao','4. Vì sao các số này','',`<div class="bg-foot" style="margin-top:0;">Rê chuột / chạm vào từng số để xem lý do cộng, trừ điểm.</div>
    <div class="bg-grid" style="grid-template-columns:repeat(${cols},1fr);">${grid}</div>
    <div class="bg-leg"><span><i class="bg-sw t10"></i>trong pool ${PK}</span><span><i class="bg-sw tx"></i>bị loại</span><span>★ tâm linh mạnh</span><span>☆ tâm linh</span><span><i class="bg-hot"></i> nóng</span><span><i class="bg-sw lastd"></i>vừa ra</span>${linh.size?'<span>✦ linh cảm</span>':''}</div>
    ${sub('Dấu vết ngày đang chạy',lui)}
    ${unwrap(tlH)}${unwrap(mm)}
    ${sub('Số vắng lâu (≥15 kỳ)',vlH)}
    ${sub('Số ra nhiều gần đây (10/20 kỳ)',ngH)}
    ${sub('Khẳng định kỳ này (đúng ≥70% số kỳ)',cl)}`,false);
  // 5. Nâng cao
  const S5=sec('nangcao','Nâng cao','pool thô · rải vé 6 kiểu · nhịp pool',`
    ${sub('Pool tín hiệu thô (chưa cộng điểm từng cỡ), 100 kỳ',`${tierRow(10,'Pool 10')}${tierRow(15,'Pool 15')}${tierRow(18,'Pool 18')}${tierRow(20,'Pool 20')}<div class="bg-foot">Pool 15 thô trúng mấy số ở 10 kỳ gần:</div><div class="bg-spk">${spark}</div>`)}
    ${wh?sub('Rải vé bao phủ trên pool (6 kiểu)',wh+'<div class="bg-foot">Ít vé nhất mà vẫn chắc trúng khi đủ số về nằm trong pool. Tiền vé luôn lớn hơn thưởng TB.</div>'):''}
    ${J.nhip?`<div class="bg-foot">Nhịp pool thô 5 kỳ gần: ${J.nhip.last.join(', ')} → TB ${J.nhip.m5} (ngưỡng ${J.nhip.thr}). Chấm trên pool thô, chưa kiểm chứng — không dùng để quyết đánh mạnh / nhẹ.</div>`:''}`,false);
  if(typeof window!=='undefined')window.__bgPool=`<div class="bg" style="--ac:${ac};--act:${J.game==='mega'?'#fff':'#111'};">${S3}</div>`;
  return `<div class="bg" style="--ac:${ac};--act:${J.game==='mega'?'#fff':'#111'};">
  <div class="bg-hd"><div><b>${J.name}</b> · kỳ <b>${J.next}</b></div><div class="bg-foot">Kỳ trước ${J.last}: ${ltWrap(J.lastRes,n=>ball(n,'lr'))}</div></div>
  ${S2}${S1}${S4}${S5}
  </div>`;
}
const BANG_CSS=`/* khung khoanh vẽ bằng outline → KHÔNG chiếm chỗ, số các hàng thẳng cột (anh 16/10/2026) *//* 16/10/2026: điện thoại vẽ outline sai màu (đen) → dùng lớp viền ::before đặt tuyệt đối (mọi trình duyệt hỗ trợ), vẫn không chiếm chỗ */.bg-lt,.bg-kep,.bg-lon{display:inline-flex;align-items:center;position:relative;}.bg-lt{gap:inherit;}.bg-lt::before,.bg-kep::before,.bg-lon::before{content:'';position:absolute;pointer-events:none;border-color:var(--text,#e8ecf5);opacity:.8;}.bg-lt::before{top:-3px;right:-3px;bottom:-3px;left:-3px;border-width:1.5px;border-style:dotted;border-radius:16px;}.bg-kep::before{top:-2px;right:-2px;bottom:-2px;left:-2px;border-width:1.5px;border-style:solid;border-radius:4px;opacity:.65;}.bg-lon::before{top:-2px;right:-2px;bottom:-2px;left:-2px;border-width:1.5px;border-style:dashed;border-radius:4px;}.bg-b.pm1,.bg-b.pm2,.bg-b.pm3{position:relative;}.bg-b.pm1::after,.bg-b.pm2::after,.bg-b.pm3::after{position:absolute;right:-5px;bottom:-5px;font-size:.5rem;line-height:1;font-weight:800;background:#000;color:#fff;border:1px solid #fff;border-radius:6px;padding:1px 2px;pointer-events:none;}.bg-b.pm1::after{content:'+1';}.bg-b.qk{box-shadow:0 4px 0 0 #b46cff;}.bg-b.qv{outline:2px solid #b46cff;outline-offset:1px;}.bg-b.qs,.bg-b.qd{position:relative;}.bg-b.qs::before{content:'Σ';position:absolute;right:-5px;top:-6px;font-size:.55rem;line-height:1;font-weight:800;background:#ffb347;color:#111;border-radius:6px;padding:1px 2px;pointer-events:none;}.bg-b.qd::after{content:'×2';position:absolute;right:-6px;bottom:-5px;font-size:.5rem;line-height:1;font-weight:800;background:#4dd0c8;color:#111;border-radius:6px;padding:1px 2px;pointer-events:none;}.bg-b.qm1,.bg-b.qm2,.bg-b.qm3{position:relative;}.bg-b.qm1::before,.bg-b.qm2::before,.bg-b.qm3::before{position:absolute;left:-4px;top:-5px;font-size:.5rem;line-height:1;font-weight:800;background:#d62828;color:#fff;border:1px solid #fff;border-radius:6px;padding:1px 2px;pointer-events:none;}.bg-b.qm1::before{content:'+1';}.bg-b.qm2::before{content:'−1';}.bg-b.qm3::before{content:'±1';}.bg-b.pm2::after{content:'−1';}.bg-b.pm3::after{content:'±1';}.bg-k10{flex-wrap:nowrap!important;gap:3px;}.bg-k10 .bg-b{min-width:24px;width:24px;height:24px;font-size:.74rem;margin:0;}.bg-k10i{margin-left:8px;white-space:nowrap;font-size:.58rem;letter-spacing:-.3px;color:var(--muted,#8b93a7);padding-left:0;}.bg-k10i i{font-style:normal;}.bg-k10i b{min-width:0!important;color:var(--text,#e8ecf5);font-weight:600;}.bg-k10d{flex:0 0 38px;font-size:.62rem;white-space:nowrap;}
.bg-b.l2{background:#2f6fd6;border-color:#2f6fd6;color:#fff;}.bg-b.l3{background:#e8e14a;border-color:#e8e14a;color:#111;}.bg-b.l4{background:#e5484d;border-color:#e5484d;color:#fff;}.bg-b.l5{background:#8e4ec6;border-color:#8e4ec6;color:#fff;}.bg-sw.l2{background:#2f6fd6;}.bg-sw.l3{background:#e8e14a;}.bg-sw.l4{background:#e5484d;}.bg-sw.l5{background:#8e4ec6;}.bg-sw.mm{background:#ff8a3d;}
.bg-main>summary{cursor:pointer;list-style:none;}.bg-main>summary::-webkit-details-marker{display:none;}.bg-main>summary h4{display:inline;margin:0;}.bg-main>summary::before{content:'▸ ';color:var(--ac);}.bg-main[open]>summary::before{content:'▾ ';}.bg-subt{display:block;color:var(--muted,#8b93a7);font-size:.78rem;margin:2px 0 0 14px;}.bg-sub{margin-top:6px;}
.bg{--ac:#f0b429;color:var(--text,#e8ecf5);font-size:.9rem;}
.bg h4{margin:0 0 8px;font-size:.95rem;color:var(--ac);}
.bg-hd{display:flex;flex-wrap:wrap;justify-content:space-between;gap:6px;align-items:center;font-size:1rem;margin-bottom:8px;}
.bg-sec{background:var(--panel2,#212a40);border:1px solid var(--border,#2c3550);border-radius:12px;padding:10px;margin:10px 0;}
.bg-foot{color:var(--muted,#8b93a7);font-size:.78rem;line-height:1.45;}
.bg-grid{display:grid;gap:4px;}
.bg-c{position:relative;text-align:center;border-radius:8px;padding:7px 0;background:rgba(255,255,255,.04);border:1px solid var(--border,#2c3550);font-size:.85rem;color:var(--muted,#8b93a7);}
.bg-c b{font-weight:600;}
.bg-c.t10{background:var(--ac);color:var(--act,#111);border-color:var(--ac);}
.bg-c.t15{background:color-mix(in srgb,var(--ac) 22%,transparent);color:var(--ac);border:2px solid var(--ac);font-weight:700;}
.bg-c.t20{background:transparent;color:var(--text,#e8ecf5);border:1px dashed var(--ac);}
.bg-c.tx{text-decoration:line-through;opacity:.45;}
.bg-c.lastd{box-shadow:inset 0 -3px 0 #4aa3ff;}
.bg-st,.bg-st2,.bg-li{position:absolute;top:-6px;right:-3px;font-style:normal;font-size:.7rem;color:#c58bff;text-shadow:0 0 2px #000;}
.bg-st2{color:#9a86c4;} .bg-li{right:auto;left:-3px;color:#4ad8ff;}
.bg-hot{position:absolute;bottom:2px;left:50%;margin-left:-3px;width:6px;height:6px;border-radius:50%;background:#ff6a3d;}
.bg-leg{display:flex;flex-wrap:wrap;gap:4px 12px;margin:8px 0 4px;font-size:.75rem;color:var(--muted,#8b93a7);}
.bg-leg span{display:inline-flex;align-items:center;gap:4px;position:relative;}
.bg-leg .bg-hot{position:static;margin:0;}
.bg-sw{display:inline-block;width:12px;height:12px;border-radius:3px;border:1px solid var(--ac);}
.bg-sw.t10{background:var(--ac);} .bg-sw.t15{background:color-mix(in srgb,var(--ac) 22%,transparent);border-width:2px;} .bg-sw.t20{background:transparent;border-style:dashed;}
.bg-sw.tx{background:transparent;border-color:var(--muted,#8b93a7);opacity:.6;} .bg-sw.lastd{background:transparent;border:0;box-shadow:inset 0 -3px 0 #4aa3ff;}
.bg-row{display:flex;flex-wrap:wrap;gap:4px;align-items:center;margin:4px 0;}
.bg-ppr{flex-wrap:nowrap!important;gap:3px;}.bg-ppr .bg-b,.bg-ppe{min-width:24px;width:24px;height:24px;font-size:.74rem;margin:0;flex:0 0 24px;}.bg-ppc{background:rgba(255,255,255,.04);color:var(--muted,#8b93a7);opacity:.55;}.bg-ppc.on{background:var(--ac);border-color:var(--ac);color:#fff;opacity:1;font-weight:700;text-shadow:0 0 2px rgba(0,0,0,.55);}.bg-ppx{position:relative;display:inline-flex;}.bg-ppc.lo.on{color:#000!important;font-weight:900;text-shadow:none;}.bg-ppc.ng.on{color:#6d28d9!important;font-weight:900;text-shadow:0 0 2px #fff,0 0 2px #fff,0 0 1px #fff;}.bg-ppx .pp-x{position:absolute;top:-6px;left:-4px;font-size:.62rem;font-style:normal;font-weight:900;line-height:1;color:#ff4d4d;text-shadow:0 0 2px #000,0 0 2px #000;pointer-events:none;}.bg-ppx .pp-t{position:absolute;top:2px;left:50%;transform:translateX(-50%);width:6px;height:6px;border-radius:50%;background:#fff;border:1px solid #111;pointer-events:none;}.bg-ppx sup{position:absolute;top:-5px;right:-4px;font-size:.58rem;line-height:1;background:var(--bg,#1b2236);color:var(--text,#e8ecf5);border-radius:6px;padding:0 2px;font-weight:700;}.bg-hang{flex-wrap:nowrap;gap:3px;}.bg-hang .bg-b{min-width:26px;width:26px;height:26px;font-size:.78rem;}.bg-hang b{min-width:26px!important;}.bg-pool b{min-width:64px;font-size:.8rem;color:var(--muted,#8b93a7);font-weight:500;}
.bg-b{display:inline-flex;align-items:center;justify-content:center;min-width:28px;height:28px;border-radius:50%;font-weight:700;font-size:.82rem;background:rgba(255,255,255,.08);border:1px solid var(--border,#2c3550);}
.bg-b.t10{background:var(--ac);color:var(--act,#111);border-color:var(--ac);} .bg-b.t15{background:color-mix(in srgb,var(--ac) 22%,transparent);color:var(--ac);border:2px solid var(--ac);}
.bg-b.t20{background:transparent;border:1px dashed var(--ac);}
.bg-b.lr{min-width:24px;height:24px;font-size:.75rem;margin-left:2px;background:#4aa3ff22;border-color:#4aa3ff;}
.bg-b.core{border:3px solid var(--ac);} .bg-b.tl{background:#7c4dcc;color:#fff;} .bg-b.out{text-decoration:underline;}
.bg-b.mm{background:#ff8a3d;color:#111;}
.bg-mmg{color:var(--muted,#8b93a7);margin:0 8px 0 2px;font-size:.75rem;}
.bg-tr{margin:6px 0 10px;}
.bg-tl{display:flex;align-items:center;gap:6px;font-weight:600;margin-bottom:3px;} .bg-tl small{color:var(--muted,#8b93a7);font-weight:400;margin-left:auto;}
.bg-bars{display:grid;gap:3px;}
.bg-bar{position:relative;height:18px;border-radius:6px;background:rgba(255,255,255,.06);overflow:hidden;}
.bg-bar>span{position:absolute;inset:0 auto 0 0;background:color-mix(in srgb,var(--ac) 70%,transparent);}
.bg-bar em{position:absolute;left:6px;top:0;line-height:18px;font-style:normal;font-size:.75rem;color:#fff;text-shadow:0 0 3px #000;}
.bg-bar em small{opacity:.8;}
.bg-bar.big{height:10px;margin:3px 0;} .bg-bar.big>span{background:#3fb950;}
.bg-bar>i{position:absolute;top:-2px;bottom:-2px;width:2px;background:#fff;}
.bg-cl{margin:8px 0;} .bg-clh{display:flex;justify-content:space-between;gap:8px;font-size:.84rem;} .bg-clh b{color:#3fb950;}
.bg-cls{font-size:.72rem;color:var(--muted,#8b93a7);} .bg-ok{color:#3fb950;}
.bg-cl.tr .bg-clh span{font-weight:700;}
.bg-tk{display:flex;flex-wrap:wrap;align-items:center;gap:4px;padding:6px 0;border-bottom:1px solid var(--border,#2c3550);}
.bg-tk small{color:var(--muted,#8b93a7);font-size:.72rem;flex-basis:100%;padding-left:26px;}
.bg-tk.alt{background:rgba(124,77,204,.12);border-radius:8px;padding:6px 4px;}
.bg-ti{width:20px;color:var(--muted,#8b93a7);font-size:.8rem;}
.bg-spk{display:flex;gap:4px;align-items:flex-end;height:54px;margin-top:4px;}
.bg-sp{flex:1;height:100%;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;}
.bg-sp span{width:100%;background:var(--ac);border-radius:3px 3px 0 0;min-height:2px;}
.bg-sp small{font-size:.7rem;color:var(--muted,#8b93a7);}
.bg-chips{gap:5px;} .bg-chip{border:1px solid #7c4dcc;border-radius:12px;padding:2px 8px;font-size:.78rem;}
.bg-chip.s{background:#7c4dcc;color:#fff;} .bg-chip small{opacity:.8;}
.bg-vl{width:100%;border-collapse:collapse;font-size:.78rem;}.bg-vl th,.bg-vl td{padding:4px 3px;border-bottom:1px solid var(--border,#2c3550);text-align:center;white-space:nowrap;}.bg-vl th{color:var(--muted,#8b93a7);font-weight:500;}
.vlx{color:#ff6b6b;font-weight:700;}.vln{color:#f0b429;font-weight:700;}.vlt{color:var(--muted,#8b93a7);}
.bg-wh{border-top:1px solid var(--border,#2c3550);padding:6px 0;}.bg-wh summary{cursor:pointer;font-size:.84rem;line-height:1.5;}.bg-wh summary small{color:var(--muted,#8b93a7);}
.bg-h20w>summary{cursor:pointer;list-style:none;}.bg-h20w>summary::-webkit-details-marker{display:none;}.bg-h20w>summary h4{display:inline;}.bg-h20w>summary h4::after{content:' ▸';}.bg-h20w[open]>summary h4::after{content:' ▾';}.bg-h20w[open]>summary{margin-bottom:8px;}
.bg-g10{border-collapse:collapse;font-size:.78rem;width:100%;}.bg-g10 th,.bg-g10 td{padding:3px 6px;border-bottom:1px solid var(--border,#2c3550);text-align:center;white-space:nowrap;}.bg-g10 th{color:var(--muted,#8b93a7);font-weight:500;}
.bg-dgw{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;margin-top:6px;}
.bg-dg{border:1px solid var(--border,#2c3550);border-radius:8px;padding:6px 8px;}.bg-dgh{margin-bottom:4px;font-size:.85rem;}
.bg-dgm{font-size:.78rem;padding:1px 6px;border-radius:8px;background:rgba(255,255,255,.08);}.bg-dgm.ok{background:rgba(63,185,80,.25);}.bg-dgm.bad{background:rgba(248,81,73,.25);}
.bg-dgr{display:grid;grid-template-columns:minmax(90px,auto) 1fr auto;align-items:center;gap:6px;font-size:.78rem;padding:1px 2px;border-radius:4px;}
.bg-dgr i{display:block;height:8px;background:color-mix(in srgb,var(--ac) 55%,transparent);border-radius:4px;}.bg-dgr.on{background:rgba(63,185,80,.22);font-weight:700;}
.bg-dgr em{font-style:normal;white-space:nowrap;}
.bg-h20k{border:1px solid var(--ac);border-radius:12px;padding:3px 10px;font-size:.8rem;cursor:pointer;}.bg-h20k.on{background:var(--ac);color:var(--act,#111);font-weight:700;}
.bg-h20s{margin:6px 0;font-size:.85rem;}
.bg-h20r{border-top:1px solid var(--border,#2c3550);padding:4px 0;}.bg-h20r summary{display:flex;flex-wrap:wrap;align-items:center;gap:3px;cursor:pointer;list-style:none;}.bg-h20r summary::-webkit-details-marker{display:none;}
.bg-h20d{min-width:86px;font-size:.78rem;color:var(--muted,#8b93a7);}
.bg-h20n{margin-left:auto;font-size:.8rem;color:var(--muted,#8b93a7);}.bg-h20n.g3{color:var(--ac);font-weight:700;}.bg-h20n.g4{color:#3fb950;font-weight:700;}
.bg-h20p{padding-left:4px;}.bg-h20p small{flex-basis:100%;color:var(--muted,#8b93a7);}
.bg-b.miss{opacity:.5;}.bg-b.dim{opacity:.35;}.bg-b.hit{box-shadow:0 0 0 2px var(--panel2,#212a40),0 0 0 4px #4ad8ff;}
.bg-warn{margin-top:6px;padding:6px 8px;border-radius:8px;background:rgba(240,180,41,.12);border:1px solid #f0b429;font-size:.8rem;}`;
if(typeof module!=='undefined')module.exports={renderBang,BANG_CSS};
