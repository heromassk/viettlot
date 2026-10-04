---
name: mega
description: Mega 6/45: nhập kết quả, chấm sổ, đưa pool + 5 vé kỳ tới theo dấu vết bi vật lý + tâm linh. Dùng khi anh nói "mega", "gợi ý mega", hoặc báo kết quả Mega (6 số).
---

# mega — gợi ý Mega 6/45

Xưng hô: gọi người dùng là **anh**, tự xưng **em**, trả lời tiếng Việt, ngắn gọn, dùng bảng.

## Nguyên tắc của anh (bắt buộc giữ)
- **Không so sánh với bốc ngẫu nhiên / bỏ bừa.** Phương pháp phải có quy luật, cơ sở, suy luận và **cố định cách tính qua các kỳ**; chấm bằng tỉ lệ đúng của chính nó, độ ổn định (10/50/200 kỳ, các khúc) và xu hướng gần đây.
- **Tâm linh / linh cảm được tôn trọng** (anh linh cảm 54 và nó về ở Power 03/10/2026). Anh nêu số linh cảm → `--linh`.
- Kết hợp nhiều cơ sở để thu hẹp pool mà vẫn giữ tỉ lệ trúng cao. Số nóng nằm ngoài pool vẫn phải cảnh báo.
- Thao tác xoá trong app luôn cần xác nhận.

## Đặc thù Mega
- Quay **lồng cầu, bi vật lý** → giả thuyết **trọng lượng bi**: số vắng ≥20 kỳ bị loại khỏi pool (ở Mega, việc bỏ số vắng lâu đúng nhiều hơn trong 200 kỳ gần); ưu tiên 10/20/50 kỳ gần vì bộ bi có thể đổi.
- Lịch quay: Thứ 4, 6, Chủ nhật (18h). Anh chơi **mọi kỳ**.
- Đà tổng chỉ dùng khi tương quan 50 kỳ > 0.2 (script tự quyết); nếu không thì dùng khoảng tổng thường gặp 200 kỳ.
- Vé (khẳng định có dấu vết, 04/10/2026): mỗi vé có ≥1 số của 2 kỳ gần nhất, ≥1 số trong 10 số nóng; ≥1 số trùng/kề kỳ trước; không trùng ≥2 số kỳ trước (lõi cũng không chứa ≥2 số kỳ trước); chẵn/lẻ và nhỏ/lớn 3±1; rải ≥4 hàng chục; không 3 số liên tiếp.
- Luật bổ sung (04/10/2026, `build/loai_tru.py`): số **cùng đuôi với số kỳ trước** −0.5 điểm (ra ít hơn 3/3 khúc).
- Luật loại vé (kỳ thật chỉ vi phạm 1–8%): trùng ≥3 số kỳ trước, toàn chẵn/lẻ, toàn nhỏ/lớn, ≥3 liên tiếp, ≥4 số cùng chục (6 số), không có số ≥2/3 dải. Các luật này giúp vé gọn, tự chúng không tăng trúng.
- `--cu` chạy cách cũ để so; luật nào làm pool kém đi trên các kỳ đã qua thì bỏ.

## Tâm linh (bắt buộc trình bày)
- Phiếu từ 20 quẻ (`build/tamlinh.js`). Top 12 phiếu +1 điểm; **tâm linh mạnh ★** (phiếu ≥ mức của số thứ 5) +1.5 điểm.
- **Số tâm linh mạnh bị luật vắng loại thì không loại hẳn** (được "cứu", để điểm quyết định) — anh: "tâm linh có số bị loại mà phiếu nhiều thì cần cân nhắc".
- Script in bảng **Tâm linh**: số, phiếu, quẻ chọn, trạng thái (trong pool #, hay ngoài pool vì luật nào), **dãy tâm linh** (top phiếu), cảnh báo **tâm linh mạnh ngoài pool**, và thêm **vé 6 "cân nhắc tâm linh"** (vé 1 đổi số điểm thấp sang số tâm linh mạnh ngoài pool).
- Luôn đưa phần này cho anh cùng pool; khi chấm sổ ghi riêng: tâm linh top 12 trúng mấy, dãy tâm linh trúng mấy, vé 6 trúng mấy.

## Quy trình
1. **Anh báo kết quả** → `python3 build/add_result.py mega "dd/mm/yyyy" n1 .. n6` (ghi all_data.json, meta index.html, CSV rồi tự build app).
   Rồi **chấm sổ**: đọc dòng `"game": "mega"` cuối trong `build/goiy_log.jsonl` (bản đã đưa anh) → so pool 10/15/20, từng tín hiệu, 5 vé, tâm linh top 12, số linh cảm → thêm 1 dòng vào bảng **Sổ chấm phương pháp Mega (tạo bảng nếu chưa có, cùng cột như sổ Power)** trong `ghi-chu-quy-luat.md`.
   Mạng chặn các trang kết quả Vietlott → không tự tra được; nếu anh chưa đưa số thì hỏi anh.
2. **Phiếu tâm linh + pool app + PP tốt nhất 50 kỳ**: `node build/tamlinh.js mega > <scratchpad>/tl_mega.json` (~30 giây).
3. **Gợi ý**: `python3 build/goiy.py mega --app <scratchpad>/tl_mega.json --json build/goiy_latest/mega.json --save [--linh ..]`
   (in markdown đầy đủ; `--json` là dữ liệu cho bảng trực quan, `--save` lưu bản đã đưa anh để chấm sổ).
4. **Hiển thị trực quan (bắt buộc)**:
   - `node build/chup.js build/goiy_latest/mega.json <scratchpad>/bang_mega.png` → gửi ảnh cho anh bằng SendUserFile (display render). Ảnh gồm: lưới số tô theo pool 10/15/20, số bị loại gạch, ★ tâm linh, chấm nóng; thanh tỉ lệ pool trúng ≥1/≥2/≥3; khẳng định kỳ này (thanh % đúng, vạch vé giữ lại, ✔ dấu vết); vé gợi ý; tâm linh; số May Mắn (Loto).
   - Trong chat chỉ tóm tắt ngắn: pool 10/15, 3–5 khẳng định mạnh nhất, vé, cảnh báo (tâm linh mạnh ngoài pool, số nóng ngoài pool), chấm kỳ vừa rồi.
5. **Đăng lại app**: `python3 build/assemble.py` (nhúng bảng gợi ý mới vào thẻ "Gợi ý kỳ tới" đầu app) → `node build/check_page.js` (0 lỗi) → Artifact publish `build/nghien-cuu-loto.html` lên **cùng URL** https://claude.ai/artifact/X8ZmKZJ3RGDKZF7j8wbxFr (giữ capabilities; dữ liệu draws/preds/mine được giữ).
6. **Commit + push** lên nhánh đang làm.

Sửa app: nguồn `build/loto_template.html` → `python3 build/assemble.py`. Bố cục app: Gợi ý kỳ tới (bảng gọn, `build/bang.js`) → Dãy của anh → Nhập kết quả → Công cụ nghiên cứu (nâng cao, gom các phần cũ).
Khi chấm sổ: chấm thêm từng **khẳng định** đã lưu (`claims` trong goiy_log) — đúng hay sai.
