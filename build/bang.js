// Bảng gợi ý trực quan — dùng chung cho app (thẻ đầu trang) và ảnh gửi trong chat.
// renderBang(J) -> HTML. J = dữ liệu từ `goiy.py --json`.
function renderBang(J){
  if(!J)return '<div class="bg-foot">Chưa có bảng gợi ý cho trò này.</div>';
  const COL={power:'#f0b429',mega:'#ff5c8a',loto:'#3fb950'},ac=COL[J.game]||'#f0b429';
  const p2=n=>String(n).padStart(2,'0'),pct=v=>v==null?'—':Math.round(v)+'%';
  const rk=J.rank,t10=new Set(rk.slice(0,10)),t15=new Set(rk.slice(0,15)),t20=new Set(rk.slice(0,20));
  const vang=new Set(J.vang),hot=new Set(J.hot),tl=J.tl||{},strong=new Set(tl.strong||[]),top=new Set(tl.top||[]),linh=new Set(J.linh||[]),last=new Set(J.lastRes);
  const core=new Set(J.core);
  const ball=(n,cls,extra)=>`<span class="bg-b ${cls||''}"${extra||''}>${p2(n)}</span>`;
  const tierCls=n=>t10.has(n)?'t10':t15.has(n)?'t15':t20.has(n)?'t20':vang.has(n)?'tx':'';
  // 1. Lưới số
  const cols=J.nb===35?7:J.nb===45?9:11;
  let grid='';for(let n=1;n<=J.nb;n++){
    const mk=(strong.has(n)?'<i class="bg-st">★</i>':top.has(n)?'<i class="bg-st2">☆</i>':'')+(hot.has(n)?'<i class="bg-hot"></i>':'')+(linh.has(n)?'<i class="bg-li">✦</i>':'');
    grid+=`<div class="bg-c ${tierCls(n)}${last.has(n)?' lastd':''}" title="${(J.why[n]||'').replace(/"/g,'')}"><b>${p2(n)}</b>${mk}</div>`;}
  // 2. Thang pool
  const tierRow=(k,lab)=>{const a=J.tiers[k],b=J.tiers50[k];return `<div class="bg-tr"><div class="bg-tl"><span class="bg-sw ${k===10?'t10':k===15?'t15':'t20'}"></span>${lab}<small>TB ${a[4].toFixed(2)} số/kỳ</small></div>
    <div class="bg-bars">${[0,1,2].map(j=>`<div class="bg-bar"><span style="width:${a[j]}%;"></span><em>≥${j+1} số: <b>${pct(a[j])}</b> <small>(50 kỳ ${pct(b[j])})</small></em></div>`).join('')}</div></div>`;};
  // 3. Khẳng định
  const cl=J.claims.filter(c=>c.r200>=70).sort((a,b)=>b.r200-a.r200).map(c=>`<div class="bg-cl${c.trace?' tr':''}">
    <div class="bg-clh"><span>${c.lab}</span><b>${pct(c.r200)}</b></div>
    <div class="bg-bar big"><span style="width:${c.r200}%;"></span><i style="left:${c.keep}%;" title="vé giữ lại"></i></div>
    <div class="bg-cls">50 kỳ gần ${pct(c.r50)} · vé giữ lại ${pct(c.keep)}${c.trace?' · <b class="bg-ok">✔ có dấu vết (đúng > giữ)</b>':''}</div></div>`).join('');
  // 4. Vé
  const tk=J.tickets.map((t,i)=>`<div class="bg-tk${t.kind.startsWith('cân nhắc')?' alt':''}"><span class="bg-ti">${i+1}</span>${t.x.map(n=>ball(n,(core.has(n)?'core ':'')+(strong.has(n)?'tl ':'')+(t20.has(n)?'':'out'))).join('')}<small>${t.kind}${t.lv>0&&t.lv<3?' · nới ràng buộc':''} · tổng ${t.sum}</small></div>`).join('');
  // 5. 10 kỳ gần
  const mx=Math.max(4,...J.last10);
  const spark=J.last10.map(h=>`<div class="bg-sp" title="${h} số"><span style="height:${h/mx*100}%;"></span><small>${h}</small></div>`).join('');
  // 6. Tâm linh
  const tlH=J.tl?`<div class="bg-sec"><h4>Tâm linh · ${tl.nm} quẻ</h4>
    <div class="bg-row">Dãy tâm linh: ${tl.day.map(n=>ball(n,'tl')).join('')}</div>
    <div class="bg-row bg-chips">${tl.top.map(n=>`<span class="bg-chip${strong.has(n)?' s':''}">${p2(n)} <small>${tl.votes[n]} phiếu${t15.has(n)?'':' · ngoài pool'}</small></span>`).join('')}</div>
    ${tl.out&&tl.out.length?`<div class="bg-warn">⚠ Tâm linh mạnh ngoài pool: <b>${tl.out.map(p2).join(' ')}</b> — xem vé "cân nhắc tâm linh".</div>`:''}
    ${tl.rescued&&tl.rescued.length?`<div class="bg-foot">Được cứu khỏi luật vắng: ${tl.rescued.map(p2).join(' ')}</div>`:''}</div>`:'';
  const mm=J.mm&&J.mm.length?`<div class="bg-sec"><h4>Số May Mắn</h4><div class="bg-row">${J.mm.map(k=>ball(k,'mm')+`<small class="bg-mmg">vắng ${J.mmGap[k]} kỳ</small>`).join('')}</div></div>`:'';
  return `<div class="bg" style="--ac:${ac};">
  <div class="bg-hd"><div><b>${J.name}</b> · kỳ <b>${J.next}</b></div><div class="bg-foot">Kỳ trước ${J.last}: ${J.lastRes.map(n=>ball(n,'lr')).join('')}</div></div>
  <div class="bg-sec"><h4>Pool số kỳ tới</h4>
    <div class="bg-grid" style="grid-template-columns:repeat(${cols},1fr);">${grid}</div>
    <div class="bg-leg"><span><i class="bg-sw t10"></i>Pool 10</span><span><i class="bg-sw t15"></i>đến 15</span><span><i class="bg-sw t20"></i>đến 20</span><span><i class="bg-sw tx"></i>bị loại (vắng lâu / luật loại)</span><span>★ tâm linh mạnh</span><span>☆ tâm linh</span><span><i class="bg-hot"></i> nóng</span><span><i class="bg-sw lastd"></i>vừa ra</span>${linh.size?'<span>✦ linh cảm</span>':''}</div>
    <div class="bg-row bg-pool"><b>Pool 10:</b> ${rk.slice(0,10).map(n=>ball(n,'t10')).join('')}</div>
    <div class="bg-row bg-pool"><b>+ đến 15:</b> ${rk.slice(10,15).map(n=>ball(n,'t15')).join('')}</div>
    <div class="bg-row bg-pool"><b>+ đến 20:</b> ${rk.slice(15,20).map(n=>ball(n,'t20')).join('')}</div>
    ${J.hotOut&&J.hotOut.length?`<div class="bg-warn">⚠ Số nóng ngoài pool 15: <b>${J.hotOut.map(p2).join(' ')}</b></div>`:''}
  </div>
  <div class="bg-sec"><h4>Pool trúng bao nhiêu (200 kỳ đã qua, chạy lại đúng cách này)</h4>${tierRow(10,'Pool 10')}${tierRow(15,'Pool 15')}${tierRow(20,'Pool 20')}
    <div class="bg-foot" style="margin-top:6px;">Pool 15 trúng mấy số ở 10 kỳ gần nhất:</div><div class="bg-spk">${spark}</div></div>
  <div class="bg-sec"><h4>Khẳng định kỳ này (đúng ≥ 70% số kỳ)</h4>${cl}
    <div class="bg-foot">Thanh = % kỳ đúng trong 200 kỳ. Vạch trắng = phần vé còn giữ lại nếu lọc theo khẳng định đó; thanh vượt qua vạch là có dấu vết thật.</div></div>
  <div class="bg-sec"><h4>Vé gợi ý</h4>${tk}
    <div class="bg-foot">Viền đậm = số lõi · ★ nền tím = tâm linh mạnh · gạch chân = ngoài pool 20. Tổng nên trong ${J.sumRange[0]}–${J.sumRange[1]}${J.da?' (theo đà tổng)':''}.</div></div>
  ${J.vl&&J.vl.length?`<div class="bg-sec"><h4>Số vắng lâu (≥15 kỳ)</h4><div style="overflow-x:auto;"><table class="bg-vl"><thead><tr><th>Số</th><th>Vắng</th><th>Ra 100/200 kỳ</th><th>Mức ra</th><th>Hay nghỉ ≥15</th><th>Dài nhất</th><th>Ra ngay kỳ kế*</th><th>Nhận định</th></tr></thead><tbody>${J.vl.map(v=>`<tr><td><b>${p2(v.n)}</b>${v.tl>=7?' <span class="bg-st" style="position:static">★</span>':''}</td><td>${v.gap}</td><td>${v.c100}/${v.c200}</td><td>${v.thua}%</td><td>${v.long15}%</td><td>${v.maxg}</td><td>${v.po==null?'—':v.po+'%'} <small>(${v.pn})</small></td><td class="${v.verdict==='Loại'?'vlx':v.verdict.startsWith('Nghiêng')?'vln':'vlt'}">${v.verdict}</td></tr>`).join('')}</tbody></table></div>
    <div class="bg-foot">Mức ra = số lần ra 200 kỳ so với kỳ vọng (dưới 85% = "lâu lâu mới ra"). Hay nghỉ ≥15 = % số lần nghỉ của chính số đó dài ≥15 kỳ. *Trong lịch sử của chính số, những lần nó đã vắng tới mức hiện tại thì bao nhiêu % ra ngay kỳ kế (trong ngoặc: số lần gặp).</div></div>`:''}
  ${J.nong&&J.nong.length?`<div class="bg-sec"><h4>Số ra nhiều gần đây (10/20 kỳ)</h4><div style="overflow-x:auto;"><table class="bg-vl"><thead><tr><th>Số</th><th>10 kỳ</th><th>20 kỳ</th><th>100/200</th><th>Mức ra</th><th>4 đoạn 25</th><th>Kỳ kế*</th><th>Trạng thái</th></tr></thead><tbody>${J.nong.map(v=>`<tr><td><b>${p2(v.n)}</b></td><td>${v.c10}</td><td>${v.c20}</td><td>${v.c100}/${v.c200}</td><td>${v.lr}%</td><td>${v.q4.join('/')}</td><td>${v.nx==null?'—':v.nx+'%'}</td><td>${v.state}</td></tr><tr><td></td><td colspan="7" class="${v.kind.startsWith('Nóng bền')?'vlx':v.kind.startsWith('Nóng,')?'vln':'vlt'}" style="text-align:left;white-space:normal;">${v.kind}</td></tr>`).join('')}</tbody></table></div>
    <div class="bg-foot">Mức ra = số lần ra 200 kỳ so với kỳ vọng. "Nóng bền" = 200 kỳ ra ≥115% kỳ vọng và ≥3/4 đoạn 25 kỳ ra nhiều — dấu hiệu bi dễ ra (có thể lệch trọng lượng). *Trong 300 kỳ, những lần số đó nóng tương tự (≥3 lần/10 kỳ) thì kỳ kế ra bao nhiêu %.</div></div>`:''}
  ${tlH}${mm}
  </div>`;
}
const BANG_CSS=`.bg{--ac:#f0b429;color:var(--text,#e8ecf5);font-size:.9rem;}
.bg h4{margin:0 0 8px;font-size:.95rem;color:var(--ac);}
.bg-hd{display:flex;flex-wrap:wrap;justify-content:space-between;gap:6px;align-items:center;font-size:1rem;margin-bottom:8px;}
.bg-sec{background:var(--panel2,#212a40);border:1px solid var(--border,#2c3550);border-radius:12px;padding:10px;margin:10px 0;}
.bg-foot{color:var(--muted,#8b93a7);font-size:.78rem;line-height:1.45;}
.bg-grid{display:grid;gap:4px;}
.bg-c{position:relative;text-align:center;border-radius:8px;padding:7px 0;background:rgba(255,255,255,.04);border:1px solid var(--border,#2c3550);font-size:.85rem;color:var(--muted,#8b93a7);}
.bg-c b{font-weight:600;}
.bg-c.t10{background:var(--ac);color:#111;border-color:var(--ac);}
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
.bg-pool b{min-width:64px;font-size:.8rem;color:var(--muted,#8b93a7);font-weight:500;}
.bg-b{display:inline-flex;align-items:center;justify-content:center;min-width:28px;height:28px;border-radius:50%;font-weight:700;font-size:.82rem;background:rgba(255,255,255,.08);border:1px solid var(--border,#2c3550);}
.bg-b.t10{background:var(--ac);color:#111;border-color:var(--ac);} .bg-b.t15{background:color-mix(in srgb,var(--ac) 22%,transparent);color:var(--ac);border:2px solid var(--ac);}
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
.bg-warn{margin-top:6px;padding:6px 8px;border-radius:8px;background:rgba(240,180,41,.12);border:1px solid #f0b429;font-size:.8rem;}`;
if(typeof module!=='undefined')module.exports={renderBang,BANG_CSS};
