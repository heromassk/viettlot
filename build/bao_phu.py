"""Bảng vé bao phủ (kiểu Đại học Manchester 2023): vé rải trên pool v số sao cho nếu ≥k số về nằm trong pool
thì CHẮC CHẮN có ≥1 vé trúng ≥m số. Dựng tham lam rồi gọt vé thừa; lưu sẵn ở build/rai_ve_bang.json.
  bao_phu(v, kb, m, k) -> danh sách vé, mỗi vé là kb vị trí 0..v-1 (vị trí 0 = số hạng 1 của pool)."""
import json, os, random
from itertools import combinations
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'rai_ve_bang.json')
_BANG = None

def bao_phu(v, kb, m, k):
    global _BANG
    if _BANG is None: _BANG = json.load(open(CACHE, encoding='utf-8')) if os.path.exists(CACHE) else {}
    key = f'{v}-{kb}-{m}-{k}'
    if key in _BANG: return _BANG[key]
    S = list(combinations(range(v), k))
    blocks = list(combinations(range(v), kb))
    if len(blocks) > 40000: blocks = random.Random(7).sample(blocks, 40000)
    def mask(b):
        bs, mk = set(b), 0
        for i, s in enumerate(S):
            if len(bs.intersection(s)) >= m: mk |= 1 << i
        return mk
    M = [mask(b) for b in blocks]; left = full = (1 << len(S)) - 1; out = []
    while left:
        j = max(range(len(M)), key=lambda j: bin(M[j] & left).count('1'))
        out.append(list(blocks[j])); left &= ~M[j]
    for b in sorted(out, key=lambda b: bin(mask(b)).count('1')):   # gọt vé thừa
        rest = [x for x in out if x is not b]; u = 0
        for x in rest: u |= mask(x)
        if u == full: out = rest
    _BANG[key] = out; json.dump(_BANG, open(CACHE, 'w', encoding='utf-8'))
    return out
