---
name: power
description: Power 6/55: nhập kết quả, chấm sổ, đưa pool + 5 vé kỳ tới theo dấu vết bi vật lý + tâm linh. Dùng khi anh nói "power", "gợi ý power", "dãy power", hoặc báo kết quả Power (6 số + ĐB).
---

# power — gợi ý Power 6/55

Xưng hô: gọi người dùng là **anh**, tự xưng **em**, trả lời tiếng Việt, ngắn gọn, dùng bảng.

## Nguyên tắc của anh (bắt buộc giữ)
- **Không so sánh với bốc ngẫu nhiên / bỏ bừa.** Phương pháp phải có quy luật, cơ sở, suy luận và **cố định cách tính qua các kỳ**; chấm bằng tỉ lệ đúng của chính nó, độ ổn định (10/50/200 kỳ, các khúc) và xu hướng gần đây.
- **Tâm linh / linh cảm được tôn trọng** (anh linh cảm 54 và nó về ở Power 03/10/2026). Anh nêu số linh cảm → `--linh`.
- Kết hợp nhiều cơ sở để thu hẹp pool mà vẫn giữ tỉ lệ trúng cao. Số nóng nằm ngoài pool vẫn phải cảnh báo.
- Thao tác xoá trong app luôn cần xác nhận.

## Đặc thù Power
- Quay **lồng cầu, bi vật lý** → giả thuyết **trọng lượng bi**: số vắng ≥20 kỳ bị loại khỏi pool; bộ bi có thể đổi nên ưu tiên 10/20/50 kỳ gần.
- Lịch quay: Thứ 3, 5, 7 (18h). Anh chơi **mọi kỳ** — cần chỗ dựa lâu dài ("1000 kỳ trúng 1 kỳ là đổi đời").
- **Đà tổng có dấu vết** (tương quan tổng kỳ liền nhau 50 kỳ ≈ +0.36, đang vùng thấp dưới mốc giữa 168) → vé chọn tổng theo khoảng đà.
- PP26 Bóng đối xứng và PP16 Gan là tốt nhất 50 kỳ gần (tháng 10/2026); bỏ khó ra và bỏ vắng ≥20 đã đúng hoàn toàn ở kỳ 03/10.
- Vé: rải ≥4 hàng chục (khẳng định 78–80%), ≥2 số >31, không 3 số liên tiếp; nếu phải nới thì script ghi rõ.
- Luật bổ sung (04/10/2026, `build/loai_tru.py`): số **vắng 11–15 kỳ** +1 điểm ("chín", ra nhiều hơn 3/3 khúc); số **vắng 6–10 kỳ** −0.5; số của **kỳ cùng thứ tuần trước** (cách 3 kỳ) −0.5 (ra ít hơn 3/3 khúc, `build/thu_them.py`).
- Luật loại vé (kỳ thật chỉ vi phạm 1–8%): trùng ≥3 số kỳ trước, toàn chẵn/lẻ, toàn nhỏ/lớn, ≥3 liên tiếp, ≥4 số cùng chục (6 số), không có số ≥2/3 dải. Các luật này giúp vé gọn, tự chúng không tăng trúng.
- `--cu` chạy cách cũ để so; luật nào làm pool kém đi trên các kỳ đã qua thì bỏ.

## Tâm linh (bắt buộc trình bày)
- Phiếu từ 20 quẻ (`build/tamlinh.js`). Top 12 phiếu +1 điểm; **tâm linh mạnh ★** (phiếu ≥ mức của số thứ 5) +1.5 điểm.
- **Số tâm linh mạnh bị luật vắng loại thì không loại hẳn** (được "cứu", để điểm quyết định) — anh: "tâm linh có số bị loại mà phiếu nhiều thì cần cân nhắc".
- Script in bảng **Tâm linh**: số, phiếu, quẻ chọn, trạng thái (trong pool #, hay ngoài pool vì luật nào), **dãy tâm linh** (top phiếu), cảnh báo **tâm linh mạnh ngoài pool**, và thêm **vé 6 "cân nhắc tâm linh"** (vé 1 đổi số điểm thấp sang số tâm linh mạnh ngoài pool).
- Luôn đưa phần này cho anh cùng pool; khi chấm sổ ghi riêng: tâm linh top 12 trúng mấy, dãy tâm linh trúng mấy, vé 6 trúng mấy.

- Luật loại mới (04/10/2026, `build/loai_nho.py`): bỏ **số ra ít nhất 100 kỳ** (đúng 93/93/91% kỳ).

## Sổ kiểm chứng suy luận (bắt buộc, theo dõi lâu dài)
- `build/theodoi.py` giữ `build/theodoi.json`: mỗi kỳ **trước khi quay** chụp số mà từng luật loại/khẳng định (cả luật đang áp dụng ● và luật đang theo dõi); **khi có kết quả** chấm đúng/sai từng luật + gợi ý đã đưa (pool 10/15/20, vé tốt nhất, tâm linh, MM).
- `build/add_result.py` **tự gọi** `theodoi.cham` (trước khi thêm kết quả) rồi `theodoi.snap` (chụp cho kỳ tới) → chỉ cần nhập kết quả như cũ. Kiểm tra dòng in "cham …: x/y luật đúng".
- App hiện thẻ **"Sổ kiểm chứng suy luận"**: % đúng từng luật, 10 kỳ gần (chấm xanh/đỏ), số bị loại kỳ tới, từng kỳ đã chấm. Khi báo kết quả cho anh, nêu luật nào đúng/sai kỳ này và tỉ lệ tích lũy.
- Luật mới: thêm vào `RULES`/`CLAIMS` trong `build/theodoi.py` (giữ id cũ), cập nhật `APPLIED` khi đưa luật vào gợi ý, rồi `python3 build/theodoi.py snap <game>`.

## Quy trình
1. **Anh báo kết quả** → `python3 build/add_result.py power "dd/mm/yyyy" n1 .. n6 ĐB` (ghi all_data.json, meta index.html, CSV rồi tự build app).
   Rồi **chấm sổ**: đọc dòng `"game": "power"` cuối trong `build/goiy_log.jsonl` (bản đã đưa anh) → so pool 10/15/20, từng tín hiệu, 5 vé, tâm linh top 12, số linh cảm → thêm 1 dòng vào bảng **Sổ chấm phương pháp Power** trong `ghi-chu-quy-luat.md`.
   Mạng chặn các trang kết quả Vietlott → không tự tra được; nếu anh chưa đưa số thì hỏi anh.
2. **Phiếu tâm linh + pool app + PP tốt nhất 50 kỳ**: `node build/tamlinh.js power > <scratchpad>/tl_power.json` (~30 giây).
3. **Gợi ý**: `python3 build/goiy.py power --app <scratchpad>/tl_power.json --json build/goiy_latest/power.json --save [--linh ..]`
   (in markdown đầy đủ; `--json` là dữ liệu cho bảng trực quan, `--save` lưu bản đã đưa anh để chấm sổ).
4. **Hiển thị trực quan (bắt buộc)**:
   - `node build/chup.js build/goiy_latest/power.json <scratchpad>/bang_power.png` → gửi ảnh cho anh bằng SendUserFile (display render). Ảnh gồm: lưới số tô theo pool 10/15/20, số bị loại gạch, ★ tâm linh, chấm nóng; thanh tỉ lệ pool trúng ≥1/≥2/≥3; khẳng định kỳ này (thanh % đúng, vạch vé giữ lại, ✔ dấu vết); vé gợi ý; tâm linh; số May Mắn (Loto).
   - Trong chat chỉ tóm tắt ngắn: pool 10/15, 3–5 khẳng định mạnh nhất, vé, cảnh báo (tâm linh mạnh ngoài pool, số nóng ngoài pool), chấm kỳ vừa rồi.
5. **Đăng lại app**: `python3 build/assemble.py` (nhúng bảng gợi ý mới vào thẻ "Gợi ý kỳ tới" đầu app) → `node build/check_page.js` (0 lỗi) → Artifact publish `build/nghien-cuu-loto.html` lên **cùng URL** https://claude.ai/artifact/X8ZmKZJ3RGDKZF7j8wbxFr (giữ capabilities; dữ liệu draws/preds/mine được giữ).
6. **Commit + push** lên nhánh đang làm.

Sửa app: nguồn `build/loto_template.html` → `python3 build/assemble.py`. Bố cục app: Gợi ý kỳ tới (bảng gọn, `build/bang.js`) → Dãy của anh → Nhập kết quả → Công cụ nghiên cứu (nâng cao, gom các phần cũ).
Khi chấm sổ: chấm thêm từng **khẳng định** đã lưu (`claims` trong goiy_log) — đúng hay sai.
