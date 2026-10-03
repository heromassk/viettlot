---
name: goiy
description: Gợi ý số tiềm năng Vietlott (power / mega / loto) theo các phương pháp dấu vết cố định + tâm linh; cập nhật kết quả, chấm sổ phương pháp, đăng lại app. Dùng khi anh nói "gợi ý", "goiy", "pool", "dãy power hôm nay", hoặc báo kết quả kỳ mới.
---

# goiy — gợi ý tiềm năng

Xưng hô: gọi người dùng là **anh**, tự xưng **em**, trả lời tiếng Việt, ngắn, bằng bảng.

## Nguyên tắc của anh (bắt buộc giữ)
- **Không so sánh với bốc ngẫu nhiên / bỏ bừa.** Mỗi phương pháp được chấm bằng tỉ lệ đúng của chính nó, độ ổn định qua các kỳ (10/50/200 kỳ) và xu hướng gần đây. Phương pháp phải có quy luật, cơ sở, suy luận và **cố định** cách tính qua các kỳ.
- Anh chơi mọi kỳ Power và Mega, nên cần chỗ dựa lâu dài: "1000 kỳ trúng 1 kỳ là thay đổi rồi".
- Power và Mega quay bằng **lồng cầu, bi vật lý**. Số vắng lâu (≥20 kỳ) có thể do lệch trọng lượng bi nên bị loại khỏi pool. Bộ bi có thể đổi, vì vậy ưu tiên nhìn 10/20/50 kỳ gần nhất. Số đang nóng mà nằm ngoài pool vẫn phải cảnh báo.
- Loto 5/35 quay bằng máy tính, nên giả thuyết trọng lượng bi không áp dụng.
- **Tâm linh và linh cảm được tôn trọng.** Anh từng linh cảm số 54 và số đó về (Power 03/10/2026). Nếu anh nêu số linh cảm, truyền vào `--linh`.
- Kết hợp nhiều cơ sở để thu hẹp pool mà vẫn giữ được tỉ lệ trúng cao.
- Thao tác xoá trong app luôn cần xác nhận.

## Quy trình
1. **Nếu anh báo kết quả mới**, cập nhật cả 3 nguồn (all_data.json, meta trong index.html, CSV), sau đó lệnh tự build lại app:
   ```
   python3 build/add_result.py power "06/10/2026" n1 n2 n3 n4 n5 n6 ĐB
   python3 build/add_result.py mega  "04/10/2026" n1 .. n6
   python3 build/add_result.py loto  "03/10/2026 21h" n1 .. n5 MM
   ```
   Sau đó **chấm sổ**: so kết quả với lần gợi ý trước (pool, từng tín hiệu, các vé, dãy tâm linh, số linh cảm) và ghi vào bảng "Sổ chấm phương pháp" trong `ghi-chu-quy-luat.md`.
2. **Lấy phiếu tâm linh, pool app và PP tốt nhất 50 kỳ** (Playwright, mất khoảng 30 giây):
   `node build/tamlinh.js power > <scratchpad>/tl.json`
3. **Tính gợi ý**:
   `python3 build/goiy.py power --app <scratchpad>/tl.json [--linh 54] [--G 20] [--k 15]`
   Script in ra markdown gồm:
   - Bảng tín hiệu và tỉ lệ đúng của chính từng tín hiệu ở 10/50/200 kỳ. Các tín hiệu: nóng, kề ±1, bóng dễ ra, bóng khó ra, vắng ≥G.
   - Đà tổng (tương quan tổng 50 kỳ), từ đó suy ra khoảng tổng nên chọn.
   - Phiếu tâm linh top 12, pool app, PP tốt nhất 50 kỳ.
   - Pool 15 theo điểm đồng thuận, kèm cảnh báo số nóng nằm ngoài pool.
   - 5 vé: 3 vé lõi + vệ tinh và 2 vé trải.

   Ràng buộc vé: tổng nằm trong khoảng đà; Power/Mega có ≥2 số >31; không có 3 số liên tiếp. Ràng buộc nào phải nới thì script ghi rõ cạnh vé.
4. **Trình bày cho anh**: pool, 5 vé, số cần chú ý. Bảng tín hiệu nêu rõ tỉ lệ của chính nó, không so ngẫu nhiên. Loto chưa có số May Mắn trong script; nếu anh cần thì chọn MM theo phần MM trong app.
5. **Đăng lại app** nếu dữ liệu đổi. Publish `build/nghien-cuu-loto.html` lên **cùng URL** https://claude.ai/artifact/X8ZmKZJ3RGDKZF7j8wbxFr và giữ capabilities `{db:{}, downloads:true}`. Trước khi đăng, kiểm tra trang không có pageerror (mở bằng Playwright).
6. **Commit và push** lên nhánh đang làm việc.

## Sửa app
- Nguồn app là `build/loto_template.html`. Sau khi sửa, chạy `python3 build/assemble.py`, lệnh này sinh `index_loto.html` và `build/nghien-cuu-loto.html`.
- Dữ liệu trong DB của artifact gồm các collection draws*, preds* và mine*. Dữ liệu này được giữ nguyên qua các phiên bản.
