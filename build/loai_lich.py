"""Ghi lại số bị loại (luật loại của goiy.py) và pool 15 của từng kỳ trong N kỳ gần, như đứng ở kỳ trước đó.
Ra build/loai_lich_<game>.json: {ngày kỳ: {loai: [...], pool: [...]}}. Dùng: python3 build/loai_lich.py mega|power [N]"""
import json, os, subprocess, sys
B = os.path.dirname(os.path.abspath(__file__)); g = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 100
D = json.load(open(os.path.join(B, 'all_data.json')))[{'mega': 'mega645', 'power': 'power655'}[g]]
out = {}; tmp = os.path.join(B, f'.loai_tmp_{g}.json')
for cut in range(N, 0, -1):
    subprocess.run([sys.executable, os.path.join(B, 'goiy.py'), g, '--json', tmp], env={**os.environ, 'GOIY_CUT': str(cut)}, stdout=subprocess.DEVNULL, check=True)
    J = json.load(open(tmp)); out[D['dates'][-cut]] = dict(loai=J['vang'], pool=J['pool'], res=sorted(D['res'][-cut]))
os.remove(tmp)
json.dump(out, open(os.path.join(B, f'loai_lich_{g}.json'), 'w'))
