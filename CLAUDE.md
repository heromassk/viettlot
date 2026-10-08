# Vietlott — ghi chú bàn giao cho phiên Claude mới

Người dùng: gọi là **anh**, tự xưng **em**, trả lời tiếng Việt, ngắn gọn, dùng bảng. Đọc kỹ các skill trong `.claude/skills/` (loto, mega, power, suyluan) trước khi làm — nguyên tắc của anh nằm ở đầu mỗi skill.

## Nguyên tắc cốt lõi của anh (không được làm trái)
- Không so với "bốc ngẫu nhiên / bỏ bừa" như thước đo thắng thua; phương pháp phải có cơ sở, **cố định cách tính qua các kỳ**, chấm bằng tỉ lệ đúng của chính nó và độ ổn định (khung 10/20/50/100 kỳ, 3 đoạn 100 kỳ).
- **Chơi bền, không chơi ăn ngay**: không đổi luật/pool vì 1 kỳ; có kỳ trúng kỳ trật.
- **Dấu vết = xác suất nghiêng**, không phải đúng 100%. Lệch nhỏ mà ổn định vẫn dùng (trọng số nhỏ).
- **Luật đúng ≥70%** (khung 50 & 100 kỳ) là dùng tốt, miễn số bị loại không ra nhiều hơn trung bình.
- Luật loại chấm trên chuỗi kỳ dài: số "lâu lâu mới ra" có ra 1 kỳ thì chỉ thua kỳ đó. **Số/bộ đang trong thời gian nghỉ thì loại.**
- Luật về bi (Power, Mega, Max 3D): họ thay bi 1–2 tháng/lần → **tối đa 100 kỳ**, so 4 khung 10/20/50/100. Khi dò quy luật (vd cộng/trừ) chỉ xét **100, 200, 500 kỳ đổ lại**, không xét sâu hơn (anh, 08/10/2026).
- **Vé Power/Mega: chẵn/lẻ chỉ 2-4, 4-2, 3-3** — không gợi ý vé 1:5, 5:1 (anh, 06/10/2026).
- **Số vé mỗi kỳ cố định (~5 vé)** (anh, 06/10/2026: "chơi bền thì không thể mua nhiều"; hôm đó lỡ mua 10 vé Power vì nôn nóng). Khi anh muốn mua nhiều hơn, nhắc nhẹ; chỉ gợi ý tăng khi bảng báo nhịp pool tốt.
- Tôn trọng tâm linh, linh cảm. Thao tác xoá trong app luôn cần xác nhận.

## Dữ liệu và công cụ
- Lấy kết quả mới: `python3 build/lay_kq.py` (nguồn github.com/vietvudanh/vietlott-data; `--xem` để xem trước). Các trang kết quả khác bị mạng chặn.
- Nhập tay 1 kỳ: `python3 build/add_result.py loto|mega|power "<ngày>" số…` (tự chấm sổ kiểm chứng + chụp luật kỳ tới + dựng app).
- Gợi ý: `node build/tamlinh.js <game> > tl.json` rồi `python3 build/goiy.py <game> --app tl.json --json build/goiy_latest/<game>.json --save`; ảnh: `node build/chup.js build/goiy_latest/<game>.json out.png`.
- App: sửa `build/loto_template.html` → `python3 build/assemble.py` → `node build/check_page.js` (0 lỗi) → đăng `build/nghien-cuu-loto.html`.
- Sổ kiểm chứng: `build/theodoi.py`, `build/theodoi.json`. Vé anh đã mua: `build/ve_anh.jsonl`. Gợi ý đã đưa: `build/goiy_log.jsonl`.
- Nghiên cứu và kết quả: `ghi-chu-quy-luat.md` (ghi nối tiếp), `ra-soat-dau-vet.md`.
- Max 3D / 3D+ / Pro: dữ liệu `build/max3d_data.json`, `build/max3dpro_data.json`; ô trong app + gợi ý 3 cặp kèm lý do từ `build/max3d_app.py` (lưu gợi ý đã đưa vào `build/max3d_goiy_log.jsonl`); tâm linh `build/max3d_tamlinh.py`; các script `build/max3d_*.py`. Sau mỗi lần `lay_kq.py`: `python3 build/max3d_app.py` → `node build/max3d_tl.js` (17 phương pháp tâm linh, ra `build/max3d_tl.json`) → `python3 build/max3d_app.py` lần nữa (ghép cặp tâm linh) → `assemble.py`.

- **Loto 5/35: anh đã bỏ (06/10/2026 chiều, "quay bằng máy không đỡ được, phí tiền")** — không đưa gợi ý, không chấm Loto nữa trừ khi anh yêu cầu. Gợi ý 06/10 21h đã lưu nhưng không theo dõi. lay_kq.py vẫn thêm kỳ Loto vào dữ liệu (không hại), không cần báo anh.
- **Keno: anh đã bỏ (06/10/2026, "khó nhai")** — không đưa vé, không chấm, lay_kq.py không gọi sổ Keno nữa. Script và kết quả cũ giữ lại để tham khảo (`build/keno_*.py`, `keno_ve_anh.jsonl`, `keno_tay.json`; ghi chú trong ghi-chu-quy-luat.md). Chỉ làm lại khi anh yêu cầu.

- **Theo dõi quẻ ngày tháng** (anh, 07/10/2026): `build/ngaythang.py` → `build/ngaythang.md` (lay_kq.py tự chạy; add_result thì chạy tay). Nhóm số dương (thứ T2=2…CN=8, ngày, tháng, năm 26) và âm (ngày, tháng, năm) cho Power/Mega/Loto; khi đưa gợi ý thì nêu số ngày tháng của kỳ tới. Chi tiết từng thành phần + tổng: `python3 build/loto_ngaythang.py loto|power|mega` → `build/<game>_ngaythang.md`. Kết quả lần đầu: Power dương thứ–ngày–tháng nhỉnh nhẹ ổn định (3 đoạn 12,2·12,4·11,6% vs 10,9%), còn lại ≈ chia đều.

- **Bộ cố định mua bền Power/Mega** (anh, 07/10/2026): `build/bo_codinh_so.json` — 6 số ra nhiều nhất 100 kỳ gần, giữ ~100 kỳ rồi chọn lại (`build/bo_codinh.py` kiểm cách chọn). Power 01 05 07 08 13 16 (từ 08/10), Mega 06 16 31 33 36 44 (từ 09/10). Mỗi kỳ có kết quả: chấm bộ này, báo anh.

## App đã đăng
- **https://claude.ai/artifact/ULkC95JvE2BsKHfXyypXHF** — link mới (05/10/2026, tài khoản hiện tại; capabilities db + downloads). Đăng lại cùng URL bằng `build/nghien-cuu-loto.html`.
- Link cũ X8ZmKZJ3RGDKZF7j8wbxFr thuộc tài khoản cũ, không đọc/sửa được; dữ liệu anh nhập tay trong app cũ (draws/preds/mine) không chuyển sang.

## Việc đang dở (05/10/2026)
- Kỳ chờ kết quả, gợi ý đã lưu trong `goiy_log.jsonl`: Power 06/10, Mega 07/10, Max 3D Pro 06/10 (đoán thử, không mua). Có kết quả → chạy `lay_kq.py` (hoặc add_result) để chấm.
- Max 3D: đã hiện pool + 3 cặp gợi ý kèm lý do trong 2 ô app (Max 3D+: loại bộ ra 5 kỳ, tiến liên tiếp, tam hoa, giữ 340 bộ nặng 50 kỳ; Pro: loại bộ ra 30 kỳ, tiến, tam hoa, 00x, giữ 400 bộ nặng 100 kỳ + quẻ lộn ĐB kỳ trước). Khi anh báo kết quả Max 3D+/Pro: `python3 build/max3d_cham.py plus|pro "dd/mm/yyyy" <20 bộ theo thứ tự ĐB 2, Nhất 4, Nhì 6, Ba 8>` (chấm cặp gợi ý + pool, ghi `build/max3d_cham.jsonl`, thêm kỳ vào dữ liệu) rồi chạy lại chuỗi max3d_app → max3d_tl → max3d_app → assemble. Ảnh kết quả từ app Vietlott SMS: tab Max 3D+ hiện ĐB 2 bộ, Nhất 4, Nhì 6, Ba 8.
- Đề xuất chưa được duyệt: số May Mắn Loto "MM kỳ trước + 2 vắng lâu" (hiện giữ "3 vắng lâu nhất").
