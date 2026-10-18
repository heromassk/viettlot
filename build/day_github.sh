#!/bin/bash
# Đẩy app + dữ liệu + code lên github.com/heromassk/viettlot (không đẩy build/_tmp, __pycache__, pdf, saoluu)
S="C:/Users/User/OneDrive/Desktop/viettlot-main"; D=/tmp/vl_push
[ -d $D/.git ] || { rm -rf $D; gh repo clone heromassk/viettlot $D; }
cd $D && git config core.autocrlf false && git config user.name heromassk && git config user.email heromassk@users.noreply.github.com
git pull -q --rebase
cp "$S"/index_loto.html "$S"/*_history.csv "$S"/*.md . && cp -r "$S"/build/. build/ && rm -rf build/__pycache__ build/_tmp
git add -A; git diff --cached --quiet && { echo "Không có gì mới"; exit 0; }
git commit -qm "Cap nhat ket qua $(date +%d/%m/%Y)

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>" && git push 2>&1 | tail -1
