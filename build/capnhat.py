#!/usr/bin/env python3
"""Cập nhật ĐỦ mọi bước sau khi có kết quả mới (anh 15/10/2026: "rà lại cách app chọn pool" — tránh bước nào chạy chậm hơn dữ liệu).
Thứ tự: tâm linh từng kỳ (kiemtra_app) → bộ cộng điểm từng cỡ pool (pool_chon, cả bản 50 kỳ) → giới hạn kép (kep_pool)
→ chấm pool thật (pool_app) → chọn bộ luật lọc vé (luat_ve, Power ghim nhịp + giới hạn tổng) → phiếu tâm linh kỳ tới (tamlinh)
→ gợi ý + lưu sổ (goiy --save) → dựng app (assemble).
  python build/add_result.py loto "15/10/2026 21h" 01 02 03 04 05 06   (thêm kết quả như cũ)
  python build/capnhat.py loto [mega power]"""
import os, subprocess, sys
B = os.path.dirname(os.path.abspath(__file__))
PIN = {'power': 'nhiptong,bientong',   # 17/10/2026 anh bỏ ghim nhịp riêng (chấm tiến bộ luật 60% → 82%)
        'loto': 'kep1', 'mega': 'kep1'}   # anh chốt: Power 2 luật tổng + nhịp riêng (15/10); Loto, Mega ghim số kép ≤1 (16/10: '11 22 33 gợi ý ngu như bò')
TMP = os.path.join(B, '_tmp'); os.makedirs(TMP, exist_ok=True)


def run(args, env=None, out=None):
    e = dict(os.environ, PYTHONUTF8='1', **(env or {}))
    print('  →', ' '.join(args), flush=True)
    r = subprocess.run([sys.executable] + args, cwd=B, env=e, stdout=open(out, 'w', encoding='utf-8') if out else subprocess.DEVNULL,
                       stderr=subprocess.PIPE, text=True, encoding='utf-8')
    if r.returncode: print(r.stderr[-1500:]); sys.exit(f'lỗi ở bước {args[0]}')


games = sys.argv[1:] or ['loto', 'mega', 'power']
run(['kiemtra_app.py', '200'])
for g in games:
    print(f'== {g}')
    run(['pool_chon.py', g]); run(['pool_chon.py', g], env=dict(SELW='50'))
    run(['kep_pool.py', g]); run(['pool_app.py', g])
    run(['nghi.py', g])   # số tình nghi (17/10/2026)
    run(['luat_ve.py', g, '100'], env=dict(PIN=PIN.get(g, '')))
    tl = os.path.join(TMP, f'tl_{g}.json')
    run(['tamlinh.py', g], out=tl)
    run(['goiy.py', g, '--app', tl, '--json', f'goiy_latest/{g}.json', '--save'], out=os.path.join(TMP, f'goiy_{g}.md'))
run(['assemble.py'])
print('xong — gợi ý chi tiết ở build/_tmp/goiy_<game>.md')
