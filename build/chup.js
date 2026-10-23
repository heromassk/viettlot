// Chụp bảng gợi ý thành ảnh PNG để gửi trong chat.
// node build/chup.js <file.json> <out.png>
const fs=require('fs'),path=require('path');
const {chromium}=require(require.resolve('playwright',{paths:['/opt/node-tools/node_modules',process.cwd()]}));
if(typeof globalThis.window==='undefined')globalThis.window={};   // bang.js đọc vài biến window.__* (lựa chọn trong app); chạy ngoài trình duyệt thì để trống
const {renderBang,BANG_CSS}=require('./bang.js');
const J=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const html=`<!doctype html><html><head><meta charset="utf-8"><style>:root{--panel:#1a2133;--panel2:#212a40;--text:#e8ecf5;--muted:#8b93a7;--border:#2c3550;}
body{margin:0;background:#0f1420;font-family:-apple-system,"Segoe UI",Roboto,sans-serif;padding:12px;}${BANG_CSS}</style></head><body><div id="o">${renderBang(J)}</div></body></html>`;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:460,height:900},deviceScaleFactor:2});
await p.setContent(html);await p.evaluate(()=>document.querySelectorAll('#o details').forEach(d=>{const s=d.querySelector('summary');if(/^\W*[23]\./.test(s&&s.textContent.trim()))d.open=true;}));await p.locator('#o').screenshot({path:process.argv[3]});await b.close();console.log('ok',process.argv[3]);})();
