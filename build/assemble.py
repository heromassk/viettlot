# Dung app tu build/loto_template.html + build/all_data.json -> index_loto.html (goc repo) va build/nghien-cuu-loto.html (ban dang len link)
import os
B=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.dirname(B)
t=open(os.path.join(B,'loto_template.html'),encoding='utf-8').read()
full=t.replace('/*DATA*/',open(os.path.join(B,'all_data.json')).read()).replace('/*LUNAR*/',open(os.path.join(B,'lunar.js'),encoding='utf-8').read())
open(os.path.join(ROOT,'index_loto.html'),'w',encoding='utf-8').write(full)
a=full.replace('<!DOCTYPE html>\n<html lang="vi">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n','').replace('</head>\n<body>\n','').replace('</body>\n</html>\n','')
a=a.replace(':root{--bg:#0f1420;',':root{color-scheme:dark;--bg:#0f1420;').replace("min-height:100vh;padding:16px 12px 60px;}","min-height:100%;padding-block:16px 60px;padding-inline:16px;}").replace("body{padding:10px 6px 60px;}","body{padding-block:10px 60px;padding-inline:16px;}")
assert a.lstrip().startswith('<title>') and 'padding-inline:16px' in a
open(os.path.join(B,'nghien-cuu-loto.html'),'w',encoding='utf-8').write(a);print('ok: index_loto.html + build/nghien-cuu-loto.html',len(a))
