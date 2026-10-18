#!/usr/bin/env python3
"""Bản Python của tamlinh.js (máy Windows không có Playwright cho Node): lấy từ app (index_loto.html) phiếu tâm linh
20 phương pháp, pool app, phương pháp tốt nhất 50 kỳ. In JSON giống hệt tamlinh.js.
  python build/tamlinh.py power|mega|loto > tl.json"""
import json, sys, pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
gi = {'loto': 0, 'mega': 1, 'power': 2}[sys.argv[1]]
JS = r"""()=>{const {out:O,N}=S.PS,ids=PM.map(q=>q[0]).filter(id=>O[id]&&O[id][N]),hk=(id,t,K)=>{const rk=rankH(id,t);return rk?rk.filter(x=>x<K).length:null;};
  const best={};for(const K of [12,15,18]){let bi=null,bv=-1;for(const id of ids){let h=0,n=0;for(let t=N-50;t<N;t++){const x=hk(id,t,K);if(x==null)continue;h+=x;n++;}if(n&&h/n>bv){bv=h/n;bi=id;}}best[K]={id:bi,tb:+bv.toFixed(2),pool:topK(O[bi][N],K).sort((a,b)=>a-b)};}
  return {next:S.M.nd,votes:S.kx.nv,methods:KX_M.map((m,i)=>[m[1],S.kx.now[i]?S.kx.now[i].nums:[]]),appPool:S.sg.pool.slice().sort((a,b)=>a-b),appMethod:S.sg.sel,appTickets:(S.sg.G.ranked||S.sg.G.tickets).map(t=>t.x),best50:best};}"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1100, 'height': 900})
    pg.goto((ROOT / 'index_loto.html').as_uri()); pg.wait_for_timeout(3000)
    pg.evaluate("()=>{$('toolsCard').open=true;}"); pg.click('#sgCard > summary')
    pg.click(f'#gameTabs .gtab >> nth={gi}'); pg.wait_for_timeout(4000)
    pg.evaluate("()=>{$('tqCard').open=true;renderTarot();}")
    pg.wait_for_function("()=>S.kx&&S.kx.nv", timeout=120000)
    r = pg.evaluate(JS); b.close()
sys.stdout.reconfigure(encoding='utf-8'); print(json.dumps(r, ensure_ascii=False))
