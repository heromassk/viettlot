#!/usr/bin/env python3
"""Sổ kiểm chứng suy luận (lưu vào build/theodoi.json, nhúng vào app).
  python3 build/theodoi.py snap <game>                 # chụp các luật cho kỳ tới (trước khi quay)
  python3 build/theodoi.py cham <game> <ngày> n1 n2 …  # có kết quả: chấm từng luật + gợi ý đã đưa (goiy_log)
add_result.py tự gọi cham rồi snap. Luật mới: thêm vào RULES (loại) hoặc CLAIMS (khẳng định), giữ nguyên id cũ."""
import json, os, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
GM = {'power': ('power655', 55, 6), 'mega': ('mega645', 45, 6), 'loto': ('loto535', 35, 5)}
# Luật đang ÁP DỤNG trong gợi ý (goiy.py) — để app đánh dấu
APPLIED = {'power': {'vang20', 'it100'}, 'mega': {'vang20', 'thua15', 'lien2', 'lt3', 'zprev'}, 'loto': {'vang20', 'thua15', 'tx15', 'vang1', 'nong35'}}
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

def topk(d, k, rev=False): return set(sorted(d, key=lambda n: ((-d[n]) if rev else d[n], n))[:k])

# (id, nhãn, hàm(R, t, c) -> tập số bị LOẠI)
RULES = [
    ('vang20', 'Bỏ số vắng ≥20 kỳ', lambda R, t, c: {n for n in c['gap'] if c['gap'][n] >= 20}),
    ('vang25', 'Bỏ số vắng ≥25 kỳ', lambda R, t, c: {n for n in c['gap'] if c['gap'][n] >= 25}),
    ('vang30', 'Bỏ số vắng ≥30 kỳ', lambda R, t, c: {n for n in c['gap'] if c['gap'][n] >= 30}),
    ('thua15', 'Bỏ số "lâu lâu mới ra" (200 kỳ ≤85% kỳ vọng) đang vắng ≥15', lambda R, t, c: {n for n in c['gap'] if c['gap'][n] >= 15 and sum(n in R[u] for u in range(max(0, t - 200), t)) <= 0.85 * min(200, t) * 6 / len(c['gap']) * (5 / 6 if len(c['gap']) == 35 else 1)}),
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
    ('nhipmin200', 'Bỏ số phá nhịp tối thiểu (200 kỳ)', lambda R, t, c: nhip_min(R, t, len(c['gap']), 200)),
    ('uprev', 'Bỏ số nhỏ nhất kỳ trước', lambda R, t, c: {min(R[t - 1])}),
    ('zprev', 'Bỏ số lớn nhất kỳ trước', lambda R, t, c: {max(R[t - 1])}),
]
def nhip_off(R, t, NB, W=200, m=5):
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

# (id, nhãn, hàm(R, t, c, NB, KB) -> (kind, nums, k)) — kind 'atleast': kỳ tới có ≥k số trong nums; 'atmost': ≤k số
CLAIMS = [
    ('kd_2ky', 'Có ≥1 số của 2 kỳ gần nhất', lambda R, t, c, NB, KB: ('atleast', R[t - 1] | R[t - 2], 1)),
    ('kd_nong10', 'Có ≥1 số trong 10 số nóng nhất 20 kỳ', lambda R, t, c, NB, KB: ('atleast', set(sorted(c['c20'], key=lambda n: (-c['c20'][n], c['gap'][n], n))[:10]), 1)),
    ('kd_ke', 'Có ≥1 số trùng hoặc kề ±1 kỳ trước', lambda R, t, c, NB, KB: ('atleast', {m for n in R[t - 1] for m in (n - 1, n, n + 1) if 1 <= m <= NB}, 1)),
    ('kd_trung2', 'Không trùng ≥2 số với kỳ trước', lambda R, t, c, NB, KB: ('atmost', set(R[t - 1]), 1)),
    # nhóm nhiều số: chấm "đúng" khi nhóm ra ÍT hơn bình quân (tỉ lệ trúng/số < KB/NB)
    ('nhom_nhip80', 'Nhóm "phá nhịp nghỉ" (100 kỳ: ≥80% lần nghỉ ≥x kỳ, mới nghỉ <x) ra ít hơn bình quân', lambda R, t, c, NB, KB: ('nhomit', nhip_p(R, t, NB), 0)),
    ('nhom_nhip', 'Nhóm nhịp riêng "lúc vắng thế này chưa từng ra" ra ít hơn bình quân', lambda R, t, c, NB, KB: ('nhomit', nhip_off(R, t, NB), 0)),
]

def snap(game):
    key, NB, KB = GM[game]
    D = json.load(open(os.path.join(HERE, 'all_data.json')))[key]
    R = [set(r) for r in D['res']]; T = len(R); c = ctx(R, NB, T)
    rules = [dict(id=i, lab=l, kind='loai', nums=sorted(f(R, T, c)), applied=i in APPLIED[game]) for i, l, f in RULES]
    for i, l, f in CLAIMS:
        kind, nums, k = f(R, T, c, NB, KB)
        rules.append(dict(id=i, lab=l, kind=kind, nums=sorted(nums), k=k, applied=False))
    db = load(); g = db.setdefault(key, {'hist': []})
    g['pending'] = dict(after=D['dates'][-1], made=datetime.datetime.now().strftime('%d/%m/%Y %H:%M'), rules=rules)
    json.dump(db, open(FILE, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f'snap {key}: {len(rules)} luật cho kỳ sau {D["dates"][-1]}')

def cham(game, date, nums, extra=None):
    key, NB, KB = GM[game]
    db = load(); g = db.setdefault(key, {'hist': []}); p = g.get('pending'); res = set(nums)
    if not p: print('chưa có ảnh chụp luật cho kỳ này — bỏ qua'); return
    out = []
    for r in p['rules']:
        hit = sorted(set(r['nums']) & res)
        if r['kind'] == 'loai': ok = not hit
        elif r['kind'] == 'atleast': ok = len(hit) >= r['k']
        elif r['kind'] == 'nhomit': ok = (len(hit) / len(r['nums']) < KB / NB) if r['nums'] else True
        else: ok = len(hit) <= r['k']
        out.append(dict(id=r['id'], lab=r['lab'], kind=r['kind'], nums=r['nums'], hit=hit, ok=ok, applied=r.get('applied', False)))
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
    g['hist'] = [h for h in g['hist'] if h['date'] != date] + [rec]
    g.pop('pending', None)
    json.dump(db, open(FILE, 'w', encoding='utf-8'), ensure_ascii=False)
    okn = sum(r['ok'] for r in out)
    print(f'cham {key} {date}: {okn}/{len(out)} luật đúng' + (f" · gợi ý pool15 trúng {rec['goiy']['p15']}, vé tốt nhất {rec['goiy']['best']}" if 'goiy' in rec else ''))

if __name__ == '__main__':
    if sys.argv[1] == 'snap': snap(sys.argv[2])
    elif sys.argv[1] == 'cham':
        xs = [int(x) for x in sys.argv[4:]]; KB = GM[sys.argv[2]][2]
        cham(sys.argv[2], sys.argv[3], xs[:KB], xs[KB] if len(xs) > KB else None)
