#!/usr/bin/env python3
"""Tự kiểm TOÀN BỘ app (anh 15/10/2026: "kiểm tra lại hết"). Mỗi mục in ĐẠT / LỖI kèm chi tiết. Chạy sau capnhat.py.
  python build/kiemtra_tong.py            (thêm --nohtml để bỏ phần mở app bằng trình duyệt)"""
import datetime as dt, json, os, sys
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B); ROOT = os.path.dirname(B)
GM = {'loto': ('loto535', 35, 5), 'mega': ('mega645', 45, 6), 'power': ('power655', 55, 6)}
J = lambda f: json.load(open(os.path.join(B, f), encoding='utf-8'))
LOI = []; N = [0]
def chk(ok, lab, chi=''):
    N[0] += 1; print(f"  {'ĐẠT' if ok else 'LỖI'} · {lab}" + ('' if ok or not chi else f'  → {chi}'))
    if not ok: LOI.append(lab)

# file kết quả phải MỚI HƠN code tạo ra nó (15/10/2026: pool_thuc.json không được ghi lại vì lỗi mà không mục nào bắt được)
for out, codes in (('pool_thuc.json', ('pool_app.py',)), ('luat_ve.json', ('luat_ve.py', 'khuon.py', 'lienhe_dang.py')), ('kep_pool.json', ('kep_pool.py',))):
    mo = os.path.getmtime(os.path.join(B, out)); mc = max(os.path.getmtime(os.path.join(B, c)) for c in codes)
    if mo < mc: print(f'  LỖI · {out} cũ hơn code ({", ".join(codes)}) — chạy lại'); LOI.append(f'{out} cũ hơn code')
DATA = J('all_data.json'); PC = J('pool_chon.json'); KP = J('kep_pool.json'); PT = J('pool_thuc.json'); LV = J('luat_ve.json'); KA = J('kiemtra_app.json')
TD = J('theodoi.json'); LOG = [json.loads(l) for l in open(os.path.join(B, 'goiy_log.jsonl'), encoding='utf-8') if l.strip()]
import luat_ve as LVm, pool_app as PA, khuon as KH

for g, (key, NB, KB) in GM.items():
    print(f'\n== {g}')
    D = DATA[key]; R = [set(r) for r in D['res']]; T = len(R); last = D['dates'][-1]
    # 1. dữ liệu
    bad = [i for i, r in enumerate(D['res']) if len(r) != KB or len(set(r)) != KB or min(r) < 1 or max(r) > NB]
    chk(not bad, f'Dữ liệu {T} kỳ, mỗi kỳ {KB} số khác nhau trong 1–{NB}', f'kỳ lỗi {bad[:5]}')
    chk(len(set(D['dates'])) == T, 'Không trùng ngày quay')
    if g == 'loto': chk(len(D['lk']) == T and all(1 <= x <= 12 for x in D['lk']), 'Số may mắn đủ và trong 1–12')
    # 2. độ mới của các bước
    for nm, v in (('bộ cộng điểm pool (pool_chon)', PC[g].get('den')), ('giới hạn kép (kep_pool)', KP[g].get('den')),
                  ('chấm pool thật (pool_thuc)', PT[g].get('den')), ('bộ luật vé (luat_ve)', LV[g].get('den'))):
        chk(v == last, f'{nm} cập nhật tới kỳ cuối {last}', f'đang ở {v}')
    chk(KA[g]['L'] == T, 'Tâm linh từng kỳ (kiemtra_app) đủ kỳ', f"{KA[g]['L']} / {T}")
    G = J(f'goiy_latest/{g}.json')
    chk(G['last'] == last, f'Gợi ý dựng sau kỳ cuối {last}', f"đang sau {G['last']}")
    # 3. pool
    vang = set(G.get('vang', []))
    for K in map(str, PA.KS):
        p = G['pools'][K]
        chk(len(p) == int(K) and len(set(p)) == len(p) and not (set(p) & vang), f'Pool {K}: đủ {K} số, không trùng, không chứa số bị loại', f'{len(p)} số, loại lọt {sorted(set(p) & vang)}')
    kc = KP[g].get('cap', {})
    for K, c in kc.items():
        chk(sum(1 for n in G['pools'][K] if n % 11 == 0) <= c, f'Pool {K}: tối đa {c} số kép (luật đã áp)')
    chk(G['poolThuc'] == PT[g], 'Bảng "Pool trúng bao nhiêu" trong app = số chấm pool thật')
    # 4. luật vé: dựng lại độc lập phải giống app
    LKA = D['lk'] if g == 'loto' else None
    BV = LVm.build(R, LKA, NB, KB, T, g)
    labs = [r['lab'] for r in BV['rules'] + BV['lienhe']]; labs_app = [r['lab'] for r in G['khuon']['rules'] + G['khuon']['lienhe']]
    chk(labs == labs_app, 'Luật vé trong app = dựng lại độc lập', f'app {labs_app} · dựng lại {labs}')
    chk(set(LV[g]['nhom']) >= set(LV[g].get('pin', [])), 'Luật anh ghim có trong bộ chọn', str(LV[g].get('pin')))
    chk(G['khuon']['pass50'] == LV[g]['pass50'] and G['khuon']['pass100'] == LV[g]['pass100'], f"% lọt khuôn hiển thị = chấm tiến cả bộ ({LV[g]['pass50']}/{LV[g]['pass100']}%)")
    t = LV[g].get('tien')
    if t is not None and t < 70:
        why = f"do anh ghim {LV[g]['pin']}" if LV[g].get('pin') else 'luật dạng của game này yếu khi chấm tiến'
        print(f"  CẢNH BÁO · Cả bộ luật vé chấm tiến chỉ {t}% (10 kỳ gần {LV[g].get('tien10')}/10), dưới 70% — {why}")
    else: chk(t is not None and t >= 70, 'Cả bộ luật vé chấm tiến ≥70%', str(t))
    chk(G['khuon'].get('tien') == t, 'App hiện đúng % chấm tiến của bộ luật vé', f"app {G['khuon'].get('tien')} · {t}")
    # 5. vé
    tk = G['tickets']; prev = sorted(R[-1])
    can = (G.get('tl') or {}).get('out') or []   # vé thứ 7 (thay thế tâm linh) chỉ có khi tâm linh mạnh nằm ngoài pool 18
    chk(len(tk) == (7 if can else 6), f"{7 if can else 6} vé (vé tâm linh thay thế {'có' if can else 'không cần'})", f'{len(tk)} vé')
    xs = [tuple(t['x']) for t in tk]
    chk(len(set(xs)) == len(xs), 'Không có vé trùng nhau')
    chk(all(len(set(x)) == KB and all(1 <= v <= NB for v in x) for x in xs), f'Mỗi vé {KB} số khác nhau trong 1–{NB}')
    nok = [i + 1 for i, t in enumerate(tk) if not LVm.ok(BV, sorted(t['x']), t.get('lk'), prev, NB, KB)]
    chk(not nok, 'Mọi vé vừa đủ bộ luật vé', f'vé lệch: {nok}')
    for K, TK in (G.get('ticketsK') or {}).items():   # vé theo từng cỡ pool (anh 16/10/2026)
        bad = [i + 1 for i, t in enumerate(TK) if not LVm.ok(BV, sorted(t['x']), t.get('lk'), prev, NB, KB)]
        ng = [i + 1 for i, t in enumerate(TK) if 'tâm linh' not in t['kind'] and not set(t['x']) <= set(G['pools'][K]) | set(G['pools']['25'])]
        chk(TK and not bad and not ng and len({tuple(t['x']) for t in TK}) == len(TK), f'Vé pool {K}: {len(TK)} vé vừa luật, không trùng, lấy số trong pool {K}/25', f'lệch {bad} · ngoài pool {ng}')
    p25 = set(G['pools']['18']) | set(G['pools']['25']) | set((G.get('tl') or {}).get('strong', []))   # vé rải lấy từ pool 18; đổi số lấy thêm từ pool 25
    out = [(i + 1, sorted(set(t['x']) - p25)) for i, t in enumerate(tk) if set(t['x']) - p25 and 'tâm linh' not in t['kind']]
    chk(not out, 'Vé thường chỉ dùng số trong pool 18 hoặc 25', f'{out}')
    if g == 'loto': chk(all(t.get('lk') for t in tk), 'Vé Loto có số may mắn')
    # 6. sổ theo dõi + log
    tdk = TD.get(key, {})
    chk((tdk.get('w10') or {}).get('dates', [None])[-1] == last, 'Sổ theo dõi: chấm 10 kỳ gần tới kỳ cuối', str((tdk.get('w10') or {}).get('dates', [])[-1:]))
    chk((tdk.get('pending') or {}).get('after') == last, 'Sổ theo dõi: đã chụp luật cho kỳ tới')
    lg = [l for l in LOG if l['game'] == g and l['next'] == G['next']]
    chk(bool(lg) and lg[-1].get('pools') == G['pools'] and lg[-1]['tickets'] == [t['x'] for t in tk], f"Gợi ý kỳ {G['next']} đã lưu vào sổ (đúng bản đang hiện)")

# 7. app
if '--nohtml' not in sys.argv:
    print('\n== app index_loto.html')
    from playwright.sync_api import sync_playwright
    import pathlib
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(pathlib.Path(os.path.join(ROOT, 'index_loto.html')).as_uri()); pg.wait_for_timeout(2500)
        for gk, (key, NB, KB) in GM.items():
            r = pg.evaluate("""(k)=>{try{setGame(k);renderBangCard();renderTD();const b=document.getElementById('bangIn'),t=document.getElementById('tdIn');
              return {bang:b?b.textContent.length:0,pool:(()=>{const p=document.getElementById('poolIn');return p?p.textContent.includes('Độ trúng của mọi cỡ pool'):false;})(),td:t?t.textContent.length:0,nd:S.M.nd,gy:GOIY[k.replace(/\\d+/,'')]?GOIY[k.replace(/\\d+/,'')].next:null};}catch(e){return {err:String(e)}}}""", key)
            chk('err' not in r and r['bang'] > 1000 and r['pool'], f'{gk}: bảng gợi ý hiện đủ (có bảng pool thật)', str(r))
            chk('err' not in r and r['td'] > 500, f'{gk}: sổ theo dõi hiện được', str(r))
            if 'err' not in r and r.get('gy'): chk(r['gy'] == r['nd'], f'{gk}: gợi ý đúng kỳ tới của app', f"gợi ý {r['gy']} · app {r['nd']}")
        chk(not errs, 'Không có lỗi JavaScript', '; '.join(errs[:3]))
        b.close()

print(f"\n### Tổng: {N[0] - len(LOI)}/{N[0]} đạt" + (f" · LỖI: {'; '.join(LOI)}" if LOI else ' · không có lỗi'))
