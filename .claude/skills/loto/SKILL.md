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
- Bỏ số vắng ≥15 kỳ vẫn giữ như một cách cố định, nhưng không giải thích bằng trọng lượng bi.

## Quy trình
1. **Anh báo kết quả** → `python3 build/add_result.py loto "dd/mm/yyyy 13h|21h" n1 .. n5 MM` (ghi all_data.json, meta index.html, CSV rồi tự build app).
   Rồi **chấm sổ**: đọc dòng `"game": "loto"` cuối trong `build/goiy_log.jsonl` (bản đã đưa anh) → so pool 10/15/20, từng tín hiệu, 5 vé, tâm linh top 12, số linh cảm, 3 số May Mắn → thêm 1 dòng vào bảng **Sổ chấm phương pháp Loto 5/35** trong `ghi-chu-quy-luat.md`.
   Mạng chặn các trang kết quả Vietlott → không tự tra được; nếu anh chưa đưa số thì hỏi anh.
2. **Phiếu tâm linh + pool app + PP tốt nhất 50 kỳ**: `node build/tamlinh.js loto > <scratchpad>/tl_loto.json` (~30 giây).
3. **Gợi ý**: `python3 build/goiy.py loto --app <scratchpad>/tl_loto.json --save [--linh ..] [--G 15] [--k 15]`
4. **Trình bày — LUÔN đưa pool ra**: Pool 10 / 15 / 20, bảng xếp hạng từng số (điểm, cơ sở, c10/c20, vắng), 5 vé (lõi + vệ tinh, trải), **3 số May Mắn**, số nóng ngoài pool, tỉ lệ của chính pool ở 10/50/200 kỳ. Kèm chấm kỳ vừa rồi nếu có.
5. **Đăng lại app** khi dữ liệu đổi: `node build/check_page.js` (phải 0 lỗi) → Artifact publish `build/nghien-cuu-loto.html` lên **cùng URL** https://claude.ai/artifact/X8ZmKZJ3RGDKZF7j8wbxFr (giữ capabilities db + downloads; dữ liệu draws/preds/mine được giữ).
6. **Commit + push** lên nhánh đang làm.

Sửa app: nguồn `build/loto_template.html` → `python3 build/assemble.py`.
