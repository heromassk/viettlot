# Dung app tu build/loto_template.html + build/all_data.json -> index_loto.html (goc repo) va build/nghien-cuu-loto.html (ban dang len link)
import os
B=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.dirname(B)
t=open(os.path.join(B,'loto_template.html'),encoding='utf-8').read()
import json,glob
GO={}
for f in glob.glob(os.path.join(B,'goiy_latest','*.json')):
    j=json.load(open(f,encoding='utf-8'));GO[{'power':'power655','mega':'mega645','loto':'loto535'}[j['game']]]=j
# pool app đã đưa cho từng kỳ (goiy_log.jsonl, bản cuối mỗi kỳ) — để bảng pool đối chiếu cả các kỳ mà pool_thuc.json chưa có (anh 20/10/2026)
_LG=os.path.join(B,'goiy_log.jsonl')
if os.path.exists(_LG):
    _PL={}
    for _l in open(_LG,encoding='utf-8'):
        try:_e=json.loads(_l)
        except Exception:continue
        if _e.get('pools') and _e.get('next'):_PL.setdefault(_e['game'],{})[_e['next']]={k:v for k,v in _e['pools'].items()}
        if _e.get('next') and _e.get('tamlinh') and _e['next'] in _PL.get(_e['game'],{}):_PL[_e['game']][_e['next']]['_tl']={'top':_e['tamlinh'],'strong':_e.get('tl_strong',[]),'votes':_e.get('tl_votes',{})}   # tâm linh đã đưa kỳ đó (anh 20/10/2026)
    for _g,_k in (('loto','loto535'),('mega','mega645'),('power','power655')):
        if _k in GO and _g in _PL:GO[_k]['poolLog']=dict(list(_PL[_g].items())[-60:])
bj=open(os.path.join(B,'bang.js'),encoding='utf-8').read()
css=bj[bj.index('const BANG_CSS=`')+16:bj.index('`;',bj.index('const BANG_CSS=`'))]
TD=json.load(open(os.path.join(B,'theodoi.json'),encoding='utf-8')) if os.path.exists(os.path.join(B,'theodoi.json')) else {}
M3=open(os.path.join(B,'max3d_app.json'),encoding='utf-8').read() if os.path.exists(os.path.join(B,'max3d_app.json')) else '{}'
t=t.replace('/*MAX3D*/',M3).replace('/*THEODOI*/',json.dumps(TD,ensure_ascii=False)).replace('/*GOIY*/',json.dumps(GO,ensure_ascii=False)).replace('/*BANGJS*/',bj).replace('/*BANGCSS*/',css)
full=t.replace('/*DATA*/',open(os.path.join(B,'all_data.json')).read()).replace('/*LUNAR*/',open(os.path.join(B,'lunar.js'),encoding='utf-8').read())
open(os.path.join(ROOT,'index_loto.html'),'w',encoding='utf-8').write(full)
a=full.replace('<!DOCTYPE html>\n<html lang="vi">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n','').replace('</head>\n<body>\n','').replace('</body>\n</html>\n','')
a=a.replace(':root{--bg:#0f1420;',':root{color-scheme:dark;--bg:#0f1420;').replace("min-height:100vh;padding:16px 12px 60px;}","min-height:100%;padding-block:16px 60px;padding-inline:16px;}").replace("body{padding:10px 6px 60px;}","body{padding-block:10px 60px;padding-inline:16px;}")
assert a.lstrip().startswith('<title>') and 'padding-inline:16px' in a
open(os.path.join(B,'nghien-cuu-loto.html'),'w',encoding='utf-8').write(a);print('ok: index_loto.html + build/nghien-cuu-loto.html',len(a))
