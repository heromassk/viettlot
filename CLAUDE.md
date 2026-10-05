# Vietlott — ghi chú bàn giao cho phiên Claude mới

Người dùng: gọi là **anh**, tự xưng **em**, trả lời tiếng Việt, ngắn gọn, dùng bảng. Đọc kỹ các skill trong `.claude/skills/` (loto, mega, power, suyluan) trước khi làm — nguyên tắc của anh nằm ở đầu mỗi skill.

## Nguyên tắc cốt lõi của anh (không được làm trái)
- Không so với "bốc ngẫu nhiên / bỏ bừa" như thước đo thắng thua; phương pháp phải có cơ sở, **cố định cách tính qua các kỳ**, chấm bằng tỉ lệ đúng của chính nó và độ ổn định (khung 10/20/50/100 kỳ, 3 đoạn 100 kỳ).
- **Chơi bền, không chơi ăn ngay**: không đổi luật/pool vì 1 kỳ; có kỳ trúng kỳ trật.
- **Dấu vết = xác suất nghiêng**, không phải đúng 100%. Lệch nhỏ mà ổn định vẫn dùng (trọng số nhỏ).
- **Luật đúng ≥70%** (khung 50 & 100 kỳ) là dùng tốt, miễn số bị loại không ra nhiều hơn trung bình.
- Luật loại chấm trên chuỗi kỳ dài: số "lâu lâu mới ra" có ra 1 kỳ thì chỉ thua kỳ đó. **Số/bộ đang trong thời gian nghỉ thì loại.**
- Luật về bi (Power, Mega, Max 3D): họ thay bi 1–2 tháng/lần → **tối đa 100 kỳ**, so 4 khung 10/20/50/100.
- Tôn trọng tâm linh, linh cảm. Thao tác xoá trong app luôn cần xác nhận.

## Dữ liệu và công cụ
- Lấy kết quả mới: `python3 build/lay_kq.py` (nguồn github.com/vietvudanh/vietlott-data; `--xem` để xem trước). Các trang kết quả khác bị mạng chặn.
- Nhập tay 1 kỳ: `python3 build/add_result.py loto|mega|power "<ngày>" số…` (tự chấm sổ kiểm chứng + chụp luật kỳ tới + dựng app).
- Gợi ý: `node build/tamlinh.js <game> > tl.json` rồi `python3 build/goiy.py <game> --app tl.json --json build/goiy_latest/<game>.json --save`; ảnh: `node build/chup.js build/goiy_latest/<game>.json out.png`.
- App: sửa `build/loto_template.html` → `python3 build/assemble.py` → `node build/check_page.js` (0 lỗi) → đăng `build/nghien-cuu-loto.html`.
- Sổ kiểm chứng: `build/theodoi.py`, `build/theodoi.json`. Vé anh đã mua: `build/ve_anh.jsonl`. Gợi ý đã đưa: `build/goiy_log.jsonl`.
- Nghiên cứu và kết quả: `ghi-chu-quy-luat.md` (ghi nối tiếp), `ra-soat-dau-vet.md`.
- Max 3D / 3D+ / Pro: dữ liệu `build/max3d_data.json`, `build/max3dpro_data.json`; ô trong app + gợi ý 3 cặp kèm lý do từ `build/max3d_app.py` (lưu gợi ý đã đưa vào `build/max3d_goiy_log.jsonl`); tâm linh `build/max3d_tamlinh.py`; các script `build/max3d_*.py`. Sau mỗi lần `lay_kq.py`: `python3 build/max3d_app.py` → `node build/max3d_tl.js` (17 phương pháp tâm linh, ra `build/max3d_tl.json`) → `python3 build/max3d_app.py` lần nữa (ghép cặp tâm linh) → `assemble.py`.

## App đã đăng
- https://claude.ai/artifact/X8ZmKZJ3RGDKZF7j8wbxFr — thuộc tài khoản cũ. Tài khoản mới không ghi đè được link này trừ khi được chia sẻ quyền sửa; nếu không, đăng thành link mới từ `build/nghien-cuu-loto.html`.

## Việc đang dở (05/10/2026)
- Kỳ chờ kết quả, gợi ý đã lưu trong `goiy_log.jsonl`: Loto 05/10 21h, Power 06/10, Mega 07/10. Có kết quả → chạy `lay_kq.py` (hoặc add_result) để chấm.
- Max 3D: đã hiện pool + 3 cặp gợi ý kèm lý do trong 2 ô app (Max 3D+: loại bộ ra 5 kỳ, tiến liên tiếp, tam hoa, giữ 340 bộ nặng 50 kỳ; Pro: loại bộ ra 20 kỳ, tiến, tam hoa + quẻ lộn ĐB kỳ trước). Chưa làm: chấm sổ kiểm chứng Max 3D từ `max3d_goiy_log.jsonl` khi có kết quả.
- Đề xuất chưa được duyệt: số May Mắn Loto "MM kỳ trước + 2 vắng lâu" (hiện giữ "3 vắng lâu nhất").
