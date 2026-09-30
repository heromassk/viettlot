"""Nghiên cứu chính các bộ số trúng: cấu trúc, tần suất, dự đoán theo nóng/lạnh/gan, và 'nhịp' giữa các kỳ."""
import sys, os, math, random
from math import comb
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from study import load
from combo import chi2_sf, hyper

def zp(z): return math.erfc(abs(z)/math.sqrt(2))

def structure(mx, c, D):
    n = len(D); odd = (mx+1)//2; low = mx//2
    rng = random.Random(1); sims = [sorted(rng.sample(range(1, mx+1), c)) for _ in range(200000)]
    out = {}
    def dist(name, f, theory=None):
        obs = Counter(f(s) for s in D)
        th = theory or {k: v/len(sims) for k, v in Counter(f(s) for s in sims).items()}
        out[name] = (obs, th)
    dist('Số lẻ', lambda s: sum(x % 2 for x in s), {k: hyper(mx, odd, c, k) for k in range(c+1)})
    dist(f'Số nhỏ (1–{low})', lambda s: sum(x <= low for x in s), {k: hyper(mx, low, c, k) for k in range(c+1)})
    dist('Cặp số liền nhau', lambda s: sum(b-a == 1 for a, b in zip(s, s[1:])))
    step = 20 if mx > 40 else 15
    dist('Tổng', lambda s: sum(s)//step*step)
    pat = Counter((sum(x % 2 for x in s), sum(x <= low for x in s)) for s in D).most_common(5)
    return out, pat

def show_dist(name, obs, th, n):
    keys = sorted(set(obs) | {k for k, v in th.items() if v*n >= 0.5})
    print(f'  {name}:')
    for k in keys:
        o, e = obs.get(k, 0), th.get(k, 0)*n
        print(f'     {str(k):>6s}: {o:4d} kỳ ({o/n*100:4.1f}%)  lý thuyết {e/n*100:4.1f}%  ' + '█'*round(o/n*60))

def walk_forward(mx, c, D, start=30):
    """Mỗi kỳ, chọn c số chỉ bằng dữ liệu các kỳ trước; đếm số trúng so với ngẫu nhiên c*c/mx."""
    strat = {
        'Số NÓNG (về nhiều nhất từ đầu)': lambda past: sorted(range(1, mx+1), key=lambda x: (-sum(x in s for s in past), x)),
        'Số NÓNG 30 kỳ gần nhất': lambda past: sorted(range(1, mx+1), key=lambda x: (-sum(x in s for s in past[-30:]), x)),
        'Số LẠNH (về ít nhất từ đầu)': lambda past: sorted(range(1, mx+1), key=lambda x: (sum(x in s for s in past), x)),
        'Số GAN (lâu chưa về nhất)': lambda past: sorted(range(1, mx+1), key=lambda x: (-gap(past, x), x)),
        'Số vừa về kỳ trước': lambda past: sorted(past[-1]) + sorted(set(range(1, mx+1)) - past[-1]),
    }
    def gap(past, x):
        for k in range(len(past)-1, -1, -1):
            if x in past[k]: return len(past)-1-k
        return len(past)
    p = c/mx; var1 = c*p*(1-p)*(mx-c)/(mx-1)
    res = {}
    for name, f in strat.items():
        H = 0; m = 0
        for i in range(start, len(D)):
            pick = set(f(D[:i])[:c]); H += len(pick & D[i]); m += 1
        E = m*c*c/mx; z = (H-E)/math.sqrt(m*var1)
        res[name] = (H/m, E/m, z)
    return res

def rhythm(D, mx, c):
    low = mx//2
    feats = {'số lẻ': lambda s: sum(x % 2 for x in s), 'số nhỏ': lambda s: sum(x <= low for x in s), 'tổng': sum}
    out = {}
    for name, f in feats.items():
        v = [f(s) for s in D]; a, b = v[:-1], v[1:]
        ma, mb = sum(a)/len(a), sum(b)/len(b)
        r = sum((x-ma)*(y-mb) for x, y in zip(a, b))/math.sqrt(sum((x-ma)**2 for x in a)*sum((y-mb)**2 for y in b))
        out[name] = (r, r*math.sqrt(len(a)))
    return out

if __name__ == '__main__':
    for game in ['power655', 'mega645', 'loto535']:
        mx, c, lmx, draws = load(game); D = [d['nums'] for d in draws]; n = len(D)
        print(f'\n################ {game}: {n} kỳ, {c} số trong 1–{mx}')
        print('1) CẤU TRÚC BỘ SỐ TRÚNG (so với lý thuyết nếu bốc ngẫu nhiên)')
        st, pat = structure(mx, c, [sorted(s) for s in D])
        for name, (obs, th) in st.items(): show_dist(name, obs, th, n)
        sums = [sum(s) for s in D]
        print(f'     Tổng TB {sum(sums)/n:.1f} (lý thuyết {c*(mx+1)/2:.1f}), nhỏ nhất {min(sums)}, lớn nhất {max(sums)}')
        print('  Kiểu (lẻ, nhỏ) hay gặp nhất:', ', '.join(f'{a} lẻ-{b} nhỏ: {k} kỳ' for (a, b), k in pat))
        print('2) TẦN SUẤT TỪNG SỐ')
        f = Counter(x for s in D for x in s); e = n*c/mx
        x2 = sum((f.get(k, 0)-e)**2/e for k in range(1, mx+1))
        top = sorted(range(1, mx+1), key=lambda k: -f.get(k, 0))
        print(f'  Kỳ vọng mỗi số {e:.1f} lần. Kiểm định đều: p = {chi2_sf(x2, mx-1):.3f} ' + ('(không có số bị "ưu")' if chi2_sf(x2, mx-1) > 0.05 else '(CÓ LỆCH)'))
        print('  Về nhiều nhất:', ', '.join(f'{k}({f[k]})' for k in top[:8]))
        print('  Về ít nhất:  ', ', '.join(f'{k}({f.get(k,0)})' for k in top[-8:]))
        # khoảng dao động tự nhiên: mô phỏng
        rng = random.Random(3); spread = []
        for _ in range(300):
            ff = Counter(x for _ in range(n) for x in rng.sample(range(1, mx+1), c)); spread.append((max(ff.values()), min(ff.get(k, 0) for k in range(1, mx+1))))
        print(f'  Nếu hoàn toàn ngẫu nhiên, số về nhiều nhất thường ~{sorted(a for a,_ in spread)[150]} lần, ít nhất ~{sorted(b for _,b in spread)[150]} lần → thực tế {f[top[0]]} / {f.get(top[-1],0)}')
        last = {k: next((n-1-i for i in range(n-1, -1, -1) if k in D[i]), n) for k in range(1, mx+1)}
        gan = sorted(last.items(), key=lambda t: -t[1])[:6]
        print('  Số gan hiện tại (số kỳ chưa về):', ', '.join(f'{k}({g})' for k, g in gan))
        if lmx:
            lf = Counter(d['lucky'] for d in draws if d['lucky']); le = n/lmx
            print(f"  Số may mắn 1–{lmx}: kỳ vọng {le:.1f}; p = {chi2_sf(sum((lf.get(k,0)-le)**2/le for k in range(1,lmx+1)), lmx-1):.3f}; " + ', '.join(f'{k}:{lf.get(k,0)}' for k in range(1, lmx+1)))
        print('3) CHỌN THEO NÓNG / LẠNH / GAN — có trúng hơn ngẫu nhiên không? (chỉ dùng dữ liệu trước mỗi kỳ)')
        for name, (h, ex, z) in walk_forward(mx, c, D).items():
            print(f'  {name:32s}: TB trúng {h:.3f} số/kỳ, ngẫu nhiên {ex:.3f} → {(h/ex-1)*100:+5.1f}%  z {z:5.2f} p={zp(z):.3f}')
        print('4) NHỊP GIỮA 2 KỲ LIÊN TIẾP (tương quan; 0 = không liên quan)')
        for name, (r, z) in rhythm([sorted(s) for s in D], mx, c).items():
            print(f'  {name:8s}: r = {r:+.3f}  (z {z:+.2f}, p={zp(z):.3f})')
