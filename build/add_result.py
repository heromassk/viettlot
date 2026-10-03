"""Them ket qua 1 ky vao toan bo du lieu (build/all_data.json, index.html, CSV) roi dung lai app.
Vi du:
  python3 build/add_result.py loto "03/10/2026 21h" 05 07 10 11 34 08     (5 so + so may man)
  python3 build/add_result.py mega "04/10/2026" 01 06 20 27 31 41          (6 so)
  python3 build/add_result.py power "06/10/2026" 07 11 13 16 18 54 41      (6 so + so dac biet)
"""
import sys,os,re,json,subprocess
B=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.dirname(B)
G={'loto':('loto535',5,True),'mega':('mega645',6,False),'power':('power655',6,True)}
g,date,nums=sys.argv[1],sys.argv[2],[int(x) for x in sys.argv[3:]]
key,C,ext=G[g];main=sorted(nums[:C]);x=nums[C] if ext and len(nums)>C else None
assert len(main)==C and len(set(main))==C,'sai so luong so'
d=json.load(open(os.path.join(B,'all_data.json')));P=d[key]
assert date not in P['dates'],'ky nay da co'
P['dates'].append(date);P['res'].append(main)
if 'lk' in P:P['lk'].append(x)
json.dump(d,open(os.path.join(B,'all_data.json'),'w'),separators=(',',':'))
p=os.path.join(ROOT,'index.html');t=open(p,encoding='utf-8').read()
m=re.search(r'(<script id="data-%s" type="application/json">)(.*?)(</script>)'%key,t,re.S);j=json.loads(m.group(2));M=j['meta']
if M['nextDates'] and M['nextDates'][0]==date:M['nextDates'].pop(0);M['ND']-=1
M['dates'].append(date);M['results'].append(main);M['L']+=1
if key=='loto535':M['luckyRes'].append(x)
if key=='power655':M['bonus'].append(x)
t=t[:m.start(2)]+json.dumps(j,ensure_ascii=False,separators=(',',':'))+t[m.end(2):];open(p,'w',encoding='utf-8').write(t)
csv=os.path.join(ROOT,key+'_history.csv');row=','.join([date[:10]]+['%02d'%v for v in main]+(['%02d'%x] if key=='loto535' else []))
old=open(csv,encoding='utf-8').read();open(csv,'w',encoding='utf-8').write(row+'\n'+old)
subprocess.run([sys.executable,os.path.join(B,'assemble.py')],check=True);print('da them',key,date,main,x)
