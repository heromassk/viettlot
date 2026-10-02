# Phương pháp nghiên cứu quy luật (làm trên Loto trước, sau áp cho Mega / Power)

Quy ước chung
- Dữ liệu: 500 kỳ gần nhất của game. Mỗi game độc lập.
- Xếp số mỗi kỳ từ bé đến lớn: u v w x y (Mega/Power thêm z). Số may mắn (Loto) / số đặc biệt (Power) là dãy riêng.
- Một "dãy vị trí" = giá trị của cùng một vị trí qua các kỳ (dãy u, dãy v…).
- Một quy luật được ghi: đúng bao nhiêu kỳ / tổng số kỳ áp dụng (%), ổn định (tỉ lệ trong từng đoạn 100 kỳ),
  và kiểm tra trên dữ liệu mới (học 250 kỳ đầu → đúng bao nhiêu % ở 250 kỳ sau).
- Ngưỡng: quy luật ≥ 60% coi là mạnh; ưu tiên quy luật ổn định qua các đoạn.

## PP1. Khoảng theo vị trí
Khoảng hẹp nhất chứa 50/60/70/80/90% giá trị của từng dãy vị trí. Ghép khoảng 5 vị trí → % kỳ cả 5 cùng đúng, số bộ còn lại.

## PP2. Khi biết kỳ trước (theo giá trị)
Chia giá trị kỳ trước thành 5 nhóm → khoảng hẹp nhất chứa ≥70% giá trị kỳ sau cho từng nhóm.

## PP3. Quan hệ kỳ sau – kỳ trước
Cách kỳ trước ≤ k, cùng/khác chẵn lẻ, cùng số dư chia 3/4/5, lặp đúng giá trị, đảo chiều tăng/giảm.
"Kỳ trước" xét theo: liền trước, cùng giờ hôm trước (13h→13h, 21h→21h), cùng thứ, cùng ngày dương, cùng ngày âm, cách 2/3/4/7/14 kỳ.

## PP4. Quy luật có điều kiện "nếu kỳ trước ≥ c thì giảm / ≤ c thì tăng"

## PP5. Dãy chênh lệch (tăng/giảm, cấp số)
d = kỳ sau − kỳ trước. Khoảng của d; tiếp tục cấp số (d sau = d trước); đảo ngược (d sau ≈ −d trước);
chênh bậc 2; hướng theo độ lớn chênh trước (giảm mạnh ≤−6, giảm nhẹ, đứng, tăng nhẹ, tăng mạnh ≥6);
mẫu 3 dấu gần nhất ("−++", "+−−"…); khoảng 70% theo (độ lớn chênh × mức giá trị) và (mẫu dấu × mức giá trị).

## PP6. Dãy zic zắc (đường chéo qua các kỳ)
Các bộ: chéo lên u→v→w→x→y, chéo xuống, nảy u…y…u, nảy y…u…y, nhảy (u,w,y,v,x), (u,x,v,y,w), cặp (u,v), (x,y), (u,y), (u,w,y), (v,x);
mọi điểm xuất phát. Quy luật: chênh giữa 2 bước nằm trong khoảng 70% (theo từng cặp vị trí chuyển tiếp).

## PP7. Khoảng cách trong cùng kỳ (A = v−u, B = w−v, C, D…)
Khoảng thường gặp theo x kỳ / cùng ngày dương / âm; chia nhỏ %; khoảng hẹp nhất ≥70% và từng giá trị; tự tìm cách chia;
khi biết 1 số → khoảng các số còn lại.

## PP8. Tổng đối xứng (u+y, v+x; Mega/Power: u+z, v+y, w+x)
Khoảng thường gặp, chia nhóm, theo x kỳ / cùng ngày dương / âm.

## PP9. Cùng ngày các tháng trước (dương / âm)
Số ra, số phiếu, khoảng cách, tổng 2 số liền, tổng 3 số liền; số / tổng lặp lại.

## PP10. Bộ kiểm định chung
Tần suất từng số, số may mắn, cặp số, chu kỳ lặp, 13h vs 21h, thứ, chia dư, tương quan giữa các kỳ, Markov chuyển tiếp.

## PP11. Dò tự động quy luật HƯỚNG (kỳ sau tăng / giảm / tăng-hoặc-đứng / giảm-hoặc-đứng)
Đặc điểm của kỳ vừa ra (dùng 1 hoặc ghép 2 đặc điểm):
- chênh (giảm mạnh ≤−6, giảm nhẹ, đứng, tăng nhẹ, tăng mạnh ≥6), mẫu 3 dấu gần nhất,
- mức giá trị (5 nhóm theo phân vị), số vị trí vừa tăng (0–1, 2–3, 4–5), tổng 5 số tăng/giảm (chênh/3 chia 5 mức),
- khoảng cách tới số bên cạnh (sát ≤3, vừa 4–8, xa ≥9), giờ kỳ tới (13h/21h), thứ kỳ tới, ngày âm kỳ tới (1–10, 11–20, 21–30).
Giữ quy luật: áp dụng ≥ 40 kỳ, đúng ≥ 65% ở cả 250 kỳ đầu và 250 kỳ sau, mỗi đoạn 100 kỳ ≥ 55%.

## PP12. Gộp phiếu nhiều quy luật hướng
Mỗi quy luật (chọn từ 250 kỳ đầu, ≥65%) đang áp dụng bỏ 1 phiếu tăng hoặc giảm; hiệu số phiếu ≥ K (3/5/8) thì dự đoán theo bên nhiều phiếu.
Đổi hướng thành khoảng: tăng → [số vừa ra, đỉnh khoảng 90%], giảm → [đáy khoảng 90%, số vừa ra].

## PP13. Quan hệ các số trong cùng kỳ
Hiệu số mọi cặp vị trí (v−u, w−u…, y−u), tổng 2 số mọi cặp, tổng 3 số liền, tổng 5, số lẻ, số ≥ 18, khoảng cách lớn/nhỏ nhất.
Mỗi đại lượng: khoảng hẹp nhất chứa x%, ổn định 5 đoạn, nửa đầu → nửa sau, % bộ (trong mọi tổ hợp) còn lại.

## PP14. Ghép nhiều ràng buộc để thu hẹp
Mỗi ràng buộc lấy khoảng 70/80/90/95%; máy tự chọn tham lam (mỗi bước chọn ràng buộc giữ % kỳ đúng cao nhất trên % bộ còn lại);
thêm khoảng hướng dự đoán kỳ tới; đếm số bộ còn lại; lấy 10 bộ điểm cao nhất (điểm = tổng log tần suất số tại từng vị trí, các bộ trùng nhau ≤ 2 số).

## Công cụ: index_loto.html (trang nghiên cứu riêng Loto)
Thêm kết quả ngay trên trang (lưu trình duyệt, xuất dữ liệu); dự đoán hướng (PP11–12) + kiểm tra nửa đầu → nửa sau; nhật ký 30 kỳ;
khoảng theo vị trí (PP1); dãy vị trí các kỳ gần đây; quan hệ trong kỳ (PP13); thu hẹp (PP14).

## PP15–PP27. Chọn POOL số (thu hẹp từ 35 số), chấm điểm từng số rồi lấy K số điểm cao nhất
- PP15 Nóng: số lần ra trong w kỳ (10/20/30/50/100).
- PP16 Gan: số kỳ từ lần ra cuối (lâu chưa ra điểm cao).
- PP17 Chu kỳ lặp: |số kỳ chưa ra − chu kỳ trung bình của số đó| nhỏ thì điểm cao (đến hạn). PP17b: tần suất chu kỳ đúng bằng khoảng hiện tại.
- PP18 Tích lũy: độ dốc đường tích lũy (số lần ra 30 kỳ gần − nửa số lần ra 60 kỳ trước đó); "đang giảm" → sắp hồi.
- PP19 Cấp số các lần ra: 2 (hoặc 3) lần ra gần nhất cách đều → lần ra tiếp theo đúng kỳ tới.
- PP20 Số kề kỳ trước ±1 / ±2; PP20c lặp lại số kỳ trước.
- PP21 Tần suất số tại từng vị trí (500 kỳ).
- PP22 Markov số → số: số i ra kỳ trước thì kỳ sau hay ra số j.
- PP23 Cặp hay đi cùng (đồng xuất hiện) với số kỳ trước.
- PP24 Cùng giờ (60 kỳ cùng 13h/21h), PP24b cùng thứ, PP24c cùng ngày âm.
- PP25 Đầu – đuôi (chữ số hàng chục / đơn vị hay ra 30 kỳ).
- PP26 Bóng đối xứng 36−n; tổng / hiệu các cặp số kỳ trước.
- PP27 Gộp: mỗi kỳ chọn 5 phương pháp có thành tích tốt nhất 50 kỳ gần nhất, cộng điểm hạng có trọng số.
Đánh giá: mỗi kỳ chỉ dùng dữ liệu trước nó; pool K = 5/8/10/12/15/18/20; ghi TB số trúng trong pool, % kỳ ≥2, ≥3 số; trên 500 và 200 kỳ;
và "sau kỳ trượt": kỳ trước pool < 3 số thì kỳ sau ≥ 3 số bao nhiêu %.

## PP28. Chấm lại 305 phương pháp của index.html cũ (số gợi ý tính sẵn từng kỳ)
Giải nén dữ liệu gợi ý (b64 → gzip → mảng Uint32, mỗi phương pháp × kỳ: 2 từ bit số chính + 1 từ bit số may mắn).
Trên 500 kỳ, tách chung / 13h / 21h: % kỳ ≥1, ≥2, ≥3 số trúng; % số gợi ý trúng; TB số gợi ý; số may mắn trúng %.
Kiểm tra ổn định: nửa đầu (250) → nửa sau (250); với chênh lệch 13h/21h kiểm tra cả số lượng số gợi ý theo giờ.

## Áp cho Mega / Power (đã làm 02/10/2026)
- Script chung: research.py <game> (PP1, PP3, PP5, PP11–14), pool_g.py <game> (PP15–27), old_g.py <game> (PP28).
- Ngưỡng co giãn theo số lượng số N: mạnh = 6×N/35; cách số bên: sát ≤ 3N/35, xa ≥ 8N/35+1. Đếm bộ còn lại: mẫu 300.000 bộ ngẫu nhiên × tổng C(N,6).
