# Vietlott — ghi chú bàn giao cho phiên Claude mới

Người dùng: gọi là **anh**, tự xưng **em**, trả lời tiếng Việt, ngắn gọn, dùng bảng. Đọc kỹ các skill trong `.claude/skills/` (loto, mega, power, suyluan) trước khi làm — nguyên tắc của anh nằm ở đầu mỗi skill.

## Nguyên tắc cốt lõi của anh (không được làm trái)
- Không so với "bốc ngẫu nhiên / bỏ bừa" như thước đo thắng thua; phương pháp phải có cơ sở, **cố định cách tính qua các kỳ**, chấm bằng tỉ lệ đúng của chính nó và độ ổn định (khung 10/20/50/100 kỳ, 3 đoạn 100 kỳ).
- **Chơi bền, không chơi ăn ngay**: không đổi luật/pool vì 1 kỳ; có kỳ trúng kỳ trật.
- **Dấu vết = xác suất nghiêng**, không phải đúng 100%. Lệch nhỏ mà ổn định vẫn dùng (trọng số nhỏ).
- **Luật đúng ≥70%** (khung 50 & 100 kỳ) là dùng tốt, miễn số bị loại không ra nhiều hơn trung bình.
- Luật loại chấm trên chuỗi kỳ dài: số "lâu lâu mới ra" có ra 1 kỳ thì chỉ thua kỳ đó. **Số/bộ đang trong thời gian nghỉ thì loại.**
- Luật về bi (Power, Mega, Max 3D): họ thay bi 1–2 tháng/lần → **tối đa 100 kỳ**, so 4 khung 10/20/50/100. **Power/Mega: mọi phép xét/dò quy luật/backtest chỉ dùng tối đa 200 kỳ gần nhất** (khung 10/20/50/100/200; anh, 09/10/2026 — thay cho 100/200/500 trước đó).
- **Vé Power/Mega: chẵn/lẻ chỉ 2-4, 4-2, 3-3** — không gợi ý vé 1:5, 5:1 (anh, 06/10/2026).
- **Từ 10/10/2026 mua đều mỗi ngày 3 vé** (anh, sau kỳ Mega 09/10 trật 0/6: "không nản, bình tĩnh"): Power/Mega dùng ma trận pool 9 → 3 vé (`goiy.py <game> --mt 9`; 3 nhóm × 3 số, mỗi vé 2 nhóm). Chấm lùi Mega 100 kỳ: vé tốt nhất TB 1,25, ≥3 số 9% (ma trận 12/6 vé: 1,67, 17%).
- (cũ) **Power: mua ma trận pool 12 → 6 vé** (anh 08/10/2026: "5 vé cũng phải dùng ma trận để bao số"; `goiy.py power --mt 12`). 
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

- **Bộ cố định mua bền Power/Mega** (anh, 07/10/2026): `build/bo_codinh_so.json` — 6 số ra nhiều nhất 100 kỳ gần, giữ ~100 kỳ rồi chọn lại (`build/bo_codinh.py` kiểm cách chọn). **Power đã bỏ** (anh 09/10/2026: "bộ quá thấp k hợp lý" — 0,59–0,68 số/kỳ, ≥3 số 4/300 kỳ). Chỉ còn Mega 06 16 31 33 36 44 (từ 09/10): mỗi kỳ có kết quả chấm bộ này, báo anh.

## App đã đăng
- **https://claude.ai/artifact/ULkC95JvE2BsKHfXyypXHF** — link mới (05/10/2026, tài khoản hiện tại; capabilities db + downloads). Đăng lại cùng URL bằng `build/nghien-cuu-loto.html`.
- Link cũ X8ZmKZJ3RGDKZF7j8wbxFr thuộc tài khoản cũ, không đọc/sửa được; dữ liệu anh nhập tay trong app cũ (draws/preds/mine) không chuyển sang.

## Việc đang dở (05/10/2026)
- Kỳ chờ kết quả, gợi ý đã lưu trong `goiy_log.jsonl`: Power 06/10, Mega 07/10, Max 3D Pro 06/10 (đoán thử, không mua). Có kết quả → chạy `lay_kq.py` (hoặc add_result) để chấm.
- Max 3D: đã hiện pool + 3 cặp gợi ý kèm lý do trong 2 ô app (Max 3D+: loại bộ ra 5 kỳ, tiến liên tiếp, tam hoa, giữ 340 bộ nặng 50 kỳ; Pro: loại bộ ra 30 kỳ, tiến, tam hoa, 00x, giữ 400 bộ nặng 100 kỳ + quẻ lộn ĐB kỳ trước). Khi anh báo kết quả Max 3D+/Pro: `python3 build/max3d_cham.py plus|pro "dd/mm/yyyy" <20 bộ theo thứ tự ĐB 2, Nhất 4, Nhì 6, Ba 8>` (chấm cặp gợi ý + pool, ghi `build/max3d_cham.jsonl`, thêm kỳ vào dữ liệu) rồi chạy lại chuỗi max3d_app → max3d_tl → max3d_app → assemble. Ảnh kết quả từ app Vietlott SMS: tab Max 3D+ hiện ĐB 2 bộ, Nhất 4, Nhì 6, Ba 8.
- Đề xuất chưa được duyệt: số May Mắn Loto "MM kỳ trước + 2 vắng lâu" (hiện giữ "3 vắng lâu nhất").

- **Máy học Mega** (anh, 09/10/2026): `build/mega_pipeline.py` học trọng số ≤200 kỳ, ô "Máy học Mega" trong app, sổ tiến `build/hoc_log.jsonl`. lay_kq.py tự chạy. Chạy song song để chấm tiến, chưa thay pool chính (chấm lùi kém hơn cách hiện tại).

- **Pool 25 Power** (anh duyệt 10/10/2026): `build/pool25_power.py` — cộng hạng chéo Mega 7 kỳ + vắng ≈25 + vắng ≈27 kỳ; 100 kỳ gần ≥4 số 42%, ≥3 số 72% (100 kỳ cũ hơn chỉ 23%). Ô "Pool 25 Power" trong app, sổ tiến `build/pool25_power_log.jsonl`; lay_kq/add_result tự chạy. Thay nếu ≥4 dưới 35% liên tục 20 kỳ. Quét 2.891–5.491 phương pháp: `build/pool25_quet.py`. Nhãn hồ sơ số không giúp loại thêm trong pool này. **Pool 20** (anh chốt 10/10: "20 số đạt 30% trên 4 số cũng ok"): bỏ số có đúng 3 phiếu tâm linh khỏi pool 25 (100 kỳ: ≥4 ~30%, 2 nửa 30·30) — chạy `node build/tamlinh.js power > tl.json` rồi `python3 build/pool25_power.py --tl tl.json` trước mỗi kỳ.
