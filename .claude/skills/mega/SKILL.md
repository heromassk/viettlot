---
name: mega
description: Mega 6/45: nhập kết quả, chấm sổ, đưa pool + 5 vé kỳ tới theo dấu vết bi vật lý + tâm linh. Dùng khi anh nói "mega", "gợi ý mega", hoặc báo kết quả Mega (6 số).
---

# mega — gợi ý Mega 6/45

Xưng hô: gọi người dùng là **anh**, tự xưng **em**, trả lời tiếng Việt, ngắn gọn, dùng bảng.

## Nguyên tắc của anh (bắt buộc giữ)
- **Luật đúng ≥70% là dùng tốt (anh, 05/10/2026).** Vắng lâu, khoảng nghỉ, nhịp… đúng ≥70% ở khung 50 và 100 kỳ thì dùng, miễn số bị loại không ra nhiều hơn trung bình. Chấm bằng `python3 build/luat_khung.py power|mega|loto` (4 khung 10/20/50/100 kỳ).
- **Luật không sai, chỉ là không xét quá nhiều kỳ (anh, 05/10/2026).** Xét quá khứ quá dài thì tính chất khác (bi đã thay). Mọi luật liên quan bi của Power/Mega dùng khung gần (Power 100, Mega 150 kỳ); khi kiểm luật mới cũng ưu tiên khung gần.
- **Tối đa 100 kỳ, xét theo 4 khung 10 / 20 / 50 / 100 kỳ (anh, 05/10/2026).** Họ thay bi khoảng 1–2 tháng/lần, nên luật nào về bi của Power/Mega chỉ xét tối đa 100 kỳ. Phải so dấu vết giữa 4 khung: số nào đồng nhất (nóng hoặc lạnh ở cả 4 khung), số nào "mới nóng" / "mới nguội". Theo dõi trường hợp vừa thay bi: 20 kỳ gần lệch hẳn 50 kỳ trước thì tin khung 10/20, bớt tin khung 50/100. Công cụ: `python3 build/khung_bi.py power|mega|loto`.
- **Luật liên quan bi chỉ xét x kỳ gần (anh, 05/10/2026: Vietlott thay bộ bi định kỳ).** Tính chất bi (dễ/khó ra, thưa, ra đều 4 đoạn, ra ít nhất…) dùng cửa sổ `WB` kỳ gần (`GOIY_WB`; Power 100, Mega 150 — chọn khung gần nhất không làm pool kém). Bảng số vắng lâu / số nóng ghi "Mức ra WB kỳ". Đã kiểm: tần suất từng bi ở 2 khối 100 kỳ liền nhau gần như không giữ (corr ≈0) → không nên dựa vào dữ liệu bi quá cũ.
- **Dấu vết = xác suất nghiêng, không phải đúng 100%.** Lệch nhỏ nhưng ổn định vẫn là dấu vết có giá trị (cho trọng số nhỏ, không bỏ).
- **Chơi bền, không chơi ăn ngay (anh, 04/10/2026):** không đổi luật/pool theo kết quả 1 kỳ; có kỳ trúng kỳ trật là bình thường. Khi có kết quả: chấm sổ và báo; chỉ đề xuất sửa luật khi số liệu cộng dồn nhiều kỳ (sổ kiểm chứng) cho thấy luật yếu đi, và phải kiểm trên 100–200 kỳ trước.
- **Cốt lõi (anh, 04/10/2026):** luật loại được chấm trên CHUỖI kỳ dài, không phán theo 1 kỳ. Số "lâu lâu mới ra" có ra 1 kỳ thì chỉ thua kỳ đó; sau đó nó lại vắng theo nhịp cũ → các kỳ sau vẫn loại đúng → cộng dồn vẫn thắng. Không bỏ luật vì 1 kỳ sai; chỉ xem lại khi tỉ lệ cộng dồn trong sổ kiểm chứng tụt dần nhiều kỳ (tính cách số đổi / bộ bi đổi).
- **Không so sánh với bốc ngẫu nhiên / bỏ bừa.** Phương pháp phải có quy luật, cơ sở, suy luận và **cố định cách tính qua các kỳ**; chấm bằng tỉ lệ đúng của chính nó, độ ổn định (10/50/200 kỳ, các khúc) và xu hướng gần đây.
- **Tâm linh / linh cảm được tôn trọng** (anh linh cảm 54 và nó về ở Power 03/10/2026). Anh nêu số linh cảm → `--linh`.
- Kết hợp nhiều cơ sở để thu hẹp pool mà vẫn giữ tỉ lệ trúng cao. Số nóng nằm ngoài pool vẫn phải cảnh báo.
- Thao tác xoá trong app luôn cần xác nhận.

## Đặc thù Mega
- Quay **lồng cầu, bi vật lý** → giả thuyết **trọng lượng bi**: số vắng **≥30** kỳ (đúng 94% kỳ) và số **ra 2 kỳ liền** (đúng 92%) bị loại khỏi pool; số ra nhiều cả 4 đoạn 25 kỳ +1 điểm (suyluan 04/10/2026). Trước đây dùng vắng ≥20 (chỉ đúng 72%) (ở Mega, việc bỏ số vắng lâu đúng nhiều hơn trong 200 kỳ gần); ưu tiên 10/20/50 kỳ gần vì bộ bi có thể đổi.
- Lịch quay: Thứ 4, 6, Chủ nhật (18h). Anh chơi **mọi kỳ**.
- Đà tổng chỉ dùng khi tương quan 50 kỳ > 0.2 (script tự quyết); nếu không thì dùng khoảng tổng thường gặp 200 kỳ.
- Vé (khẳng định có dấu vết, 04/10/2026): mỗi vé có ≥1 số của 2 kỳ gần nhất, ≥1 số trong 10 số nóng; ≥1 số trùng/kề kỳ trước; không trùng ≥2 số kỳ trước (lõi cũng không chứa ≥2 số kỳ trước); chẵn/lẻ và nhỏ/lớn 3±1; rải ≥4 hàng chục; không 3 số liên tiếp.
- Luật bổ sung (04/10/2026, `build/loai_tru.py`): số **cùng đuôi với số kỳ trước** −0.5 điểm (ra ít hơn 3/3 khúc).
- Luật loại vé (kỳ thật chỉ vi phạm 1–8%): trùng ≥3 số kỳ trước, toàn chẵn/lẻ, toàn nhỏ/lớn, ≥3 liên tiếp, ≥4 số cùng chục (6 số), không có số ≥2/3 dải. Các luật này giúp vé gọn, tự chúng không tăng trúng.
- `--cu` chạy cách cũ để so; luật nào làm pool kém đi trên các kỳ đã qua thì bỏ.

- **Vắng 11–15 kỳ ("chín") +1 điểm** (từ 04/10/2026, sau kỳ 4/6 số về đều vắng 11–14; pool 15 ở 50 kỳ 2.12→2.22).
- **Ý anh 04/10/2026 — loại trước:** số **vắng ≥20 kỳ** và số **"lâu lâu mới ra"** (200 kỳ ra ≤85% kỳ vọng) đang **vắng ≥15** (Mega, Loto). Bảng **"Số vắng lâu (≥15 kỳ)"** in trong gợi ý + ảnh: đang vắng, ra 100/200 kỳ, mức ra, % lần nghỉ ≥15, nghỉ dài nhất, % ra ngay kỳ kế khi đã vắng tới mức này (của chính số / mọi số), tâm linh, nhận định (Loại / Nghiêng loại / Cân nhắc / Theo dõi) — để anh tự nhận định.

- **Bảng "Số ra nhiều gần đây (10/20 kỳ)"** (anh, 04/10/2026): ra 10/20 kỳ, 100/200 kỳ, mức ra 200 kỳ, 4 đoạn 25 kỳ, đang vắng, % ra kỳ kế khi từng nóng tương tự, trạng thái, nhận xét (Nóng bền — có thể bi dễ ra / Nóng, đường dài cũng nhiều / Nóng ngắn hạn / Đang hồi). Luôn nêu cho anh cùng bảng số vắng lâu — liên hệ giả thuyết trọng lượng bi.

## Tâm linh (bắt buộc trình bày)
- Phiếu từ 20 quẻ (`build/tamlinh.js`). Top 12 phiếu +1 điểm; **tâm linh mạnh ★** (phiếu ≥ mức của số thứ 5) +1.5 điểm.
- **Số tâm linh mạnh bị luật vắng loại thì không loại hẳn** (được "cứu", để điểm quyết định) — anh: "tâm linh có số bị loại mà phiếu nhiều thì cần cân nhắc".
- Script in bảng **Tâm linh**: số, phiếu, quẻ chọn, trạng thái (trong pool #, hay ngoài pool vì luật nào), **dãy tâm linh** (top phiếu), cảnh báo **tâm linh mạnh ngoài pool**, và thêm **vé 6 "cân nhắc tâm linh"** (vé 1 đổi số điểm thấp sang số tâm linh mạnh ngoài pool).
- Luôn đưa phần này cho anh cùng pool; khi chấm sổ ghi riêng: tâm linh top 12 trúng mấy, dãy tâm linh trúng mấy, vé 6 trúng mấy.

- Luật loại mới (04/10/2026, `build/loai_nho.py`): bỏ **số ra kỳ trước VÀ kỳ t−3** (90/90/91%) và **số lớn nhất kỳ trước** (88/86/91%).

## Sổ kiểm chứng suy luận (bắt buộc, theo dõi lâu dài)
- `build/theodoi.py` giữ `build/theodoi.json`: mỗi kỳ **trước khi quay** chụp số mà từng luật loại/khẳng định (cả luật đang áp dụng ● và luật đang theo dõi); **khi có kết quả** chấm đúng/sai từng luật + gợi ý đã đưa (pool 10/15/20, vé tốt nhất, tâm linh, MM).
- `build/add_result.py` **tự gọi** `theodoi.cham` (trước khi thêm kết quả) rồi `theodoi.snap` (chụp cho kỳ tới) → chỉ cần nhập kết quả như cũ. Kiểm tra dòng in "cham …: x/y luật đúng".
- App hiện thẻ **"Sổ kiểm chứng suy luận"**: % đúng từng luật, 10 kỳ gần (chấm xanh/đỏ), số bị loại kỳ tới, từng kỳ đã chấm. Khi báo kết quả cho anh, nêu luật nào đúng/sai kỳ này và tỉ lệ tích lũy.
- Luật mới: thêm vào `RULES`/`CLAIMS` trong `build/theodoi.py` (giữ id cũ), cập nhật `APPLIED` khi đưa luật vào gợi ý, rồi `python3 build/theodoi.py snap <game>`.

## Quy trình
1. **Anh báo kết quả** → `python3 build/add_result.py mega "dd/mm/yyyy" n1 .. n6` (ghi all_data.json, meta index.html, CSV rồi tự build app).
   Anh muốn loại tay số nào kỳ này → `--bo 02,27` (ghi vào bảng + log).
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
