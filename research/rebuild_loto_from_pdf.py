"""Dựng lại loto535_history.csv từ kết quả OCR của loto.pdf (bản in trang ketquadientoan.com).
Định dạng mới: ngày, giờ quay (13h/21h), 5 số chính, số may mắn — giờ để riêng, có chữ "h".
Ô OCR bị mất chữ số (ví dụ "7" thay vì "17") được vá bằng dòng CSV cũ cùng ngày khớp 5/6 số."""
import json, collections, sys, os
OCR = sys.argv[1]            # file JSON từ bước OCR
CSV = os.path.join(os.path.dirname(__file__), '..', 'loto535_history.csv')
o = json.load(open(OCR))
old = [l.split(',') for l in open(CSV).read().split('\n') if l]
oldby = collections.defaultdict(list)
for r in old: oldby[r[0]].append(r[1:7] if not r[1].endswith('h') else r[2:8])
rows = []; fixed = []
for r in o:
    n = r['nums']
    if any(len(x) != 2 for x in n):
        cand = [c for c in oldby[r['date']] if sum(a == b for a, b in zip(c, n)) == 5]
        assert len(cand) == 1, r
        fixed.append((r['date'], n, cand[0])); n = cand[0]
    v = [int(x) for x in n]
    assert all(1 <= x <= 35 for x in v[:5]) and v[:5] == sorted(set(v[:5])) and 1 <= v[5] <= 12, r
    rows.append(f"{r['date']},{r['hour']}h,{','.join(n)}")
assert len(rows) == len(set(rows))
c = collections.Counter(x.split(',')[0] for x in rows)
print('tổng', len(rows), '| ngày có 1 kỳ:', [k for k, v in c.items() if v != 2])
print('vá chữ số bị mất:', fixed)
key = lambda x: ','.join([x.split(',')[0]] + x.split(',')[2:])
new = set(map(key, rows))
oldset = set(','.join(r[:7]) for r in old if not r[1].endswith('h'))
print('giống CSV cũ:', len(new & oldset), '| CSV cũ bị thay:', len(oldset - new), '| mới/sửa:', len(new - oldset))
for x in sorted(oldset - new, key=lambda s: s[6:10] + s[3:5] + s[:2]): print('  cũ sai:', x)
open(CSV, 'w').write('\n'.join(rows) + '\n')
