"""Dấu vết theo thứ-ngày-tháng (dương + âm lịch) và theo kỳ trước (số ra lại, liền kề, kép) — dùng chung cho
pool_chon.py (chọn bộ cộng điểm riêng cho từng cỡ pool) và goiy.py (áp cho kỳ tới). Anh 14/10/2026."""
import datetime as dt, json, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
_LUN = {}

def lunar_many(days):
    """'dd/mm/yyyy' -> (ngày âm, tháng âm), tính bằng lunar.js của app (1 lần gọi node)."""
    need = sorted({d[:10] for d in days} - set(_LUN))
    if need:
        js = open(os.path.join(HERE, 'lunar.js'), encoding='utf-8').read() + ';console.log(JSON.stringify(' + json.dumps(need) + \
             '.map(s=>{const [d,m,y]=s.split("/").map(Number);const L=solar2lunar(d,m,y);return [L.d,L.m];})));'
        _LUN.update(zip(need, map(tuple, json.loads(subprocess.run(['node', '-e', js], capture_output=True, text=True, check=True).stdout))))
    return _LUN

lon = lambda n: int(f'{n:02d}'[::-1])
_PW = None

def sigs(prev, day, NB):
    """prev: tập số kỳ trước; day: 'dd/mm/yyyy…' ngày quay của kỳ cần đoán. Trả {tên dấu vết: tập số trong 1..NB}."""
    d = dt.datetime.strptime(day[:10], '%d/%m/%Y'); ad, am = lunar_many([day])[day[:10]]
    prev = set(prev); K11 = set(range(11, NB + 1, 11))
    S = {
        'Ngày': {d.day}, 'Tháng': {d.month}, 'Ngày lộn': {lon(d.day)}, 'Ngày + tháng': {d.day + d.month},
        'Ghép tháng–ngày': {int(f'{d.month % 10}{d.day // 10}'), int(f'{d.day % 10}{d.month // 10}')},
        'Ngày ±1': {d.day - 1, d.day + 1}, 'Thứ': {d.weekday() + 2},
        'Tổng chữ số ngày tháng năm': {sum(int(c) for c in d.strftime('%d%m%Y'))},
        'Ngày âm': {ad}, 'Tháng âm': {am}, 'Ngày âm lộn': {lon(ad)}, 'Ngày âm + tháng âm': {ad + am}, 'Ngày âm ±1': {ad - 1, ad + 1},
        'Số ra kỳ trước': prev, 'Liền kề ±1 số kỳ trước': {m for n in prev for m in (n - 1, n + 1)} - prev,
        'Số kép': K11, 'Kép liền kề kép kỳ trước': {m for k in prev if k % 11 == 0 for m in (k - 11, k + 11)},
        'Lộn kỳ trước': {lon(n) for n in prev if lon(n) != n},   # anh 15/10/2026: số lộn
    }
    return {k: {n for n in v if 1 <= n <= NB} for k, v in S.items()}

NGAY = ('Thứ', 'Ngày', 'Tháng', 'Ngày lộn', 'Ngày + tháng', 'Ghép tháng–ngày', 'Ngày ±1', 'Tổng chữ số ngày tháng năm',
        'Ngày âm', 'Tháng âm', 'Ngày âm lộn', 'Ngày âm + tháng âm', 'Ngày âm ±1')
NBG = {35: 'loto', 45: 'mega', 55: 'power'}

def next_date(game, last):
    """Ngày kỳ tới theo lịch quay (Mega T4/T6/CN, Power T3/T5/T7, Loto 13h/21h hằng ngày)."""
    d = dt.datetime.strptime(last[:10], '%d/%m/%Y')
    if game == 'loto':
        return f"{last[:10]} 21h" if '13h' in last else f"{(d + dt.timedelta(days=1)).strftime('%d/%m/%Y')} 13h"
    days = {'mega': (2, 4, 6), 'power': (1, 3, 5)}[game]
    d += dt.timedelta(days=1)
    while d.weekday() not in days: d += dt.timedelta(days=1)
    return d.strftime('%d/%m/%Y')

def dang_chay(R, dates, t, NB):
    """Dấu vết ngày "đang chạy" cho kỳ t (t = len(R) là kỳ tới): đã về trúng ≥3 trong 10 kỳ gần hoặc ≥4 trong 20 kỳ gần.
    Trả [(tên, trúng/10, trúng/20, số kỳ t)] — chỉ dùng kết quả + ngày các kỳ trước t."""
    day = lambda u: dates[u] if u < len(dates) else next_date(NBG[NB], dates[-1])
    lunar_many([day(u) for u in range(max(1, t - 20), t + 1)])
    S = {u: sigs(R[u - 1], day(u), NB) for u in range(max(1, t - 20), t + 1)}
    out = []
    for nm in NGAY:
        h = lambda W: sum(bool(S[u][nm] & set(R[u])) for u in range(max(1, t - W), t))
        h10, h20 = h(10), h(20)
        if (h10 >= 3 or h20 >= 4) and S[t][nm]: out.append((nm, h10, h20, sorted(S[t][nm])))
    return out

def cand_nums(R, dates, t, NB):
    """Mọi ứng viên cộng điểm (không gồm tâm linh) cho kỳ t (t = len(R) là kỳ tới) — dùng chung pool_chon.py và goiy.py:
    17 dấu vết, bản "đang về ≥3/10" và "≥4/20" của từng cái, và "Chạy 1 số" (gộp dấu vết ngày 1 số đang chạy)."""
    day = lambda u: dates[u] if u < len(dates) else next_date(NBG[NB], dates[-1])
    lunar_many([day(u) for u in range(max(1, t - 20), t + 1)])
    S = {u: sigs(R[u - 1], day(u), NB) for u in range(max(1, t - 20), t + 1)}
    out = dict(S[t])
    for nm in S[t]:
        for W, m in ((10, 3), (20, 4)):
            h = sum(bool(S[u][nm] & set(R[u])) for u in range(max(1, t - W), t))
            out[f'{nm} (đang về ≥{m}/{W} kỳ)'] = S[t][nm] if h >= m else set()
    run = [(nm, S[t][nm]) for nm in NGAY if (out[f'{nm} (đang về ≥3/10 kỳ)'] or out[f'{nm} (đang về ≥4/20 kỳ)'])]
    out['Chạy 1 số'] = {n for nm, v in run if len(v) == 1 for n in v}
    out['Chạy tất cả'] = {n for nm, v in run for n in v}
    # Nhịp riêng của số vừa ra (anh 15/10/2026: "50 về 1 kỳ thì kỳ sau gần như nghỉ"): số của kỳ trước mà trong 20 lần ra gần nhất
    # của chính nó chỉ ra lại ngay ≤1 lần (cần ≥8 lần ra)
    nr = set()
    if t >= 1:
        for n in R[t - 1]:
            ap = [u for u in range(max(0, t - 100), t - 1) if n in R[u]][-20:]
            if len(ap) >= 8 and sum(n in R[u + 1] for u in ap) <= 1: nr.add(n)
    out['Vừa ra, nhịp riêng hay nghỉ'] = nr
    if NB == 35:   # Loto: dấu vết theo GIỜ QUAY (anh 15/10: liên hệ nhiều hơn với 10 kỳ gần, 10 kỳ cùng giờ)
        from collections import Counter
        ses = lambda u: '13' if '13h' in day(u) else '21'
        cg = [u for u in range(t - 1, max(0, t - 60), -1) if ses(u) == ses(t)]
        top = lambda us, k=8: set(n for n, _ in Counter(n for u in us for n in R[u]).most_common(k))
        p = set(R[cg[0]]) if cg else set()
        out['Số kỳ cùng giờ trước'] = p
        out['Kề ±1 số kỳ cùng giờ trước'] = {m for n in p for m in (n - 1, n + 1) if 1 <= m <= NB} - p
        # Power → Loto (anh 15/10/2026: "loto có liên hệ với power cùng ngày không"): số Power (≤35) quay CÙNG NGÀY trước Loto 21h,
        # và số của kỳ Power gần nhất trước kỳ Loto này
        global _PW
        if '_PW' not in globals() or _PW is None:
            import json as _j, os as _o
            _P = _j.load(open(_o.path.join(_o.path.dirname(_o.path.abspath(__file__)), 'all_data.json'), encoding='utf-8'))['power655']
            _PW = [(dt.datetime.strptime(x[:10], '%d/%m/%Y'), set(r)) for x, r in zip(_P['dates'], _P['res'])]
        dd = dt.datetime.strptime(day(t)[:10], '%d/%m/%Y'); h21 = ses(t) == '21'
        same = [r for d0, r in _PW if d0 == dd]
        out['Power cùng ngày'] = {n for n in same[0] if n <= NB} if (same and h21) else set()
        prevp = [r for d0, r in _PW if d0 < dd or (d0 == dd and h21)]
        out['Power kỳ gần nhất'] = {n for n in prevp[-1] if n <= NB} if prevp else set()
        out['Lộn kỳ cùng giờ trước'] = {lon(n) for n in p if lon(n) != n and 1 <= lon(n) <= NB}   # anh 15/10/2026: số lộn
        out['Nóng 10 kỳ cùng giờ'] = top(cg[:10]); out['Nóng 20 kỳ cùng giờ'] = top(cg[:20])
        out['Lạnh 10 kỳ cùng giờ'] = set(range(1, NB + 1)) - {n for u in cg[:10] for n in R[u]}
        out['Nóng 10 kỳ gần'] = top(range(t - 10, t)); out['Nóng 20 kỳ gần'] = top(range(t - 20, t))
    return out
