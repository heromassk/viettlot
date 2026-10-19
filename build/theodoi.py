#!/usr/bin/env python3
"""Sổ kiểm chứng suy luận (lưu vào build/theodoi.json, nhúng vào app).
  python3 build/theodoi.py snap <game>                 # chụp các luật cho kỳ tới (trước khi quay)
  python3 build/theodoi.py cham <game> <ngày> n1 n2 …  # có kết quả: chấm từng luật + gợi ý đã đưa (goiy_log)
  python3 build/theodoi.py chamlai                     # chấm lại mọi kỳ đã lưu theo cách chấm hiện tại
add_result.py tự gọi cham rồi snap. Luật mới: thêm vào RULES (loại) hoặc CLAIMS (khẳng định), giữ nguyên id cũ."""
import json, os, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
GM = {'power': ('power655', 55, 6), 'mega': ('mega645', 45, 6), 'loto': ('loto535', 35, 5)}
# Luật đang ÁP DỤNG trong gợi ý (goiy.py) — để app đánh dấu
APPLIED = {'power': {'it100', 'nong35', 'nhip2', 'lt3', 'tx15', 'tx10', 'zprev', 'nhom_lokep', 'nhom_kep', 'nhom_pascal', 'nhom_cau2'},
           'mega': {'vang20', 'thua15', 'lien2', 'lt3', 'zprev', 'nong35', 'tx15', 'nong10', 'nhieu100', 'nhip2'},
           'loto': {'vang20', 'thua15', 'vang1', 'nong35', 'lt3', 'nhip2', 'nhipmin100', 'nhom_nhip80', 'nhom_nhip', 'nhom_lokep', 'nhom_k7', 'nhom_k9', 'nhom_kep', 'nhom_pascal', 'nhom_keplk', 'txph13', 'kd_vang8', 'nhom_vang8'}}
FILE = os.path.join(HERE, 'theodoi.json')

def load():
    return json.load(open(FILE, encoding='utf-8')) if os.path.exists(FILE) else {}

def ctx(R, NB, t):
    gap = {}
    for n in range(1, NB + 1):
        g = 0
        while g < t and n not in R[t - 1 - g]: g += 1
        gap[n] = g
    cnt = lambda w: {n: sum(n in R[u] for u in range(max(0, t - w), t)) for n in range(1, NB + 1)}
    return dict(gap=gap, c5=cnt(5), c10=cnt(10), c20=cnt(20), c100=cnt(100))

SESS = []   # phiên của từng kỳ (Loto: '13'/'21'; trò khác rỗng) — snap() gán
def vang_phien(R, t, G):
    """Loto: số vắng ≥G kỳ tính RIÊNG trong phiên của kỳ t (13h hoặc 21h)."""
    if not SESS: return set()
    ph = SESS[t]; idx = [u for u in range(t) if SESS[u] == ph]
    out = set()
    for n in range(1, len(R[0]) and 36):
        g = 0
        for u in reversed(idx):
            if n in R[u]: break
            g += 1
        if g >= G: out.add(n)
    return out

def taixuat_phien(R, t, only=None, G=10):
    """Loto: số vừa ra ở kỳ cùng phiên hôm trước sau khi vắng ≥G kỳ trong phiên. only='13'/'21': chỉ áp cho phiên đó."""
    if not SESS or (only and SESS[t] != only): return set()
    idx = [u for u in range(t) if SESS[u] == SESS[t]]
    if len(idx) < G + 2: return set()
    last = R[idx[-1]]
    return {n for n in last if all(n not in R[idx[-j]] for j in range(2, G + 2))}

def pascal(R, t, NB):
    d = [int(c) for c in ''.join(f'{n:02d}' for n in sorted(R[t - 1]))]
    while len(d) > 2: d = [(d[i] + d[i + 1]) % 10 for i in range(len(d) - 1)]
    v = d[0] * 10 + d[1]
    return {v} if 1 <= v <= NB else set()

def cau_chay(R, t, NB, kmin=2):
    """Soi cầu vị trí: số ghép từ chữ số vị trí i,j của kỳ trước, cầu đã chạy ≥kmin kỳ liền."""
    dig = lambda u: ''.join(f'{n:02d}' for n in sorted(R[u]))
    L = len(dig(t - 1)); out = set()
    for i in range(L):
        for j in range(L):
            if i == j: continue
            run = 0
            for back in range(1, kmin + 1):
                u = t - back; v = int(dig(u - 1)[i] + dig(u - 1)[j])
                if 1 <= v <= NB and v in R[u]: run += 1
                else: break
            v = int(dig(t - 1)[i] + dig(t - 1)[j])
            if run >= kmin and 1 <= v <= NB: out.add(v)
    return out

def WBK(c):
    """Khung xét tính chất bi: Power/Mega thay bi định kỳ → không dùng quá nhiều kỳ (anh, 05/10)."""
    return 100   # mọi game tối đa 100 kỳ (anh 15/10/2026)

def topk(d, k, rev=False): return set(sorted(d, key=lambda n: ((-d[n]) if rev else d[n], n))[:k])

# (id, nhãn, hàm(R, t, c) -> tập số bị LOẠI)
RULES = [
    ('vang20', 'Bỏ số vắng ≥20 kỳ', lambda R, t, c: {n for n in c['gap'] if c['gap'][n] >= 20}),
    ('vang25', 'Bỏ số vắng ≥25 kỳ', lambda R, t, c: {n for n in c['gap'] if c['gap'][n] >= 25}),
    ('vang30', 'Bỏ số vắng ≥30 kỳ', lambda R, t, c: {n for n in c['gap'] if c['gap'][n] >= 30}),
    ('thua15', 'Bỏ số "lâu lâu mới ra" (100 kỳ gần; ≤85% kỳ vọng) đang vắng ≥15', lambda R, t, c: {n for n in c['gap'] if c['gap'][n] >= 15 and sum(n in R[u] for u in range(max(0, t - WBK(c)), t)) <= 0.85 * min(WBK(c), t) * (5 if len(c['gap']) == 35 else 6) / len(c['gap'])}),
    ('vang1', 'Bỏ số vắng lâu nhất', lambda R, t, c: topk(c['gap'], 1, True)),
    ('vang2nd', 'Bỏ số vắng lâu nhì', lambda R, t, c: topk(c['gap'], 2, True) - topk(c['gap'], 1, True)),
    ('lien2', 'Bỏ số ra 2 kỳ liền', lambda R, t, c: R[t - 1] & R[t - 2]),
    ('nong35', 'Bỏ số ra 3 lần trong 5 kỳ', lambda R, t, c: {n for n in c['c5'] if c['c5'][n] >= 3}),
    ('lt3', 'Bỏ số ra kỳ trước VÀ kỳ t−3', lambda R, t, c: R[t - 1] & R[t - 3]),
    ('tx15', 'Bỏ số tái xuất sau vắng ≥15', lambda R, t, c: {n for n in R[t - 1] if all(n not in R[u] for u in range(max(0, t - 16), t - 1))}),
    ('tx10', 'Bỏ số tái xuất sau vắng ≥10', lambda R, t, c: {n for n in R[t - 1] if all(n not in R[u] for u in range(max(0, t - 11), t - 1))}),
    ('nong10', 'Bỏ số nóng nhất 10 kỳ (≥4 lần)', lambda R, t, c: {n for n in topk(c['c10'], 1, True) if c['c10'][n] >= 4}),
    ('it100', 'Bỏ số ra ít nhất 100 kỳ', lambda R, t, c: topk(c['c100'], 1)),
    ('nhieu100', 'Bỏ số ra nhiều nhất 100 kỳ', lambda R, t, c: topk(c['c100'], 1, True)),
    ('nhip2', 'Bỏ số nhịp "ra – vắng 2 – ra" (vừa ra lại sau đúng 2 kỳ vắng)', lambda R, t, c: {n for n in R[t - 1] if n not in R[t - 2] and n not in R[t - 3] and n in R[t - 4]}),
    ('nhipmin100', 'Bỏ số phá nhịp tối thiểu (100 kỳ: luôn nghỉ ≥x kỳ, mới nghỉ <x)', lambda R, t, c: nhip_min(R, t, len(c['gap']), 100)),
    ('nhipmin200', 'Bỏ số phá nhịp tối thiểu (100 kỳ)', lambda R, t, c: nhip_min(R, t, len(c['gap']), WBK(c))),
    ('vangph20', 'Loto: bỏ số vắng ≥20 kỳ CÙNG PHIÊN (13h đúng ~80%, 21h ngược)', lambda R, t, c: vang_phien(R, t, 20) if len(c['gap']) == 35 else set()),
    ('txph13', 'Loto 13h: bỏ số tái xuất trong phiên (ra hôm trước sau vắng ≥10 kỳ 13h)', lambda R, t, c: taixuat_phien(R, t, '13') if len(c['gap']) == 35 else set()),
    ('uprev', 'Bỏ số nhỏ nhất kỳ trước', lambda R, t, c: {min(R[t - 1])}),
    ('zprev', 'Bỏ số lớn nhất kỳ trước', lambda R, t, c: {max(R[t - 1])}),
]
def nhip_off(R, t, NB, W=100, m=5):
    """Nhịp riêng từng số: ở đúng số kỳ đang vắng hiện tại, lịch sử W kỳ của chính số đó đã gặp ≥m lần mà chưa ra lần nào."""
    out = set()
    for n in range(1, NB + 1):
        g = 0
        while g < t and n not in R[t - 1 - g]: g += 1
        seen = hit = 0; run = None
        for u in range(max(0, t - W), t):
            if run is not None and run == g: seen += 1; hit += n in R[u]
            if n in R[u]: run = 0
            elif run is not None: run += 1
        if seen >= m and hit == 0: out.add(n)
    return out

def nhip_min(R, t, NB, W, m=5):
    """Nhịp tối thiểu: trong W kỳ, số đó luôn nghỉ ≥x kỳ giữa 2 lần ra (x ≥ 1, ≥m lần ra) mà hiện mới nghỉ < x kỳ."""
    out = set()
    for n in range(1, NB + 1):
        hits = [u for u in range(max(0, t - W), t) if n in R[u]]
        if len(hits) < m: continue
        mg = min(b - a - 1 for a, b in zip(hits, hits[1:])); cur = t - 1 - hits[-1]
        if mg >= 1 and cur < mg: out.add(n)
    return out

def nhip_p(R, t, NB, W=100, P=80):
    """Ý anh: trong W kỳ gần, ≥P% số lần số đó nghỉ ≥x kỳ mới ra lại (x lớn nhất thỏa, x≥1, ≥4 khoảng nghỉ); hiện mới nghỉ <x."""
    out = set()
    for n in range(1, NB + 1):
        hits = [u for u in range(max(0, t - W), t) if n in R[u]]
        gaps = sorted(b - a - 1 for a, b in zip(hits, hits[1:]))
        if len(gaps) < 4: continue
        x = gaps[int(len(gaps) * (1 - P / 100))]
        if x >= 1 and t - 1 - hits[-1] < x: out.add(n)
    return out

_PM = {}
def power_mega(R, t):
    """Mega kỳ t: số (≤45) có ở kỳ Power ngay trước đó VÀ ở Mega kỳ trước (anh 14/10/2026, theo dõi liên hệ Power→Mega)."""
    if not _PM:
        D = json.load(open(os.path.join(HERE, 'all_data.json'), encoding='utf-8'))
        d = lambda s: datetime.datetime.strptime(s[:10], '%d/%m/%Y')
        _PM.update(md=[d(s) for s in D['mega645']['dates']], pd=[d(s) for s in D['power655']['dates']], pr=D['power655']['res'])
    if t < len(_PM['md']):
        j = max((k for k, x in enumerate(_PM['pd']) if x < _PM['md'][t]), default=None)
    else:
        j = len(_PM['pd']) - 1
    return set() if j is None else {n for n in _PM['pr'][j] if n <= 45} & set(R[t - 1])

_DT = {}
def ngay_chay(R, t, NB):
    """Số của các dấu vết ngày "đang chạy" kỳ t (dauvet_ngay.dang_chay) — anh 14/10/2026."""
    import dauvet_ngay as DV
    if NB not in _DT:
        _DT[NB] = json.load(open(os.path.join(HERE, 'all_data.json'), encoding='utf-8'))[{35: 'loto535', 45: 'mega645', 55: 'power655'}[NB]]['dates']
    return {n for _, _, _, ns in DV.dang_chay([set(r) for r in R], _DT[NB], t, NB) for n in ns}

# (id, nhãn, hàm(R, t, c, NB, KB) -> (kind, nums, k)) — kind 'atleast': kỳ tới có ≥k số trong nums; 'atmost': ≤k số
CLAIMS = [
    ('kd_2ky', 'Có ≥1 số của 2 kỳ gần nhất', lambda R, t, c, NB, KB: ('atleast', R[t - 1] | R[t - 2], 1)),
    ('kd_nong10', 'Có ≥1 số trong 10 số nóng nhất 20 kỳ', lambda R, t, c, NB, KB: ('atleast', set(sorted(c['c20'], key=lambda n: (-c['c20'][n], c['gap'][n], n))[:10]), 1)),
    ('kd_ke', 'Có ≥1 số trùng hoặc kề ±1 kỳ trước', lambda R, t, c, NB, KB: ('atleast', {m for n in R[t - 1] for m in (n - 1, n, n + 1) if 1 <= m <= NB}, 1)),
    ('kd_trung2', 'Không trùng ≥2 số với kỳ trước', lambda R, t, c, NB, KB: ('atmost', set(R[t - 1]), 1)),
    # nhóm nhiều số: chấm "đúng" khi nhóm ra ÍT hơn bình quân (tỉ lệ trúng/số < KB/NB)
    ('nhom_nhip80', 'Nhóm "phá nhịp nghỉ" (100 kỳ: ≥80% lần nghỉ ≥x kỳ, mới nghỉ <x) ra ít hơn bình quân', lambda R, t, c, NB, KB: ('nhomit', nhip_p(R, t, NB), 0)),
    ('nhom_k7', 'Nhóm số của kỳ cách 7 kỳ ra NHIỀU hơn bình quân (dấu vết máy, 100 kỳ)', lambda R, t, c, NB, KB: ('nhomnhieu', R[t - 7] - R[t - 1], 0)),
    ('nhom_k9', 'Nhóm số của kỳ cách 9 kỳ ra NHIỀU hơn bình quân (dấu vết máy, 100 kỳ)', lambda R, t, c, NB, KB: ('nhomnhieu', R[t - 9] - R[t - 1], 0)),
    ('nhom_txph21', 'Loto 21h: nhóm tái xuất trong phiên ra NHIỀU hơn bình quân', lambda R, t, c, NB, KB: ('nhomnhieu', taixuat_phien(R, t, '21') if NB == 35 else set(), 0)),
    ('nhom_kep', 'Soi cầu: lô kép (11, 22, 33…) ra NHIỀU hơn bình quân', lambda R, t, c, NB, KB: ('nhomnhieu', set(range(11, NB + 1, 11)), 0)),
    ('nhom_pascal', 'Soi cầu: số cầu Pascal của kỳ trước ra NHIỀU hơn bình quân', lambda R, t, c, NB, KB: ('nhomnhieu', pascal(R, t, NB), 0)),
    ('nhom_cau2', 'Soi cầu: cầu vị trí đã chạy ≥2 kỳ ra NHIỀU hơn bình quân', lambda R, t, c, NB, KB: ('nhomnhieu', cau_chay(R, t, NB, 2), 0)),
    ('nhom_keplk', 'Soi cầu: kép liền kề của kép kỳ trước (11↔22↔33) ra NHIỀU hơn bình quân', lambda R, t, c, NB, KB: ('nhomnhieu', {m for k in R[t - 1] if k % 11 == 0 for m in (k - 11, k + 11) if 11 <= m <= NB}, 0)),
    ('nhom_lokep', 'Soi cầu: lô kẹp (kỳ trước có a, a+2 → a+1) ra ÍT hơn bình quân', lambda R, t, c, NB, KB: ('nhomit', {a + 1 for a in R[t - 1] if a + 2 in R[t - 1] and a + 1 not in R[t - 1]}, 0)),
    ('kd_ngaychay', 'Có ≥1 số của dấu vết ngày đang chạy (thứ, ngày, tháng dương/âm về ≥3/10 hoặc ≥4/20 kỳ)', lambda R, t, c, NB, KB: ('atleast', ngay_chay(R, t, NB), 1)),
    ('nhom_pwmg', 'Mega: số vừa có ở Power kỳ trước VÀ Mega kỳ trước ra NHIỀU hơn bình quân', lambda R, t, c, NB, KB: ('nhomnhieu', power_mega(R, t) if NB == 45 else set(), 0)),
    ('kd_vang8', 'Có ≥1 số vắng 8 kỳ (không ra trong 8 kỳ gần) — anh 19/10/2026', lambda R, t, c, NB, KB: ('atleast', set(range(1, NB + 1)) - set().union(*R[t - 8:t]), 1)),
    ('nhom_vang8', 'Nhóm số vắng 8 kỳ ra NHIỀU hơn bình quân (anh 19/10/2026)', lambda R, t, c, NB, KB: ('nhomnhieu', set(range(1, NB + 1)) - set().union(*R[t - 8:t]), 0)),
    ('nhom_nhip', 'Nhóm nhịp riêng "lúc vắng thế này chưa từng ra" ra ít hơn bình quân', lambda R, t, c, NB, KB: ('nhomit', nhip_off(R, t, NB), 0)),
]

def snap(game):
    key, NB, KB = GM[game]
    D = json.load(open(os.path.join(HERE, 'all_data.json')))[key]
    R = [set(r) for r in D['res']]; T = len(R); c = ctx(R, NB, T)
    global SESS
    SESS = (['13' if '13h' in x else '21' for x in D['dates']] + ['13' if '21h' in D['dates'][-1] else '21']) if game == 'loto' else []
    rules = [dict(id=i, lab=l, kind='loai', nums=sorted(f(R, T, c)), applied=i in APPLIED[game]) for i, l, f in RULES]
    for i, l, f in CLAIMS:
        kind, nums, k = f(R, T, c, NB, KB)
        rules.append(dict(id=i, lab=l, kind=kind, nums=sorted(nums), k=k, applied=i in APPLIED[game]))
    db = load(); g = db.setdefault(key, {'hist': []})
    g['pending'] = dict(after=D['dates'][-1], made=datetime.datetime.now().strftime('%d/%m/%Y %H:%M'), rules=rules)
    json.dump(db, open(FILE, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f'snap {key}: {len(rules)} luật cho kỳ sau {D["dates"][-1]}')
    w10(game)

def w10(game, W=10):
    """Chấm lùi liên tục W kỳ gần nhất (anh 15/10/2026: "liên tục chấm cho 10 kỳ gần nhất"): mỗi kỳ t dựng lại luật chỉ bằng dữ liệu
    trước t rồi chấm với kết quả kỳ t. Ghi db[key]['w10'] — app lấy cột "Đúng" và chấm màu từ đây."""
    key, NB, KB = GM[game]
    D = json.load(open(os.path.join(HERE, 'all_data.json')))[key]
    R = [set(r) for r in D['res']]; T = len(R)
    global SESS
    SESS = (['13' if '13h' in x else '21' for x in D['dates']] + ['13' if '21h' in D['dates'][-1] else '21']) if game == 'loto' else []
    out = {}
    for t in range(T - W, T):
        c = ctx(R, NB, t)
        rs = [dict(id=i, lab=l, kind='loai', nums=sorted(f(R, t, c))) for i, l, f in RULES]
        for i, l, f in CLAIMS:
            kind, nums, k = f(R, t, c, NB, KB); rs.append(dict(id=i, lab=l, kind=kind, nums=sorted(nums), k=k))
        for r in rs:
            g = grade(r, R[t], NB, KB); o = out.setdefault(r['id'], dict(lab=r['lab'], kind=r['kind'], ok=[], gh=0, gn=0))
            o['ok'].append(g['ok'])
            if g['ok'] is not None: o['gh'] += len(g['hit']); o['gn'] += len(g['nums'])
    db = load(); g = db.setdefault(key, {'hist': []})
    g['w10'] = dict(dates=D['dates'][T - W:], rules=out)
    json.dump(db, open(FILE, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f'w10 {key}: chấm lùi {W} kỳ ({D["dates"][T - W]} → {D["dates"][-1]}), {len(out)} luật')

def grade(r, res, NB, KB):
    """Chấm 1 luật với kết quả res. ok=None: kỳ này luật không có số nào để xét (không tính vào %).
    Luật nhóm (nhomit/nhomnhieu) chấm bằng tỉ lệ ra CỘNG DỒN của nhóm so với bình quân KB/NB (app tự cộng hit/nums),
    ok từng kỳ chỉ để tô chấm."""
    hit = sorted(set(r['nums']) & res)
    if r['kind'] in ('atleast', 'atmost') and 'k' not in r:   # kỳ cũ chưa lưu k: giữ kết quả đã chấm (cách chấm luật này không đổi)
        return dict(r, hit=hit)
    if r['kind'] == 'loai': ok = not hit
    elif r['kind'] == 'atleast': ok = len(hit) >= r['k']
    elif r['kind'] in ('nhomit', 'nhomnhieu'):
        ok = None if not r['nums'] else ((len(hit) / len(r['nums']) < KB / NB) if r['kind'] == 'nhomit' else (len(hit) / len(r['nums']) > KB / NB))
    else: ok = len(hit) <= r['k']
    return dict(id=r['id'], lab=r['lab'], kind=r['kind'], nums=r['nums'], hit=hit, ok=ok, applied=r.get('applied', False), **({'k': r['k']} if 'k' in r else {}))

def chamlai():
    """Chấm lại mọi kỳ đã lưu theo cách chấm hiện tại (sau khi sửa lỗi chấm)."""
    db = load()
    for game, (key, NB, KB) in GM.items():
        for h in db.get(key, {}).get('hist', []):
            h['rules'] = [grade(r, set(h['res']), NB, KB) | dict(applied=r['id'] in APPLIED[game]) for r in h['rules']]
        for r in db.get(key, {}).get('pending', {}).get('rules', []): r['applied'] = r['id'] in APPLIED[game]
    json.dump(db, open(FILE, 'w', encoding='utf-8'), ensure_ascii=False)

def cham(game, date, nums, extra=None):
    key, NB, KB = GM[game]
    db = load(); g = db.setdefault(key, {'hist': []}); p = g.get('pending'); res = set(nums)
    if not p: print('chưa có ảnh chụp luật cho kỳ này — bỏ qua'); return
    out = [grade(r, res, NB, KB) for r in p['rules']]
    rec = dict(date=date, res=sorted(res), rules=out)
    if extra is not None: rec['extra'] = extra
    # gợi ý đã đưa anh (bản lưu cuối cùng trong goiy_log cho trò này)
    lg = os.path.join(HERE, 'goiy_log.jsonl')
    if os.path.exists(lg):
        last = None
        for line in open(lg, encoding='utf-8'):
            if line.strip():
                j = json.loads(line)
                if j['game'] == game and j['next'] == date: last = j
        if last:
            rk = last.get('rank') or last['pool']
            rec['goiy'] = dict(p10=len(set(rk[:10]) & res), p15=len(set(last['pool']) & res), p20=len(set(rk[:20]) & res),
                               best=max((len(set(t) & res) for t in last['tickets']), default=0),
                               tl=len(set(last.get('tamlinh', [])) & res), core=sorted(set(last.get('core', [])) & res),
                               mm=(extra in last.get('mm', [])) if (extra is not None and last.get('mm')) else None)
            rec['goiy']['p18'] = len(set(rk[:18]) & res)
            if last.get('khuon') is not None:   # khuôn dạng kỳ tới: dạng thật có lọt khuôn không (14/10/2026)
                import khuon as KH
                D0 = json.load(open(os.path.join(HERE, 'all_data.json'), encoding='utf-8'))[key]
                prev = D0['res'][D0['dates'].index(date) - 1] if date in D0['dates'] else D0['res'][-1]
                rec['goiy']['khuon'] = all(KH.check(sp, sorted(res), extra if game == 'loto' else None, prev, NB, KB) for sp in last['khuon'])
            if last.get('pools'):   # mỗi cỡ pool có thứ hạng riêng (14/10/2026)
                P = last['pools']
                for k, key in (('10', 'p10'), ('15', 'p15'), ('18', 'p18'), ('20', 'p20')):
                    if P.get(k): rec['goiy'][key] = len(set(P[k]) & res)
            if last.get('rank_cu'):   # cách cũ chấm song song (14/10/2026)
                rc = last['rank_cu']; rec['goiy']['cu'] = dict(p10=len(set(rc[:10]) & res), p15=len(set(rc[:15]) & res), p18=len(set(rc[:18]) & res), p20=len(set(rc[:20]) & res))
    va = os.path.join(HERE, 've_anh.jsonl')   # vé anh đã mua
    if os.path.exists(va):
        mine = [json.loads(l) for l in open(va, encoding='utf-8') if l.strip()]
        mine = [m for m in mine if m['game'] == game and m['date'] == date]
        if mine: rec['ve_anh'] = [dict(x=m['x'], mm=m.get('mm'), hit=sorted(set(m['x']) & res), mmhit=(m.get('mm') == extra) if m.get('mm') is not None else None) for m in mine]
    g['hist'] = [h for h in g['hist'] if h['date'] != date] + [rec]
    g.pop('pending', None)
    json.dump(db, open(FILE, 'w', encoding='utf-8'), ensure_ascii=False)
    okn = sum(r['ok'] is True for r in out); nx = sum(r['ok'] is not None for r in out)
    print(f'cham {key} {date}: {okn}/{nx} luật đúng' + (f" · gợi ý pool15 trúng {rec['goiy']['p15']}, vé tốt nhất {rec['goiy']['best']}" if 'goiy' in rec else ''))

if __name__ == '__main__':
    if sys.argv[1] == 'snap': snap(sys.argv[2])
    elif sys.argv[1] == 'chamlai': chamlai()
    elif sys.argv[1] == 'w10': [w10(g) for g in (sys.argv[2:] or GM)]
    elif sys.argv[1] == 'cham':
        xs = [int(x) for x in sys.argv[4:]]; KB = GM[sys.argv[2]][2]
        cham(sys.argv[2], sys.argv[3], xs[:KB], xs[KB] if len(xs) > KB else None)
