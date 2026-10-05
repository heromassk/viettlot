#!/usr/bin/env python3
"""Rà soát mọi luật trong sổ (theodoi.RULES + CLAIMS) trên 2 khung 100 kỳ gần nhất (gần / trước), chạy tiến.
Với mỗi luật: tỉ lệ ra mỗi số của nhóm (so bình quân), % kỳ "không số nào về" (luật loại), cỡ nhóm, nhãn ✔ / ~ / ✘.
  python3 build/rasoat.py power|mega|loto"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import theodoi as TD
g = sys.argv[1]; key, NB, KB = TD.GM[g]
D = json.load(open(os.path.join(TD.HERE, 'all_data.json')))[key]
R = [set(r) for r in D['res']]; T = len(R); P = KB / NB * 100
TD.SESS = (['13' if '13h' in x else '21' for x in D['dates']] + ['13' if '21h' in D['dates'][-1] else '21']) if g == 'loto' else []
segs = [(T - 100, T), (T - 200, T - 100)]
C = {t: TD.ctx(R, NB, t) for t in range(T - 200, T)}
rows = []
items = [(i, l, 'loai', f) for i, l, f in TD.RULES] + [(i, l, 'claim', f) for i, l, f in TD.CLAIMS]
for i, lab, typ, f in items:
    st = []
    for a, b in segs:
        h = n = ok = cnt = 0
        for t in range(a, b):
            if typ == 'loai': s = f(R, t, C[t])
            else:
                kind, s, k = f(R, t, C[t], NB, KB)
                if kind in ('atleast', 'atmost'):
                    hit = len(s & R[t]); ok += (hit >= k) if kind == 'atleast' else (hit <= k); cnt += 1; continue
            s = set(s)
            if not s: continue
            x = len(s & R[t]); h += x; n += len(s); ok += not x; cnt += 1
        st.append((h / n * 100 if n else None, ok / cnt * 100 if cnt else None, n / max(cnt, 1), cnt))
    rows.append((i, lab, typ, st))
def tag(st, want):   # want: 'it' (luật loại / nhóm ít) hoặc 'nhieu'
    r = [x[0] for x in st]
    if None in r: return '—'
    if want == 'it':
        if all(v < P - 0.5 for v in r): return '✔ ra ít (nghiêng ổn định)'
        if r[0] < P - 0.5 or r[1] < P - 0.5: return '~ ít ở 1 khung'
        return '✘ không nghiêng' if all(abs(v - P) < 0.8 for v in r) else '✘ ngược (ra nhiều)'
    if all(v > P + 0.5 for v in r): return '✔ ra nhiều (nghiêng ổn định)'
    if r[0] > P + 0.5 or r[1] > P + 0.5: return '~ nhiều ở 1 khung'
    return '✘ không nghiêng' if all(abs(v - P) < 0.8 for v in r) else '✘ ngược (ra ít)'
print(f'## {key} — rà soát {len(rows)} luật, 100 kỳ gần / 100 kỳ trước (bình quân mỗi số {P:.1f}%)\n')
print('| Luật | Áp dụng | Ra mỗi số (gần / trước) | Kỳ không mất số (luật loại) | Cỡ nhóm TB | Nhận định |\n|---|---|---|---|---|---|')
for i, lab, typ, st in rows:
    applied = '●' if i in TD.APPLIED[g] else ''
    if all(x[3] == 0 for x in st): continue          # luật không áp cho trò này
    if typ == 'claim' and st[0][0] is None and st[0][1] is not None:
        print(f"| {lab} | | — | đúng {st[0][1]:.0f} / {st[1][1]:.0f}% kỳ | — | khẳng định |"); continue
    want = 'nhieu' if 'NHIỀU' in lab else 'it'
    r = ' / '.join('—' if x[0] is None else f'{x[0]:.1f}%' for x in st)
    ok = ' / '.join('—' if x[1] is None else f'{x[1]:.0f}%' for x in st) if typ == 'loai' else ''
    print(f"| {lab} | {applied} | {r} | {ok} | {st[0][2]:.1f} | {tag(st, want)} |")
