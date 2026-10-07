#!/usr/bin/env python3
"""Lấy kết quả Vietlott mới từ kho công khai github.com/vietvudanh/vietlott-data (tự crawl vietlott.vn mỗi ngày) — anh, 05/10/2026.
  python3 build/lay_kq.py            # cập nhật cả Power, Mega, Loto, Max 3D, Max 3D Pro
  python3 build/lay_kq.py --xem      # chỉ xem kỳ mới, chưa ghi
Power/Mega/Loto: kỳ mới được thêm bằng add_result.py (tự chấm sổ + chụp luật kỳ tới + dựng lại app).
Loto: kho không ghi 13h/21h → lấy theo thứ tự id sau kỳ cuối trùng khớp với dữ liệu của anh, phiên xen kẽ 13h → 21h.
Max 3D / 3D Pro: ghi lại build/max3d_data.json, max3dpro_data.json rồi chạy max3d_app.py."""
import json, os, subprocess, sys, datetime
B = os.path.dirname(os.path.abspath(__file__))
REPO = '/home/user/vietvudanh/vietlott-data'; URL = 'https://github.com/vietvudanh/vietlott-data'
XEM = '--xem' in sys.argv
env = dict(os.environ, GIT_LFS_SKIP_SMUDGE='1')
if os.path.isdir(os.path.join(REPO, '.git')):
    subprocess.run(['git', '-C', REPO, 'fetch', '-q', '--depth', '1', 'origin'], check=True, env=env)
    subprocess.run(['git', '-C', REPO, 'reset', '-q', '--hard', 'FETCH_HEAD'], check=True, env=env)
else:
    subprocess.run(['git', 'clone', '-q', '--depth', '1', URL, REPO], check=True, env=env)
print('kho dữ liệu cập nhật lúc', subprocess.run(['git', '-C', REPO, 'log', '-1', '--format=%cd'], capture_output=True, text=True).stdout.strip())
rd = lambda f: sorted((json.loads(l) for l in open(os.path.join(REPO, 'data', f)) if l.strip()), key=lambda x: int(x['id']))
vn = lambda d: '/'.join(d.split('-')[::-1])
A = json.load(open(os.path.join(B, 'all_data.json')))
moi = []
for g, key, f, C in (('mega', 'mega645', 'power645.jsonl', 6), ('power', 'power655', 'power655.jsonl', 6)):
    have = set(A[key]['dates']); last = datetime.datetime.strptime(A[key]['dates'][-1], '%d/%m/%Y')
    for x in rd(f):
        d = vn(x['date'])
        if d in have:
            i = A[key]['dates'].index(d)
            if sorted(x['result'][:C]) != A[key]['res'][i]: print(f'⚠ {g} {d}: kho {x["result"]} khác dữ liệu anh {A[key]["res"][i]}')
        elif datetime.datetime.strptime(d, '%d/%m/%Y') > last:
            moi.append((g, d, sorted(x['result'][:C]) + x['result'][C:C + 1]))
# Loto
L = rd('power535.jsonl'); P = A['loto535']
tail = (P['res'][-1], P['lk'][-1])
idx = next((i for i in range(len(L) - 1, -1, -1) if (sorted(L[i]['result'][:5]), L[i]['result'][5]) == tail), None)
if idx is None:
    print('⚠ loto: kỳ cuối của anh chưa có trong kho (kho chậm hơn) → chưa thêm Loto')
else:
    ld, ls = P['dates'][-1][:10], P['dates'][-1][-3:]
    for x in L[idx + 1:]:
        d = vn(x['date'])
        ses = '21h' if (d == ld and ls == '13h') else '13h'
        if d == ld and ls == '21h': print(f'⚠ loto {d}: đã đủ 13h và 21h mà kho còn kỳ id {x["id"]} → dừng, cần anh xem'); break
        moi.append(('loto', f'{d} {ses}', sorted(x['result'][:5]) + [x['result'][5]])); ld, ls = d, ses
for g, d, n in moi: print('kỳ mới:', g, d, ' '.join(f'{v:02d}' for v in n))
if not moi: print('Power/Mega/Loto: không có kỳ mới')
if XEM: sys.exit()
for g, d, n in moi:
    subprocess.run([sys.executable, os.path.join(B, 'add_result.py'), g, d] + [str(v) for v in n], check=True)
# Max 3D, Max 3D Pro
for f, out in (('3d.jsonl', 'max3d_data.json'), ('3d_pro.jsonl', 'max3dpro_data.json')):
    rows = {}
    for x in rd(f):
        k = {kk.lower(): v for kk, v in x['result'].items()}
        nums = k['giải đặc biệt'] + k['giải nhất'] + k['giải nhì'] + k['giải ba']
        if len(nums) == 20: rows[int(x['id'])] = (vn(x['date']), nums)
    ids = sorted(rows); old = json.load(open(os.path.join(B, out)))
    new = {'dates': [rows[i][0] for i in ids], 'ids': ids, 'res': [rows[i][1] for i in ids], 'nguon': 'github.com/vietvudanh/vietlott-data'}
    # giữ các kỳ anh nhập tay (max3d_cham.py) mới hơn kho
    dk = lambda d: datetime.datetime.strptime(d, '%d/%m/%Y')
    for d, r in zip(old['dates'], old['res']):
        if d not in new['dates'] and dk(d) > dk(new['dates'][-1]):
            new['dates'].append(d); new['res'].append(r); new['ids'].append(new['ids'][-1] + 1)
        elif d in new['dates'] and new['res'][new['dates'].index(d)] != r: print(f'⚠ {out} {d}: kho khác số anh nhập')
    json.dump(new, open(os.path.join(B, out), 'w'))
    print(f'{out}: {len(ids)} kỳ (thêm {len(ids) - len(old["res"])}), kỳ cuối {rows[ids[-1]][0]}')
subprocess.run([sys.executable, os.path.join(B, 'max3d_app.py')], check=True)
subprocess.run([sys.executable, os.path.join(B, 'assemble.py')], check=True)
# Quẻ ngày tháng (anh, 07/10/2026): cập nhật build/ngaythang.md sau mỗi lần lấy kết quả
if not XEM:
    subprocess.run([sys.executable, os.path.join(B, 'ngaythang.py')], check=True, stdout=subprocess.DEVNULL)
    for g in ('loto', 'power', 'mega'): subprocess.run([sys.executable, os.path.join(B, 'loto_ngaythang.py'), g], check=True, stdout=subprocess.DEVNULL)
    print('Ngày tháng: đã cập nhật build/ngaythang.md')
