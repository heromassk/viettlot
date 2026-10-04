---
name: loto
description: Loto 5/35: nhập kết quả 13h/21h, chấm sổ, đưa pool + 5 vé + 3 số May Mắn kỳ tới theo dấu vết riêng của Loto (máy tính quay) + tâm linh. Dùng khi anh nói "loto", "gợi ý loto", hoặc báo kết quả Loto (5 số + may mắn).
---

# loto — gợi ý Loto 5/35

Xưng hô: gọi người dùng là **anh**, tự xưng **em**, trả lời tiếng Việt, ngắn gọn, dùng bảng.

## Nguyên tắc của anh (bắt buộc giữ)
- **Không so sánh với bốc ngẫu nhiên / bỏ bừa.** Phương pháp phải có quy luật, cơ sở, suy luận và **cố định cách tính qua các kỳ**; chấm bằng tỉ lệ đúng của chính nó, độ ổn định (10/50/200 kỳ, các khúc) và xu hướng gần đây.
- **Tâm linh / linh cảm được tôn trọng** (anh linh cảm 54 và nó về ở Power 03/10/2026). Anh nêu số linh cảm → `--linh`.
- Kết hợp nhiều cơ sở để thu hẹp pool mà vẫn giữ tỉ lệ trúng cao. Số nóng nằm ngoài pool vẫn phải cảnh báo.
- Thao tác xoá trong app luôn cần xác nhận.

## Đặc thù Loto
- Quay bằng **máy tính, không có bi** → không dùng lý thuyết trọng lượng bi. Ngày 2 kỳ: **13h và 21h**.
- Dấu vết đã kiểm (04/10/2026, 924 kỳ, `build/loto_dauvet.py`, chi tiết trong ghi-chu-quy-luat.md):
  - **Mỗi phiên có tính cách riêng** (13h ổn định hơn 21h; 13h và 21h không giống nhau) → tín hiệu *nóng cùng phiên 100 kỳ*.
  - **Chuyển kỳ** (số hay theo sau các số kỳ trước) — ổn định nhất qua 3 khúc → tín hiệu *chuyển kỳ* (+1.5 điểm).
  - **Số May Mắn cân bằng** (MM ra nhiều khúc này thì khúc sau ít) → chọn **3 MM vắng lâu nhất** (≈30% trúng, ổn định).
  - **Không có dấu vết**: đà tổng, cặp số, đuôi số → script không dùng đà, chỉ dùng khoảng tổng thường gặp 200 kỳ.
- Luật bổ sung (04/10/2026, `build/loai_tru.py`): **số vừa ra kỳ trước** −1 điểm (ra ít hơn 3/3 khúc); **không loại số vắng lâu nữa** (vắng ≥31 kỳ ra nhiều hơn 3/3 khúc).
- Luật loại vé (kỳ thật chỉ vi phạm 1–8%): trùng ≥3 số kỳ trước, toàn chẵn/lẻ, toàn nhỏ/lớn, ≥3 liên tiếp, ≥4 số cùng chục (6 số), không có số ≥2/3 dải. Các luật này giúp vé gọn, tự chúng không tăng trúng.
- `--cu` chạy cách cũ để so; luật nào làm pool kém đi trên các kỳ đã qua thì bỏ.

## Tâm linh (bắt buộc trình bày)
- Phiếu từ 20 quẻ (`build/tamlinh.js`). Top 12 phiếu +1 điểm; **tâm linh mạnh ★** (phiếu ≥ mức của số thứ 5) +1.5 điểm.
- **Số tâm linh mạnh bị luật vắng loại thì không loại hẳn** (được "cứu", để điểm quyết định) — anh: "tâm linh có số bị loại mà phiếu nhiều thì cần cân nhắc".
- Script in bảng **Tâm linh**: số, phiếu, quẻ chọn, trạng thái (trong pool #, hay ngoài pool vì luật nào), **dãy tâm linh** (top phiếu), cảnh báo **tâm linh mạnh ngoài pool**, và thêm **vé 6 "cân nhắc tâm linh"** (vé 1 đổi số điểm thấp sang số tâm linh mạnh ngoài pool).
- Luôn đưa phần này cho anh cùng pool; khi chấm sổ ghi riêng: tâm linh top 12 trúng mấy, dãy tâm linh trúng mấy, vé 6 trúng mấy.

## Quy trình
1. **Anh báo kết quả** → `python3 build/add_result.py loto "dd/mm/yyyy 13h|21h" n1 .. n5 MM` (ghi all_data.json, meta index.html, CSV rồi tự build app).
   Rồi **chấm sổ**: đọc dòng `"game": "loto"` cuối trong `build/goiy_log.jsonl` (bản đã đưa anh) → so pool 10/15/20, từng tín hiệu, 5 vé, tâm linh top 12, số linh cảm, 3 số May Mắn → thêm 1 dòng vào bảng **Sổ chấm phương pháp Loto 5/35** trong `ghi-chu-quy-luat.md`.
   Mạng chặn các trang kết quả Vietlott → không tự tra được; nếu anh chưa đưa số thì hỏi anh.
2. **Phiếu tâm linh + pool app + PP tốt nhất 50 kỳ**: `node build/tamlinh.js loto > <scratchpad>/tl_loto.json` (~30 giây).
3. **Gợi ý**: `python3 build/goiy.py loto --app <scratchpad>/tl_loto.json --json build/goiy_latest/loto.json --save [--linh ..]`
   (in markdown đầy đủ; `--json` là dữ liệu cho bảng trực quan, `--save` lưu bản đã đưa anh để chấm sổ).
4. **Hiển thị trực quan (bắt buộc)**:
   - `node build/chup.js build/goiy_latest/loto.json <scratchpad>/bang_loto.png` → gửi ảnh cho anh bằng SendUserFile (display render). Ảnh gồm: lưới số tô theo pool 10/15/20, số bị loại gạch, ★ tâm linh, chấm nóng; thanh tỉ lệ pool trúng ≥1/≥2/≥3; khẳng định kỳ này (thanh % đúng, vạch vé giữ lại, ✔ dấu vết); vé gợi ý; tâm linh; số May Mắn (Loto).
   - Trong chat chỉ tóm tắt ngắn: pool 10/15, 3–5 khẳng định mạnh nhất, vé, cảnh báo (tâm linh mạnh ngoài pool, số nóng ngoài pool), chấm kỳ vừa rồi.
5. **Đăng lại app**: `python3 build/assemble.py` (nhúng bảng gợi ý mới vào thẻ "Gợi ý kỳ tới" đầu app) → `node build/check_page.js` (0 lỗi) → Artifact publish `build/nghien-cuu-loto.html` lên **cùng URL** https://claude.ai/artifact/X8ZmKZJ3RGDKZF7j8wbxFr (giữ capabilities; dữ liệu draws/preds/mine được giữ).
6. **Commit + push** lên nhánh đang làm.

Sửa app: nguồn `build/loto_template.html` → `python3 build/assemble.py`. Bố cục app: Gợi ý kỳ tới (bảng gọn, `build/bang.js`) → Dãy của anh → Nhập kết quả → Công cụ nghiên cứu (nâng cao, gom các phần cũ).
Khi chấm sổ: chấm thêm từng **khẳng định** đã lưu (`claims` trong goiy_log) — đúng hay sai.
