"""Số cộng/trừ trỏ tới, có ra trong kết quả, nhưng bị luật loại của goiy.py bỏ khỏi pool (anh, 08/10/2026).
Cần build/loai_lich_<game>.json (loai_lich.py). Dùng: python3 build/congtru_loai.py mega|power"""
import json, sys, os
B = os.path.dirname(os.path.abspath(__file__)); g = sys.argv[1]
key, N = {'mega': ('mega645', 45), 'power': ('power655', 55)}[g]
D = json.load(open(os.path.join(B, 'all_data.json')))[key]; L = json.load(open(os.path.join(B, f'loai_lich_{g}.json')))
R = [set(sorted(r)[:6]) for r in D['res']]; ix = {d: i for i, d in enumerate(D['dates'])}
CASES = {'mega': [(14, 10), (6, 5), (13, 7)], 'power': [(1, 5), (16, 5), (3, 7)]}[g]
def pool(t, d, k):
    v = {}
    for j in range(1, k + 1):
        for x in R[t - j]:
            for m in (x - d, x + d):
                if 1 <= m <= N: v[m] = v.get(m, 0) + 1
    return sorted((m for m in v if m not in R[t - 1]), key=lambda m: (-v[m], m))[:12]
print(f'{g.upper()} — {len(L)} kỳ gần, luật loại = số goiy.py bỏ khỏi pool kỳ đó\n')
for d, k in CASES:
    nl = hl = nk = hk = 0; miss = []
    for dt, e in L.items():
        t = ix[dt]; P = set(pool(t, d, k)); lo = set(e['loai'])
        a = P & lo; b = P - lo
        nl += len(a); hl += len(a & R[t]); nk += len(b); hk += len(b & R[t])
        for m in sorted(a & R[t]): miss.append(f'{dt[:5]}:{m:02d}')
    print(f'±{d} qua {k} kỳ: số trong pool cộng/trừ BỊ LOẠI: {nl} lượt, ra {hl} ({100*hl/max(nl,1):.1f}%)  ·  KHÔNG bị loại: {nk} lượt, ra {hk} ({100*hk/max(nk,1):.1f}%)')
    print(f'   bị loại mà vẫn ra ({len(miss)}): ' + ' '.join(miss[-25:]))
# luật loại nói chung trong cùng các kỳ
tl = sum(len(e['loai']) for e in L.values()); th = sum(len(set(e['loai']) & set(e['res'])) for e in L.values())
print(f'\nCả luật loại (mọi số bị loại): {tl} lượt, ra {th} ({100*th/tl:.1f}%) — mức TB mỗi số {600/N:.1f}%')
