# Ghi chú: hướng nghiên cứu quy luật (Loto 5/35 và các game)

## Quan điểm của người dùng (giữ nguyên khi làm tiếp)
- Kiên định với các phương pháp quy luật; mục tiêu là **cơ sở có tỉ lệ %**, không cần quy luật chính xác.
- **Không so sánh với ngẫu nhiên** trong các phần mới, chỉ đưa ra tỉ lệ % đúng của quy luật.
- Máy cần "học xác suất": tỉ lệ % tự cập nhật khi có kết quả mới; kỳ này không trùng thì kỳ khác có thể trùng.
- Mặc định xét trên **500 kỳ gần nhất**; các game độc lập, quy luật chỉ cần đúng trong 1 game.
- Xét cả ngày dương và **ngày âm** (theo tâm linh nên ưu tiên ngày âm), cùng thứ, 13h / 21h.
- Số xếp từ bé đến lớn: u v w x y (z với Mega/Power); khoảng cách A = v−u, B = w−v…; tổng đối xứng u+z, v+y, w+x.

## Quy luật gần đúng đã tìm được (Loto, 500 kỳ đến 01/10/2026)
| Quy luật | Tỉ lệ đúng |
|---|---|
| u nằm trong 1–8 / 1–10 / 1–13 | 72% / 81% / 91% |
| y nằm trong 29–35 / 27–35 / 24–35 | 70% / 83% / 91% |
| v nằm trong 6–17 | 70% |
| x nằm trong 19–31 | 71% |
| Số may mắn trong 2–10 / 1–10 / 2–12 | 76% / 84% / 92% |
| Nếu u kỳ trước ≥ 8 thì u giảm | 84.1% |
| Nếu u kỳ trước ≤ 2 thì u tăng | 83.6% |
| Nếu u cách 7 kỳ ≤ 2 thì u tăng | 88.2% |
| Nếu v kỳ trước ≤ 6 thì v tăng | 89.6% |
| Nếu w kỳ trước ≤ 11 thì w tăng | 96.2% |
| Nếu w kỳ trước ≥ 24 thì w giảm | 86.3% |
| Nếu x kỳ trước ≥ 30 thì x giảm | 88.4% |
| Nếu x kỳ trước ≤ 18 thì x tăng | 87.5% |
| Nếu y kỳ trước ≤ 28 thì y tăng | 83.1% |
| Nếu y kỳ trước ≥ 33 thì y giảm | 73.2% |
| Nếu số may mắn kỳ trước ≥ 10 thì giảm | 82.3% |
| Nếu u vừa tăng thì kỳ sau giảm | 69.2% |
| u cách u kỳ trước ≤ 5 | 61.5% |
| y cách y kỳ trước ≤ 5 | 66.1% |

## Các mục đã thêm vào index.html (chưa push)
- Kết quả Power 01/10/2026, Loto 01/10/2026 21h.
- Cùng ngày các tháng trước (dương/âm, khoảng cách, tổng 2 số, tổng 3 số).
- Khoảng cách A, B, C… (x kỳ, cùng ngày dương/âm, chia nhỏ %, khoảng ≥70%, biết 1 số).
- Tổng đối xứng (u+z, v+y, w+x).
- Lá số may mắn hôm đó (Tarot, quẻ Mai Hoa theo giờ rút / gieo xu).

## Nghiên cứu sâu Loto (500 kỳ 25/01/2026 → 01/10/2026)
- Không có quy luật chính xác 100% nào không tầm thường.
- Khoảng ổn định nhất (đúng đều ở cả 5 đoạn 100 kỳ, học 250 đầu → 250 sau giữ nguyên):
  u 1–8 (72%), 1–10 (81%), 1–13 (91%) · v 6–17 (70%), 5–19 (84%) · w 12–25 (72%), 9–25 (82%) ·
  x 19–31 (71%), 18–33 (82%) · y 29–35 (70%), 27–35 (83%), 24–35 (91%) · số may mắn 2–10 (76%), 1–10 (84%).
- Cả 5 số cùng trong khoảng 70%: 116/500 kỳ (23%), vùng còn 73.528 bộ; khoảng 80%: 222/500 (44%), còn 137.622 bộ;
  khoảng 90%: 335/500 (67%), còn 216.846 bộ; khoảng 95%: 418/500 (84%), còn 264.610 bộ.
- Kỳ sau so với kỳ trước: u cách ≤ 8 đúng 78%, y cách ≤ 8 đúng 84%, số may mắn cách ≤ 5 đúng 72%; đảo chiều tăng/giảm đúng ~61%.
- Dãy zic zắc (chéo lên/xuống, nảy, nhảy cách): chênh lệch nằm trong khoảng 70% đúng 61–73% ở 250 kỳ sau; tốt nhất "v,x xen kẽ" và "u,w,y" ~73%.

## Dãy tăng/giảm (chênh lệch kỳ sau − kỳ trước), Loto 500 kỳ
- Quy luật hướng ổn định nhất (học 250 đầu → đúng ở 250 sau):
  u tăng mạnh (≥ +6) → kỳ sau giảm 84% → 87% · u giảm mạnh (≤ −6) → tăng 70% → 70%
  v tăng mạnh → giảm 85% → 78% · v giảm mạnh → tăng 70% → 79%
  w giảm mạnh → tăng 70% → 74% · w tăng mạnh → giảm 62% → 70%
  x giảm mạnh → tăng 70% → 85% · y giảm mạnh → tăng 89% → 87% · số may mắn tăng mạnh → giảm 74% → 79%
- Mẫu 3 dấu: "+ − −" → kỳ sau tăng 66–82% (y 82%, x 76%, w 72%); "− + +" → kỳ sau giảm 77–88%.
- Tiếp tục cấp số đúng (chênh sau = chênh trước): chỉ 2–5%; đảo ngược ±4: 38–59%. Tương quan chênh trước/chênh sau ≈ −0.5.
- Khoảng 70% theo điều kiện tăng/giảm KHÔNG hẹp hơn khoảng 70% thường (u ~8, v ~12, w ~13, x ~12, y ~7–8, MM ~8 giá trị).

## Mục tiêu dài hạn (người dùng xác nhận 02/10/2026)
- Tìm xác suất xuất hiện theo từng vị trí; quy luật đúng **≥ 60%** đã được coi là mạnh.
- Không cần trúng ngay; tích lũy và theo dõi quy luật qua thời gian để dần nắm chắc quy luật có tỉ lệ trùng cao tại từng vị trí.
- Ưu tiên: quy luật bền (đúng đều qua các đoạn thời gian), máy tự cập nhật tỉ lệ khi có kết quả mới.

## Dò tự động quy luật hướng + gộp phiếu (Loto 500 kỳ, PP11–PP12)
- Thử 3.544 quy luật; chọn 725 quy luật ≥65% ở 250 kỳ đầu → ở 250 kỳ sau trung bình đúng 74.5%, 615 quy luật vẫn ≥60%.
- 475 quy luật ổn định (≥65% cả 2 nửa, mỗi đoạn 100 kỳ ≥55%): u 81, v 97, w 89, x 109, y 64, số may mắn 35.
- Quy luật mạnh nhất dựa vào MỨC giá trị: đang ở nhóm cao nhất (mức 5/5) → kỳ sau giảm/đứng 90–98%; nhóm thấp nhất → tăng/đứng 92–100%.
  Ví dụ: u mức 5/5 & khoảng cách tới v ≤ 3 → u giảm 98% (55/56); x mức 5/5 & kỳ tới 21h → x giảm/đứng 98% (65/66);
  w mức 1/5 & kỳ tới 21h → w tăng 95% (52/55); v giảm mạnh & mức 1/5 → v tăng 94% (48/51).
- Gộp phiếu (chọn ở 250 đầu, kiểm 250 sau), hiệu ≥ 8 phiếu: u 75%, v 74%, w 82%, x 82%, y 82%; số may mắn ≥ 3 phiếu 85%.
- Đổi hướng thành khoảng: khoảng rộng hơn khoảng 70% thường, tỉ lệ tương đương (u ~10 giá trị 66–70%, y ~10 giá trị 70–75%); riêng số may mắn ≥ 5 phiếu: ~10 giá trị đúng 88%, ≥ 8 phiếu: 92%.
- Dự đoán hướng kỳ 02/10/2026 13h: u GIẢM (25 phiếu, khoảng 1–7), v GIẢM (19, 3–11), w GIẢM (19, 8–24), x GIẢM (6, 16–28), y GIẢM (22, 24–34), số may mắn GIẢM (11, 1–11).

## Quan hệ trong cùng kỳ (PP13–PP14), Loto 500 kỳ
- Khoảng 70% ổn định của mọi hiệu / tổng (mỗi đoạn 100 kỳ 62–79%): v−u 1–7, x−u 11–24, y−u 16–29, x−v 3–14, y−v 11–23, y−w 3–15,
  u+y 29–42, v+x 25–46, v+y 35–51, w+x 32–55, tổng 5 số 66–109, số lẻ 1–3 (80%), số ≥18 là 1–3 (79%), khoảng cách nhỏ nhất 1–2 (73%).
- Máy tự chọn 5 ràng buộc (mức 80%): 33% số kỳ thỏa tất cả (nửa đầu → nửa sau 34%), vùng còn 91.432 bộ (28%).
  Thêm hướng dự đoán kỳ 02/10 13h (5 vị trí đều giảm): vùng còn 14.857 bộ (4.6%).
- Kiểm tra hướng gộp phiếu trong trang (học 250 đầu → 250 sau), ≥ 8 phiếu: u 77%, v 76%, w 78%, x 80%, y 86%, MM 94%.
  Nhật ký 30 kỳ gần nhất (≥ 3 phiếu): đúng chung 123/157 = 78%.

## Pool số (PP15–PP27), Loto, pool 15 số
| PP | 500 kỳ TB · ≥2 · ≥3 | 200 kỳ TB · ≥2 · ≥3 |
|---|---|---|
| PP16 Gan | 2.25 · 75% · 41% | 2.27 · 75% · 43% |
| PP17 Chu kỳ TB | 2.18 · 74% · 38% | 2.30 · 77% · 46% |
| PP23 Cặp đi cùng | 2.21 · 75% · 39% | 2.18 · 72% · 41% |
| PP24c Cùng ngày âm | 2.20 · 75% · 37% | 2.27 · 79% · 40% |
| PP27 Gộp | 2.20 · 74% · 37% | 2.23 · 75% · 37% |
- Pool 10 số (PP16): TB 1.56, ≥2 số 50%; pool 20 số: TB ~3.0, ≥2 số 90–92%, ≥3 số 68–74%.
- Pool K số luôn chứa trung bình khoảng 5×K/35 số; các phương pháp chênh nhau khoảng ±0.1 số.
- "Kỳ này trượt, kỳ sau về": sau 1–2 kỳ pool trượt (< 3 số), tỉ lệ kỳ sau ≥ 3 số = 36–41%, bằng tỉ lệ chung (không có hiện tượng về bù).
- Người dùng muốn: mỗi kỳ mới đối chiếu kết quả với phương pháp → index_loto.html tự làm (nhật ký pool 30 kỳ, nhật ký hướng 30 kỳ).

## 305 phương pháp cũ trên 500 kỳ Loto (PP28)
- ≥1 số trúng ≥70%: 61 phương pháp (chung), 62 (13h), 55 (21h); ít số nhất là các phương pháp 7 số (Can/Chi/Nạp âm/Mai Hoa…):
  ChiH bịkhắc 76% (13h 76 / 21h 76), GiờH đượcsinh 75%, MHdương Thểkhắc 75%, Nạp khắc 73%, MHâm sinhThể 73% — TB ~1.0–1.1 số trúng.
  Ổn định: 56 phương pháp ≥70% ở nửa đầu → 49 vẫn ≥70% ở nửa sau.
- ≥2 số trúng ≥70%: 12 phương pháp, đều gợi ý ≥ 15 số (Lâu 15 75%, Lạnh 50/15 75%, Nóng 200/15 75%, Nóng 500/15 75%; Bát vượng 21 số 95%).
- ≥3 số trúng ≥70%: chỉ "Sinh nhật" (31 số, 100%).
- Mỗi số gợi ý trúng cao nhất ~15–16% (Rút cửu tinh 16.2%, Hợp Khỉ 16.2%, Life 9 15.8%).
- 13h khác 21h: MHdương/MHâm đuôi quẻ 13h ~40% vs 21h ~70% (ổn định 2 nửa) vì 21h gợi ý gấp đôi số (7.3 vs 3.6 số); mỗi số gợi ý trúng như nhau.
  Bát khuyết 13h 72–75% vs 21h 61–66% (cùng 7 số) là khác biệt thật nhất về giờ trong 305 phương pháp.
- Số may mắn (gợi ý 5 số): Lặp 15 trúng 44.6%, Lâu 15 43.8%, Nạp tháng 43.0%.

## Mục đích app Loto (người dùng xác nhận 02/10/2026)
- Lưu mọi dữ liệu trên trang (kết quả nhập, gợi ý từng kỳ) — link: https://claude.ai/artifact/X8ZmKZJ3RGDKZF7j8wbxFr (collections `draws`, `preds`).
- Thu hẹp pool toàn dãy (từ 35 số) và pool từng vị trí nhỏ nhất có thể nhưng giữ tỉ lệ trúng cao.
- Từ pool + quy luật xác suất cao → gợi ý 5 dãy tiềm năng mỗi kỳ; kèm phân tích kỳ tới để người dùng tự nhận định.
- Kiểm tra cách gợi ý trên 60 kỳ (pool 15, khoảng 80%): pool trúng TB 2.33 số; dãy tốt nhất trong 5 dãy trúng TB 1.28 số
  (0 số 22%, 1 số 38%, 2 số 30%, 3 số 10%); số may mắn nằm trong 5 số gợi ý 40%.

## App 3 game (02/10/2026)
- Link vẫn https://claude.ai/artifact/X8ZmKZJ3RGDKZF7j8wbxFr — 3 tab Loto / Mega / Power, mỗi tab độc lập, lưu riêng
  (Loto: draws, preds · Mega: draws_mega645, preds_mega645 · Power: draws_power655, preds_power655).
- Power: số đặc biệt chỉ có dữ liệu 101 kỳ gần nhất (từ 02/2026) nên chưa phân tích hướng cho ĐB, chỉ gợi ý theo tần suất.
- Kiểm tra 60 kỳ (pool 15, khoảng 80%): Mega pool TB 2.18 số, dãy tốt nhất TB 1.33 (3 số 7%); Power pool TB 1.78, dãy tốt nhất TB 1.18 (3 số 2%).

## Nghiên cứu Mega 6/45 (500 kỳ 19/07/2023 → 30/09/2026), cùng cách làm như Loto
- Khoảng 70% ổn định (5 đoạn, học 250 đầu → 250 sau): u 1–8 (71%), v 4–17 (71%), w 10–25 (71%), x 16–32 (73%), y 28–41 (70%, sau 80%), z 37–45 (75%).
  Khoảng 90%: u 1–15, v 3–23, w 9–31, x 16–38, y 23–43, z 32–45.
- Cả 6 cùng trong khoảng 70%: 21% kỳ (vùng còn ~1,62 triệu bộ / 8,1 triệu); 80%: 40% (~3,1 tr); 90%: 69% (~5,1 tr).
- Kỳ sau – kỳ trước: u và z cách ≤ 9 đúng 81%; đảo chiều 56–63%.
- Mạnh (ngưỡng ±8): z giảm mạnh → tăng 91% (91→91); u tăng mạnh → giảm 85%; v tăng mạnh → giảm 82%; y giảm mạnh → tăng 78%; x giảm mạnh → tăng 77%.
  Mẫu "+ − −" → tăng 65–78%, "− + +" → giảm 68–78% (z 78% cả hai).
- Dò tự động: 456 quy luật ổn định. Mạnh nhất vẫn dựa vào MỨC: mức 1/5 → tăng/đứng 92–100% (u 54/54); mức 5/5 + tổng tăng mạnh → giảm 91–96%.
- Gộp phiếu (≥ 8 phiếu, kiểm 250 sau): u 61%, v 64%, w 67%, x 71%, y 70%, z 73% — yếu hơn Loto ở u, v.
- Pool 15 số (500 / 200 kỳ): PP18 tích lũy tăng 2.08/2.02, PP20 kề ±1 2.07/2.08, PP17b chu kỳ hay gặp 2.06/2.04, PP24 cùng thứ 2.01–2.04/2.09.
  Pool 20 số: TB ~2.7, ≥2 số 85–87%, ≥3 số 54–60%. Sau kỳ trượt không có hiện tượng về bù.
- 291 phương pháp cũ: ≥1 số trúng ≥70%: 69 (68 ổn định), ít số nhất là nhóm Nạp âm / Can giờ 9 số (~75%, TB 1.2);
  ≥2 số ≥70%: Nạp năm 18 số 81%, Nạp tháng 18 số 78%, Hành cửu tinh 18 số 77%; ≥3 số ≥70%: Bát vượng2 (25 số) 74%, Bát vượng (27) 85%.
- Gợi ý 5 dãy, kiểm 60 kỳ: dãy tốt nhất TB 1.37 số (2 số 37%, 3 số 8%).

## Nghiên cứu Power 6/55 (500 kỳ 18/07/2023 → 01/10/2026)
- Khoảng 70%: u 1–11, v 5–21, w 15–34, x 24–43, y 34–50, z 46–55; 90%: u 1–17, v 2–27, w 8–38, x 16–45, y 27–52, z 40–55.
- Cả 6 trong khoảng 70%: 21% kỳ (~5,7 triệu bộ / 29 triệu); 80%: 37% (~11 tr); 90%: 64% (~17,9 tr).
- Mạnh (ngưỡng ±9): u tăng mạnh → giảm 89% (86→92); z giảm mạnh → tăng 85%; y giảm mạnh → tăng 80%; "− + +" ở u → giảm 80%, ở x 79%.
- Dò tự động: 429 quy luật ổn định; u mức 1/5 → tăng/đứng 100% (61/61); y mức 5/5 + tổng tăng mạnh → giảm 97%; u mức 5/5 + âm 11–20 → giảm 95%.
- Gộp phiếu ≥ 8: u 70%, v 70%, w 72%, x 73%, y 78%, z 71%.
- Pool 15 số: PP20 kề ±1 1.74/1.63, PP16 gan 1.70/1.73, PP18 tích lũy tăng 1.69/1.72; pool 20: TB ~2.2, ≥2 số 71–75%, ≥3 số ~40%.
- 293 phương pháp cũ: ≥2 số ≥70%: Nạp tháng/Nạp năm/Hành cửu tinh 22 số ~76%; ≥3 số: Bát vượng (33) 83%, Bát vượng2 (35) 86%.
- Số ĐB: chỉ 101 kỳ; KHÔNG BAO GIỜ trùng 1 trong 6 số chính cùng kỳ (0/101) → gợi ý ĐB loại số đã có trong dãy.
- Gợi ý 5 dãy, kiểm 60 kỳ: dãy tốt nhất TB 1.27 số (2 số 33%, 3 số 3%).

## Cập nhật app sau nghiên cứu Mega/Power (02/10/2026)
- Ngưỡng "tăng/giảm mạnh" và "cách số bên cạnh" co giãn theo game (6×N/35: Loto 6, Mega 8, Power 9); "số vị trí vừa tăng" chia 0–2/3–4/5–6 cho game 6 số.
- Thêm phương pháp pool: PP17b chu kỳ hay gặp, PP18t tích lũy tăng, PP20b kề ±2, PP26 bóng N+1−n. Máy tự chọn phương pháp tốt nhất 200 kỳ.
- Khi pool dồn cụm, không bộ nào thỏa điều kiện hình dạng → vẫn gợi ý và ghi rõ đã bỏ điều kiện.

## Thu hẹp pool làm kỹ (02/10/2026) — pool_deep.py
- Mỗi game gộp 24 phương pháp mới (thêm nóng 5/200 kỳ, gan ÷ chu kỳ…) + toàn bộ phương pháp cũ: Loto 329, Mega 315, Power 318.
- Cách kiểm: chọn / học trên 250 kỳ trước → chấm trên 250 kỳ sau (chưa từng thấy), pool 10/15/20.
- Pool 15, kết quả 250 kỳ sau:
  Loto: tốt nhất & bền nhất Gan / Gan÷chu kỳ 2.27–2.29 (≥3 số 42–43%), Lâu 15 2.27; trung bình mọi phương pháp 2.16.
  Mega: Kề ±2 2.08, Nạp tháng 2.10, Tích lũy tăng 2.08; trung bình 1.96; phương pháp tốt nhất 250 kỳ trước thường tụt ở 250 kỳ sau.
  Power: Gan 1.68, Lâu 15 1.68, bỏ phiếu đều tất cả 318 pp 1.74 (≥3 số 25%); trung bình 1.70.
- Gộp top 5/10/20/40, bỏ phiếu có trọng số, tự chọn lại mỗi kỳ theo 30–200 kỳ gần nhất, máy học (hồi quy logistic trên cả ~320 pp):
  KHÔNG cách nào vượt phương pháp đơn tốt nhất; tất cả nằm trong khoảng ±0.1 số quanh mức trung bình.
- Kết luận: số trúng trong pool gần như chỉ phụ thuộc số lượng pool K (≈ C×K/N); chọn pp bền (Loto: Gan) là đủ.

## Chọn 2 dãy ★ trong 5 dãy + phản biện (02/10/2026)
- 4 tiêu chí xếp hạng (mỗi tiêu chí xếp 0–100 trong 5 dãy, điểm = trung bình): đồng thuận các phương pháp pool, tần suất số tại đúng vị trí,
  hợp hướng tăng/giảm dự đoán, hình dạng điển hình (tổng, số lẻ, khoảng cách nhỏ nhất). ★1 = điểm cao nhất; ★2 = điểm cao nhất trong các dãy chung ≤ C−3 số với ★1.
- Kiểm 300 kỳ: 2 dãy xếp đầu trúng TB gần bằng 3 dãy còn lại ở cả 3 game (Loto 0.74–0.76 vs 0.74–0.76, Mega 0.76–0.83 vs 0.82–0.86, Power 0.60–0.76 vs 0.59–0.75);
  tương quan từng tiêu chí với số trúng ≈ 0 (−0.06…+0.03). → điểm xếp hạng chỉ để cân nhắc; lợi ích chắc chắn là 2 dãy ít trùng → phủ nhiều số hơn.
- App ghi lý do chọn / phản biện cho từng số của 2 dãy ★, tự kiểm cách xếp hạng trên 60 kỳ; nhật ký có cột "2 dãy ★".

## Gợi ý V2 (02/10/2026) — nghiên cứu riêng từng game, kiểm 400–500 kỳ
- Chọn pp pool tổng theo 50/100/200/300/500 kỳ: không cửa sổ nào thắng đều (chênh ±0.1 số). App tự đo 4 cửa sổ 100/200/300/500 trên 300 kỳ gần nhất của từng game và dùng cửa sổ tốt nhất
  (hiện: Loto 200, Mega 100, Power 300). Pp bền nhất cả 3 game: Gan (Loto gan/chu kỳ 2.31 cả 2 nửa).
- Pool riêng từng vị trí: tốt nhất = các số hay ra nhất ở vị trí đó trong 500 kỳ (hơn biên độ, theo mức kỳ trước, ghép, hay ghép pool tổng).
  Số lượng cần để đúng ≥60%: Loto u7 v11 w13 x12 y6; Mega u7 v12 w14 x13 y12 z7; Power u9 v15 w17 x17 y15 z8. Vị trí giữa luôn rộng.
- Tổng: kỳ trước ở 1/3 thấp → kỳ sau tăng 78–86%; 1/3 cao → giảm 81–83% (cả 3 game). Tổng 80%: Loto 62–116, Mega 97–172, Power 131–224.
- Số lẻ hay gặp: Loto 1–3 lẻ 80%; Mega 2–4 lẻ 83%; Power 2–4 lẻ 81%.
- Biên độ 70% từng vị trí: Loto u −7..+6, y −6..+5; Mega u −9..+5, z −8..+6; Power u −10..+7, z −8..+9 (giữa rộng hơn).
- V2 tạo 5 dãy: mỗi số từ pool riêng vị trí (mức 60/70/80%), cộng điểm nếu có trong pool tổng/hợp hướng, tổng 80% + tăng/giảm theo mức tổng kỳ trước, số lẻ nhóm ≥75%, 5 dãy phủ nhiều số nhất.
- So V1 → V2 làm lại 100 kỳ: dãy tốt nhất trong 5: Loto 1.20 → 1.70, Mega 1.33 → 1.82, Power 1.17 → 1.59; có dãy ≥2 số: 30→60, 43→69, 30→55 kỳ.
  NHƯNG trung bình mỗi dãy gần như không đổi (0.73→0.73, 0.72→0.81, 0.67→0.67): phần tăng đến từ việc 5 dãy phủ 25–30 số khác nhau thay vì 9–12.

## Thu hẹp pool nhỏ nhất với xác suất trúng ≥ 70% (02/10/2026)
- Pool tổng: mỗi pp tìm K nhỏ nhất mà pool chứa ≥ h số trúng ở ≥ X% số kỳ; chọn pp có K nhỏ nhất.
  Đặt đúng 70% (đo 300 kỳ) → 200 kỳ sau chỉ đạt 62–72% (chọn trúng pp "gặp may"). Đặt 75% đo trên 500 kỳ → 200 kỳ sau đạt 72–80% ở cả 3 game × 3 mức. → app dùng 75%/500.
  Cỡ pool: Loto ≥1 số 8, ≥2 số 15, ≥3 số 22 · Mega 8 / 16–17 / 24 · Power 11 / 21 / 30.
- Pool riêng vị trí: đặt đúng mức → Power y, z tụt 65–66%; cộng 5% (đặt 75%) → mọi vị trí cả 3 game đạt 71–83% ở 200 kỳ sau.
  Cỡ (mức 70% thật): Loto u 9–10, v 14, w 16, x 15, y 8; Mega u 10, v 17, w 19, x 18, y 16, z 10; Power u 12, v 19, w 24, x 22, y 19, z 12.
- Bắt buộc 5 dãy chỉ dùng số trong pool tổng: kém hơn (dãy tốt nhất giảm 0.1–0.3 số) → không dùng, chỉ cộng điểm.

## So 9 cách tạo dãy từ pool (tk_eval.py, Loto 319 kỳ, Mega/Power 400 kỳ, mỗi kỳ chỉ dùng dữ liệu trước nó)
- Cách: ngẫu nhiên trong pool, theo điểm chia liên tiếp, phủ đều pool (vòng quay), tập trung top số, vị trí (app), vị trí ∩ pool tổng,
  pool tổng + tần suất vị trí, cặp hay đi cùng, lọc hình dạng + điểm vị trí.
- Mỗi dãy TB: Loto 0.69–0.72, Mega 0.75–0.82, Power 0.64–0.68 với MỌI cách (= C×C/N: 0.71 / 0.80 / 0.65). Không cách nào làm từng dãy đúng hơn.
- 2 dãy (tốt hơn): 1.0–1.2 số mọi cách (trừ tập trung 0.8–0.86).
- 5 dãy: app hiện tại tốt nhất ở cả 3 game: Loto 1.68 (≥2: 60%, ≥3: 7.8%), Mega 1.79 (69%, 10.2%), Power 1.62 (56%, 7.0%),
  vì phủ 3.4–3.9 số trúng (lấy cả số ngoài pool tổng); các cách chỉ trong pool tổng phủ tối đa ~2.1–2.3 (= số trúng có trong pool).
- Tập trung top số kém nhất (5 dãy gần giống nhau).

## Cho máy học 300 kỳ biết trước → kiểm 200 kỳ sau (learn.py, 02/10/2026)
- 30 đặc điểm mỗi số: 24 pp pool, trong pool tổng / hạng, tần suất vị trí, hợp biên độ, xác suất biên độ, hợp hướng tăng/giảm (theo mức kỳ trước),
  trong phạm vi 70% vị trí, tổng tăng/giảm × số lớn/nhỏ, vừa ra kỳ trước, cách số kỳ trước.
- Cách học: từng đặc điểm, hồi quy logistic (3 mức), cộng hạng top 2/3/5 đặc điểm, tìm trọng số (300 lần thử). 6 lần tách (Loto 2, Mega 2, Power 2).
- Top 10 số (học → kiểm): logistic Loto 1.69→1.41, 1.68→1.45; Mega 1.54→1.40, 1.54→1.45; Power 1.23→1.02, 1.31→1.03.
  Mức chung 10 số bất kỳ: Loto 1.43, Mega 1.33, Power 1.09. Mọi cách học đều đẹp ở 300 kỳ học rồi rơi về mức chung ở 200 kỳ kiểm;
  không cách nào thắng đều qua các lần tách. Học càng phức tạp càng tụt mạnh (học thuộc đúng 300 kỳ đó).
- Kết luận: đặc điểm tăng/giảm, phạm vi, biên độ, vị trí trong pool không giúp đoán SỐ NÀO sẽ ra; chỉ giúp mô tả hình dạng kết quả (tổng, số lẻ, khoảng).

## Cây chia nhỏ từng vị trí (02/10/2026)
- Từ khoảng 80% chia đôi liên tục; tỉ lệ ổn định (học 300 → kiểm 200 lệch 0–4%).
  Loto u: 01–11 88% → 01–04 47% → 01–02 25%. Loto y: 27–35 85% → 33–35 44% → 33–34 27%.
  Mega z: 35–45 83% → 43–45 37% → 45 15%. Power z: 43–55 81% → 52–55 38% → 55 12%.
- Mỗi lần chia đôi, xác suất giảm khoảng một nửa. Dựa vào kỳ trước để chọn nhánh: lệch ±3–6%, không ổn định → không dùng.
- App: mục ③ "Chia nhỏ từng vị trí", đường vàng theo nhánh có xác suất trên mỗi số cao hơn.

## Ghép dãy bảo đảm (wheel) + kết quả Loto 02/10/2026 13h: 06 23 30 32 34, MM 09
- Wheel đã kiểm hết trường hợp: Loto 10 số/2 dãy, 12 số/4 dãy (≥3 trúng trong nhóm → 1 dãy ≥2), 7 số/5 dãy (→ 1 dãy đủ 3);
  Mega/Power 12 số/2 dãy, 14 số/4 dãy (→ ≥2), 8 số/4 dãy (→ đủ 3). Số lấy = top v của pp pool tổng.
- 200 kỳ: điều kiện xảy ra Loto 13% (10 số) / 25% (12) / 3% (7); Mega 17% / 28% / 3%; Power 14% / 21% / 4%; bảo đảm đúng 100% khi điều kiện xảy ra.
  Dãy tốt nhất ≥2 số: Loto 26% / 45% / 27%; Mega 32% / 50% / 32%; Power 22% / 39% / 25% — thấp hơn 5 dãy phủ rộng (55–76%) vì ít dãy hơn và chỉ dùng số trong pool.
- Kỳ 02/10 13h: gợi ý đã lưu (bản sáng, PP17): pool trúng 06, 30; các dãy trúng tối đa 1 số; MM 09 đúng ở dãy 1.
  Bản hiện tại làm lại: pool (PP18) chỉ trúng 23; dãy ★1 trúng 34 + MM 09; các dãy tối đa 1 số; wheel 10/12/7 số: tối đa 1 số (điều kiện không xảy ra).

## 2 phương án pool (02/10/2026)
- Chọn cặp trên 200 kỳ A → kiểm 200 kỳ B: cặp tốt nhất giữ được (Loto 74→75%, Mega 76→76%, Power 82→77% "ít nhất 1 pool ≥3 số"); 1 pool ~41–46%.
  Cặp tốt luôn là 1 pool nguội (gan) + 1 pool nóng/chu kỳ. 4 dãy ghép bảo đảm từ 2 pool ≈ ngang 5 dãy hiện tại → giữ 5 dãy.
- App: mỗi kỳ tự chọn cặp trong 16 pp theo 200 kỳ trước. Hiện cả 3 game: Gan (PP16) + Chu kỳ hay gặp (PP17b), gần như không trùng
  (hợp lại Loto 30/35, Mega 34/45, Power 42/55 số). Kiểm 200 kỳ (chọn cặp mỗi kỳ bằng 200 kỳ trước): ≥3 số 72–78%, ≥2 số 99% (1 pool: 41–44%, 74–77%).
- Kỳ 02/10 13h: Pool A (gan) trúng 23, 30; Pool B (chu kỳ hay gặp) trúng 06, 32, 34.
- SỬA LẠI (người dùng chỉ ra đúng): 2 pool gần như không trùng phủ 30/35 số → "1 pool ≥3 số" gần như do phép đếm (5 số chia 2 nhóm).
  So công bằng cùng tổng số lượng (300 kỳ): Loto cặp ≤20 số 55% vs 1 pool 20 số 61%; ≤23: 60% vs 76%; Mega ≤22: 59% vs 65%; Power ≤26: 53% vs 61%.
  → nhiều pool KÉM hơn 1 pool cùng cỡ. Đã gỡ phần "2 phương án pool" khỏi app.

## Loto 5/35 quay bằng máy tính (không có bi vật lý), kiểm tra 02/10/2026
- Loto 5/35 không quay bi mà máy tính sinh số, nên giả thuyết "bi lệch" không áp dụng. Câu hỏi đúng là bộ sinh số có để lại dấu vết không.
- 7 phép kiểm trên 921 kỳ (lặp lại kỳ trước, tương quan tổng, chẵn lẻ, tần suất cặp, tần suất đơn, nửa đầu/nửa sau, số liền nhau) so với 300 lần bốc ngẫu nhiên: cả 7 đều nằm trong khoảng 95% của bốc ngẫu nhiên. Số may mắn cũng đều.
- Gần ngưỡng nhất: tần suất đơn (p≈0.08, số 34 ra 161 lần so với kỳ vọng 132). Với 7 phép kiểm thì có 1 phép gần ngưỡng là bình thường. Kiểm lại sau 200 kỳ nữa.
- Mega/Power (có bi): tần suất đều (p 0.89 / 0.49), không thấy bi lệch.

## Thiên văn / lịch (02/10/2026)
- Đã kiểm 6 cách chia theo lịch (pha mặt trăng 8 nhóm, ngày âm, thứ, tháng dương, ngày trong tháng, mùa) × 3 game. Với mỗi cách chia: số ra có lệch theo nhóm không, tổng có lệch theo nhóm không, và pool "cùng nhóm" có trúng hơn ngẫu nhiên không (300 kỳ cuối). Kết quả gần như toàn bộ ngang ngẫu nhiên. Pha mặt trăng và ngày âm: p 0.40–0.94.
- Ứng viên duy nhất cần theo dõi: Power, ngày 21–31 tổng thấp hơn (163.6 so với 171–173). Nửa đầu dữ liệu p=0.01; nửa sau (hướng đã biết trước) p=0.03 một phía. Mức tác động rất nhỏ: thêm khoảng +0.14 số ≤27 mỗi kỳ. Đã làm 36 phép kiểm nên vẫn có thể là tình cờ. Kiểm lại trên các kỳ từ 03/10/2026 trở đi.

## 16 phương pháp tâm linh / dân gian (02/10/2026)
- Đã đưa vào app (mục ⑥) và kiểm trên toàn bộ các kỳ: Tiểu Lục Nhâm, Đại Lục Nhâm (rút gọn), Thái Ất (rút gọn), Huyền Không Phi Tinh, Nhị thập bát tú, Hoàng đạo/Hắc đạo, Nạp âm, Bóng âm dương, Bạc nhớ, Chạm, Tổng chạm, Lộn + kép, Thần số học, Tử vi (Mệnh/Cục/Tử Vi), Xin xăm, Bát trạch.
- Tỉ số so với chọn bừa: 0.94–1.08 ở cả 3 game. Không có phép nào p < 0.01.
- Gần ngưỡng: "Lộn + kép" ở Loto (1.08, p 0.04) và Power (1.07, p 0.02). Tách riêng thì phần đóng góp là các số kép cố định (11, 22, 33…): Loto 1.11 (nửa đầu 1.13, nửa sau 1.10), Power 1.08. Thực chất đây là tần suất của vài số cố định, cùng loại với tín hiệu "Loto tần suất lệch p≈0.08". Theo dõi tiếp.

## Khoanh vùng từng bi (02/10/2026)
- Power (1001 kỳ): 12/55 bi lệch cùng chiều ở cả 4 giai đoạn (ngẫu nhiên 3–12, p≈0.04). Bi 22 (z +2.51) và 41 (+2.21) ra nhiều ở cả 4 đoạn. Bi 15, 35, 50 ra ít ở cả 4 đoạn. Chưa bi nào đạt ngưỡng chắc chắn |z| ≥ 3.1.
- Mega (1001 kỳ): chỉ 4/45 bi bền, ngang ngẫu nhiên. Không có dấu hiệu.
- Theo dõi Power 22, 41 trên các kỳ mới.

## Ghi chú về máy quay
- Mega 6/45 và Power 6/55: quay bằng **lồng quay** (bi vật lý, rơi tự do, không thổi khí). Bi lệch (nặng, nhẹ, mòn, méo) có thể làm số đó dễ ra hoặc khó ra; nhìn kết quả chỉ biết dễ/khó ra, không biết chắc nặng hay nhẹ.
- Loto 5/35: quay bằng **máy tính** (bộ sinh số), không có bi. Dấu vết, nếu có, là của bộ sinh số.
- Đã thêm "Theo dõi vết qua các đoạn liên tiếp" (đoạn 25/50/100 kỳ, chuỗi cùng chiều, đường tích lũy). 500 kỳ gần nhất, đoạn 50 kỳ: Mega có bi 21, 40 ra ít 7 đoạn liên tiếp; Power có bi 49 ra ít 7 đoạn liên tiếp. Số bi có chuỗi ≥ 4 vẫn ngang ngẫu nhiên (Mega p 0.85, Power p 0.93).

## Power: tổng kỳ này dính tổng kỳ trước, giai đoạn gần (03/10/2026)
- Toàn bộ 1001 kỳ: tương quan +0.04 (p 0.2), bình thường. Từng đoạn 200 kỳ: −0.01 đến +0.085.
- Gần đây bất thường: 100 kỳ +0.21 (p 0.03); 50 kỳ (09/06–01/10/2026) +0.37 (p 0.006). Trong 50 kỳ đó, tổng nằm cùng phía trung vị (168) với kỳ trước ở 76% số kỳ (bình thường 50%). Chỉ có 13 chuỗi so với kỳ vọng ~25 (runs test z≈−3.6). Tổng TB 50 kỳ là 157 (chung 169).
- Đã thử 6 khoảng nên vẫn có thể là tình cờ (p 50 kỳ sau khi tính 6 lần thử ≈ 0.04). Giả thuyết: thay bộ bi hoặc lồng quay đổi trạng thái. Kiểm tiếp trên các kỳ từ 03/10/2026: quy tắc "tổng kỳ trước dưới 168 thì kỳ sau dưới 168", ghi đúng/sai.

## Sổ chấm phương pháp Power (bắt đầu 03/10/2026)
Nguyên tắc (theo yêu cầu của anh): phương pháp có cơ sở, cố định qua các kỳ, chấm bằng kết quả của chính nó; không so với ngẫu nhiên.
| Kỳ | Kết quả | Bỏ vắng≥20 (12 20 30 50) | Bỏ khó ra (04 06 37 49 12 50) | Số nóng ★ (01 05 07 11 18 25) | Kề ±1 kỳ trước | Đà tổng thấp | Pool dấu vết 15 | Tâm linh pool 12 | Dãy tốt nhất |
|---|---|---|---|---|---|---|---|---|---|
| 03/10 | 07 11 13 16 18 54 · ĐB 41 | 4/4 bỏ đúng | 6/6 bỏ đúng | 3 trúng (07 11 18) | 1 (54) | đúng (tổng 119) | 4 trúng (07 11 18 54) | 3 (07 13 54) | 01 07 11 22 43 54 → 3 số |
| 06/10 | 06 07 18 20 24 27 · ĐB 01 (tổng 102; 2 số lặp kỳ trước 07 18) | (không dùng vắng≥20) | khó ra: 06 về (sai) | nóng: 07 18 trúng | kề: 06 | đúng (102 trong 101–189) | **bản gốc** pool 15: 2 (07 18), vé tốt 1 số · **bản anh loại số kỳ trước** (đã mua 5 vé): pool 15: 0, 5 vé 0 số | tâm linh 12: 2 (06 18) | luật ● sai: it100 (06), nhip2 (18 — luật 99%); sổ 18/35 |

## Dấu vết Loto 5/35 (máy tính quay, không bi) — nghiên cứu 04/10/2026, 924 kỳ, `build/loto_dauvet.py`
Chấm bằng tỉ lệ của chính phương pháp, chạy tiến (chỉ dùng dữ liệu trước kỳ), chia 3 khúc để xem độ ổn định.
- **Mỗi phiên có "tính cách" riêng**: tần suất từng số ở phiên 13h nửa đầu khớp nửa sau (corr 0.33); 21h yếu hơn (0.22); 13h và 21h không giống nhau (−0.02) → tách phiên khi xét nóng/lạnh.
- **Chuyển kỳ (số a kỳ trước → số nào hay theo sau a)**, pool 15: TB 2.25 / 2.14 / 2.26 qua 3 khúc, 50 kỳ gần 2.44, ≥3 số 40% — ổn định nhất trong các cách thử. Cùng phiên hôm trước (lag 2): 2.10 / 2.09 / 2.32, 50 kỳ gần 2.40 (đang lên).
- Nóng cùng phiên 100 kỳ: 2.25 / 2.15 / 2.21, ≥3 số 38%. Lạnh kém hơn nóng ở cả 3 khúc với số chính.
- **Số May Mắn có xu hướng cân bằng**: số MM ra nhiều khúc này thì khúc sau ra ít (corr giữa các khúc −0.31). MM lạnh (ít ra 300 kỳ) top 3: 28.6% / 24.5% / 23.2%, trong khi MM nóng top 3: 21.2% / 19.5% / 19.5% — lạnh hơn nóng ở mọi khúc. MM vắng lâu nhất top 3: 29.9% / 24.5% / 28.6%, 50 kỳ gần 32%.
- Không thấy dấu vết: cặp số hay đi cùng (không lặp lại giữa 2 nửa), đà tổng (corr ≈ 0), kề ±1, đuôi số (chỉ do cấu trúc 1–35).

## Suy luận loại trừ bổ sung — kiểm 04/10/2026 (`build/loai_tru.py`, 600 kỳ gần, 3 khúc)
Cấp số (chỉ ghi luật đứng vững cả 3 khúc; chênh lệch nhỏ, cỡ 1 điểm %):
- Power: số **vắng 6–10 kỳ** ra ít hơn nhóm còn lại 3/3 khúc → giảm nhẹ; số **vắng 11–15 kỳ** ra NHIỀU hơn 3/3 → đừng loại, nên ưu tiên. Số vắng ≥31 đang tăng dần (10% → 12% → 14%) → cảnh giác với luật bỏ vắng lâu.
- Mega: số **cùng đuôi với số kỳ trước** ra ít hơn 3/3 (nhóm lớn ~16 số → chỉ dùng để giảm điểm, không loại). Số quá nóng (≥4/10 kỳ) đang giảm dần 16.5% → 14.2% → 12.4%.
- Loto: **số vừa ra kỳ trước** ra ít hơn 3/3 (13.5% vs 14.4%) → giảm điểm; số **vắng ≥31** ra nhiều hơn 3/3 → với Loto không nên loại số vắng lâu.
Cấp vé (kỳ thật vi phạm, ổn định qua 3 khúc): ≥3 số trùng kỳ trước ~1%; toàn chẵn/lẻ ~2–3%; toàn nhỏ/lớn ~1–5%; ≥3 số liên tiếp ~3–6%; ≥4 số cùng chục (Power/Mega) ~3–7%; không có số ≥2/3 dải ~4–8%.
Lưu ý: cả bộ luật cấp vé bỏ ~15–20% số vé có thể, và cũng bỏ ~14–20% kỳ thật → là chỗ dựa để gọn vé, không tự làm tăng trúng.
Bỏ vắng ≥G gần như không đổi pool 15 (số vắng lâu hiếm khi vào top) → luật này chủ yếu dùng khi anh tự chọn số.

## Khẳng định ≥70% về kỳ tới — nghiên cứu 04/10/2026 (`build/khang_dinh.py`, 600 kỳ, 3 khúc)
Tiêu chí của anh: một cách suy luận đúng ≥70% số kỳ (10 kỳ đúng 7) là tiềm năng. Cột "vé giữ lại" = phần vé còn lại sau khi lọc theo khẳng định đó (đo độ thu hẹp). Đúng cao hơn giữ lại = có dấu vết thật.
- **Mega (rõ nhất, hợp thuyết bi vật lý):** có ≥1 số của 2 kỳ gần nhất: đúng 86/87/91%, 50 kỳ 92% (giữ 84%). Có ≥1 số trong 10 số nóng nhất 20 kỳ: 88/82/81% (giữ 79%). Gộp 5 khẳng định cấu trúc (≥1 trùng/kề kỳ trước, không trùng ≥2, chẵn/lẻ 3±1, nhỏ/lớn 3±1, ≥4 chục khác nhau): đúng 35/38/50%, 50 kỳ 50%, chỉ giữ 33% vé.
- **Power:** có số ở ≥4 chục khác nhau: 78/78/80% (giữ 75%); còn lại đúng ≈ giữ lại.
- **Loto:** các khẳng định đúng ≈ giữ lại (máy tính quay — không thấy lệch).
- **Khẳng định theo pool (goiy.py, 200 kỳ):** Power pool 10 có ≥1 số 73%, pool 20 có ≥2 số 71%; Mega pool 10 ≥1 80%, pool 15 ≥2 72%, pool 20 ≥2 86%; Loto pool 15 ≥2 68%, pool 20 ≥2 90%.

## Thử thêm suy luận — 04/10/2026 (`build/thu_them.py`, 600 kỳ, 3 khúc)
- **Power: số của kỳ cùng thứ tuần trước (cách 3 kỳ) ra lại ít hơn ở cả 3 khúc** (9.9 / 10.4 / 9.6% mỗi số, các số khác ~11%) → đưa vào gợi ý Power −0.5 điểm; pool 15 ở 200 kỳ 1.67 → 1.69 số/kỳ, ≥3 số 20% → 22%.
- Không thấy "tính cách theo thứ" (T3/T5/T7, T4/T6/CN) — không có dấu hiệu mỗi ngày dùng bộ bi riêng.
- Số "đến hạn" theo nhịp riêng từng số: không ổn định (Power 2/3 khúc, Mega 1/3).
- Cặp số hay đi cùng: không lặp lại giữa hai nửa dữ liệu (Power, Mega).

## Mega — dấu hiệu 100 kỳ gần nhất (04/10/2026, `build/suyluan.py mega`)
Cách chấm theo ý anh: mỗi luật loại được chấm theo TỪNG KỲ (kỳ đó không số bị loại nào về = đúng). Sai vài kỳ không sao vì chơi lâu dài; quan trọng là đúng nhiều kỳ và ổn định. So 100 kỳ gần với 100 kỳ trước đó.
- Bỏ số vắng ≥30: đúng 94% kỳ (100 trước: 88%), bỏ ~0.9 số/kỳ. Vắng ≥25: 85% (82%). Vắng ≥20: 72% (67%).
- Bỏ số ra 2 kỳ liền: 92% (92%). Gộp vắng ≥30 + ra 2 kỳ liền: **87%** (81%), bỏ ~1.6 số/kỳ.
- Bỏ số quá nóng (≥4/10 kỳ): 84% (81%).
- KHÔNG nên bỏ: số khó ra 100/200 kỳ (60–68%), 3–5 số ra ít nhất (38–62%), số ít ra cả 4 đoạn 25 kỳ (51% — chúng hay quay lại).
- Số nhiều ra cả 4 đoạn 25 kỳ (hiện 16 31 36): 36% kỳ có ≥1 số này (nhóm chỉ 2–3 số).

## Khía cạnh mới — 04/10/2026 (`build/khia_canh.py`, 3 đoạn 100 kỳ gần → xa, chạy tiến)
Đã thử: số lộn (12↔21), chạm tổng, cách ±2, số kỳ t−2/t−3, nguyên tố, chia hết cho 3, cùng vị trí ±1, số ra ≥2 lần/5 kỳ, số "tái xuất", hàng chục nhiều nhất/vắng mặt kỳ trước; hồi về trung vị (tổng, lẻ, u, z, số nhỏ); hình dạng: đếm chia hết 3, nguyên tố, khe nhỏ nhất, tổng đuôi, tổng mod 9, cặp đối xứng, số khe ≤3. (Bóng âm dương +5 không áp được cho số 2 chữ số trong dải này.)
Đứng được (cùng chiều cả 3 đoạn / đúng > vé giữ lại):
- **Mega:** số của kỳ t−3 (cùng thứ tuần trước) ra ít hơn 3/3 (12.2/12.9/12.6% vs 13.4%) — giống Power. Hồi về trung vị của TỔNG: đúng 77/76/71% (vé giữ 69%). Tổng mod 9 ∈ {1,3,4,5,6,7,8}: 87/92% (vé giữ 78%) — theo dõi.
- **Power:** tổng mod 9 (tập gọn 85%): 82/85% (vé giữ 78%) — theo dõi.
- **Loto:** số "tái xuất" (ra kỳ trước sau vắng ≥10) ra ít hơn 3/3 (10.3/12.5/10.5% vs 14.4%), ~1 số/kỳ → loại. Số ra ≥2 lần trong 5 kỳ ít hơn 3/3 (nhẹ). Hồi về trung vị của số nhỏ (≤17): 73/71/76% (vé giữ 66%).
Không đứng được: số lộn, chạm tổng, ±2, nguyên tố (nhóm số), chia hết 3, cùng vị trí ±1, hàng chục; hồi về trung vị của u, z (≈ vé giữ lại).
Lưu ý: "hồi về trung vị" phải tính kỳ bằng nhau là SAI, và luôn kèm cột vé giữ lại — nếu không sẽ thấy tỉ lệ cao giả (90%+).

## Luật loại nhỏ kiểu "bỏ số vắng lâu" — 04/10/2026 (`build/loai_nho.py`, 3 đoạn 100 kỳ, chấm theo từng kỳ)
Mỗi luật chỉ bỏ ~1 số/kỳ. ✔ = đúng ≥85% cả 3 đoạn và ≥ vé giữ lại.
- **Mega:** ra 2 kỳ liền 92/92/91% (đang dùng); ra kỳ trước VÀ kỳ t−3 90/90/91%; số lớn nhất (z) kỳ trước 88/86/91%; số ra nhiều nhất 100 kỳ 90/87/90% (ngược với cộng điểm "ra đều 4 đoạn" — theo dõi). Theo dõi: số vắng lâu nhất 92/85/90%, ra 3 lần/5 kỳ 92/94/87%.
- **Power:** số ra ít nhất 100 kỳ 93/93/91% (hợp thuyết bi khó ra). Theo dõi: ra 3 lần/5 kỳ 96/96/91%, ra kỳ trước & t−3 93/90/93%, z kỳ trước 91/89/88%.
- **Loto:** số "tái xuất" sau vắng ≥15: 96/93/97%, ≥10: 92/88/91%; số vắng lâu nhất 89/90/89%; ra 3 lần/5 kỳ 92/95/91%; u và z kỳ trước 86–91%; ra cả t−3 & t−6 96/97/91%.
Chênh với vé giữ lại chỉ 1–5 điểm — đúng kiểu "cơ sở nhỏ, ổn định".

## Nhịp riêng từng số: "ra – vắng k kỳ – ra" → kỳ ngay sau? (04/10/2026, 3 đoạn 100 kỳ)
Ý anh: số 03 ra, vắng 2 kỳ, ra lại ở kỳ thứ 4 rồi lại vắng vài kỳ.
- **Vắng đúng 2 kỳ rồi ra → kỳ ngay sau ra ÍT hơn bình quân ở cả 3 trò, cả 3 đoạn:** Mega 11.1/10.2/10.5% (bình quân 13.3%), Power 5.0/9.1/8.0% (10.9%), Loto 8.8/9.3/10.9% (14.3%). Mẫu nhỏ (40–60 lần/đoạn) → đưa vào sổ kiểm chứng (luật `nhip2`), chưa áp dụng.
- Mega: vắng đúng 3 kỳ rồi ra → kỳ sau ra NHIỀU hơn 3/3 (16.0/15.1/18.0%).
- Power: vắng 7–10 rồi ra → kỳ sau ra ít hơn (7.9/6.5/11.0%).
- "Vắng tiếp ≥3 kỳ sau khi ra" không ổn định ở nhịp nào.

## Nhịp riêng từng số (ý anh: ra kỳ 1, 5, 9… → kỳ 2, 3, 6, 7, 8 loại đúng) — 04/10/2026 (`build/nhip.py`)
Cách tính: với mỗi số, xem lịch sử 200 kỳ của CHÍNH số đó — mỗi khi nó đã vắng đúng g kỳ (bằng số kỳ đang vắng hiện tại) thì kỳ kế nó có ra không. Đã gặp ≥5 lần mà chưa ra lần nào → loại.
- **Mega:** nhóm bị loại ra ít hơn ở cả 3 đoạn (10.8/11.7/10.5% so với 13.6–13.8% các số còn lại) → nhịp riêng có dấu vết. Nhưng mỗi kỳ nhóm này ~7 số nên loại cả nhóm chỉ đúng 40–50% kỳ; dùng làm −điểm thì pool 15 không tốt hơn (2.14 → 2.11) → chưa áp dụng, đưa vào sổ kiểm chứng (`nhom_nhip`: đúng khi nhóm ra ít hơn bình quân).
- **Power:** nhóm bị loại ra NHIỀU hơn ở 2/3 đoạn → không dùng. **Loto:** ít hơn 2/3 đoạn → chưa ổn định.
- Bài học: loại 1 số bất kỳ vốn đã đúng ~86–89% số kỳ; "lợi" thật nằm ở chỗ nhóm bị loại ra ít hơn các số còn lại.

## Nhịp tối thiểu từng số (ý anh: "luôn nghỉ ≥x kỳ mới ra lại" mà vừa ra → kỳ này không ra) — 04/10/2026 (`build/nhip_min.py`)
Trong cửa sổ W kỳ, số đó có ≥5 lần ra và khoảng nghỉ nhỏ nhất giữa 2 lần ra là x (≥1); hiện mới nghỉ < x → loại.
- **Loto (W=100):** nhóm bị loại ra ít hơn cả 3 đoạn (12.9/7.4/11.6% vs 14.3–14.6%); đúng 86/89/82% kỳ, ~1.2 số/kỳ.
- **Power (W=200):** ít hơn 3/3 nhưng rất nhẹ (9.9/10.7/10.0% vs 10.9%); đúng 93/91/90% kỳ, ~0.7 số/kỳ.
- **Mega:** không ổn định — W=100 gần đây nhóm này lại ra NHIỀU hơn (17%).
- Thực tế x hầu hết = 1 (số chưa từng ra 2 kỳ liền trong cửa sổ); với 200 kỳ gần như số nào cũng có lúc ra liền nên luật ít khi kích hoạt.
- **Bản đúng ý anh (không cần 100%): trong 100 kỳ gần, ≥80% số lần số đó nghỉ ≥x kỳ mới ra lại; mới nghỉ <x → kỳ này khó ra.**
  Loto: nhóm này ra ít hơn ở cả 3 đoạn (13.2/12.9/13.3% vs 14.5–14.6%) ✔; Mega: lại ra NHIỀU hơn (14.9/13.9/13.1% vs 13.0–13.4%) ✘; Power: lẫn lộn ✘.
  Mỗi kỳ nhóm có ~6–10 số → loại cả nhóm chỉ đúng 25–44% kỳ; từng số thì "không ra" đúng ~86–87% kỳ (Loto) nhưng phần lớn là vì số nào cũng thường không ra; lợi thật ≈ 1.3 điểm %. Dùng làm −điểm cho Loto: pool 15 không tốt hơn (2.42 → 2.34 ở 50 kỳ) → chưa áp dụng, đưa vào sổ kiểm chứng (`nhom_nhip80`).
Đã đưa vào sổ kiểm chứng (nhipmin100, nhipmin200), chưa áp dụng.

## Gộp luật loại để thu hẹp pool — 04/10/2026 (`build/thu_hep.py`)
"Không mất số" = kỳ đó không số bị loại nào về (100 kỳ gần / 100 kỳ trước). Mỗi số bỏ thêm tốn ~4–8 điểm % an toàn.
- Mega: ra 3 lần/5 kỳ (92/94%, bỏ 0.9) → + phá nhịp tối thiểu 200 (88/92%) → + vắng ≥30 (84/81%, bỏ 2.2) → + z kỳ trước (77/74%) → … 60% khi bỏ ~4.8 số.
- Power: nhịp ra–vắng 2–ra (99/96%) → + ra 3 lần/5 kỳ (96/92%) → + ít nhất 100 kỳ (89/85%, bỏ 1.9) → + phá nhịp tối thiểu 100 (63/64%, bỏ 4.8).
- Loto: nhịp ra–vắng 2–ra (95/96%) → + tái xuất ≥10 (87/85%) → + vắng lâu nhất (77/76%) → + phá nhịp 100 (68/68%) → + ra 3 lần/5 kỳ (62/64%, bỏ 4.1).
Kết luận: luật loại an toàn ≥80% kỳ chỉ bỏ được ~2–3 số/kỳ; phần thu hẹp lớn (xuống 15–20 số) vẫn phải nhờ chấm điểm (pool 15 trúng TB ~2.1 số/kỳ).

## Loto — kỳ nào nên đánh mạnh? (04/10/2026, 400 kỳ chạy tiến)
- Phiên 13h vs 21h: pool 15 trúng TB 2.21 vs 2.18 — như nhau.
- "Độ đồng thuận" điểm (top 5 vượt xa phần còn lại): KHÔNG giúp (cao: 2.12, thấp: 2.25).
- **Nhịp pool**: 5 kỳ gần pool 15 trúng TB ≥ ngưỡng 1/3 tốt nhất (~2.4) → kỳ tới TB 2.40/2.41, ≥3 số 51%/52% (hai nửa 200 kỳ) so với 1.9–2.3 và 32–45% lúc khác → dùng làm chỉ báo "kỳ đánh mạnh".

## Số May Mắn Loto — nghiên cứu sâu 04/10/2026 (`build/somayman.py`, đoạn 150 kỳ gần → xa)
Chọn 3 MM (3/12 ⇒ phần giữ lại 25%):
- 3 MM vắng lâu nhất (đang dùng): 29 / 27 / 21 / 31%.
- **MM kỳ trước + 2 MM vắng lâu nhất: 33 / 34 / 23 / 29%** — tốt nhất 2 đoạn gần.
- MM kỳ trước ±1: 29 / 29 / 24 / 28%. Ít ra nhất 60/120 kỳ, nóng nhất, cùng phiên, tổng mod 12: ≈25% (không dấu vết).
- **MM hay lặp lại ngay kỳ sau**: 10.0 / 15.3 / 8.7 / 7.3% (bình quân 8.3%) → KHÔNG nên loại MM vừa ra.
- Luật loại MM: loại MM vừa ra / cùng phiên hôm trước đều kém hơn phần giữ lại → không dùng; loại MM ra ≥2 lần/5 kỳ, ≥3 lần/10 kỳ ≈ ngang → không lợi.

## Loto — dấu vết máy ở khung 100 / 200 kỳ gần (04/10/2026, `build/dauvet_may.py`)
Mục tiêu: xác suất nghiêng, không cần quy luật 100%.
- Lặp theo độ trễ: khung 100 kỳ — số của kỳ cách 4 kỳ ra ÍT (12.6/12.2%), cách 7 kỳ ra NHIỀU (16.0/16.0%), cách 9 kỳ NHIỀU (17.0/15.6%) (bình quân 14.3%); khung 200 kỳ không xác nhận → trôi, đưa vào sổ theo dõi (nhom_k7, nhom_k9).
- Số ra nhiều nhất 200 kỳ → kỳ kế 15.1/14.8% (nhỉnh hơn); ít nhất 200 kỳ → 13.0/14.0% (kém hơn) — lệch dài hạn giữ nhẹ (đang dùng qua tín hiệu "dễ ra").
- Vị trí u..y dính kỳ trước: không (≈50%). Tính cách theo phiên / phiên×thứ ở 100–200 kỳ gần: không còn (corr ≈0).
Kết luận: dấu vết máy Loto rất mờ, chỉ ±1–2 điểm % và hay trôi → Loto chơi nhẹ, chỉ đánh mạnh khi "nhịp pool" tốt.

## Loto — tách riêng phiên 13h và 21h (05/10/2026, `build/phien.py`, khung 100/200 kỳ của chính phiên)
- **13h: số vắng ≥20 kỳ (tính trong phiên 13h) ra ÍT** — nhóm ra 11.2/14.7% (100 kỳ gần/trước), 12.9/12.0% (200 kỳ) vs 14.3%; loại đúng 78–80% kỳ, bỏ ~1.8 số → nên loại cho 13h.
- **21h: số vắng ≥20 kỳ (phiên 21h) ra NHIỀU** — 19.0/14.5%, 16.4/17.9% → KHÔNG loại cho 21h (21h hay "cân bằng" quay lại).
- Lặp theo ngày (k=1..7 cùng phiên), nóng/lạnh giữ sang kỳ kế: không ổn định ở cả 2 phiên.
- MM: 13h — 3 MM vắng lâu nhất (trong phiên) chỉ 21–22% (dưới 25%) → không hợp; 21h lúc 19% lúc 27%.
- Pool 15 nóng 50 kỳ cùng phiên: 13h TB 2.12–2.18, 21h 2.10–2.27 — như nhau.
Đưa vào sổ theo dõi: vangph20.

## Loto — tìm thêm dấu vết theo phiên (05/10/2026, `build/phien2.py`)
Hai phiên có "tính cách" ngược nhau:
- **13h kiểu "lạnh giữ lạnh"**: số tái xuất trong phiên (ra hôm trước sau vắng ≥10 kỳ 13h) ra ÍT ở cả 4 khung: 10.9/10.8% (100 kỳ), 10.8/13.7% (200 kỳ) vs 14.3%, ~1 số/kỳ → loại (sổ: txph13). Số vắng ≥20 kỳ trong phiên cũng ít (xem mục trước).
- **21h kiểu "cân bằng"**: số tái xuất trong phiên ra NHIỀU: 15.2/18.9%, 17.0/16.1% → giữ (sổ: nhom_txph21); số vắng ≥20 trong phiên ra nhiều; số vắng 10–19 kỳ ra ít 3/4 khung.
- Liên hệ 13h→21h cùng ngày, 21h→13h hôm sau: không ổn định. Hồi về trung vị tổng theo phiên: đúng 76–79% kỳ (vé giữ ~74%, lợi nhẹ).

## "Luận số / soi cầu" trên mạng — kiểm bằng dữ liệu Vietlott (05/10/2026, `build/soicau.py`, 2 nửa 150 kỳ)
Luận số trên mạng = các cách soi cầu của lô đề: bạc nhớ (cặp số hay theo sau một dữ kiện), lô gan (vắng lâu), lô rơi (lặp kỳ trước), lô kép, đầu/đuôi câm, cầu vị trí (ghép 2 chữ số ở 2 vị trí cố định của kết quả kỳ trước, "cầu chạy" k ngày thì đánh tiếp), cầu Pascal (cộng dồn chữ số).
Kết quả (bình quân mỗi số: Loto 14.3, Mega 13.3, Power 10.9%):
- **Cầu vị trí "đang chạy thì chạy tiếp"**: KHÔNG đúng ở Loto/Power (cầu chạy 1–3 kỳ ra 6–19% lộn xộn); Mega nhích nhẹ theo độ dài cầu (chạy 2: 14.0/16.1%, chạy 3: 17.4/20.0% nhưng chỉ ~25 lần).
- **Cầu Pascal**: Power 14.3/14.1% (cao hơn 10.9% cả 2 nửa, ~80 lần/nửa); Loto 16/19% (~45 lần); Mega lộn xộn.
- **Lô kép**: Loto 18.9/16.9% (cao hơn 14.3% cả 2 nửa); Mega/Power bình thường.
- **Lô gan**: Mega ra ít (11.3/11.5%) — khớp thuyết bi; Power nửa gần ra nhiều (15.6%); Loto hơi ít.
- Lô rơi, đầu câm, đuôi câm: ≈ bình thường.
- **Thêm (05/10): các cách soi khác** (bình quân Loto 14.3 / Mega 13.3 / Power 10.9%):
  - **Kép liền kề** (kỳ trước có kép → kép bên cạnh 11↔22↔33): Loto 17.4/17.8, Mega 18.2/14.3, Power 13.1/13.6% — cao hơn ở cả 3 trò, cả 2 nửa (mẫu nhỏ) → theo dõi (nhom_keplk).
  - **Lô kẹp** (a, a+2 → a+1): Power 8.6/6.7%, Loto 13.3/12.1% — ra ÍT → theo dõi (nhom_lokep).
  - **Bạch thủ** (cầu chạy dài nhất): Power 12.7/12.2% nhích nhẹ; Loto/Mega không.
  - **Theo ngày dương** (ngày, tháng, ngày+tháng): Loto 15.2/16.5% nhích nhẹ; Mega/Power không.
  - Nuôi kép, cạnh kép, chạm nhiều nhất, xiên 2 (cặp hay đi cùng): không có dấu vết.
Đưa vào sổ theo dõi: nhom_kep, nhom_pascal, nhom_cau2. Nhận xét: phần lớn "soi cầu" là đọc chuỗi ngẫu nhiên; vài cái nhích nhẹ cần theo dõi thêm.

## Bi Power/Mega chỉ xét x kỳ gần (05/10/2026, theo ý anh: thay bi định kỳ)
- Tần suất từng số ở 2 khối 100 kỳ liền nhau: corr TB Power +0.03, Mega −0.03 (mức nhiễu 90% ≈0.16–0.21) → "tính chất bi" không giữ quá ~100 kỳ, đúng với việc thay bi.
- goiy.py: các tín hiệu bi (dễ/khó ra, thưa, ra đều 4 đoạn, ít nhất 100 kỳ) dùng cửa sổ WB: Power 100, Mega 150 (thử 50–200, pool 15 gần như nhau: Power 1.73–1.77, Mega 2.09–2.15).

## Sổ chấm phương pháp Loto 5/35 (bắt đầu 03/10/2026 21h, chấm bằng `build/goiy.py`)
| Kỳ | Kết quả | Nóng | Kề ±1 | Dễ ra | Bỏ khó ra | Bỏ vắng≥15 | Đà/khoảng tổng | Pool dấu vết 15 | Vé tốt nhất |
|---|---|---|---|---|---|---|---|---|---|
| 03/10 21h | 10 12 29 33 35 · MM 07 | 1/6 (10) | 1/7 (12) | 0/7 | 3/3 bỏ đúng | 5/6 (29 về sau 15+ kỳ) | sai: tổng 119 ngoài 77–105 | 2 (10 12) | 1 số |
| 04/10 13h | 02 19 22 32 35 · MM 04 | 0/4 | 1/7 (32) | 2/8 (22 35) | 3/3 bỏ đúng | 4/5 (19 về, vắng 15+) | sai: tổng 110 ngoài 77–106 | **3 (22 32 35)**; pool 10: 2 · tâm linh 12: **3 (19 22 32)** | 1 số |
| 05/10 13h | 09 14 15 16 35 · MM 02 | — | — | — | luật ● 8/9 đúng (tx10 sai: 16 về) | — | — | **3 (14 15 35)**; pool 10: 2 (15 35) · pool 20: 4 · tâm linh 12: 3 · MM 06 01 10 trật (02 lặp lại kỳ trước) | 1 số; vé anh: 1 số mỗi vé (35 / 15) |
| 05/10 21h | 01 13 16 20 26 · MM 11 (tổng 76) | 0/7 | 1 (13) | 1 (13) | bỏ khó ra sai: 01 26 về | luật ● 7/10 đúng (vắng≥20, lâu lâu mới ra, vắng lâu nhất cùng sai vì 26 về sau vắng lâu) | sai: tổng 76 ngoài 78–107 | 1 (13); pool 10: 1 · pool 20: 2 (13 20) · tâm linh 12: 1 (13★) · khẳng định 6/8 (sai: pool 15 ≥2, ≥1 số nóng) · MM 06 01 10 trật | 1 số (vé 1, 2, 4, 6); sổ 20/35 luật đúng |
| 06/10 13h | 21 22 23 24 27 · MM 01 (tổng 117; 4 số liên tiếp, cả 5 số đầu 2) | 0/8 | 2 (21 27) | 2 (22 27) | bỏ khó ra sai: 24 về | luật ● 8/10 đúng (vắng ≥20 + vắng lâu nhất sai: 27 về) | sai: tổng 117 ngoài 77–107 | 1 (22); pool 10/20: 1/1 · tâm linh 12: 1 (24★) · khẳng định 3/8 (sai: pool 15 ≥2, pool 20 ≥2, 2 kỳ gần, nóng, rải ≥3 chục) · **MM 01 trúng** | 1 số (vé 4: 22, vé 6: 24); sổ 25/35 luật đúng |

## Sổ chấm phương pháp Mega 6/45 (bắt đầu 04/10/2026; chi tiết từng luật trong app → "Sổ kiểm chứng suy luận")
| Kỳ | Kết quả | Luật loại (đã áp dụng) | Bị loại | Pool 10 / 15 / 20 | Vé tốt nhất | Tâm linh 12 | Bao 7 anh | Ghi chú |
|---|---|---|---|---|---|---|---|---|
| 04/10 | 15 20 29 37 40 45 (tổng 186) | **đúng hết** (8 số bị loại, không số nào về); sổ: 24/25 luật đúng | 02 05 08 19 27 31 41 42 | 1 / 1 / 3 (15; 20 45) | 1 | 0 | 1 (15) | 4/6 số về đang vắng 11–14 kỳ (29 37 40 45) → thêm +1 điểm "vắng 11–15" cho Mega (pool 15 ở 50 kỳ 2.12→2.22). Tổng 186 > 126 đúng xu hướng hồi về trung vị. |
| 07/10 | 10 14 36 37 41 43 (tổng 181) | **đúng hết** 10/10 luật ● (bỏ 05 08 19 20 32 42 45 15 16 — không số nào về) | 05 08 19 32 42 | 2 / 2 / 3 (36 41; 43) | lõi 36 41 về (31 trật) | vé tốt nhất 2 số (vé 1, 2, 3, 6) | tâm linh 12: 1 (41) | khẳng định sai 2: "≥1 số nóng 20 kỳ", "rải ≥4 hàng chục" (chỉ 3 chục) |
| 04/10 21h | 07 16 30 31 33 · MM 02 | 0/4 nóng | 2 (31 33) | — | — | luật loại áp dụng đúng hết (bỏ 10 19 26 27 35) | — | pool 10/15/20: 0/2/4 | vé tốt nhất 1; **vé anh** 09 11 19 28 34 mm06 & 11 14 20 28 34 mm10: 0 số, MM trật; sổ 23/25 luật đúng |


# Dấu vết bi theo 4 khung 10/20/50/100 kỳ (05/10/2026)

Tối đa 100 kỳ vì họ thay bi 1–2 tháng/lần. Goiy và sổ kiểm chứng của Power/Mega đã chuyển sang khung 100 kỳ (Mega trước đây dùng 150).

## power655 — 1. Hai khối W kỳ liền nhau có giống nhau không (tương quan tần suất từng số, TB trên 300 kỳ gần)

| Khung W | Thực tế | Quay ngẫu nhiên: TB (khoảng 90% của 30 lần thử) | Nhận xét |
|---|---|---|---|
| 10 | -0.002 | +0.006 (-0.017 … +0.045) | nằm trong vùng ngẫu nhiên |
| 20 | +0.011 | -0.002 (-0.055 … +0.039) | nằm trong vùng ngẫu nhiên |
| 50 | -0.018 | -0.002 (-0.057 … +0.060) | nằm trong vùng ngẫu nhiên |
| 100 | +0.041 | -0.007 (-0.146 … +0.083) | nằm trong vùng ngẫu nhiên |

## 2–3. Tỉ lệ ra kỳ kế của mỗi số trong nhóm (trung bình 10.9%) — 3 đoạn 100 kỳ: gần → xa

| Nhóm | Cỡ TB | Đoạn 1 | Đoạn 2 | Đoạn 3 | Kết luận |
|---|---|---|---|---|---|
| nóng 10 | 16.2 | 9.7% | 11.3% | 11.2% | — |
| lạnh 10 | 38.8 | 11.4% | 10.7% | 10.8% | — |
| nóng 20 | 20.4 | 10.2% | 11.4% | 11.2% | ▲ 2/3 |
| lạnh 20 | 34.6 | 11.3% | 10.6% | 10.7% | — |
| nóng 50 | 25.1 | 11.1% | 10.6% | 11.5% | — |
| lạnh 50 | 29.9 | 10.8% | 11.2% | 10.4% | — |
| nóng 100 | 29.4 | 10.6% | 10.7% | 11.0% | — |
| lạnh 100 | 25.6 | 11.2% | 11.2% | 10.8% | — |
| NÓNG đồng nhất 4 khung | 8.3 | 10.8% | 11.6% | 11.0% | — |
| LẠNH đồng nhất 4 khung | 16.4 | 11.8% | 10.9% | 10.5% | — |
| mới nóng (10,20↑ 50,100↓) | 1.6 | 7.5% | 15.8% | 11.7% | ▲ 2/3 |
| mới nguội (10,20↓ 50,100↑) | 6.6 | 10.8% | 9.4% | 11.8% | — |

## 4. Dò "vừa thay bi": độ giống 20 kỳ gần ↔ 50 kỳ trước đó (300 kỳ). Thấp nhất 1/3 = "lệch hẳn, nghi vừa thay bi"

| Nhóm | Khi LỆCH HẲN (nghi thay bi) | Khi bình thường | Khi GIỐNG NHAU |
|---|---|---|---|
| nóng 10 | 10.0% | 11.8% | 10.4% |
| nóng 20 | 10.5% | 11.9% | 10.4% |
| nóng 50 | 10.7% | 11.8% | 10.7% |
| nóng 100 | 10.7% | 10.8% | 10.8% |
| lạnh 20 | 11.1% | 10.3% | 11.2% |
| lạnh 100 | 11.1% | 11.0% | 11.0% |
| NÓNG đồng nhất 4 khung | 10.4% | 11.8% | 11.1% |
| LẠNH đồng nhất 4 khung | 10.9% | 10.7% | 11.6% |

## 5. Hiện trạng kỳ tới (sau 03/10/2026)

- Độ giống 20 kỳ gần ↔ 50 kỳ trước: **+0.12** (cao hơn 84% các kỳ trong 300 kỳ) → giống nhau — khung dài còn dùng được
- NÓNG đồng nhất 4 khung: 01 07 11 13 18 25 38 47
- LẠNH đồng nhất 4 khung: 03 06 10 12 15 17 19 20 30 34 35 37 42 46 48 49 50 51
- mới nóng (10,20↑ 50,100↓): 36 54
- mới nguội (10,20↓ 50,100↑): 16 23 28 33 41 44 45


## mega645 — 1. Hai khối W kỳ liền nhau có giống nhau không (tương quan tần suất từng số, TB trên 300 kỳ gần)

| Khung W | Thực tế | Quay ngẫu nhiên: TB (khoảng 90% của 30 lần thử) | Nhận xét |
|---|---|---|---|
| 10 | +0.012 | -0.005 (-0.042 … +0.042) | nằm trong vùng ngẫu nhiên |
| 20 | +0.048 | -0.010 (-0.068 … +0.051) | nằm trong vùng ngẫu nhiên |
| 50 | -0.008 | +0.003 (-0.040 … +0.087) | nằm trong vùng ngẫu nhiên |
| 100 | -0.013 | +0.014 (-0.089 … +0.120) | nằm trong vùng ngẫu nhiên |

## 2–3. Tỉ lệ ra kỳ kế của mỗi số trong nhóm (trung bình 13.3%) — 3 đoạn 100 kỳ: gần → xa

| Nhóm | Cỡ TB | Đoạn 1 | Đoạn 2 | Đoạn 3 | Kết luận |
|---|---|---|---|---|---|
| nóng 10 | 17.6 | 13.3% | 13.1% | 13.8% | — |
| lạnh 10 | 27.4 | 13.4% | 13.5% | 13.0% | — |
| nóng 20 | 22.9 | 13.4% | 13.6% | 14.1% | — |
| lạnh 20 | 22.1 | 13.3% | 13.0% | 12.6% | ▼ 2/3 |
| nóng 50 | 23.3 | 13.2% | 13.9% | 13.8% | ▲ 2/3 |
| lạnh 50 | 21.7 | 13.4% | 12.7% | 12.8% | ▼ 2/3 |
| nóng 100 | 20.9 | 13.4% | 13.1% | 13.9% | — |
| lạnh 100 | 24.1 | 13.3% | 13.6% | 12.9% | — |
| NÓNG đồng nhất 4 khung | 8.9 | 13.3% | 12.8% | 13.1% | — |
| LẠNH đồng nhất 4 khung | 11.8 | 13.0% | 12.8% | 11.8% | ▼ ra ÍT hơn 3/3 |
| mới nóng (10,20↑ 50,100↓) | 2.4 | 12.3% | 13.6% | 17.0% | — |
| mới nguội (10,20↓ 50,100↑) | 3.0 | 12.8% | 14.9% | 13.9% | ▲ 2/3 |

## 4. Dò "vừa thay bi": độ giống 20 kỳ gần ↔ 50 kỳ trước đó (300 kỳ). Thấp nhất 1/3 = "lệch hẳn, nghi vừa thay bi"

| Nhóm | Khi LỆCH HẲN (nghi thay bi) | Khi bình thường | Khi GIỐNG NHAU |
|---|---|---|---|
| nóng 10 | 13.6% | 13.3% | 13.4% |
| nóng 20 | 13.3% | 13.5% | 14.3% |
| nóng 50 | 13.5% | 13.8% | 13.7% |
| nóng 100 | 13.4% | 13.6% | 13.3% |
| lạnh 20 | 13.4% | 13.1% | 12.3% |
| lạnh 100 | 13.3% | 13.1% | 13.3% |
| NÓNG đồng nhất 4 khung | 13.0% | 13.4% | 12.8% |
| LẠNH đồng nhất 4 khung | 12.2% | 13.2% | 12.1% |

## 5. Hiện trạng kỳ tới (sau 04/10/2026)

- Độ giống 20 kỳ gần ↔ 50 kỳ trước: **+0.19** (cao hơn 88% các kỳ trong 300 kỳ) → giống nhau — khung dài còn dùng được
- NÓNG đồng nhất 4 khung: 02 03 06 12 15 20 26 27 31 33 38 41
- LẠNH đồng nhất 4 khung: 05 08 14 19 23 24 28 32 34 42
- mới nóng (10,20↑ 50,100↓): 01 10 18
- mới nguội (10,20↓ 50,100↑): 37 44


## loto535 — 1. Hai khối W kỳ liền nhau có giống nhau không (tương quan tần suất từng số, TB trên 300 kỳ gần)

| Khung W | Thực tế | Quay ngẫu nhiên: TB (khoảng 90% của 30 lần thử) | Nhận xét |
|---|---|---|---|
| 10 | +0.037 | -0.006 (-0.047 … +0.029) | **có dấu vết giữ lại** |
| 20 | +0.021 | -0.013 (-0.081 … +0.048) | nằm trong vùng ngẫu nhiên |
| 50 | +0.052 | -0.009 (-0.093 … +0.122) | nằm trong vùng ngẫu nhiên |
| 100 | +0.073 | +0.007 (-0.090 … +0.136) | nằm trong vùng ngẫu nhiên |

## 2–3. Tỉ lệ ra kỳ kế của mỗi số trong nhóm (trung bình 14.3%) — 3 đoạn 100 kỳ: gần → xa

| Nhóm | Cỡ TB | Đoạn 1 | Đoạn 2 | Đoạn 3 | Kết luận |
|---|---|---|---|---|---|
| nóng 10 | 15.0 | 15.1% | 13.7% | 13.8% | ▼ 2/3 |
| lạnh 10 | 20.0 | 13.7% | 14.7% | 14.7% | ▲ 2/3 |
| nóng 20 | 19.5 | 14.9% | 14.1% | 14.0% | — |
| lạnh 20 | 15.5 | 13.5% | 14.5% | 14.6% | — |
| nóng 50 | 14.8 | 14.3% | 14.2% | 14.2% | — |
| lạnh 50 | 20.2 | 14.3% | 14.4% | 14.3% | — |
| nóng 100 | 16.9 | 14.2% | 14.8% | 14.9% | ▲ 2/3 |
| lạnh 100 | 18.1 | 14.4% | 13.7% | 13.8% | ▼ 2/3 |
| NÓNG đồng nhất 4 khung | 7.2 | 16.0% | 12.6% | 14.4% | — |
| LẠNH đồng nhất 4 khung | 9.3 | 14.6% | 13.2% | 14.5% | — |
| mới nóng (10,20↑ 50,100↓) | 3.0 | 15.7% | 14.6% | 13.8% | ▲ 2/3 |
| mới nguội (10,20↓ 50,100↑) | 1.7 | 12.4% | 18.1% | 16.0% | ▲ 2/3 |

## 4. Dò "vừa thay bi": độ giống 20 kỳ gần ↔ 50 kỳ trước đó (300 kỳ). Thấp nhất 1/3 = "lệch hẳn, nghi vừa thay bi"

| Nhóm | Khi LỆCH HẲN (nghi thay bi) | Khi bình thường | Khi GIỐNG NHAU |
|---|---|---|---|
| nóng 10 | 14.0% | 13.2% | 15.4% |
| nóng 20 | 15.0% | 13.5% | 14.5% |
| nóng 50 | 14.7% | 13.5% | 14.4% |
| nóng 100 | 15.4% | 13.3% | 15.2% |
| lạnh 20 | 13.4% | 15.3% | 14.0% |
| lạnh 100 | 13.3% | 15.2% | 13.4% |
| NÓNG đồng nhất 4 khung | 14.5% | 13.1% | 15.1% |
| LẠNH đồng nhất 4 khung | 12.8% | 16.9% | 12.9% |

## 5. Hiện trạng kỳ tới (sau 04/10/2026 21h)

- Độ giống 20 kỳ gần ↔ 50 kỳ trước: **-0.06** (cao hơn 27% các kỳ trong 300 kỳ) → **lệch hẳn — nghi vừa thay bi**, tin khung 10/20 hơn
- NÓNG đồng nhất 4 khung: 02 07 10 11 30 34 35
- LẠNH đồng nhất 4 khung: 04 05 09 18 21 23 25 26 29 31
- mới nóng (10,20↑ 50,100↓): 12 17
- mới nguội (10,20↓ 50,100↑): 16 19 27




# Luật loại theo 4 khung gần (05/10/2026) — anh: luật đúng ≥70% là dùng tốt

Tiêu chí: đúng ≥70% ở cả khung 50 và 100 kỳ, và số bị loại ra không nhiều hơn trung bình. Luật đạt được đưa vào gợi ý dưới dạng trọng số trừ điểm (dấu vết = nghiêng xác suất, không loại cứng):
- Power thêm lt3, tx15, tx10, zprev.
- Mega thêm nong35, tx15, nong10, nhieu100, nhip2.
- Loto thêm txph13.

Kiểm thử 200 kỳ, pool 15 trúng TB: Power 1.76→1.75, Mega 2.095→2.11, Loto 2.335→2.335 (tương đương).

## power655 — luật loại, % kỳ đúng ở 4 khung gần (kỳ gần nhất → lùi)

| Luật | Đang dùng | Cỡ TB | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | Ra mỗi số (TB 10.9%) | Đạt ≥70% | Kỳ tới loại |
|---|---|---|---|---|---|---|---|---|---|
| vang20 |  | 4.4 | 60% | 50% | 56% | 51% | 14.7% | ✘ | 12 20 30 50 |
| vang25 |  | 2.1 | 70% | 75% | 78% | 71% | 15.7% | ✔ | 12 |
| vang30 |  | 0.9 | 70% | 85% | 86% | 83% | 20.7% | ✔ | — |
| thua15 |  | 4.3 | 60% | 60% | 58% | 54% | 13.3% | ✘ | 10 12 15 19 20 |
| vang1 |  | 1.0 | 90% | 85% | 86% | 82% | 18.0% | ✔ | 12 |
| vang2nd |  | 1.0 | 80% | 85% | 90% | 88% | 12.0% | ✔ | 20 |
| lien2 |  | 0.6 | 80% | 90% | 90% | 91% | 15.0% | ✔ | 13 |
| nong35 | ✔ | 0.6 | 80% | 90% | 96% | 96% | 7.0% | ✔ | 13 |
| lt3 | ✔ | 0.8 | 90% | 90% | 94% | 93% | 8.9% | ✔ | 13 |
| tx15 | ✔ | 1.1 | 100% | 100% | 92% | 93% | 7.6% | ✔ | — |
| tx10 | ✔ | 2.0 | 90% | 90% | 84% | 86% | 8.0% | ✔ | 16 |
| nong10 |  | 0.6 | 80% | 90% | 92% | 90% | 17.5% | ✔ | 11 |
| it100 | ✔ | 1.0 | 90% | 95% | 96% | 93% | 7.0% | ✔ | 06 |
| nhieu100 |  | 1.0 | 100% | 100% | 96% | 90% | 10.0% | ✔ | 07 |
| nhip2 | ✔ | 0.4 | 90% | 95% | 98% | 99% | 5.0% | ✔ | 18 |
| nhipmin100 |  | 3.2 | 70% | 70% | 66% | 72% | 9.0% | ~ | 06 07 16 35 54 |
| nhipmin200 |  | 3.2 | 70% | 70% | 66% | 72% | 9.0% | ~ | 06 07 16 35 54 |
| vangph20 |  | 0.0 | 100% | 100% | 100% | 100% | 0.0% | ✔ | — |
| txph13 |  | 0.0 | 100% | 100% | 100% | 100% | 0.0% | ✔ | — |
| uprev |  | 1.0 | 90% | 95% | 86% | 90% | 10.0% | ✔ | 07 |
| zprev | ✔ | 1.0 | 100% | 95% | 96% | 91% | 9.0% | ✔ | 54 |

## mega645 — luật loại, % kỳ đúng ở 4 khung gần (kỳ gần nhất → lùi)

| Luật | Đang dùng | Cỡ TB | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | Ra mỗi số (TB 13.3%) | Đạt ≥70% | Kỳ tới loại |
|---|---|---|---|---|---|---|---|---|---|
| vang20 | ✔ | 2.6 | 70% | 60% | 74% | 72% | 11.5% | ✔ | 05 08 19 42 |
| vang25 |  | 1.4 | 90% | 80% | 86% | 85% | 10.5% | ✔ | 05 08 42 |
| vang30 |  | 0.9 | 100% | 90% | 96% | 94% | 6.8% | ✔ | 05 42 |
| thua15 | ✔ | 2.8 | 80% | 70% | 76% | 72% | 11.9% | ✔ | 05 08 19 32 42 |
| vang1 |  | 1.0 | 100% | 90% | 92% | 92% | 8.0% | ✔ | 05 |
| vang2nd |  | 1.0 | 100% | 90% | 94% | 91% | 9.0% | ✔ | 42 |
| lien2 | ✔ | 0.8 | 90% | 90% | 92% | 92% | 10.3% | ✔ | 20 |
| nong35 | ✔ | 0.9 | 100% | 100% | 96% | 92% | 8.5% | ✔ | — |
| lt3 | ✔ | 0.9 | 90% | 90% | 92% | 90% | 11.2% | ✔ | — |
| tx15 | ✔ | 0.6 | 100% | 100% | 98% | 94% | 10.0% | ✔ | — |
| tx10 |  | 1.5 | 100% | 95% | 84% | 81% | 13.5% | ✔ | 29 37 40 45 |
| nong10 | ✔ | 0.8 | 100% | 95% | 96% | 95% | 5.9% | ✔ | 15 |
| it100 |  | 1.0 | 100% | 100% | 90% | 85% | 15.0% | ✔ | 05 |
| nhieu100 | ✔ | 1.0 | 90% | 85% | 88% | 90% | 10.0% | ✔ | 16 |
| nhip2 | ✔ | 0.5 | 90% | 95% | 94% | 94% | 11.1% | ✔ | — |
| nhipmin100 |  | 1.4 | 80% | 70% | 78% | 76% | 17.1% | ✔ | 40 |
| nhipmin200 |  | 1.4 | 80% | 70% | 78% | 76% | 17.1% | ✔ | 40 |
| vangph20 |  | 0.0 | 100% | 100% | 100% | 100% | 0.0% | ✔ | — |
| txph13 |  | 0.0 | 100% | 100% | 100% | 100% | 0.0% | ✔ | — |
| uprev |  | 1.0 | 90% | 85% | 82% | 85% | 15.0% | ✔ | 15 |
| zprev | ✔ | 1.0 | 100% | 95% | 88% | 88% | 12.0% | ✔ | 45 |

## loto535 — luật loại, % kỳ đúng ở 4 khung gần (kỳ gần nhất → lùi)

| Luật | Đang dùng | Cỡ TB | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | Ra mỗi số (TB 14.3%) | Đạt ≥70% | Kỳ tới loại |
|---|---|---|---|---|---|---|---|---|---|
| vang20 | ✔ | 1.5 | 80% | 85% | 80% | 79% | 15.0% | ✔ | 26 27 |
| vang25 |  | 0.6 | 90% | 95% | 94% | 91% | 14.1% | ✔ | 26 |
| vang30 |  | 0.3 | 90% | 95% | 96% | 96% | 12.5% | ✔ | 26 |
| thua15 | ✔ | 1.3 | 80% | 90% | 80% | 84% | 12.9% | ✔ | 26 |
| vang1 | ✔ | 1.0 | 100% | 100% | 94% | 89% | 11.0% | ✔ | 26 |
| vang2nd |  | 1.0 | 80% | 85% | 84% | 79% | 21.0% | ✔ | 27 |
| lien2 |  | 0.6 | 80% | 90% | 88% | 89% | 17.5% | ✔ | — |
| nong35 | ✔ | 0.7 | 90% | 95% | 90% | 92% | 11.9% | ✔ | 10 |
| lt3 | ✔ | 0.7 | 100% | 100% | 94% | 92% | 11.0% | ✔ | 33 |
| tx15 | ✔ | 0.5 | 90% | 95% | 96% | 96% | 10.2% | ✔ | 31 |
| tx10 | ✔ | 1.0 | 90% | 90% | 94% | 92% | 10.4% | ✔ | 16 31 |
| nong10 |  | 0.8 | 80% | 70% | 74% | 81% | 23.5% | ✔ | 10 |
| it100 |  | 1.0 | 90% | 90% | 84% | 85% | 15.0% | ✔ | 04 |
| nhieu100 |  | 1.0 | 90% | 90% | 88% | 85% | 15.0% | ✔ | 30 |
| nhip2 | ✔ | 0.6 | 90% | 90% | 92% | 95% | 8.8% | ✔ | — |
| nhipmin100 | ✔ | 1.2 | 80% | 80% | 84% | 86% | 12.8% | ✔ | 31 |
| nhipmin200 |  | 0.3 | 100% | 100% | 98% | 95% | 16.1% | ✔ | — |
| vangph20 |  | 1.6 | 70% | 75% | 76% | 80% | 14.1% | ✔ | 18 26 |
| txph13 | ✔ | 0.5 | 100% | 100% | 94% | 96% | 7.7% | ✔ | — |
| uprev |  | 1.0 | 90% | 85% | 90% | 86% | 14.0% | ✔ | 07 |
| zprev |  | 1.0 | 70% | 80% | 84% | 87% | 13.0% | ✔ | 33 |



# Số May Mắn Loto theo 4 khung (05/10/2026)

## Số May Mắn Loto — chọn 3 số, % kỳ trúng (trung bình 25%)

| Cách chọn | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 100 kỳ trước đó | Kỳ tới |
|---|---|---|---|---|---|---|
| Vắng lâu nhất (đang dùng) | 40% | 35% | 32% | 31% | 28% | 06 01 10 |
| Vắng ngắn nhất (vừa ra) | 0% | 10% | 22% | 23% | 23% | 02 04 07 |
| MM kỳ trước + 2 vắng lâu nhất | 30% | 30% | 32% | 32% | 27% | 02 06 01 |
| Nóng 10 kỳ | 20% | 20% | 26% | 27% | 20% | 02 08 03 |
| Nóng 20 kỳ | 30% | 15% | 26% | 28% | 20% | 05 03 08 |
| Nóng 50 kỳ | 20% | 15% | 16% | 23% | 19% | 02 03 04 |
| Nóng 100 kỳ | 40% | 20% | 18% | 24% | 27% | 02 05 07 |
| Lạnh 20 kỳ | 40% | 40% | 34% | 32% | 27% | 06 01 04 |
| Lạnh 50 kỳ | 20% | 25% | 34% | 27% | 21% | 01 07 09 |
| Lạnh 100 kỳ | 20% | 25% | 32% | 27% | 22% | 06 01 04 |
| Vắng lâu nhất cùng phiên (13h/21h) | 20% | 15% | 32% | 24% | 17% | 07 01 12 |
| Nóng 20 kỳ cùng phiên | 30% | 25% | 20% | 20% | 19% | 03 04 02 |
| MM kỳ trước ±1 (3 số) | 10% | 10% | 20% | 22% | 27% | 01 02 03 |
| MM trùng số chính kỳ trước (≤12) | 40% | 35% | 36% | 33% | 22% | 07 06 01 |
| Đuôi số chính kỳ trước (n mod 12) | 40% | 40% | 32% | 28% | 23% | 07 04 06 |
| Tổng kỳ trước mod 12 ±1 | 30% | 25% | 18% | 19% | 23% | 08 09 10 |

- MM lặp lại kỳ trước: 8% ở 100 kỳ (ngẫu nhiên 8,3%)
- Số ra lúc đang vắng bao lâu (100 kỳ): 0–2: 21%, 3–5: 16%, 6–11: 23%, 12–20: 22%, 21–30: 18%
  (ngẫu nhiên: 0–2: 23%, 3–5: 18%, 6–11: 24%, 12–20: 21%, ≥21: 14%)
- Đang vắng: 06: 21, 01: 18, 10: 11, 12: 10, 03: 7, 11: 6, 09: 5, 08: 4, 05: 3, 07: 2, 04: 1, 02: 0
- 10 kỳ gần: 02 08 03 11 09 08 05 07 04 02

Kết luận: "3 số vắng lâu nhất" ổn định nhất (31% ở 100 kỳ, 28% ở 100 kỳ trước đó, trung bình 25%), nên giữ. Chọn 1 số/vé chỉ khoảng 10%/kỳ.


# Số May Mắn Loto — hướng loại và pool rộng (05/10/2026)

## A. LOẠI số May Mắn — % kỳ đúng (số bị loại không về)

| Luật loại | Chia đều | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 100 kỳ trước | Kỳ tới |
|---|---|---|---|---|---|---|---|
| Loại MM vừa ra kỳ trước (1 số) | 92% | 100% | 100% | 94% | 92% | 92% | 02 |
| Loại 2 MM của 2 kỳ gần nhất | 83% | 100% | 90% | 86% | 84% | 87% | 02 04 |
| Loại 3 MM của 3 kỳ gần nhất | 75% | 100% | 90% | 80% | 79% | 77% | 02 04 07 |
| Loại số ra ≥2 lần trong 10 kỳ | 0% | 90% | 85% | 80% | 78% | 86% | 02 08 |
| Loại số ra nhiều nhất 20 kỳ (top 2) | 83% | 90% | 95% | 84% | 84% | 84% | 03 05 |
| Loại số ra nhiều nhất 50 kỳ (top 2) | 83% | 80% | 90% | 90% | 84% | 87% | 02 03 |

## B. POOL số May Mắn — chọn N số xếp theo "vắng lâu nhất", % kỳ trúng

| Pool | Chia đều | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 100 kỳ trước | Kỳ tới |
|---|---|---|---|---|---|---|---|
| 3 số vắng lâu nhất | 25% | 40% | 35% | 32% | 31% | 28% | 01 06 10 |
| 4 số vắng lâu nhất | 33% | 40% | 45% | 42% | 39% | 39% | 01 06 10 12 |
| 5 số vắng lâu nhất | 42% | 60% | 60% | 52% | 47% | 51% | 01 03 06 10 12 |
| 6 số vắng lâu nhất | 50% | 70% | 65% | 62% | 57% | 57% | 01 03 06 10 11 12 |
| 7 số vắng lâu nhất | 58% | 90% | 80% | 70% | 62% | 65% | 01 03 06 09 10 11 12 |
| 8 số vắng lâu nhất | 67% | 90% | 85% | 74% | 71% | 67% | 01 03 06 08 09 10 11 12 |

## C. POOL = bỏ các số vừa ra (3 kỳ gần) → còn lại

| Pool | Chia đều | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 100 kỳ trước | Kỳ tới |
|---|---|---|---|---|---|---|---|
| Bỏ MM 3 kỳ gần → 9 số còn lại | 0% | 100% | 90% | 80% | 79% | 77% | 01 03 05 06 08 09 10 11 12 |


# Max 3D / 3D+ / 3D Pro — luật và xác suất (05/10/2026)

Lịch quay: Max 3D và 3D+ quay thứ 2, 4, 6 lúc 18h; Max 3D Pro quay thứ 3, 5, 7. Mỗi kỳ quay 20 bộ số 000–999: ĐB 2 bộ, Nhất 4, Nhì 6, Ba 8. Giải cố định theo vé 10.000đ, không chia như Jackpot; mua nhiều thì nhân lên. **Trúng hạng cao lĩnh luôn mọi giải tương ứng bên dưới** (anh xác nhận; khớp ca 36 tỷ).

## Max 3D — chọn 1 bộ số, vé 10.000đ

| Hạng | Số bộ | Giải | Xác suất/kỳ | Đóng góp hoàn tiền |
|---|---|---|---|---|
| ĐB | 2 | 1,000,000đ | 0.20% | 20.0% |
| Nhất | 4 | 350,000đ | 0.40% | 14.0% |
| Nhì | 6 | 210,000đ | 0.60% | 12.6% |
| Ba | 8 | 100,000đ | 0.80% | 8.0% |
| **Tổng** | 20 | | **1.98% có giải** (≈1/50 kỳ) | **54.6%** |

## Max 3D+ — chọn 2 bộ số, vé 10.000đ

| Hạng | Điều kiện | Giải | Xác suất/kỳ | Khoảng 1 lần / | Đóng góp hoàn tiền |
|---|---|---|---|---|---|
| ĐB | cả 2 bộ trùng 2 số ĐB | 1,000,000,000đ | 0.00020% | 500,000 kỳ | 20.0% |
| Nhất | cả 2 bộ nằm trong 4 số giải Nhất | 40,000,000đ | 0.00120% | 83,500 kỳ | 4.8% |
| Nhì | cả 2 bộ trong 6 số giải Nhì | 10,000,000đ | 0.00299% | 33,467 kỳ | 3.0% |
| Ba | cả 2 bộ trong 8 số giải Ba | 5,000,000đ | 0.00557% | 17,965 kỳ | 2.8% |
| Tư | cả 2 bộ nằm trong 20 số | 1,000,000đ | 0.03732% | 2,679 kỳ | 3.7% |
| Năm | mỗi bộ trùng 1 số ĐB | 150,000đ | 0.39980% | 250 kỳ | 6.0% |
| Sáu | mỗi bộ trùng 1 số Nhất/Nhì/Ba | 40,000đ | 3.56956% | 28 kỳ | 14.3% |
| **Tổng** | | | **3.92% có giải** | 25 kỳ | **54.6%** |

Vé trúng ĐB thường lĩnh: 1 tỷ + Tư 1 triệu + 2 × Năm 150.000đ = 1.001.300.000đ.

## Max 3D Pro — chọn 2 bộ số, vé 10.000đ

| Hạng | Điều kiện | Giải | Xác suất/kỳ | Khoảng 1 lần / | Đóng góp hoàn tiền |
|---|---|---|---|---|---|
| ĐB (đúng thứ tự) | 2 bộ trùng 2 số ĐB đúng thứ tự quay | 2,000,000,000đ | 0.00010% | 1,000,000 kỳ | 20.0% |
| Phụ ĐB (ngược thứ tự) | 2 bộ trùng 2 số ĐB ngược thứ tự | 400,000,000đ | 0.00010% | 1,000,000 kỳ | 4.0% |
| Nhất | cả 2 bộ nằm trong 4 số giải Nhất | 30,000,000đ | 0.00120% | 83,500 kỳ | 3.6% |
| Nhì | cả 2 bộ trong 6 số giải Nhì | 10,000,000đ | 0.00299% | 33,467 kỳ | 3.0% |
| Ba | cả 2 bộ trong 8 số giải Ba | 4,000,000đ | 0.00557% | 17,965 kỳ | 2.2% |
| Tư | cả 2 bộ nằm trong 20 số | 1,000,000đ | 0.03732% | 2,679 kỳ | 3.7% |
| Năm | mỗi bộ trùng 1 số ĐB | 100,000đ | 0.39980% | 250 kỳ | 4.0% |
| Sáu | mỗi bộ trùng 1 số Nhất/Nhì/Ba | 40,000đ | 3.56956% | 28 kỳ | 14.3% |
| **Tổng** | | | **3.92% có giải** | 25 kỳ | **54.8%** |

Vé trúng ĐB thường lĩnh: 2 tỷ + Tư 1 triệu + 2 × Năm 100.000đ = 2.001.200.000đ. Kiểm ca 36 tỷ: 15 × 2 tỷ + 15 × 400 triệu + 30 × 1 triệu + 60 × 100.000đ = 36.036.000.000đ (+ 1 giải Sáu 40.000đ = 36.036.040.000đ, khớp báo chí).

Chưa có dữ liệu kết quả Max 3D trong repo — cần anh tải CSV lên để dò dấu vết theo từng hàng trăm/chục/đơn vị.

## Max 3D — cách quay (anh xác nhận 05/10/2026)
- Max 3D, 3D+ và 3D Pro quay bằng **bi vật lý trong lồng quay khí nén**. Mỗi bộ số quay **lần lượt từng chữ số**: hàng trăm → chục → đơn vị.
- Hệ quả: mỗi kỳ có 60 lần quay chữ số 0–9. Dấu vết nằm ở **từng viên bi chữ số**. Một bộ số nặng hay nhẹ là tích độ nặng của 3 chữ số; ví dụ chữ số nặng 11% thay vì 10% thì bộ 3 chữ số đó có khả năng ×1,33.
- Áp nguyên tắc như Power/Mega: họ thay bi định kỳ, nên chỉ xét tối đa 100 kỳ và so 4 khung 10/20/50/100.
- Công cụ `build/max3d_dauvet.py` (thử với `--thu` trên dữ liệu giả lập: bi lệch ±10%, thay bi mỗi 20 kỳ). Script nhận ra đúng "1 bộ bi dùng chung" và "dấu vết giữ lại ở khung 20–50 kỳ"; 3 chữ số nặng nhất trúng khoảng 30–31,5% (chia đều 30%).


# Max 3D — dò dấu vết bi trên dữ liệu thật (05/10/2026)

Nguồn: github.com/vietvudanh/vietlott-data (crawl hằng ngày từ vietlott.vn). Đối chiếu Power 6/55 của nguồn này với dữ liệu của anh: 1001/1001 kỳ khớp. Max 3D: 1136 kỳ (22/04/2019 → 02/10/2026); Max 3D Pro: 783 kỳ (14/09/2021 → 03/10/2026); mỗi loại thiếu 4 kỳ (nghỉ Tết).

Kỳ có bộ số trùng nhau trong 20 bộ: Max 3D 19,2%, Pro 17,8% (lý thuyết quay từng chữ số có trả bi: 17,3%). Khớp với cách quay từng chữ số anh nói.

## Max 3D — 1136 kỳ (22/04/2019 → 02/10/2026)

### 1. Tỉ lệ ra từng chữ số (chia đều 10%) — cả 3 hàng

| Chữ số | 10 kỳ gần | 20 kỳ gần | 50 kỳ gần | 100 kỳ gần | 100 kỳ trước đó |
|---|---|---|---|---|---|
| 0 | 11.8% | 10.8% | 10.4% | 9.8% | 10.4% |
| 1 | 9.7% | 10.2% | 9.7% | 10.3% | 9.9% |
| 2 | 7.7% | 9.2% | 9.3% | 9.4% | 10.6% |
| 3 | 10.0% | 9.8% | 10.7% | 10.2% | 9.8% |
| 4 | 12.2% | 10.0% | 9.6% | 9.9% | 9.9% |
| 5 | 9.5% | 9.8% | 9.8% | 9.3% | 10.5% |
| 6 | 10.3% | 9.8% | 9.9% | 10.7% | 9.9% |
| 7 | 8.5% | 10.4% | 10.0% | 9.9% | 9.4% |
| 8 | 9.3% | 10.3% | 10.5% | 10.4% | 9.7% |
| 9 | 11.0% | 9.7% | 10.2% | 10.1% | 9.8% |

### 2. Một lồng hay ba lồng? Độ lệch chữ số giữa các hàng (100 kỳ gần)

- Hàng trăm: 0:10.2 1:11.3 2:8.8 3:10.0 4:9.5 5:10.1 6:10.2 7:9.6 8:10.6 9:9.7
- Hàng chục: 0:9.5 1:9.4 2:11.2 3:9.8 4:10.1 5:8.8 6:10.8 7:9.4 8:10.8 9:10.2
- Hàng đơn vị: 0:9.8 1:10.2 2:8.2 3:10.8 4:10.0 5:9.1 6:10.8 7:10.7 8:10.0 9:10.4
- Tương quan độ lệch giữa 3 hàng, TB các khối 20 kỳ trên toàn bộ 1136 kỳ: **-0.031** (quay ngẫu nhiên: -0.043 … +0.047)
  → không cùng chiều rõ — có thể mỗi hàng 1 lồng/bộ bi riêng, hoặc độ lệch quá nhỏ

### 3. Bi vừa ra có ra lại ngay không

- Chữ số lặp lại ở lần quay kế tiếp: **10.5%** (chia đều 10%)

### 4. Dấu vết có giữ không: tương quan tần suất 2 khối W kỳ liền nhau (TB) — so với quay ngẫu nhiên

| Khung W | Thực tế | Quay ngẫu nhiên (10 lần thử: thấp nhất … cao nhất) | Nhận xét |
|---|---|---|---|
| 10 | +0.032 | -0.072 … +0.052 | trong vùng ngẫu nhiên |
| 20 | +0.084 | -0.110 … +0.135 | trong vùng ngẫu nhiên |
| 50 | +0.106 | -0.076 … +0.126 | trong vùng ngẫu nhiên |
| 100 | +0.174 | -0.206 … +0.357 | trong vùng ngẫu nhiên |

### 5. 3 chữ số nặng nhất của khung W → tỉ lệ ra ở kỳ kế (chia đều 30%), chấm 300 kỳ gần chia 3 đoạn

| Khung | Đoạn gần | Đoạn giữa | Đoạn xa |
|---|---|---|---|
| 10 kỳ | 30.0% | 29.9% | 30.4% |
| 20 kỳ | 30.1% | 29.6% | 30.5% |
| 50 kỳ | 30.1% | 30.0% | 29.4% |
| 100 kỳ | 29.2% | 31.3% | 30.4% |

### 6. Theo từng hàng: 3 chữ số nặng nhất của hàng (khung W) → % ra ở hàng đó kỳ kế (chia đều 30%)

| Khung | Đoạn gần | Đoạn giữa | Đoạn xa |
|---|---|---|---|
| 10 kỳ | 31.5% | 30.7% | 29.7% |
| 20 kỳ | 31.6% | 30.7% | 29.5% |
| 50 kỳ | 30.4% | 31.4% | 30.0% |
| 100 kỳ | 29.9% | 32.0% | 30.1% |

### 7. Theo từng hàng: 3 chữ số NHẸ nhất của hàng (khung W) → % ra kỳ kế (chia đều 30%)

| Khung | Đoạn gần | Đoạn giữa | Đoạn xa |
|---|---|---|---|
| 10 kỳ | 29.7% | 30.0% | 31.2% |
| 20 kỳ | 29.5% | 29.7% | 30.2% |
| 50 kỳ | 30.0% | 29.3% | 29.4% |
| 100 kỳ | 29.3% | 27.9% | 29.2% |

## Max 3D Pro

## Max 3D — 783 kỳ (14/09/2021 → 03/10/2026)

### 1. Tỉ lệ ra từng chữ số (chia đều 10%) — cả 3 hàng

| Chữ số | 10 kỳ gần | 20 kỳ gần | 50 kỳ gần | 100 kỳ gần | 100 kỳ trước đó |
|---|---|---|---|---|---|
| 0 | 11.3% | 10.9% | 10.3% | 10.3% | 9.9% |
| 1 | 9.0% | 8.8% | 9.8% | 9.9% | 10.6% |
| 2 | 8.7% | 8.8% | 9.7% | 9.9% | 9.7% |
| 3 | 10.7% | 9.8% | 10.5% | 10.3% | 10.0% |
| 4 | 7.7% | 9.7% | 10.1% | 10.0% | 9.8% |
| 5 | 9.7% | 10.3% | 9.7% | 10.0% | 9.7% |
| 6 | 8.7% | 10.1% | 10.0% | 9.9% | 10.6% |
| 7 | 10.3% | 9.8% | 9.7% | 9.9% | 10.1% |
| 8 | 13.0% | 11.8% | 10.3% | 10.1% | 9.9% |
| 9 | 11.0% | 10.1% | 9.9% | 9.7% | 9.7% |

### 2. Một lồng hay ba lồng? Độ lệch chữ số giữa các hàng (100 kỳ gần)

- Hàng trăm: 0:10.9 1:9.3 2:9.8 3:10.2 4:9.7 5:10.3 6:9.4 7:10.0 8:10.1 9:10.3
- Hàng chục: 0:9.5 1:10.8 2:10.2 3:10.5 4:10.0 5:9.6 6:10.0 7:9.6 8:9.4 9:10.5
- Hàng đơn vị: 0:10.4 1:9.6 2:9.7 3:10.3 4:10.4 5:10.1 6:10.3 7:10.2 8:10.7 9:8.2
- Tương quan độ lệch giữa 3 hàng, TB các khối 20 kỳ trên toàn bộ 783 kỳ: **-0.030** (quay ngẫu nhiên: -0.059 … +0.045)
  → không cùng chiều rõ — có thể mỗi hàng 1 lồng/bộ bi riêng, hoặc độ lệch quá nhỏ

### 3. Bi vừa ra có ra lại ngay không

- Chữ số lặp lại ở lần quay kế tiếp: **9.7%** (chia đều 10%)

### 4. Dấu vết có giữ không: tương quan tần suất 2 khối W kỳ liền nhau (TB) — so với quay ngẫu nhiên

| Khung W | Thực tế | Quay ngẫu nhiên (10 lần thử: thấp nhất … cao nhất) | Nhận xét |
|---|---|---|---|
| 10 | -0.007 | -0.084 … +0.115 | trong vùng ngẫu nhiên |
| 20 | -0.126 | -0.119 … +0.204 | ngược chiều |
| 50 | +0.104 | -0.156 … +0.101 | **có dấu vết giữ lại** |
| 100 | +0.244 | -0.202 … +0.253 | trong vùng ngẫu nhiên |

### 5. 3 chữ số nặng nhất của khung W → tỉ lệ ra ở kỳ kế (chia đều 30%), chấm 300 kỳ gần chia 3 đoạn

| Khung | Đoạn gần | Đoạn giữa | Đoạn xa |
|---|---|---|---|
| 10 kỳ | 29.7% | 30.9% | 29.8% |
| 20 kỳ | 29.8% | 30.4% | 29.8% |
| 50 kỳ | 28.5% | 30.7% | 29.6% |
| 100 kỳ | 29.7% | 30.7% | 30.5% |

### 6. Theo từng hàng: 3 chữ số nặng nhất của hàng (khung W) → % ra ở hàng đó kỳ kế (chia đều 30%)

| Khung | Đoạn gần | Đoạn giữa | Đoạn xa |
|---|---|---|---|
| 10 kỳ | 30.1% | 30.6% | 29.7% |
| 20 kỳ | 29.3% | 30.7% | 29.2% |
| 50 kỳ | 29.4% | 30.8% | 28.8% |
| 100 kỳ | 29.6% | 30.6% | 30.2% |

### 7. Theo từng hàng: 3 chữ số NHẸ nhất của hàng (khung W) → % ra kỳ kế (chia đều 30%)

| Khung | Đoạn gần | Đoạn giữa | Đoạn xa |
|---|---|---|---|
| 10 kỳ | 30.2% | 31.4% | 29.7% |
| 20 kỳ | 30.1% | 30.0% | 29.5% |
| 50 kỳ | 30.6% | 29.4% | 30.2% |
| 100 kỳ | 30.6% | 29.0% | 29.4% |


# Max 3D+ — suy luận theo nhóm bộ số (05/10/2026)

## max3d_data.json — 1136 kỳ (22/04/2019 → 02/10/2026). Mỗi bộ ra ≥1 lần/kỳ: chia đều 1.98%

| Nhóm bộ số | Cỡ TB | Đoạn 1 (gần) | Đoạn 2 | Đoạn 3 | Kết luận | Kỳ tới |
|---|---|---|---|---|---|---|
| Bộ vừa ra kỳ trước | 20 | 1.66% (×0.84) | 1.46% (×0.74) | 2.17% (×1.09) | — | 20 bộ |
| Bộ ra trong 10 kỳ gần | 182 | 1.95% (×0.98) | 1.95% (×0.99) | 1.99% (×1.01) | — | 177 bộ |
| Bộ ra ≥2 lần trong 50 kỳ | 261 | 2.16% (×1.09) | 1.97% (×1.00) | 1.81% (×0.92) | — | 260 bộ |
| Bộ vắng ≥100 kỳ | 131 | 2.09% (×1.05) | 2.19% (×1.10) | 1.89% (×0.95) | — | 141 bộ |
| Giải ĐB kỳ trước | 2 | 1.50% (×0.76) | 0.50% (×0.25) | 2.50% (×1.26) | — | 357 728 |
| Lộn (đảo chữ số) của bộ kỳ trước | 78 | 1.77% (×0.89) | 2.02% (×1.02) | 1.85% (×0.93) | — | 85 bộ |
| Bộ ±1 của bộ kỳ trước | 39 | 2.29% (×1.16) | 2.11% (×1.07) | 1.56% (×0.79) | — | 39 bộ |
| Tam hoa (aaa) | 10 | 2.30% (×1.16) | 2.30% (×1.16) | 1.60% (×0.81) | — | 10 bộ |
| Có 2 chữ số giống nhau (aab, aba, baa) | 270 | 2.02% (×1.02) | 1.97% (×0.99) | 1.97% (×0.99) | — | 270 bộ |
| 100 bộ NẶNG nhất (chữ số theo hàng, 100 kỳ) | 100 | 1.94% (×0.98) | 2.13% (×1.08) | 2.06% (×1.04) | — | 100 bộ |
| 100 bộ NHẸ nhất (chữ số theo hàng, 100 kỳ) | 100 | 1.89% (×0.95) | 1.79% (×0.90) | 1.94% (×0.98) | — | 100 bộ |
| 343 bộ tránh 3 chữ số nhẹ mỗi hàng (100 kỳ) | 343 | 1.99% (×1.00) | 2.16% (×1.09) | 2.01% (×1.01) | — | 343 bộ |
| 100 bộ NẶNG nhất (20 kỳ) | 100 | 2.27% (×1.15) | 2.08% (×1.05) | 1.95% (×0.98) | — | 100 bộ |
| 100 bộ NẶNG nhất (50 kỳ) | 100 | 2.16% (×1.09) | 2.28% (×1.15) | 2.01% (×1.01) | — | 100 bộ |

Độ nhiễu: nhóm 100 bộ, mỗi đoạn 100 kỳ ±0,14 điểm (≈ ×0,93–1,07) là bình thường. Không nhóm nào lệch đều 3/3 đoạn quá mức nhiễu. Nghiêng cùng chiều: bộ NẶNG 50 kỳ (×1,09 · 1,15 · 1,01), bộ NHẸ 100 kỳ (×0,95 · 0,90 · 0,98).


# Max 3D+ / Pro — 6 chữ số của 2 bộ ĐB: biến thiên và thu hẹp khoảng (05/10/2026)

## max3d_data.json — 6 chữ số của 2 bộ ĐB, 1136 kỳ (22/04/2019 → 02/10/2026)

### Biến thiên từng vị trí (300 kỳ gần)

| Vị trí | TB | Đổi so với kỳ trước: giữ nguyên · ±1 · ±2–3 · ±4–5 (vòng) | Chữ số ra nhiều nhất / ít nhất 100 kỳ |
|---|---|---|---|
| Bộ 1 · trăm | 4.63 | 14% · 17% · 39% · 30% (chia đều 10 · 20 · 40 · 30) | 1 (13 lần) / 6 (7 lần) |
| Bộ 1 · chục | 4.68 | 11% · 24% · 36% · 29% (chia đều 10 · 20 · 40 · 30) | 6 (19 lần) / 4 (5 lần) |
| Bộ 1 · đơn vị | 4.56 | 9% · 20% · 44% · 28% (chia đều 10 · 20 · 40 · 30) | 8 (16 lần) / 2 (5 lần) |
| Bộ 2 · trăm | 4.51 | 8% · 21% · 46% · 25% (chia đều 10 · 20 · 40 · 30) | 6 (13 lần) / 1 (7 lần) |
| Bộ 2 · chục | 4.31 | 10% · 22% · 38% · 30% (chia đều 10 · 20 · 40 · 30) | 3 (16 lần) / 5 (4 lần) |
| Bộ 2 · đơn vị | 4.76 | 8% · 20% · 48% · 23% (chia đều 10 · 20 · 40 · 30) | 8 (21 lần) / 2 (3 lần) |

### Khoảng 5 chữ số — % kỳ chữ số rơi vào khoảng (chia đều 50%), TB 6 vị trí · từng đoạn gần → xa

| Cách thu hẹp | Đoạn 1 | Đoạn 2 | Đoạn 3 | Tệ nhất / tốt nhất trong 6 vị trí (đoạn 1) |
|---|---|---|---|---|
| Nhiều nhất ở chính vị trí, 20 kỳ | 53.0% | 49.7% | 51.5% | 50% / 60% |
| Nhiều nhất ở chính vị trí, 50 kỳ | 53.7% | 49.8% | 52.2% | 49% / 57% |
| Nhiều nhất ở chính vị trí, 100 kỳ | 51.8% | 49.3% | 51.7% | 42% / 61% |
| Nhiều nhất cả hàng (20 bộ), 20 kỳ | 53.7% | 52.5% | 52.3% | 42% / 66% |
| Nhiều nhất cả hàng (20 bộ), 50 kỳ | 53.5% | 50.7% | 50.0% | 51% / 59% |
| Nhiều nhất cả hàng (20 bộ), 100 kỳ | 50.0% | 50.0% | 49.7% | 46% / 55% |
| Quanh chữ số kỳ trước (vòng) | 52.5% | 47.3% | 52.7% | 44% / 58% |
| Quanh chữ số kỳ trước (khoảng liền) | 50.2% | 46.7% | 51.8% | 46% / 55% |
| Quanh trung vị 10 kỳ | 50.8% | 46.8% | 49.3% | 46% / 58% |
| Bỏ chữ số kỳ trước + ít nhất 20 kỳ | 54.3% | 52.3% | 51.2% | 46% / 65% |

### Khoảng 7 chữ số — % kỳ chữ số rơi vào khoảng (chia đều 70%), TB 6 vị trí · từng đoạn gần → xa

| Cách thu hẹp | Đoạn 1 | Đoạn 2 | Đoạn 3 | Tệ nhất / tốt nhất trong 6 vị trí (đoạn 1) |
|---|---|---|---|---|
| Nhiều nhất ở chính vị trí, 20 kỳ | 72.8% | 68.2% | 69.0% | 64% / 81% |
| Nhiều nhất ở chính vị trí, 50 kỳ | 70.8% | 68.3% | 71.3% | 66% / 74% |
| Nhiều nhất ở chính vị trí, 100 kỳ | 70.2% | 69.2% | 71.3% | 61% / 78% |
| Nhiều nhất cả hàng (20 bộ), 20 kỳ | 70.7% | 70.2% | 72.5% | 63% / 77% |
| Nhiều nhất cả hàng (20 bộ), 50 kỳ | 69.3% | 71.8% | 70.2% | 61% / 76% |
| Nhiều nhất cả hàng (20 bộ), 100 kỳ | 71.8% | 72.2% | 69.5% | 68% / 76% |
| Quanh chữ số kỳ trước (vòng) | 73.0% | 72.7% | 71.8% | 65% / 82% |
| Quanh chữ số kỳ trước (khoảng liền) | 68.8% | 68.7% | 71.7% | 62% / 72% |
| Quanh trung vị 10 kỳ | 71.3% | 68.8% | 68.3% | 66% / 77% |
| Bỏ chữ số kỳ trước + ít nhất 20 kỳ | 72.0% | 70.8% | 67.8% | 68% / 81% |

## max3dpro_data.json — 6 chữ số của 2 bộ ĐB, 783 kỳ (14/09/2021 → 03/10/2026)

### Biến thiên từng vị trí (300 kỳ gần)

| Vị trí | TB | Đổi so với kỳ trước: giữ nguyên · ±1 · ±2–3 · ±4–5 (vòng) | Chữ số ra nhiều nhất / ít nhất 100 kỳ |
|---|---|---|---|
| Bộ 1 · trăm | 4.70 | 10% · 18% · 37% · 34% (chia đều 10 · 20 · 40 · 30) | 9 (15 lần) / 1 (3 lần) |
| Bộ 1 · chục | 4.41 | 7% · 17% · 41% · 35% (chia đều 10 · 20 · 40 · 30) | 8 (15 lần) / 2 (4 lần) |
| Bộ 1 · đơn vị | 4.61 | 10% · 21% · 39% · 30% (chia đều 10 · 20 · 40 · 30) | 7 (17 lần) / 2 (6 lần) |
| Bộ 2 · trăm | 4.47 | 11% · 20% · 40% · 30% (chia đều 10 · 20 · 40 · 30) | 8 (15 lần) / 6 (6 lần) |
| Bộ 2 · chục | 4.87 | 12% · 23% · 31% · 34% (chia đều 10 · 20 · 40 · 30) | 9 (18 lần) / 1 (5 lần) |
| Bộ 2 · đơn vị | 4.48 | 12% · 17% · 40% · 31% (chia đều 10 · 20 · 40 · 30) | 6 (19 lần) / 2 (6 lần) |

### Khoảng 5 chữ số — % kỳ chữ số rơi vào khoảng (chia đều 50%), TB 6 vị trí · từng đoạn gần → xa

| Cách thu hẹp | Đoạn 1 | Đoạn 2 | Đoạn 3 | Tệ nhất / tốt nhất trong 6 vị trí (đoạn 1) |
|---|---|---|---|---|
| Nhiều nhất ở chính vị trí, 20 kỳ | 52.2% | 47.0% | 49.5% | 47% / 59% |
| Nhiều nhất ở chính vị trí, 50 kỳ | 51.8% | 46.8% | 50.2% | 42% / 58% |
| Nhiều nhất ở chính vị trí, 100 kỳ | 52.3% | 50.3% | 48.8% | 45% / 57% |
| Nhiều nhất cả hàng (20 bộ), 20 kỳ | 49.5% | 48.5% | 48.5% | 42% / 55% |
| Nhiều nhất cả hàng (20 bộ), 50 kỳ | 51.2% | 48.8% | 44.8% | 44% / 59% |
| Nhiều nhất cả hàng (20 bộ), 100 kỳ | 53.0% | 52.3% | 48.7% | 48% / 61% |
| Quanh chữ số kỳ trước (vòng) | 48.3% | 48.7% | 46.5% | 42% / 53% |
| Quanh chữ số kỳ trước (khoảng liền) | 52.0% | 47.3% | 46.3% | 46% / 59% |
| Quanh trung vị 10 kỳ | 50.5% | 51.0% | 49.0% | 44% / 61% |
| Bỏ chữ số kỳ trước + ít nhất 20 kỳ | 54.2% | 48.3% | 47.7% | 48% / 63% |

### Khoảng 7 chữ số — % kỳ chữ số rơi vào khoảng (chia đều 70%), TB 6 vị trí · từng đoạn gần → xa

| Cách thu hẹp | Đoạn 1 | Đoạn 2 | Đoạn 3 | Tệ nhất / tốt nhất trong 6 vị trí (đoạn 1) |
|---|---|---|---|---|
| Nhiều nhất ở chính vị trí, 20 kỳ | 71.7% | 67.8% | 70.5% | 67% / 75% |
| Nhiều nhất ở chính vị trí, 50 kỳ | 69.5% | 67.3% | 68.3% | 66% / 72% |
| Nhiều nhất ở chính vị trí, 100 kỳ | 71.3% | 69.2% | 69.7% | 66% / 76% |
| Nhiều nhất cả hàng (20 bộ), 20 kỳ | 70.5% | 70.0% | 70.8% | 63% / 78% |
| Nhiều nhất cả hàng (20 bộ), 50 kỳ | 71.5% | 68.8% | 66.5% | 65% / 77% |
| Nhiều nhất cả hàng (20 bộ), 100 kỳ | 69.5% | 67.3% | 68.8% | 65% / 76% |
| Quanh chữ số kỳ trước (vòng) | 70.7% | 68.2% | 64.3% | 66% / 79% |
| Quanh chữ số kỳ trước (khoảng liền) | 74.2% | 69.0% | 66.2% | 69% / 79% |
| Quanh trung vị 10 kỳ | 70.2% | 69.7% | 70.7% | 64% / 78% |
| Bỏ chữ số kỳ trước + ít nhất 20 kỳ | 71.0% | 70.3% | 69.3% | 65% / 75% |

Độ nhiễu: TB 6 vị trí × 100 kỳ, ±2 điểm là bình thường. Max 3D+: "nhiều nhất cả hàng (20 bộ), 20 kỳ" khoảng 5 chữ số trúng 53,7 · 52,5 · 52,3% (chia đều 50%), cả 3 đoạn trên mức. Nếu cả 6 vị trí cùng nghiêng như vậy: 5^6 = 15.625 cặp bộ số (1,6% của 1 triệu cặp) chứa cặp ĐB khoảng 2,2% số kỳ (×1,4). Pro: chưa có cách nào ổn định.


# Max 3D / Pro — quan hệ 20 bộ trong 1 kỳ, so với các kỳ trước ≤50 kỳ (05/10/2026)

## max3d_data.json — quan hệ 20 bộ trong kỳ, 300 kỳ gần (21/10/2024 → 02/10/2026)

| Chỉ số | Thực tế | Quay ngẫu nhiên: TB (khoảng 90%) | Nhận xét |
|---|---|---|---|
| Chữ số ra nhiều nhất trong 20 (TB, mỗi hàng) | +4.456 | +4.407 (+4.362 … +4.466) | trong vùng ngẫu nhiên |
| Độ dao động số chữ số nhỏ 0–4 giữa các kỳ (độ lệch chuẩn) | +2.135 | +2.236 (+2.173 … +2.310) | **thấp hơn ngẫu nhiên** |
| Tương quan nhỏ/lớn giữa 3 hàng cùng kỳ | +0.031 | +0.001 (-0.044 … +0.057) | trong vùng ngẫu nhiên |
| Trong kỳ: 10 bộ đầu ↔ 10 bộ sau (tương quan chữ số) | +0.016 | -0.001 (-0.019 … +0.022) | trong vùng ngẫu nhiên |
| Kỳ này ↔ TB 1 kỳ trước (tương quan chữ số mỗi hàng) | -0.014 | -0.000 (-0.019 … +0.017) | trong vùng ngẫu nhiên |
| Kỳ này ↔ TB 5 kỳ trước (tương quan chữ số mỗi hàng) | -0.017 | -0.001 (-0.022 … +0.021) | trong vùng ngẫu nhiên |
| Kỳ này ↔ TB 10 kỳ trước (tương quan chữ số mỗi hàng) | +0.004 | -0.001 (-0.019 … +0.015) | trong vùng ngẫu nhiên |
| Kỳ này ↔ TB 20 kỳ trước (tương quan chữ số mỗi hàng) | +0.019 | +0.000 (-0.015 … +0.017) | **cao hơn ngẫu nhiên** |
| Kỳ này ↔ TB 50 kỳ trước (tương quan chữ số mỗi hàng) | +0.025 | +0.001 (-0.017 … +0.020) | **cao hơn ngẫu nhiên** |
| Nhỏ/lớn: kỳ này ↔ kỳ trước (tương quan) | -0.026 | -0.002 (-0.056 … +0.055) | trong vùng ngẫu nhiên |
| Chẵn/lẻ: kỳ này ↔ kỳ trước (tương quan) | -0.017 | -0.005 (-0.060 … +0.059) | trong vùng ngẫu nhiên |

### Tỉ lệ ra từng chữ số theo hàng: kỳ gần nhất (02/10/2026) so với các kỳ trước (chia đều 10%)

**Hàng trăm**

| Khung | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| Kỳ gần nhất | **20** | 5 | **15** | **20** | 5 | 10 | 0 | **15** | 10 | 0 |
| 5 kỳ | 11 | 10 | 11 | 10 | 12 | 9 | 6 | 8 | 10 | **13** |
| 10 kỳ | 10 | 10 | 8 | 10 | 12 | 11 | 8 | 6 | **13** | 12 |
| 20 kỳ | 11 | 10 | 10 | 11 | 10 | 11 | 8 | 9 | 11 | 9 |
| 50 kỳ | 10 | 10 | 8 | 11 | 9 | 11 | 9 | 9 | 12 | 10 |

**Hàng chục**

| Khung | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| Kỳ gần nhất | 5 | 0 | **15** | **20** | **15** | 5 | 10 | 10 | 5 | **15** |
| 5 kỳ | 9 | 8 | 10 | **13** | 11 | 10 | 12 | 8 | 5 | **14** |
| 10 kỳ | 11 | 8 | 7 | 12 | **14** | 7 | **14** | 10 | 6 | 12 |
| 20 kỳ | 10 | 10 | 8 | 10 | 10 | 9 | 12 | 10 | 10 | 10 |
| 50 kỳ | 10 | 9 | 10 | 9 | 10 | 8 | 11 | 10 | 10 | 11 |

**Hàng đơn vị**

| Khung | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| Kỳ gần nhất | 10 | 10 | 0 | 5 | 10 | **20** | **15** | 10 | 5 | **15** |
| 5 kỳ | 12 | 9 | 8 | 6 | 10 | **13** | 10 | **13** | 7 | 12 |
| 10 kỳ | **14** | 10 | 8 | 8 | 12 | 10 | 10 | 10 | 9 | 9 |
| 20 kỳ | 12 | 10 | 10 | 8 | 10 | 9 | 8 | 12 | 10 | 10 |
| 50 kỳ | 10 | 10 | 9 | 12 | 10 | 10 | 10 | 11 | 10 | 9 |


## max3dpro_data.json — quan hệ 20 bộ trong kỳ, 300 kỳ gần (22/10/2024 → 03/10/2026)

| Chỉ số | Thực tế | Quay ngẫu nhiên: TB (khoảng 90%) | Nhận xét |
|---|---|---|---|
| Chữ số ra nhiều nhất trong 20 (TB, mỗi hàng) | +4.399 | +4.407 (+4.362 … +4.466) | trong vùng ngẫu nhiên |
| Độ dao động số chữ số nhỏ 0–4 giữa các kỳ (độ lệch chuẩn) | +2.246 | +2.236 (+2.173 … +2.310) | trong vùng ngẫu nhiên |
| Tương quan nhỏ/lớn giữa 3 hàng cùng kỳ | +0.015 | +0.001 (-0.044 … +0.057) | trong vùng ngẫu nhiên |
| Trong kỳ: 10 bộ đầu ↔ 10 bộ sau (tương quan chữ số) | +0.010 | -0.001 (-0.019 … +0.022) | trong vùng ngẫu nhiên |
| Kỳ này ↔ TB 1 kỳ trước (tương quan chữ số mỗi hàng) | -0.009 | -0.000 (-0.019 … +0.017) | trong vùng ngẫu nhiên |
| Kỳ này ↔ TB 5 kỳ trước (tương quan chữ số mỗi hàng) | -0.017 | -0.001 (-0.022 … +0.021) | trong vùng ngẫu nhiên |
| Kỳ này ↔ TB 10 kỳ trước (tương quan chữ số mỗi hàng) | -0.005 | -0.001 (-0.019 … +0.015) | trong vùng ngẫu nhiên |
| Kỳ này ↔ TB 20 kỳ trước (tương quan chữ số mỗi hàng) | +0.000 | +0.000 (-0.015 … +0.017) | trong vùng ngẫu nhiên |
| Kỳ này ↔ TB 50 kỳ trước (tương quan chữ số mỗi hàng) | -0.006 | +0.001 (-0.017 … +0.020) | trong vùng ngẫu nhiên |
| Nhỏ/lớn: kỳ này ↔ kỳ trước (tương quan) | -0.050 | -0.002 (-0.056 … +0.055) | trong vùng ngẫu nhiên |
| Chẵn/lẻ: kỳ này ↔ kỳ trước (tương quan) | +0.024 | -0.005 (-0.060 … +0.059) | trong vùng ngẫu nhiên |


Kết luận: trong 1 kỳ không thấy bi nghiêng về phía nào (dồn chữ số, nhỏ/lớn, 3 hàng cùng phía, 10 bộ đầu ↔ 10 bộ sau đều như quay đều). Max 3D: tần suất chữ số mỗi hàng giữ lại nhẹ ở khung 20 và 50 kỳ (vượt khoảng ngẫu nhiên); khung 1–10 kỳ không có. Pro: không có.


# Max 3D / Pro — khoảng nghỉ (05/10/2026)

## Max 3D

### A. Chữ số theo hàng (20 bộ) — tỉ lệ chiếm trong 20 lần quay kỳ kế (chia đều 10%)

| Đang vắng | Cỡ TB/kỳ | Đoạn 1 (gần) | Đoạn 2 | Đoạn 3 | Nhận xét |
|---|---|---|---|---|---|
| 0 (vừa ra kỳ trước) | 525.1 | 10.03% | 10.06% | 9.92% | — |
| 1 kỳ | 65.5 | 9.81% | 9.38% | 10.71% | — |
| 2 kỳ | 8.3 | 9.59% | 10.47% | 8.97% | — |
| ≥3 kỳ | 1.1 | 9.00% | 11.67% | 9.17% | — |

(Cỡ TB/kỳ ở bảng A tính theo lần quay: 20 lần × số chữ số trong nhóm × 3 hàng.)

### B. 6 vị trí của 2 bộ ĐB — % ra ở vị trí đó kỳ kế (chia đều 10%)

| Đang vắng | Cỡ TB/kỳ | Đoạn 1 (gần) | Đoạn 2 | Đoạn 3 | Nhận xét |
|---|---|---|---|---|---|
| 0–4 kỳ | 24.4 | 10.70% | 9.92% | 10.07% | — |
| 5–9 kỳ | 14.2 | 10.46% | 10.64% | 9.52% | — |
| 10–19 kỳ | 13.7 | 9.25% | 9.67% | 9.40% | ▼ ít hơn 3/3 |
| 20–29 kỳ | 4.8 | 8.52% | 10.04% | 11.86% | — |
| ≥30 kỳ | 2.9 | 8.53% | 8.93% | 12.92% | — |

### C. Bộ số — % ra kỳ kế (chia đều 1,98%)

| Đang vắng | Cỡ TB/kỳ | Đoạn 1 (gần) | Đoạn 2 | Đoạn 3 | Nhận xét |
|---|---|---|---|---|---|
| 0 (vừa ra) | 19.8 | 1.66% | 1.46% | 2.17% | — |
| 1–9 kỳ | 161.8 | 1.98% | 2.01% | 1.97% | — |
| 10–49 kỳ | 450.8 | 1.99% | 1.99% | 1.95% | — |
| 50–99 kỳ | 236.3 | 1.95% | 1.87% | 2.10% | — |
| 100–199 kỳ | 111.6 | 2.10% | 2.24% | 1.99% | — |
| ≥200 kỳ | 19.7 | 2.01% | 1.86% | 1.41% | — |

Bộ vắng lâu nhất hiện tại: 378 (575 kỳ), 505 (476 kỳ), 556 (384 kỳ), 243 (318 kỳ), 910 (289 kỳ), 725 (241 kỳ), 533 (237 kỳ), 861 (229 kỳ), 959 (226 kỳ), 042 (220 kỳ)

## Max 3D Pro

### A. Chữ số theo hàng (20 bộ) — tỉ lệ chiếm trong 20 lần quay kỳ kế (chia đều 10%)

| Đang vắng | Cỡ TB/kỳ | Đoạn 1 (gần) | Đoạn 2 | Đoạn 3 | Nhận xét |
|---|---|---|---|---|---|
| 0 (vừa ra kỳ trước) | 526.3 | 10.06% | 9.93% | 10.04% | — |
| 1 kỳ | 63.7 | 9.58% | 10.30% | 9.94% | — |
| 2 kỳ | 8.3 | 9.58% | 11.25% | 8.89% | — |
| ≥3 kỳ | 1.7 | 8.75% | 18.00% | 7.50% | — |

(Cỡ TB/kỳ ở bảng A tính theo lần quay: 20 lần × số chữ số trong nhóm × 3 hàng.)

### B. 6 vị trí của 2 bộ ĐB — % ra ở vị trí đó kỳ kế (chia đều 10%)

| Đang vắng | Cỡ TB/kỳ | Đoạn 1 (gần) | Đoạn 2 | Đoạn 3 | Nhận xét |
|---|---|---|---|---|---|
| 0–4 kỳ | 24.6 | 10.65% | 9.17% | 10.09% | — |
| 5–9 kỳ | 14.6 | 9.76% | 10.36% | 9.13% | — |
| 10–19 kỳ | 13.9 | 9.25% | 9.91% | 10.99% | — |
| 20–29 kỳ | 4.8 | 10.67% | 12.33% | 9.64% | — |
| ≥30 kỳ | 2.1 | 7.91% | 14.39% | 9.21% | — |

### C. Bộ số — % ra kỳ kế (chia đều 1,98%)

| Đang vắng | Cỡ TB/kỳ | Đoạn 1 (gần) | Đoạn 2 | Đoạn 3 | Nhận xét |
|---|---|---|---|---|---|
| 0 (vừa ra) | 19.8 | 1.67% | 1.86% | 1.76% | ▼ ít hơn 3/3 |
| 1–9 kỳ | 162.7 | 1.96% | 1.80% | 1.87% | — |
| 10–49 kỳ | 457.1 | 2.02% | 2.04% | 2.00% | — |
| 50–99 kỳ | 227.0 | 1.97% | 2.06% | 1.94% | — |
| 100–199 kỳ | 117.3 | 1.94% | 1.82% | 2.17% | — |
| ≥200 kỳ | 16.1 | 1.78% | 3.01% | 2.25% | — |

Bộ vắng lâu nhất hiện tại: 028 (374 kỳ), 244 (309 kỳ), 822 (275 kỳ), 359 (268 kỳ), 531 (268 kỳ), 036 (267 kỳ), 815 (264 kỳ), 733 (263 kỳ), 389 (262 kỳ), 091 (261 kỳ)

Luật "không chọn 20 bộ vừa ra kỳ trước": kỳ đúng (không bộ nào lặp lại) Max 3D 71 · 75 · 62%, Pro 69 · 70 · 71% (chia đều 67%). Gộp 2 game, bộ vừa ra lặp lại 1,76% so với 1,98% (nghiêng nhẹ ~−11%). Các mức vắng khác của chữ số và bộ số: không có dấu vết.


# Max 3D / Pro — gộp dấu vết để loại bớt bộ số (05/10/2026)

## max3d_data.json — giữ lại p% bộ điểm cao (gộp dấu vết)

| Cách | Giữ | Bộ trúng nằm trong nhóm giữ (gần · giữa · xa) | Chia đều | Cả 2 ĐB trong nhóm giữ | Chia đều |
|---|---|---|---|---|---|
| Nặng 20 kỳ + bỏ bộ vừa ra | 70% | 71.6% · 70.8% · 70.2% | 70% | 52% · 54% · 49% | 49% |
| Nặng 20 kỳ + bỏ bộ vừa ra | 50% | 52.5% · 50.5% · 49.1% | 50% | 29% · 32% · 26% | 25% |
| Nặng 20 kỳ + bỏ bộ vừa ra | 34% | 36.3% · 34.8% · 31.9% | 34% | 9% · 16% · 10% | 12% |
| Nặng 20 kỳ + bỏ bộ vừa ra | 20% | 21.9% · 20.4% · 19.1% | 20% | 5% · 5% · 2% | 4% |
| Nặng 50 kỳ + bỏ bộ vừa ra | 70% | 71.3% · 71.5% · 70.0% | 70% | 47% · 47% · 46% | 49% |
| Nặng 50 kỳ + bỏ bộ vừa ra | 50% | 50.0% · 50.9% · 51.4% | 50% | 27% · 30% · 33% | 25% |
| Nặng 50 kỳ + bỏ bộ vừa ra | 34% | 34.3% · 36.1% · 35.4% | 34% | 15% · 13% · 13% | 12% |
| Nặng 50 kỳ + bỏ bộ vừa ra | 20% | 21.1% · 21.9% · 19.4% | 20% | 3% · 7% · 1% | 4% |
| Nặng 100 kỳ + bỏ bộ vừa ra | 70% | 70.7% · 72.5% · 70.8% | 70% | 49% · 48% · 49% | 49% |
| Nặng 100 kỳ + bỏ bộ vừa ra | 50% | 50.3% · 52.6% · 51.5% | 50% | 26% · 25% · 21% | 25% |
| Nặng 100 kỳ + bỏ bộ vừa ra | 34% | 34.4% · 37.2% · 35.7% | 34% | 12% · 11% · 14% | 12% |
| Nặng 100 kỳ + bỏ bộ vừa ra | 20% | 20.5% · 22.3% · 19.8% | 20% | 4% · 6% · 3% | 4% |

## max3dpro_data.json — giữ lại p% bộ điểm cao (gộp dấu vết)

| Cách | Giữ | Bộ trúng nằm trong nhóm giữ (gần · giữa · xa) | Chia đều | Cả 2 ĐB trong nhóm giữ | Chia đều |
|---|---|---|---|---|---|
| Nặng 20 kỳ + bỏ bộ vừa ra | 70% | 70.6% · 71.7% · 70.1% | 70% | 52% · 43% · 38% | 49% |
| Nặng 20 kỳ + bỏ bộ vừa ra | 50% | 49.5% · 51.2% · 50.0% | 50% | 26% · 20% · 23% | 25% |
| Nặng 20 kỳ + bỏ bộ vừa ra | 34% | 32.7% · 34.2% · 32.9% | 34% | 12% · 11% · 9% | 12% |
| Nặng 20 kỳ + bỏ bộ vừa ra | 20% | 19.2% · 20.4% · 19.6% | 20% | 2% · 4% · 2% | 4% |
| Nặng 50 kỳ + bỏ bộ vừa ra | 70% | 70.1% · 71.2% · 70.0% | 70% | 50% · 46% · 46% | 49% |
| Nặng 50 kỳ + bỏ bộ vừa ra | 50% | 49.1% · 52.0% · 49.4% | 50% | 29% · 29% · 21% | 25% |
| Nặng 50 kỳ + bỏ bộ vừa ra | 34% | 32.5% · 35.4% · 32.2% | 34% | 17% · 14% · 7% | 12% |
| Nặng 50 kỳ + bỏ bộ vừa ra | 20% | 18.9% · 21.4% · 18.1% | 20% | 7% · 3% · 2% | 4% |
| Nặng 100 kỳ + bỏ bộ vừa ra | 70% | 69.0% · 70.0% · 71.6% | 70% | 55% · 45% · 47% | 49% |
| Nặng 100 kỳ + bỏ bộ vừa ra | 50% | 49.2% · 51.5% · 50.0% | 50% | 31% · 19% · 22% | 25% |
| Nặng 100 kỳ + bỏ bộ vừa ra | 34% | 33.0% · 34.5% · 33.6% | 34% | 18% · 10% · 8% | 12% |
| Nặng 100 kỳ + bỏ bộ vừa ra | 20% | 19.4% · 21.2% · 19.9% | 20% | 5% · 5% · 2% | 4% |

## Max 3D và Pro có dùng chung bi? (5 chữ số nặng nhất mỗi hàng, chia đều 50%)

| Đích | Độ nặng lấy từ | Khung | Đoạn 1 (gần) | Đoạn 2 | Đoạn 3 |
|---|---|---|---|---|---|
| Max 3D | chính nó | 45 ngày (~19 kỳ) | 51.1% | 50.0% | 50.0% |
| Max 3D | game kia | 45 ngày (~19 kỳ) | 49.0% | 50.9% | 51.0% |
| Max 3D | gộp cả 2 | 45 ngày (~19 kỳ) | 50.9% | 50.6% | 50.6% |
| Max 3D | chính nó | 120 ngày (~51 kỳ) | 50.1% | 52.1% | 50.0% |
| Max 3D | game kia | 120 ngày (~51 kỳ) | 50.8% | 50.5% | 50.2% |
| Max 3D | gộp cả 2 | 120 ngày (~51 kỳ) | 50.8% | 51.4% | 50.2% |
| Max 3D Pro | chính nó | 45 ngày (~19 kỳ) | 50.0% | 49.7% | 50.2% |
| Max 3D Pro | game kia | 45 ngày (~19 kỳ) | 50.2% | 50.3% | 50.4% |
| Max 3D Pro | gộp cả 2 | 45 ngày (~19 kỳ) | 49.5% | 49.6% | 49.8% |
| Max 3D Pro | chính nó | 120 ngày (~51 kỳ) | 49.0% | 50.2% | 49.5% |
| Max 3D Pro | game kia | 120 ngày (~51 kỳ) | 50.1% | 50.7% | 49.8% |
| Max 3D Pro | gộp cả 2 | 120 ngày (~51 kỳ) | 49.8% | 50.5% | 49.1% |

Kết luận: Max 3D (3D+) "nặng 50 kỳ + bỏ bộ vừa ra", giữ 34% (340 bộ): bộ trúng 34,3 · 36,1 · 35,4%, cặp ĐB 15 · 13 · 13% (chia đều 12%) — nghiêng nhẹ ổn định. Pro: không. Lấy độ nặng từ game kia hoặc gộp 2 game không giúp → khả năng 2 game dùng máy/bộ bi riêng, hoặc dấu vết quá nhỏ.


# Max 3D / Pro — bộ đã ra 5 / 10 kỳ gần có lặp lại không (05/10/2026)

## Max 3D (3D+) — 1136 kỳ

| Nhóm | Cỡ TB | Mỗi bộ ra kỳ kế (gần · giữa · xa) | Chia đều | Kỳ có ≥1 bộ lặp lại (thực · kỳ vọng) |
|---|---|---|---|---|
| Ra ở kỳ trước | 20 | 1.66% (×0.84) · 1.46% (×0.74) · 2.17% (×1.09) | 1.98% | 31% · 33% |
| Ra trong 2–5 kỳ trước (không tính kỳ trước) | 76 | 1.99% (×1.00) · 1.98% (×1.00) · 2.09% (×1.05) | 1.98% | 80% · 78% |
| Ra trong 6–10 kỳ trước | 86 | 1.97% (×1.00) · 2.04% (×1.03) · 1.87% (×0.94) | 1.98% | 85% · 82% |
| Ra trong 5 kỳ gần (gộp) | 95 | 1.92% (×0.97) · 1.88% (×0.95) · 2.10% (×1.06) | 1.98% | 86% · 85% |
| Ra trong 10 kỳ gần (gộp) | 182 | 1.95% (×0.98) · 1.95% (×0.99) · 1.99% (×1.01) | 1.98% | 98% · 97% |
| Ra ≥2 lần trong 10 kỳ | 16 | 2.35% (×1.19) · 1.77% (×0.89) · 2.00% (×1.01) | 1.98% | 28% · 27% |

## Max 3D Pro — 783 kỳ

| Nhóm | Cỡ TB | Mỗi bộ ra kỳ kế (gần · giữa · xa) | Chia đều | Kỳ có ≥1 bộ lặp lại (thực · kỳ vọng) |
|---|---|---|---|---|
| Ra ở kỳ trước | 20 | 1.67% (×0.84) · 1.86% (×0.94) · 1.76% (×0.89) | 1.98% | 30% · 33% |
| Ra trong 2–5 kỳ trước (không tính kỳ trước) | 76 | 2.00% (×1.01) · 1.82% (×0.92) · 1.78% (×0.90) | 1.98% | 76% · 78% |
| Ra trong 6–10 kỳ trước | 87 | 1.93% (×0.97) · 1.78% (×0.90) · 1.94% (×0.98) | 1.98% | 82% · 82% |
| Ra trong 5 kỳ gần (gộp) | 96 | 1.93% (×0.97) · 1.83% (×0.92) · 1.77% (×0.89) | 1.98% | 85% · 85% |
| Ra trong 10 kỳ gần (gộp) | 183 | 1.93% (×0.97) · 1.81% (×0.91) · 1.85% (×0.94) | 1.98% | 99% · 97% |
| Ra ≥2 lần trong 10 kỳ | 15 | 2.12% (×1.07) · 1.31% (×0.66) · 1.62% (×0.82) | 1.98% | 24% · 26% |

Kết luận: Max 3D chỉ "ra ở kỳ trước" hơi ít lặp; 2–10 kỳ như mọi bộ. Pro: bộ đã ra trong 5–10 kỳ gần lặp ít hơn ở cả 3 đoạn (×0,89–0,97). Không dùng làm luật loại cứng: nhóm 10 kỳ có ≥1 bộ lặp ở 98–99% số kỳ.


# Max 3D / Pro — khoảng nghỉ lặp lại của bộ số (05/10/2026)

## Max 3D (3D+) — 1136 kỳ (22/04/2019 → 02/10/2026)

| Ra lại trong vòng | 1 kỳ | 5 kỳ | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 200 kỳ |
|---|---|---|---|---|---|---|---|
| Lần ra ở 300 kỳ trước khúc 200 kỳ cuối | 2.4% | 10.2% | 18.6% | 33.3% | 63.1% | 86.4% | 98.4% |
| Lần ra ở các kỳ cũ hơn | 2.0% | 9.6% | 18.4% | 33.2% | 63.3% | 86.7% | 98.0% |
| **Quay đều (lý thuyết)** | 2.0% | 9.5% | 18.1% | 33.0% | 63.2% | 86.5% | 98.2% |

- Khoảng nghỉ lặp lại: trung bình **48 kỳ**, trung vị **34 kỳ** (quay đều: TB 50, trung vị 35 kỳ); dài nhất 628 kỳ
- Ra lại đúng sau 1 kỳ: 450 lần (2.09% số lần lặp; quay đều 1.98%)
- Ra lại đúng sau 2 kỳ: 425 lần (1.98% số lần lặp; quay đều 1.94%)
- Ra lại đúng sau 3 kỳ: 445 lần (2.07% số lần lặp; quay đều 1.90%)

## Max 3D Pro — 783 kỳ (14/09/2021 → 03/10/2026)

| Ra lại trong vòng | 1 kỳ | 5 kỳ | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 200 kỳ |
|---|---|---|---|---|---|---|---|
| Lần ra ở 300 kỳ trước khúc 200 kỳ cuối | 2.0% | 9.4% | 17.8% | 32.7% | 63.6% | 86.4% | 98.1% |
| Lần ra ở các kỳ cũ hơn | 2.1% | 9.9% | 18.1% | 32.4% | 63.5% | 86.5% | 98.3% |
| **Quay đều (lý thuyết)** | 2.0% | 9.5% | 18.1% | 33.0% | 63.2% | 86.5% | 98.2% |

- Khoảng nghỉ lặp lại: trung bình **47 kỳ**, trung vị **33 kỳ** (quay đều: TB 50, trung vị 35 kỳ); dài nhất 491 kỳ
- Ra lại đúng sau 1 kỳ: 307 lần (2.12% số lần lặp; quay đều 1.98%)
- Ra lại đúng sau 2 kỳ: 301 lần (2.07% số lần lặp; quay đều 1.94%)
- Ra lại đúng sau 3 kỳ: 281 lần (1.94% số lần lặp; quay đều 1.90%)

Kết luận: phân bố khoảng nghỉ lặp lại trùng gần như tuyệt đối với quay đều ở mọi mốc 1–200 kỳ, cả 2 game, cả khúc gần lẫn cũ. Không có nhịp lặp riêng.


# Max 3D / Pro — loại bộ đang trong thời gian nghỉ (anh, 05/10/2026: "nếu nó đang trong thời gian nghỉ thì loại")

## max3d_data.json — giữ lại p% bộ điểm cao (gộp dấu vết)

| Cách | Giữ | Bộ trúng nằm trong nhóm giữ (gần · giữa · xa) | Chia đều | Cả 2 ĐB trong nhóm giữ | Chia đều |
|---|---|---|---|---|---|
| Nặng 50 kỳ + bỏ bộ đang nghỉ (ra trong 1 kỳ gần) | 50% | 50.0% · 50.9% · 51.4% | 50% | 27% · 30% · 33% | 25% |
| Nặng 50 kỳ + bỏ bộ đang nghỉ (ra trong 1 kỳ gần) | 34% | 34.3% · 36.1% · 35.4% | 34% | 15% · 13% · 13% | 12% |
| Nặng 50 kỳ + bỏ bộ đang nghỉ (ra trong 5 kỳ gần) | 50% | 50.8% · 50.9% · 50.6% | 50% | 24% · 31% · 29% | 25% |
| Nặng 50 kỳ + bỏ bộ đang nghỉ (ra trong 5 kỳ gần) | 34% | 34.7% · 36.2% · 34.7% | 34% | 13% · 14% · 14% | 12% |
| Nặng 50 kỳ + bỏ bộ đang nghỉ (ra trong 10 kỳ gần) | 50% | 51.7% · 50.3% · 49.0% | 50% | 28% · 24% · 25% | 25% |
| Nặng 50 kỳ + bỏ bộ đang nghỉ (ra trong 10 kỳ gần) | 34% | 34.2% · 35.4% · 34.5% | 34% | 11% · 16% · 16% | 12% |
| Nặng 50 kỳ + bỏ bộ đang nghỉ (ra trong 20 kỳ gần) | 50% | 49.9% · 50.7% · 50.2% | 50% | 20% · 23% · 26% | 25% |
| Nặng 50 kỳ + bỏ bộ đang nghỉ (ra trong 20 kỳ gần) | 34% | 34.4% · 34.1% · 34.2% | 34% | 9% · 14% · 14% | 12% |

## max3dpro_data.json — giữ lại p% bộ điểm cao (gộp dấu vết)

| Cách | Giữ | Bộ trúng nằm trong nhóm giữ (gần · giữa · xa) | Chia đều | Cả 2 ĐB trong nhóm giữ | Chia đều |
|---|---|---|---|---|---|
| Nặng 50 kỳ + bỏ bộ đang nghỉ (ra trong 1 kỳ gần) | 50% | 49.1% · 52.0% · 49.4% | 50% | 29% · 29% · 21% | 25% |
| Nặng 50 kỳ + bỏ bộ đang nghỉ (ra trong 1 kỳ gần) | 34% | 32.5% · 35.4% · 32.2% | 34% | 17% · 14% · 7% | 12% |
| Nặng 50 kỳ + bỏ bộ đang nghỉ (ra trong 5 kỳ gần) | 50% | 48.5% · 52.1% · 49.6% | 50% | 27% · 27% · 15% | 25% |
| Nặng 50 kỳ + bỏ bộ đang nghỉ (ra trong 5 kỳ gần) | 34% | 33.2% · 35.9% · 33.0% | 34% | 16% · 13% · 5% | 12% |
| Nặng 50 kỳ + bỏ bộ đang nghỉ (ra trong 10 kỳ gần) | 50% | 48.1% · 52.5% · 49.8% | 50% | 24% · 32% · 19% | 25% |
| Nặng 50 kỳ + bỏ bộ đang nghỉ (ra trong 10 kỳ gần) | 34% | 32.6% · 37.0% · 33.4% | 34% | 12% · 17% · 6% | 12% |
| Nặng 50 kỳ + bỏ bộ đang nghỉ (ra trong 20 kỳ gần) | 50% | 50.8% · 51.8% · 51.1% | 50% | 23% · 27% · 18% | 25% |
| Nặng 50 kỳ + bỏ bộ đang nghỉ (ra trong 20 kỳ gần) | 34% | 33.3% · 35.9% · 34.9% | 34% | 12% · 12% · 7% | 12% |

Kết luận: loại bộ đang nghỉ không làm mất tỉ lệ (bộ đang nghỉ ra bằng hoặc ít hơn mức chia đều), nên dùng được để thu nhỏ pool. Max 3D+: nặng 50 kỳ + loại bộ ra trong 5 kỳ, giữ 340 bộ → bộ trúng 34,7 · 36,2 · 34,7%, cặp ĐB 13 · 14 · 14% (chia đều 12%), ổn định cả 3 đoạn. Pro: loại bộ ra trong 20 kỳ, giữ 50% → 50,8 · 51,8 · 51,1%.


# Max 3D / Pro — dạng bộ số (05/10/2026)

## Max 3D (3D+) — 1136 kỳ (22/04/2019 → 02/10/2026), 22720 lần quay

| Dạng | Số bộ | Lần ra (cả lịch sử) | Kỳ vọng | Tỉ lệ so với chia đều: cả lịch sử | 3 đoạn 100 kỳ gần → xa |
|---|---|---|---|---|---|
| Tiến liên tiếp (123, 789) | 8 | 156 | 182 | ×0.86 | ×0.69 · ×0.81 · ×0.81 |
| Lùi liên tiếp (321, 987) | 8 | 194 | 182 | ×1.07 | ×1.19 · ×0.81 · ×1.06 |
| Tam hoa (000, 111…) | 10 | 211 | 227 | ×0.93 | ×1.15 · ×1.15 · ×0.85 |
| Kép đầu (112, 330…) | 90 | 2041 | 2045 | ×1.00 | ×0.98 · ×1.08 · ×0.96 |
| Kép kẹp (121, 303…) | 90 | 1941 | 2045 | ×0.95 | ×0.94 · ×0.84 · ×0.97 |
| Kép cuối (211, 033…) | 90 | 2102 | 2045 | ×1.03 | ×1.14 · ×1.06 · ×1.04 |
| Ba chữ số khác nhau, còn lại | 704 | 16075 | 15995 | ×1.01 | ×0.99 · ×1.00 · ×1.01 |

- Kỳ có ≥1 tam hoa (300 kỳ gần): 20% (kỳ vọng 18%) → luật "loại tam hoa" đúng 80% số kỳ

## Max 3D Pro — 783 kỳ (14/09/2021 → 03/10/2026), 15660 lần quay

| Dạng | Số bộ | Lần ra (cả lịch sử) | Kỳ vọng | Tỉ lệ so với chia đều: cả lịch sử | 3 đoạn 100 kỳ gần → xa |
|---|---|---|---|---|---|
| Tiến liên tiếp (123, 789) | 8 | 115 | 125 | ×0.92 | ×0.69 · ×0.94 · ×0.56 |
| Lùi liên tiếp (321, 987) | 8 | 131 | 125 | ×1.05 | ×0.69 · ×0.94 · ×1.44 |
| Tam hoa (000, 111…) | 10 | 158 | 157 | ×1.01 | ×0.90 · ×0.85 · ×1.05 |
| Kép đầu (112, 330…) | 90 | 1389 | 1409 | ×0.99 | ×0.94 · ×0.95 · ×0.96 |
| Kép kẹp (121, 303…) | 90 | 1349 | 1409 | ×0.96 | ×1.13 · ×0.89 · ×0.94 |
| Kép cuối (211, 033…) | 90 | 1364 | 1409 | ×0.97 | ×1.01 · ×0.97 · ×0.93 |
| Ba chữ số khác nhau, còn lại | 704 | 11154 | 11025 | ×1.01 | ×1.00 · ×1.03 · ×1.02 |

- Kỳ có ≥1 tam hoa (300 kỳ gần): 18% (kỳ vọng 18%) → luật "loại tam hoa" đúng 82% số kỳ

Kết luận: tam hoa ra đúng mức (×0,93 · ×1,01), loại được (kỳ đúng 80–82%) nhưng không lợi thêm. Tiến liên tiếp (123…789) ra ít hơn ở cả 2 game (×0,86 · ×0,92; 3 đoạn gần đều thấp) → loại. Kép kẹp (121, 303…) ít hơn nhẹ ở cả 2 game (×0,95 · ×0,96) → trừ điểm nhẹ. Kép đầu, kép cuối, lùi liên tiếp: như chia đều.


# Max 3D / Pro — tâm linh (05/10/2026)

## Max 3D (3D+) — 1136 kỳ

### Quẻ chọn BỘ SỐ — mỗi bộ ra kỳ đó (chia đều 1.98%)

| Quẻ | 100 kỳ gần | 100 kỳ giữa | 100 kỳ xa | Cả lịch sử |
|---|---|---|---|---|
| Ngày + tháng âm (25/8 → 258, 825) | 4.52% (×2.28) | 3.52% (×1.78) | 1.52% (×0.76) | 1.99% (×1.01) |
| Ngày + tháng dương (05/10 → 050, 005…) | 2.50% (×1.26) | 3.02% (×1.52) | 2.01% (×1.01) | 2.17% (×1.09) |
| Bóng âm dương 2 số ĐB kỳ trước | 1.50% (×0.76) | 4.00% (×2.02) | 0.00% (×0.00) | 1.67% (×0.84) |
| Lộn 2 số ĐB kỳ trước | 1.68% (×0.85) | 2.21% (×1.12) | 0.56% (×0.29) | 1.45% (×0.73) |
| Tam hoa theo thần số học ngày | 5.00% (×2.52) | 0.00% (×0.00) | 2.00% (×1.01) | 1.59% (×0.80) |

### Quẻ chọn CHỮ SỐ — tỉ lệ chiếm trong 60 lần quay chữ số của kỳ (so với chia đều)

| Quẻ | 100 kỳ gần | 100 kỳ giữa | 100 kỳ xa | Cả lịch sử |
|---|---|---|---|---|
| Ngũ hành ngày (Hà Đồ, 2 chữ số) | ×1.00 | ×0.99 | ×1.05 | ×1.00 |
| Can ngày (chữ số đuôi năm can: Canh 0…Kỷ 9) | ×0.95 | ×0.92 | ×1.01 | ×0.99 |
| Thần số học ngày (1 chữ số) | ×1.00 | ×0.96 | ×1.03 | ×1.00 |
| Ngày âm (chữ số đuôi + đầu) | ×1.05 | ×1.03 | ×1.01 | ×1.00 |
| Tổng chạm ĐB1 kỳ trước (1 chữ số) | ×0.95 | ×1.04 | ×1.04 | ×1.00 |

## Max 3D Pro — 783 kỳ

### Quẻ chọn BỘ SỐ — mỗi bộ ra kỳ đó (chia đều 1.98%)

| Quẻ | 100 kỳ gần | 100 kỳ giữa | 100 kỳ xa | Cả lịch sử |
|---|---|---|---|---|
| Ngày + tháng âm (25/8 → 258, 825) | 2.51% (×1.27) | 1.51% (×0.76) | 4.04% (×2.04) | 1.93% (×0.97) |
| Ngày + tháng dương (05/10 → 050, 005…) | 1.50% (×0.76) | 1.51% (×0.76) | 2.53% (×1.27) | 2.12% (×1.07) |
| Bóng âm dương 2 số ĐB kỳ trước | 1.50% (×0.76) | 1.00% (×0.50) | 2.00% (×1.01) | 1.79% (×0.90) |
| Lộn 2 số ĐB kỳ trước | 3.91% (×1.97) | 2.75% (×1.39) | 3.87% (×1.95) | 2.64% (×1.33) |
| Tam hoa theo thần số học ngày | 2.00% (×1.01) | 3.00% (×1.51) | 1.00% (×0.50) | 2.17% (×1.10) |

### Quẻ chọn CHỮ SỐ — tỉ lệ chiếm trong 60 lần quay chữ số của kỳ (so với chia đều)

| Quẻ | 100 kỳ gần | 100 kỳ giữa | 100 kỳ xa | Cả lịch sử |
|---|---|---|---|---|
| Ngũ hành ngày (Hà Đồ, 2 chữ số) | ×1.00 | ×0.97 | ×0.98 | ×0.99 |
| Can ngày (chữ số đuôi năm can: Canh 0…Kỷ 9) | ×1.00 | ×0.98 | ×0.99 | ×1.00 |
| Thần số học ngày (1 chữ số) | ×1.03 | ×1.09 | ×0.99 | ×1.04 |
| Ngày âm (chữ số đuôi + đầu) | ×0.98 | ×0.99 | ×1.01 | ×0.99 |
| Tổng chạm ĐB1 kỳ trước (1 chữ số) | ×1.06 | ×1.03 | ×0.98 | ×0.99 |

## Quẻ kỳ tới

**Max 3D+ 05/10/2026** (âm 25/8, ngày Nhâm – hành Thủy, thần số học 7; ĐB kỳ trước 357 728)
- Ngày + tháng âm (25/8 → 258, 825): 258 825
- Ngày + tháng dương (05/10 → 050, 005…): 005 050
- Bóng âm dương 2 số ĐB kỳ trước: 273 802
- Lộn 2 số ĐB kỳ trước: 753 827
- Tam hoa theo thần số học ngày: 777
- Ngũ hành ngày (Hà Đồ, 2 chữ số): 1 6
- Can ngày (chữ số đuôi năm can: Canh 0…Kỷ 9): 2
- Thần số học ngày (1 chữ số): 7
- Ngày âm (chữ số đuôi + đầu): 2 5
- Tổng chạm ĐB1 kỳ trước (1 chữ số): 5

**Max 3D Pro 06/10/2026** (âm 26/8, ngày Quý – hành Thủy, thần số học 8; ĐB kỳ trước 509 954)
- Ngày + tháng âm (25/8 → 258, 825): 268 826
- Ngày + tháng dương (05/10 → 050, 005…): 006 060
- Bóng âm dương 2 số ĐB kỳ trước: 054 409
- Lộn 2 số ĐB kỳ trước: 459 905
- Tam hoa theo thần số học ngày: 888
- Ngũ hành ngày (Hà Đồ, 2 chữ số): 1 6
- Can ngày (chữ số đuôi năm can: Canh 0…Kỷ 9): 3
- Thần số học ngày (1 chữ số): 8
- Ngày âm (chữ số đuôi + đầu): 2 6
- Tổng chạm ĐB1 kỳ trước (1 chữ số): 4


Ghi chú: quẻ bộ số chỉ 1–2 bộ/kỳ nên mỗi đoạn 100 kỳ chỉ kỳ vọng ~4 lần trúng, dao động ×0–2,5 là bình thường; tin cột "cả lịch sử". Nổi bật: Pro "lộn 2 số ĐB kỳ trước" ×1,97 · ×1,39 · ×1,95, cả lịch sử ×1,33 (ở Max 3D thì ngược, ×0,73) → đưa vào sổ theo dõi. Quẻ chữ số đều ≈ ×1,00.


# Max 3D / Pro — 17 phương pháp tâm linh của app (05/10/2026)

Chạy KX_M (Lục Nhâm, Thái Ất, Huyền Không, Nhị thập bát tú, Hoàng đạo, Nạp âm, Thần số học, Tử vi, Xin xăm, Tarot, Mai Hoa, Kỳ Môn, Tứ trụ, Bát trạch) + bóng, lộn 2 số ĐB kỳ trước, trên bộ số 000–999, ngày sinh anh 16/06/1991 âm giờ Sửu. Tỉ lệ = số lần trúng / kỳ vọng.

## plus kỳ tới 05/10/2026 · phiếu cao nhất 8
| Phương pháp | 100 kỳ gần | giữa | xa | cả lịch sử |
| Tiểu Lục Nhâm | ×1.02 | ×0.98 | ×0.97 | ×1.00 |
| Đại Lục Nhâm (rút gọn) | ×0.98 | ×0.97 | ×0.98 | ×0.98 |
| Thái Ất (thời kế, rút gọn) | ×1.03 | ×1.01 | ×1.00 | ×0.99 |
| Huyền Không Phi Tinh | ×0.96 | ×1.05 | ×1.02 | ×1.00 |
| Nhị thập bát tú | ×1.06 | ×1.05 | ×1.06 | ×0.99 |
| Hoàng đạo / Hắc đạo | ×1.07 | ×1.06 | ×1.04 | ×1.01 |
| Ngũ hành nạp âm | ×1.00 | ×1.10 | ×1.00 | ×1.01 |
| Thần số học | ×1.00 | ×0.99 | ×1.04 | ×1.00 |
| Tử vi (Mệnh, Cục, sao Tử Vi) | ×1.00 | ×1.00 | ×0.95 | ×0.99 |
| Xin xăm (100 quẻ) | ×0.99 | ×1.01 | ×0.98 | ×0.97 |
| Tarot (3 lá) | ×1.09 | ×0.90 | ×1.10 | ×0.85 |
| Mai Hoa (giờ quay) | ×1.30 | ×1.04 | ×0.65 | ×0.86 |
| Kỳ Môn Độn Giáp | ×0.94 | ×1.30 | ×1.03 | ×1.09 |
| Tứ trụ (dụng thần) | ×1.02 | ×1.05 | ×1.02 | ×1.00 |
| Bát trạch (cung mệnh) | ×1.04 | ×1.00 | ×0.93 | ×0.98 |
| Bóng âm dương 2 số ĐB kỳ trước | ×1.38 | ×1.75 | ×0.13 | ×0.98 |
| Lộn 2 số ĐB kỳ trước | ×0.75 | ×1.00 | ×0.25 | ×0.68 |
Theo số phiếu (cả lịch sử): 0 phiếu: ×0.99 (2151 lần) · 1 phiếu: ×1.02 (5076 lần) · 2 phiếu: ×1.00 (5741 lần) · 3 phiếu: ×0.99 (4357 lần) · 4 phiếu: ×1.01 (2852 lần) · 5 phiếu: ×0.98 (1591 lần) · 6 phiếu: ×0.98 (688 lần) · 7 phiếu: ×0.93 (202 lần) · 8 phiếu: ×0.94 (40 lần) · 9 phiếu: ×0.31 (2 lần) · 10 phiếu: ×0.00 (0 lần)
Top bộ: 014(8) 054(8) 004(7) 009(7) 064(7) 144(7) 194(7) 234(7) 324(7) 374(7) 414(7) 504(7)

## pro kỳ tới 06/10/2026 · phiếu cao nhất 7
| Phương pháp | 100 kỳ gần | giữa | xa | cả lịch sử |
| Tiểu Lục Nhâm | ×0.98 | ×1.00 | ×1.01 | ×1.01 |
| Đại Lục Nhâm (rút gọn) | ×1.00 | ×0.99 | ×0.99 | ×0.97 |
| Thái Ất (thời kế, rút gọn) | ×0.96 | ×0.95 | ×0.98 | ×1.00 |
| Huyền Không Phi Tinh | ×1.02 | ×1.01 | ×1.05 | ×1.03 |
| Nhị thập bát tú | ×0.99 | ×1.08 | ×0.92 | ×0.97 |
| Hoàng đạo / Hắc đạo | ×0.90 | ×1.12 | ×1.06 | ×1.01 |
| Ngũ hành nạp âm | ×0.96 | ×0.99 | ×1.04 | ×1.01 |
| Thần số học | ×1.01 | ×0.96 | ×0.99 | ×0.99 |
| Tử vi (Mệnh, Cục, sao Tử Vi) | ×1.03 | ×0.98 | ×0.95 | ×0.99 |
| Xin xăm (100 quẻ) | ×0.97 | ×0.99 | ×0.98 | ×1.02 |
| Tarot (3 lá) | ×0.60 | ×0.59 | ×0.99 | ×0.85 |
| Mai Hoa (giờ quay) | ×1.04 | ×1.31 | ×0.78 | ×1.07 |
| Kỳ Môn Độn Giáp | ×1.32 | ×0.94 | ×0.84 | ×1.01 |
| Tứ trụ (dụng thần) | ×0.93 | ×0.99 | ×0.97 | ×1.00 |
| Bát trạch (cung mệnh) | ×1.04 | ×0.93 | ×0.98 | ×0.99 |
| Bóng âm dương 2 số ĐB kỳ trước | ×1.13 | ×0.88 | ×1.00 | ×0.94 |
| Lộn 2 số ĐB kỳ trước | ×2.00 | ×1.25 | ×1.75 | ×1.25 |
Theo số phiếu (cả lịch sử): 0 phiếu: ×1.02 (1507 lần) · 1 phiếu: ×0.98 (3417 lần) · 2 phiếu: ×1.00 (3943 lần) · 3 phiếu: ×1.03 (3120 lần) · 4 phiếu: ×0.98 (1899 lần) · 5 phiếu: ×0.99 (1101 lần) · 6 phiếu: ×0.95 (463 lần) · 7 phiếu: ×1.01 (149 lần) · 8 phiếu: ×0.98 (30 lần) · 9 phiếu: ×3.16 (11 lần) · 10 phiếu: ×0.00 (0 lần) · 11 phiếu: ×0.00 (0 lần)
Top bộ: 054(7) 019(6) 059(6) 090(6) 139(6) 144(6) 179(6) 199(6) 234(6) 239(6) 319(6) 324(6)

Kết luận: các phương pháp tâm linh ra ngang mức chia đều (×0,85–1,09 cả lịch sử); bộ nhiều phiếu cũng vậy. Dùng để chọn trong pool (không thiệt). Riêng Pro "lộn 2 số ĐB kỳ trước" ×1,25 cả lịch sử, 3 đoạn ×2,00 · 1,25 · 1,75.


# Max 3D / Pro — dạng 00x, 0x0, x00 (05/10/2026)

00x (000–009): Max 3D+ ×1,01 cả lịch sử (3 đoạn ×0,90 · ×1,30 · ×1,20), Pro ×1,02. Không hiếm hơn mức chia đều. Kỳ có ≥1 bộ 00x: 19–20% → luật loại 00x đúng ~80% kỳ, số bị loại không ra nhiều hơn TB → anh muốn loại (05/10) nên đưa vào danh sách loại cùng tam hoa. 0x0 ×0,95 / ×0,93; x00 ×0,98 / ×0,86 (Pro).


# Max 3D Pro — thu hẹp pool từ ~640 bộ (05/10/2026)

## max3dpro_data.json

| Cách | Cỡ pool | Bộ trúng trong pool (gần · giữa · xa) | Chia đều | Cả 2 ĐB trong pool | Chia đều |
|---|---|---|---|---|---|
| Hiện tại: bỏ ra 20 kỳ, tiến, tam hoa, 00x | 649 | 65.9% · 66.3% · 66.0% | 64.9% | 45% · 46% · 38% | 42% |
| Bỏ ra 30 kỳ (+ tiến, tam hoa, 00x) | 529 | 54.2% · 55.4% · 54.2% | 52.9% | 30% · 36% · 27% | 28% |
| Bỏ ra 50 kỳ | 350 | 34.5% · 35.0% · 36.4% | 35.0% | 10% · 11% · 11% | 12% |
| Bỏ ra 20 kỳ + kép kẹp + 0x0/x00 | 584 | 58.0% · 59.7% · 58.8% | 58.4% | 36% · 37% · 28% | 34% |
| Bỏ ra 30 kỳ + kép kẹp + 0x0/x00 | 476 | 47.7% · 49.4% · 48.5% | 47.6% | 22% · 29% · 20% | 23% |
| Hiện tại → giữ 340 bộ nặng 20 kỳ | 340 | 34.1% · 34.8% · 34.8% | 34.0% | 14% · 8% · 6% | 12% |
| Hiện tại → giữ 340 bộ nặng 100 kỳ | 340 | 34.2% · 35.4% · 34.3% | 34.0% | 15% · 12% · 8% | 12% |
| Hiện tại → giữ 340 bộ NHẸ 20 kỳ (ngược) | 340 | 34.7% · 34.3% · 34.4% | 34.0% | 12% · 14% · 13% | 12% |

| Hiện tại → giữ 340 bộ nặng 100 kỳ | 340 | 34.2% · 35.4% · 34.2% | 34.0% | 15% · 12% · 8% | 12% |
| Bỏ ra 30 kỳ → giữ 340 bộ nặng 100 kỳ | 340 | 33.2% · 36.5% · 35.6% | 34.0% | 11% · 17% · 9% | 12% |
| Bỏ ra 30 kỳ → giữ 400 bộ nặng 100 kỳ | 400 | 40.4% · 42.9% · 42.1% | 40.0% | 14% · 25% · 14% | 16% |
| Hiện tại → giữ 340 bộ NHẸ 20 kỳ (ngược) | 340 | 34.8% · 34.2% · 34.4% | 34.0% | 12% · 14% · 13% | 12% |

Chọn: loại bộ ra trong 30 kỳ (đang nghỉ) + tiến, tam hoa, 00x, rồi giữ 400 bộ chữ số nặng nhất theo hàng (100 kỳ): bộ trúng trong pool 40,4 · 42,9 · 42,1% (chia đều 40%), cả 3 đoạn trên mức. Cặp ĐB trong pool 14 · 25 · 14% (chia đều 16%) — chưa ổn định.


# Max 3D / Pro — bộ số ≥500 theo kỳ (05/10/2026)

Max 3D+: TB bộ ≥500/kỳ 10 kỳ 9,4 · 20 kỳ 9,6 · 50 kỳ 10,2 · 100 kỳ 10,0; cả lịch sử 49,4%. 10 kỳ gần: 9 13 12 7 10 9 11 9 7 7. Kỳ trước nhiều/ít số lớn → kỳ sau vẫn ~9,8–10 (không nối tiếp). Pro: 10 kỳ gần TB 11,3 (13 11 7 12 12 12 11 14 10 11), 100 kỳ 10,0; kỳ trước ≤8 → kỳ sau 10,15, ≥12 → 9,84 (hồi nhẹ, chưa chắc); tương quan TB 20 kỳ ↔ kỳ sau −0,07. Theo khoảng trăm 100 kỳ: đều 176–230/200. Kết luận: không có dấu vết lớn/nhỏ dùng được.


# Max 3D — "đợt" chữ số theo khối 10 kỳ (05/10/2026, anh hỏi đợt này nhiều 9, đợt trước nhiều 8, 7)

Max 3D+ khối 14/09→05/10: 0 và 9 mỗi số 12%; khối 21/08→11/09: 8 12%, 7 11%. Đúng như anh nhận xét. Nhưng kiểm 300 kỳ: 2 chữ số nhiều nhất khối 10 kỳ trước chỉ chiếm 20,4% ở khối sau (chia đều 20%) — đợt không kéo dài sang đợt sau. Pro: 20,2%. Độ lệch ±2 điểm/khối 10 kỳ là dao động bình thường (600 lần quay).


# Max 3D — phân tích 1 đợt 20 kỳ (05/10/2026)

Max 3D+ 21/08→05/10: 62 bộ ra ≥2 lần (ngẫu nhiên ~61); 152 và 361 ra 4 lần. Hàng trăm nhiều 1, 5 (46); chục 6 (51); đơn vị 0 (48), 7 (47). Pro 20/08→03/10: 584 ra 5 lần, 780 4 lần; 48 bộ ≥2 lần; cả 3 hàng 8 nhiều nhất (141/120), 1 và 2 ít (105). Kiểm cả lịch sử: bộ ra ≥3 kỳ trong 20 kỳ → kỳ sau ×0,99 (3D+), ×0,92 (Pro); bộ ra ≥4 kỳ/khối 20 kỳ: 0,68 và 0,46 so với lý thuyết 0,75 → không có bộ "ruột". Chữ số nhiều nhất mỗi hàng 10 kỳ → 10 kỳ sau 30,5% / 29,9% (chia đều 30%). Không có dấu vết trong đợt.


# Max 3D / Pro — bộ quanh bộ ra nhiều bất thường (05/10/2026, ý anh)


## Max 3D+ — 1137 kỳ

| Bộ "nóng" (trong 20 kỳ) | Nhóm quanh | Số lần xét | Kỳ kế (×) | 5 kỳ kế (×) |
|---|---|---|---|---|
| ≥3 lần | A. đổi ±1 một chữ số (6 bộ) | 7218 | 1.88% (×0.95) | 10.1% (×1.06) |
| ≥3 lần | B. trùng 2 hàng (27 bộ) | 32481 | 2.06% (×1.04) | 9.8% (×1.03) |
| ≥3 lần | C. ±1, ±2 giá trị (4 bộ) | 4812 | 1.60% (×0.81) | 9.5% (×1.00) |
| ≥3 lần | Chính bộ đó | 1203 | 2.41% (×1.22) | 9.9% (×1.04) |
| ≥4 lần | A. đổi ±1 một chữ số (6 bộ) | 792 | 1.64% (×0.83) | 9.7% (×1.02) |
| ≥4 lần | B. trùng 2 hàng (27 bộ) | 3564 | 1.77% (×0.89) | 9.7% (×1.02) |
| ≥4 lần | C. ±1, ±2 giá trị (4 bộ) | 528 | 1.14% (×0.57) | 9.7% (×1.01) |
| ≥4 lần | Chính bộ đó | 132 | 2.27% (×1.15) | 9.8% (×1.03) |

## Max 3D Pro — 783 kỳ

| Bộ "nóng" (trong 20 kỳ) | Nhóm quanh | Số lần xét | Kỳ kế (×) | 5 kỳ kế (×) |
|---|---|---|---|---|
| ≥3 lần | A. đổi ±1 một chữ số (6 bộ) | 4830 | 2.17% (×1.10) | 9.2% (×0.97) |
| ≥3 lần | B. trùng 2 hàng (27 bộ) | 21735 | 2.07% (×1.05) | 9.6% (×1.01) |
| ≥3 lần | C. ±1, ±2 giá trị (4 bộ) | 3220 | 1.99% (×1.00) | 8.1% (×0.85) |
| ≥3 lần | Chính bộ đó | 805 | 2.36% (×1.19) | 9.1% (×0.95) |
| ≥4 lần | A. đổi ±1 một chữ số (6 bộ) | 462 | 2.81% (×1.42) | 9.7% (×1.02) |
| ≥4 lần | B. trùng 2 hàng (27 bộ) | 2079 | 2.45% (×1.24) | 10.8% (×1.13) |
| ≥4 lần | C. ±1, ±2 giá trị (4 bộ) | 308 | 2.60% (×1.31) | 6.8% (×0.72) |
| ≥4 lần | Chính bộ đó | 77 | 5.19% (×2.62) | 10.4% (×1.09) |

Kết luận: Max 3D+ bộ quanh ra ngang chia đều (kỳ kế ×0,57–1,04, 5 kỳ ×1,00–1,06). Pro, bộ nóng ≥4 lần: bộ quanh kỳ kế ×1,24–1,42 nhưng 5 kỳ ×0,72–1,13 và mẫu nhỏ (kỳ vọng ~9 lần trúng) → chưa chắc, theo dõi trong sổ.


# Max 3D ↔ Pro so chéo kỳ liền trước (05/10/2026, anh: 2 game dùng chung bộ quay)

## Max 3D kỳ t ← Max 3D Pro kỳ ngay trước (779 cặp kỳ)

| Nhóm từ kỳ trước | Cả lịch sử | 300 lần gần | So với: cùng game kỳ trước (cả lịch sử) |
|---|---|---|---|
| 20 bộ của kỳ trước | ×0.86 | ×0.92 | ×1.03 |
| 2 bộ ĐB kỳ trước | ×0.58 | ×0.76 | ×0.71 |
| Lộn 2 bộ ĐB kỳ trước | ×1.01 | ×0.93 | ×0.68 |
| Quanh (±1 một chữ số) 20 bộ kỳ trước | ×1.03 | ×1.00 | ×0.99 |

- Chữ số theo hàng: tương quan với kỳ trước của Max 3D Pro: +0.012 · với kỳ trước cùng game: -0.006 · quay ngẫu nhiên: +0.005 (±0.014)

## Max 3D Pro kỳ t ← Max 3D kỳ ngay trước (781 cặp kỳ)

| Nhóm từ kỳ trước | Cả lịch sử | 300 lần gần | So với: cùng game kỳ trước (cả lịch sử) |
|---|---|---|---|
| 20 bộ của kỳ trước | ×1.09 | ×1.09 | ×1.00 |
| 2 bộ ĐB kỳ trước | ×1.03 | ×0.76 | ×0.87 |
| Lộn 2 bộ ĐB kỳ trước | ×1.00 | ×1.13 | ×1.33 |
| Quanh (±1 một chữ số) 20 bộ kỳ trước | ×1.03 | ×1.01 | ×1.01 |

- Chữ số theo hàng: tương quan với kỳ trước của Max 3D: +0.004 · với kỳ trước cùng game: +0.004 · quay ngẫu nhiên: +0.005 (±0.014)

## Kỳ gần nhất mỗi game
- Max 3D 05/10/2026: ĐB 546 085 · Nhất 472 486 159 586 · Nhì 525 877 261 110 123 238 · Ba 399 183 166 713 699 490 993 152
- Max 3D Pro 03/10/2026: ĐB 509 954 · Nhất 467 123 573 811 · Nhì 579 176 078 659 477 730 · Ba 607 598 017 166 408 320 593 633

Kết luận: 20 bộ Pro kỳ trước → Max 3D kỳ sau ×0,86 (ít lặp, ~−2,4 độ lệch chuẩn); 20 bộ Max 3D kỳ trước → Pro kỳ sau ×1,09 (lặp nhiều hơn nhẹ, cả lịch sử và 300 kỳ gần). Hai chiều ngược nhau → chưa kết luận chung bộ quay tạo dấu vết; chữ số theo hàng không liên quan. Theo dõi trong sổ.


# Max 3D / Pro — chữ số ra nhiều nhất kỳ trước có ra nhiều kỳ sau (05/10/2026, anh; cả chéo Max 3D ↔ Pro chung bộ quay)

Script: `build/max3d_chusonhieu.py`. Tỉ lệ chữ số đó trong kỳ sau, chia đều 10%; "Đúng" = ra trên mức TB.

## Max 3D+ — 1137 kỳ

| Kỳ trước lấy từ | Chữ số | Phạm vi | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 3 đoạn 100 kỳ | Cả lịch sử | Đúng (cả LS) |
|---|---|---|---|---|---|---|---|---|
| cùng game | nhiều nhất | cả 60 | 10.2% | 9.8% | 9.5% | 9.4% | 9.4% · 9.9% · 10.3% | 9.9% | 40.1% (TB 39.4%) |
| cùng game | nhiều nhất | hàng trăm | 8.1% | 8.6% | 8.2% | 8.4% | 8.4% · 9.9% · 9.9% | 9.8% | 30.5% (TB 32.3%) |
| cùng game | nhiều nhất | hàng chục | 11.1% | 10.7% | 10.5% | 10.2% | 10.2% · 10.8% · 8.6% | 10.0% | 32.9% (TB 32.3%) |
| cùng game | nhiều nhất | hàng đơn vị | 10.2% | 9.5% | 11.7% | 10.5% | 10.5% · 10.4% · 11.2% | 10.0% | 32.9% (TB 32.3%) |
| cùng game | ít nhất | cả 60 | 10.4% | 10.2% | 10.6% | 10.1% | 10.1% · 10.2% · 10.2% | 10.1% | 37.8% (TB 39.4%) |
| cùng game | ít nhất | hàng trăm | 12.4% | 11.4% | 10.4% | 9.7% | 9.7% · 10.0% · 10.5% | 10.1% | 32.3% (TB 32.3%) |
| cùng game | ít nhất | hàng chục | 10.9% | 10.8% | 10.4% | 10.2% | 10.2% · 9.1% · 10.9% | 10.3% | 33.9% (TB 32.3%) |
| cùng game | ít nhất | hàng đơn vị | 8.5% | 8.8% | 10.2% | 9.5% | 9.5% · 9.9% · 10.4% | 10.0% | 32.1% (TB 32.3%) |
| Max 3D Pro | nhiều nhất | cả 60 | 9.8% | 9.9% | 9.3% | 9.5% | 9.5% · 10.3% · 10.3% | 10.1% | 38.9% (TB 39.4%) |
| Max 3D Pro | nhiều nhất | hàng trăm | 10.2% | 10.4% | 10.3% | 9.8% | 9.8% · 9.4% · 11.0% | 9.9% | 32.6% (TB 32.3%) |
| Max 3D Pro | nhiều nhất | hàng chục | 7.9% | 8.5% | 9.5% | 9.6% | 9.6% · 10.7% · 11.2% | 10.2% | 34.6% (TB 32.3%) |
| Max 3D Pro | nhiều nhất | hàng đơn vị | 11.6% | 10.4% | 11.1% | 10.8% | 10.8% · 10.5% · 9.6% | 10.2% | 35.0% (TB 32.3%) |
| Max 3D Pro | ít nhất | cả 60 | 10.4% | 9.8% | 9.9% | 10.2% | 10.2% · 9.9% · 9.6% | 9.9% | 38.1% (TB 39.4%) |
| Max 3D Pro | ít nhất | hàng trăm | 10.5% | 10.4% | 8.9% | 9.2% | 9.2% · 9.0% · 10.1% | 9.9% | 32.6% (TB 32.3%) |
| Max 3D Pro | ít nhất | hàng chục | 10.7% | 9.5% | 10.4% | 10.1% | 10.1% · 9.3% · 10.0% | 9.7% | 31.4% (TB 32.3%) |
| Max 3D Pro | ít nhất | hàng đơn vị | 11.8% | 11.2% | 10.6% | 10.1% | 10.1% · 9.8% · 9.7% | 10.1% | 33.3% (TB 32.3%) |

Chia đều: 10,0%. Độ nhiễu 1 kỳ: cả 60 ±3,9 điểm, 1 hàng ±6,7 điểm → khung 100 kỳ ±0,4 / ±0,7, cả lịch sử ±0,1–0,2.

## Max 3D Pro — 783 kỳ

| Kỳ trước lấy từ | Chữ số | Phạm vi | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 3 đoạn 100 kỳ | Cả lịch sử | Đúng (cả LS) |
|---|---|---|---|---|---|---|---|---|
| cùng game | nhiều nhất | cả 60 | 10.6% | 9.9% | 10.2% | 10.1% | 10.1% · 9.9% · 10.0% | 10.1% | 39.4% (TB 39.4%) |
| cùng game | nhiều nhất | hàng trăm | 12.5% | 11.2% | 10.1% | 9.9% | 9.9% · 9.1% · 10.2% | 9.9% | 32.7% (TB 32.3%) |
| cùng game | nhiều nhất | hàng chục | 11.6% | 11.6% | 11.7% | 11.3% | 11.3% · 10.4% · 9.2% | 10.5% | 34.1% (TB 32.3%) |
| cùng game | nhiều nhất | hàng đơn vị | 9.2% | 8.8% | 8.9% | 9.4% | 9.4% · 9.8% · 8.9% | 9.9% | 32.8% (TB 32.3%) |
| cùng game | ít nhất | cả 60 | 9.8% | 10.3% | 9.7% | 9.5% | 9.5% · 10.7% · 10.2% | 10.1% | 39.7% (TB 39.4%) |
| cùng game | ít nhất | hàng trăm | 8.4% | 8.2% | 9.2% | 8.9% | 8.9% · 10.4% · 9.6% | 9.9% | 32.0% (TB 32.3%) |
| cùng game | ít nhất | hàng chục | 8.8% | 9.0% | 10.4% | 10.3% | 10.3% · 10.1% · 10.4% | 10.3% | 34.2% (TB 32.3%) |
| cùng game | ít nhất | hàng đơn vị | 8.2% | 10.6% | 9.4% | 9.2% | 9.2% · 10.5% · 9.4% | 10.1% | 32.8% (TB 32.3%) |
| Max 3D+ | nhiều nhất | cả 60 | 8.5% | 9.0% | 9.5% | 10.1% | 10.1% · 10.0% · 10.2% | 10.2% | 42.1% (TB 39.4%) |
| Max 3D+ | nhiều nhất | hàng trăm | 10.2% | 11.1% | 11.0% | 10.7% | 10.7% · 9.5% · 10.4% | 10.4% | 35.5% (TB 32.3%) |
| Max 3D+ | nhiều nhất | hàng chục | 7.6% | 8.9% | 8.9% | 10.1% | 10.1% · 9.6% · 9.4% | 10.1% | 32.8% (TB 32.3%) |
| Max 3D+ | nhiều nhất | hàng đơn vị | 10.8% | 9.3% | 9.2% | 9.4% | 9.4% · 10.0% · 10.3% | 10.0% | 31.3% (TB 32.3%) |
| Max 3D+ | ít nhất | cả 60 | 12.3% | 10.1% | 9.3% | 9.4% | 9.4% · 10.0% · 10.1% | 9.9% | 37.5% (TB 39.4%) |
| Max 3D+ | ít nhất | hàng trăm | 11.5% | 9.7% | 9.9% | 9.7% | 9.7% · 10.1% · 9.7% | 9.7% | 29.2% (TB 32.3%) |
| Max 3D+ | ít nhất | hàng chục | 11.1% | 11.3% | 10.9% | 10.0% | 10.0% · 8.9% · 9.8% | 10.0% | 30.8% (TB 32.3%) |
| Max 3D+ | ít nhất | hàng đơn vị | 10.4% | 11.0% | 10.0% | 10.2% | 10.2% · 10.0% · 11.0% | 10.2% | 33.9% (TB 32.3%) |

Chia đều: 10,0%. Độ nhiễu 1 kỳ: cả 60 ±3,9 điểm, 1 hàng ±6,7 điểm → khung 100 kỳ ±0,4 / ±0,7, cả lịch sử ±0,1–0,2.

Max 3D+ 05/10/2026: chữ số nhiều nhất cả 60: 1 (9 lần); mỗi hàng: 1 / 8,9 / 3,6

Max 3D Pro 03/10/2026: chữ số nhiều nhất cả 60: 7 (10 lần); mỗi hàng: 5 / 7 / 3,7

Kết luận: không có dấu vết. Chữ số nhiều nhất (cả 60 hoặc từng hàng) kỳ trước → kỳ sau 9,8–10,5% cả lịch sử, cùng game hay chéo game đều vậy; ngang chữ số ít nhất. Khung 10–100 kỳ lệch ±1–2 điểm nhưng 3 đoạn 100 kỳ đổi chiều (vd Pro hàng chục 11,3 · 10,4 · 9,2%) → dao động. Chéo Max 3D+ → Pro, cả 60: đúng 42,1% so TB 39,4% (~1,5 độ lệch chuẩn) nhưng tỉ lệ chỉ 10,2% → không dùng.


# Max 3D / Pro — toàn bộ 10 chữ số theo số lần ra kỳ trước (05/10/2026, anh: "kiểm toàn bộ", không theo hàng)

Script: `build/max3d_chusonhieu.py` (thay bản theo hàng). Tỉ lệ trong 60 chữ số kỳ sau, chia đều 10%.

## Max 3D+ ← kỳ trước cùng game (1136 cặp kỳ)

| Nhóm | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 3 đoạn 100 kỳ (gần → xa) | Cả lịch sử |
|---|---|---|---|---|---|---|
| Hạng 1 | 10.2% | 9.8% | 9.5% | 9.4% | 9.4% · 9.9% · 10.3% | 9.9% |
| Hạng 2 | 9.1% | 9.7% | 9.7% | 10.0% | 10.0% · 9.6% · 9.8% | 10.0% |
| Hạng 3 | 10.0% | 10.2% | 10.4% | 10.5% | 10.5% · 10.1% · 9.8% | 9.9% |
| Hạng 4 | 9.0% | 8.8% | 9.5% | 9.4% | 9.4% · 10.3% · 9.7% | 9.9% |
| Hạng 5 | 9.5% | 9.0% | 9.6% | 9.9% | 9.9% · 9.6% · 10.0% | 9.9% |
| Hạng 6 | 9.1% | 9.9% | 9.9% | 9.9% | 9.9% · 9.6% · 10.1% | 9.9% |
| Hạng 7 | 11.6% | 10.8% | 10.2% | 10.2% | 10.2% · 10.1% · 10.3% | 10.1% |
| Hạng 8 | 11.2% | 10.5% | 9.6% | 9.9% | 9.9% · 10.4% · 9.8% | 10.1% |
| Hạng 9 | 9.9% | 11.1% | 11.0% | 10.5% | 10.5% · 10.1% · 9.9% | 10.2% |
| Hạng 10 | 10.4% | 10.2% | 10.6% | 10.1% | 10.1% · 10.2% · 10.2% | 10.1% |
| Top 2 | 9.6% | 9.8% | 9.6% | 9.7% | 9.7% · 9.8% · 10.0% | 10.0% |
| Top 3 | 9.8% | 9.9% | 9.8% | 10.0% | 10.0% · 9.9% · 10.0% | 10.0% |
| Top 5 | 9.6% | 9.5% | 9.7% | 9.9% | 9.9% · 9.9% · 9.9% | 9.9% |
| Đáy 2 | 10.1% | 10.6% | 10.8% | 10.3% | 10.3% · 10.1% · 10.1% | 10.1% |
| Đáy 3 | 10.5% | 10.6% | 10.4% | 10.2% | 10.2% · 10.2% · 10.0% | 10.1% |
| Đáy 5 | 10.4% | 10.5% | 10.3% | 10.1% | 10.1% · 10.1% · 10.1% | 10.1% |

| Số lần ra kỳ trước | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 3 đoạn 100 kỳ (gần → xa) | Cả lịch sử |
|---|---|---|---|---|---|---|
| 0–3 lần | 10.3% | 10.5% | 10.4% | 10.3% | 10.3% · 10.2% · 9.9% | 10.1% (962 kỳ) |
| 4 lần | 10.1% | 10.6% | 10.7% | 10.2% | 10.2% · 10.4% · 10.2% | 10.2% (891 kỳ) |
| 5 lần | 10.4% | 10.5% | 10.1% | 10.3% | 10.3% · 9.9% · 10.6% | 10.0% (945 kỳ) |
| 6 lần (TB) | 10.0% | 9.7% | 9.8% | 9.9% | 9.9% · 9.5% · 9.7% | 9.8% (955 kỳ) |
| 7 lần | 7.9% | 8.0% | 9.7% | 9.9% | 9.9% · 10.2% · 9.7% | 10.0% (883 kỳ) |
| 8 lần | 11.2% | 11.5% | 11.0% | 10.2% | 10.2% · 9.9% · 9.7% | 10.0% (781 kỳ) |
| ≥9 lần | 9.8% | 9.8% | 9.5% | 9.5% | 9.5% · 10.2% · 10.1% | 10.0% (1016 kỳ) |

## Max 3D+ ← kỳ trước của Max 3D Pro (779 cặp kỳ)

| Nhóm | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 3 đoạn 100 kỳ (gần → xa) | Cả lịch sử |
|---|---|---|---|---|---|---|
| Hạng 1 | 9.8% | 9.9% | 9.3% | 9.5% | 9.5% · 10.3% · 10.3% | 10.1% |
| Hạng 2 | 8.3% | 9.8% | 10.3% | 10.6% | 10.6% · 10.1% · 10.4% | 10.2% |
| Hạng 3 | 8.1% | 8.6% | 9.7% | 10.2% | 10.2% · 10.1% · 10.1% | 9.9% |
| Hạng 4 | 11.0% | 9.9% | 9.9% | 9.9% | 9.9% · 9.9% · 10.0% | 9.9% |
| Hạng 5 | 10.6% | 10.0% | 10.2% | 9.8% | 9.8% · 9.5% · 10.1% | 9.9% |
| Hạng 6 | 10.6% | 10.3% | 10.5% | 10.1% | 10.1% · 9.8% · 9.8% | 10.0% |
| Hạng 7 | 10.5% | 10.8% | 10.0% | 9.7% | 9.7% · 9.9% · 9.9% | 9.9% |
| Hạng 8 | 11.4% | 10.8% | 10.3% | 10.2% | 10.2% · 10.2% · 9.9% | 10.0% |
| Hạng 9 | 9.2% | 10.0% | 10.0% | 9.9% | 9.9% · 10.3% · 10.0% | 10.1% |
| Hạng 10 | 10.4% | 9.8% | 9.9% | 10.2% | 10.2% · 9.9% · 9.6% | 9.9% |
| Top 2 | 9.1% | 9.8% | 9.8% | 10.0% | 10.0% · 10.2% · 10.3% | 10.2% |
| Top 3 | 8.7% | 9.4% | 9.8% | 10.1% | 10.1% · 10.2% · 10.2% | 10.1% |
| Top 5 | 9.6% | 9.6% | 9.9% | 10.0% | 10.0% · 10.0% · 10.2% | 10.0% |
| Đáy 2 | 9.8% | 9.9% | 9.9% | 10.0% | 10.0% · 10.1% · 9.8% | 10.0% |
| Đáy 3 | 10.4% | 10.2% | 10.1% | 10.1% | 10.1% · 10.1% · 9.8% | 10.0% |
| Đáy 5 | 10.4% | 10.4% | 10.1% | 10.0% | 10.0% · 10.0% · 9.8% | 10.0% |

| Số lần ra kỳ trước | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 3 đoạn 100 kỳ (gần → xa) | Cả lịch sử |
|---|---|---|---|---|---|---|
| 0–3 lần | 10.1% | 9.7% | 10.0% | 10.1% | 10.1% · 9.8% · 10.2% | 10.0% (656 kỳ) |
| 4 lần | 11.4% | 10.7% | 10.5% | 10.4% | 10.4% · 9.8% · 10.2% | 10.0% (609 kỳ) |
| 5 lần | 10.9% | 9.8% | 9.6% | 9.7% | 9.7% · 10.0% · 10.0% | 10.0% (637 kỳ) |
| 6 lần (TB) | 10.7% | 10.2% | 10.3% | 9.9% | 9.9% · 9.9% · 10.0% | 10.0% (653 kỳ) |
| 7 lần | 10.3% | 9.9% | 10.2% | 10.0% | 10.0% · 10.1% · 9.6% | 9.8% (616 kỳ) |
| 8 lần | 7.7% | 9.7% | 9.7% | 10.2% | 10.2% · 9.8% · 10.0% | 9.9% (552 kỳ) |
| ≥9 lần | 8.9% | 9.8% | 9.6% | 9.7% | 9.7% · 10.5% · 9.9% | 10.2% (687 kỳ) |

## Max 3D Pro ← kỳ trước cùng game (782 cặp kỳ)

| Nhóm | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 3 đoạn 100 kỳ (gần → xa) | Cả lịch sử |
|---|---|---|---|---|---|---|
| Hạng 1 | 10.6% | 9.9% | 10.2% | 10.1% | 10.1% · 9.9% · 10.0% | 10.1% |
| Hạng 2 | 9.7% | 8.6% | 9.4% | 9.7% | 9.7% · 9.9% · 10.0% | 10.0% |
| Hạng 3 | 11.0% | 10.4% | 10.4% | 10.5% | 10.5% · 10.3% · 9.9% | 10.1% |
| Hạng 4 | 10.0% | 9.8% | 10.5% | 10.1% | 10.1% · 9.8% · 10.4% | 10.0% |
| Hạng 5 | 10.1% | 9.8% | 10.1% | 10.3% | 10.3% · 10.0% · 10.0% | 10.0% |
| Hạng 6 | 9.6% | 9.7% | 9.8% | 10.2% | 10.2% · 10.0% · 9.8% | 10.0% |
| Hạng 7 | 9.1% | 10.3% | 9.8% | 9.6% | 9.6% · 9.8% · 9.7% | 10.0% |
| Hạng 8 | 9.3% | 10.3% | 9.9% | 10.0% | 10.0% · 9.8% · 10.1% | 10.0% |
| Hạng 9 | 10.9% | 11.0% | 10.2% | 10.1% | 10.1% · 9.8% · 9.9% | 9.9% |
| Hạng 10 | 9.8% | 10.3% | 9.7% | 9.5% | 9.5% · 10.7% · 10.2% | 10.1% |
| Top 2 | 10.2% | 9.2% | 9.8% | 9.9% | 9.9% · 9.9% · 10.0% | 10.0% |
| Top 3 | 10.4% | 9.6% | 10.0% | 10.1% | 10.1% · 10.1% · 10.0% | 10.0% |
| Top 5 | 10.3% | 9.7% | 10.1% | 10.1% | 10.1% · 10.0% · 10.1% | 10.0% |
| Đáy 2 | 10.3% | 10.6% | 10.0% | 9.8% | 9.8% · 10.3% · 10.0% | 10.0% |
| Đáy 3 | 10.0% | 10.5% | 9.9% | 9.8% | 9.8% · 10.1% · 10.1% | 10.0% |
| Đáy 5 | 9.7% | 10.3% | 9.9% | 9.9% | 9.9% · 10.0% · 9.9% | 10.0% |

| Số lần ra kỳ trước | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 3 đoạn 100 kỳ (gần → xa) | Cả lịch sử |
|---|---|---|---|---|---|---|
| 0–3 lần | 10.1% | 10.5% | 9.8% | 9.9% | 9.9% · 10.2% · 10.6% | 10.1% (658 kỳ) |
| 4 lần | 11.9% | 11.2% | 9.9% | 10.0% | 10.0% · 9.7% · 9.9% | 10.0% (611 kỳ) |
| 5 lần | 10.1% | 10.4% | 10.1% | 9.9% | 9.9% · 9.6% · 9.6% | 10.0% (640 kỳ) |
| 6 lần (TB) | 9.5% | 9.0% | 9.9% | 10.0% | 10.0% · 9.8% · 9.8% | 9.9% (656 kỳ) |
| 7 lần | 10.5% | 10.4% | 10.9% | 10.3% | 10.3% · 10.7% · 10.3% | 10.1% (618 kỳ) |
| 8 lần | 9.5% | 8.8% | 9.5% | 10.0% | 10.0% · 9.8% · 9.5% | 9.8% (556 kỳ) |
| ≥9 lần | 10.2% | 9.5% | 10.0% | 10.0% | 10.0% · 10.0% · 10.3% | 10.1% (690 kỳ) |

## Max 3D Pro ← kỳ trước của Max 3D+ (782 cặp kỳ)

| Nhóm | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 3 đoạn 100 kỳ (gần → xa) | Cả lịch sử |
|---|---|---|---|---|---|---|
| Hạng 1 | 8.5% | 9.0% | 9.5% | 10.1% | 10.1% · 10.0% · 10.2% | 10.2% |
| Hạng 2 | 9.3% | 9.7% | 9.8% | 9.9% | 9.9% · 9.9% · 9.9% | 10.0% |
| Hạng 3 | 10.4% | 10.0% | 10.1% | 10.2% | 10.2% · 10.0% · 9.8% | 9.8% |
| Hạng 4 | 10.3% | 10.0% | 10.3% | 10.3% | 10.3% · 10.6% · 9.8% | 9.9% |
| Hạng 5 | 9.2% | 9.6% | 10.2% | 10.2% | 10.2% · 10.2% · 10.0% | 10.1% |
| Hạng 6 | 9.4% | 10.3% | 10.1% | 10.0% | 10.0% · 10.1% · 10.0% | 10.0% |
| Hạng 7 | 9.0% | 9.7% | 9.8% | 9.7% | 9.7% · 9.9% · 10.3% | 10.1% |
| Hạng 8 | 11.1% | 11.1% | 10.8% | 10.1% | 10.1% · 10.1% · 10.1% | 10.2% |
| Hạng 9 | 10.4% | 10.6% | 10.1% | 10.2% | 10.2% · 9.4% · 9.8% | 9.8% |
| Hạng 10 | 12.3% | 10.1% | 9.3% | 9.4% | 9.4% · 10.0% · 10.1% | 9.9% |
| Top 2 | 8.9% | 9.3% | 9.7% | 10.0% | 10.0% · 9.9% · 10.0% | 10.1% |
| Top 3 | 9.4% | 9.5% | 9.8% | 10.1% | 10.1% · 10.0% · 10.0% | 10.0% |
| Top 5 | 9.6% | 9.6% | 10.0% | 10.1% | 10.1% · 10.1% · 9.9% | 10.0% |
| Đáy 2 | 11.3% | 10.4% | 9.7% | 9.8% | 9.8% · 9.7% · 10.0% | 9.9% |
| Đáy 3 | 11.2% | 10.6% | 10.1% | 9.9% | 9.9% · 9.8% · 10.0% | 10.0% |
| Đáy 5 | 10.4% | 10.4% | 10.0% | 9.9% | 9.9% · 9.9% · 10.1% | 10.0% |

| Số lần ra kỳ trước | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 3 đoạn 100 kỳ (gần → xa) | Cả lịch sử |
|---|---|---|---|---|---|---|
| 0–3 lần | 12.3% | 10.5% | 9.6% | 9.7% | 9.7% · 9.9% · 10.0% | 9.9% (673 kỳ) |
| 4 lần | 10.1% | 10.6% | 10.1% | 9.6% | 9.6% · 10.0% · 10.2% | 9.9% (608 kỳ) |
| 5 lần | 9.1% | 9.6% | 9.5% | 9.6% | 9.6% · 10.0% · 9.8% | 10.1% (652 kỳ) |
| 6 lần (TB) | 8.8% | 10.4% | 10.7% | 10.5% | 10.5% · 10.3% · 10.3% | 10.0% (664 kỳ) |
| 7 lần | 9.6% | 10.2% | 9.8% | 9.8% | 9.8% · 10.1% · 9.4% | 9.7% (604 kỳ) |
| 8 lần | 9.7% | 9.4% | 10.2% | 10.3% | 10.3% · 9.9% · 9.7% | 10.0% (527 kỳ) |
| ≥9 lần | 8.3% | 8.6% | 9.8% | 9.9% | 9.9% · 9.9% · 10.4% | 10.2% (706 kỳ) |

Chia đều 10,0%. Nhiễu 1 chữ số: ±3,9 điểm/kỳ → 10 kỳ ±1,2 · 20 kỳ ±0,9 · 50 kỳ ±0,55 · 100 kỳ ±0,4 · cả lịch sử ±0,1–0,14.

Max 3D+ 05/10/2026: 1:9 · 9:8 · 5:7 · 6:7 · 2:6 · 3:6 · 8:6 · 4:4 · 7:4 · 0:3

Max 3D Pro 03/10/2026: 7:10 · 0:7 · 3:7 · 5:7 · 6:7 · 1:6 · 9:6 · 4:4 · 8:4 · 2:2

Kết luận: không có dấu vết. Cả 4 hướng (3D+→3D+, Pro→3D+, Pro→Pro, 3D+→Pro), mọi hạng 1–10, top/đáy 2/3/5, mọi mức số lần ra: cả lịch sử 9,7–10,2% (trong nhiễu ±0,14). Khung 10–50 kỳ lệch 1–2 điểm nhưng 3 đoạn 100 kỳ không giữ chiều → không dùng để loại/chọn chữ số.


# Keno 20/80 — kiểm nhanh dấu vết (05/10/2026, anh hỏi)

Script: `build/keno_dauvet.py`, dữ liệu `keno.jsonl` của kho vietvudanh/vietlott-data.

Keno: 86492 kỳ (2022-12-04 → 2026-10-05); kỳ vọng 25,0%

| Nhóm | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 3 đoạn 100 kỳ | 5000 kỳ | Cả lịch sử |
|---|---|---|---|---|---|---|---|
| ra kỳ trước | 25.0% | 24.5% | 23.1% | 23.9% | 23.9% · 25.0% · 25.0% | 25.1% | 25.0% |
| vắng ≥5 kỳ | 27.7% | 27.5% | 27.1% | 26.4% | 26.4% · 25.9% · 25.7% | 24.9% | 25.0% |
| vắng ≥10 kỳ | 14.2% | 24.6% | 29.0% | 27.0% | 27.0% · 29.2% · 25.0% | 25.0% | 24.9% |
| vắng ≥15 kỳ | 5.6% | 5.6% | 19.2% | 27.9% | 27.9% · 29.5% · 26.4% | 24.7% | 25.0% |
| 10 nóng nhất 20 kỳ | 27.0% | 23.0% | 23.0% | 25.7% | 25.7% · 23.8% · 24.3% | 25.0% | 25.0% |
| 10 lạnh nhất 20 kỳ | 18.0% | 24.0% | 27.2% | 25.5% | 25.5% · 28.0% · 25.1% | 25.0% | 25.0% |
| 10 nóng nhất 100 kỳ | 25.0% | 21.0% | 25.6% | 23.7% | 23.7% · 22.4% · 25.8% | 25.0% | 25.0% |
| 10 lạnh nhất 100 kỳ | 33.0% | 28.5% | 28.0% | 26.1% | 26.1% · 23.7% · 24.3% | 24.8% | 25.0% |
| 10 nóng nhất 500 kỳ | 23.0% | 24.0% | 22.6% | 23.9% | 23.9% · 22.8% · 27.6% | 25.3% | 25.0% |
| 10 lạnh nhất 500 kỳ | 35.0% | 32.5% | 26.6% | 25.3% | 25.3% · 27.7% · 23.0% | 24.7% | 25.0% |

Tần suất cả lịch sử: lệch lớn nhất z = +3.2 (số 11), nhỏ nhất -1.9 (số 1); ngẫu nhiên 80 số thường trong ±2,5.
Tương quan tần suất nửa đầu ↔ nửa sau: -0.111 (0 = không có số "ruột")

Kết luận: Keno quay bằng máy tính, không có dấu vết. Mọi nhóm (ra kỳ trước, vắng ≥5/10/15, nóng/lạnh 20/100/500 kỳ) ở 5000 kỳ và cả lịch sử đều 24,7–25,3% (kỳ vọng 25%). Khung 10–100 kỳ lệch vài điểm nhưng không giữ qua 3 đoạn. Không có số "ruột": tần suất nửa đầu ↔ nửa sau tương quan −0,11.


# Keno — cơ cấu giải các bậc và chấm cách chọn bậc 7–10 (05/10/2026, anh)

Bảng giải lấy từ các trang hướng dẫn (vietlott.vn bị chặn, tra qua tìm kiếm); kiểm bằng xác suất: mọi bậc trả ~55% → các số khớp nhau. Chẵn/Lẻ (1 bên): 11–12 số 20.000, 13–14 số 40.000, ≥15 số 200.000 (trả ~57%); Hòa (10–10) 26.000 (theo nguồn). Lớn/Nhỏ: chưa xác nhận được mức thưởng. Script `build/keno_bac.py`.

## Lý thuyết mỗi bậc (vé 10.000đ)

| Bậc | Trả thưởng TB | % kỳ có giải | Giải thường gặp nhất |
|---|---|---|---|
| 10 | 55.2% | 11.0% | trúng 5: 20,000đ (5.1%) |
| 9 | 54.7% | 21.7% | trúng 4: 10,000đ (11.4%) |
| 8 | 54.7% | 19.1% | trúng 0: 10,000đ (8.8%) |
| 7 | 55.1% | 23.7% | trúng 3: 10,000đ (17.5%) |
| 6 | 54.5% | 16.2% | trúng 3: 10,000đ (13.0%) |
| 5 | 54.9% | 9.7% | trúng 3: 10,000đ (8.4%) |
| 4 | 55.1% | 25.9% | trúng 2: 10,000đ (21.3%) |
| 3 | 55.5% | 15.3% | trúng 2: 20,000đ (13.9%) |
| 2 | 54.1% | 6.0% | trúng 2: 90,000đ (6.0%) |
| 1 | 50.0% | 25.0% | trúng 1: 20,000đ (25.0%) |

## Bậc 7 — tiền về / tiền bỏ (kỳ vọng 55.1%) · % kỳ có giải

| Cách chọn | 100 kỳ | 1000 kỳ | 10000 kỳ | Cả lịch sử | % kỳ có giải (cả LS) | TB số trúng (kỳ vọng 1.75) |
|---|---|---|---|---|---|---|
| nóng 100 kỳ | 37% | 69% | 52% | 64% | 23.7% | 1.748 |
| lạnh 100 kỳ | 165% | 49% | 47% | 45% | 23.6% | 1.750 |
| nóng 20 kỳ | 42% | 33% | 49% | 59% | 23.6% | 1.748 |
| vắng lâu nhất | 64% | 56% | 47% | 44% | 23.6% | 1.750 |
| cố định 1–n | 44% | 38% | 44% | 49% | 23.5% | 1.744 |

## Bậc 8 — tiền về / tiền bỏ (kỳ vọng 54.7%) · % kỳ có giải

| Cách chọn | 100 kỳ | 1000 kỳ | 10000 kỳ | Cả lịch sử | % kỳ có giải (cả LS) | TB số trúng (kỳ vọng 2.00) |
|---|---|---|---|---|---|---|
| nóng 100 kỳ | 34% | 42% | 44% | 48% | 19.1% | 1.997 |
| lạnh 100 kỳ | 84% | 33% | 38% | 44% | 18.8% | 2.001 |
| nóng 20 kỳ | 32% | 25% | 45% | 44% | 19.1% | 1.998 |
| vắng lâu nhất | 125% | 51% | 50% | 44% | 19.1% | 1.999 |
| cố định 1–n | 26% | 34% | 47% | 46% | 19.0% | 1.995 |

## Bậc 9 — tiền về / tiền bỏ (kỳ vọng 54.7%) · % kỳ có giải

| Cách chọn | 100 kỳ | 1000 kỳ | 10000 kỳ | Cả lịch sử | % kỳ có giải (cả LS) | TB số trúng (kỳ vọng 2.25) |
|---|---|---|---|---|---|---|
| nóng 100 kỳ | 29% | 35% | 44% | 46% | 21.8% | 2.250 |
| lạnh 100 kỳ | 62% | 39% | 46% | 46% | 21.4% | 2.251 |
| nóng 20 kỳ | 41% | 31% | 47% | 46% | 21.7% | 2.247 |
| vắng lâu nhất | 57% | 46% | 59% | 49% | 21.7% | 2.248 |
| cố định 1–n | 41% | 36% | 44% | 50% | 21.6% | 2.247 |

## Bậc 10 — tiền về / tiền bỏ (kỳ vọng 55.2%) · % kỳ có giải

| Cách chọn | 100 kỳ | 1000 kỳ | 10000 kỳ | Cả lịch sử | % kỳ có giải (cả LS) | TB số trúng (kỳ vọng 2.50) |
|---|---|---|---|---|---|---|
| nóng 100 kỳ | 27% | 31% | 49% | 45% | 11.1% | 2.502 |
| lạnh 100 kỳ | 42% | 40% | 43% | 43% | 10.9% | 2.501 |
| nóng 20 kỳ | 22% | 20% | 34% | 36% | 11.0% | 2.497 |
| vắng lâu nhất | 31% | 29% | 56% | 41% | 11.0% | 2.497 |
| cố định 1–n | 37% | 30% | 47% | 44% | 10.9% | 2.496 |

Dữ liệu: 86492 kỳ (2022-12-04 → 2026-10-05). Tiền về 1 kỳ dao động rất mạnh (giải lớn hiếm) → khung 100–1000 kỳ có thể lệch hàng chục %; TB số trúng mới là thước đo ổn định.

Kết luận: TB số trúng của mọi cách chọn bằng đúng kỳ vọng (n/4) tới 3 chữ số thập phân → không cách chọn nào hơn. Tiền về thực tế 36–64% (thấp hơn 55% vì chưa ai trong các cách thử trúng giải lớn; giải lớn quyết định phần lớn tỉ lệ trả).


# Keno — kiểm kỹ 10 kỳ gần nhất, ra lặp lại? (05/10/2026, anh)

Script `build/keno_10ky.py`.

## 1. 10 kỳ gần nhất — trùng với kỳ trước (kỳ vọng 5,0 số)

| Kỳ | Ngày | 20 số | Trùng kỳ trước | Số trùng | Trùng 1 trong 2–3 kỳ trước |
|---|---|---|---|---|---|
| #0298136 | 2026-10-05 | 02 11 12 19 20 29 31 32 36 37 39 41 46 47 49 52 60 66 75 80 | **0** |  | 9 |
| #0298137 | 2026-10-05 | 03 05 06 09 11 15 20 24 26 27 30 33 43 50 54 58 61 67 73 76 | **2** | 11 20 | 9 |
| #0298138 | 2026-10-05 | 04 05 09 10 11 12 18 20 25 28 35 47 50 54 64 66 71 72 74 75 | **6** | 05 09 11 20 50 54 | 7 |
| #0298139 | 2026-10-05 | 06 08 10 12 14 18 19 20 28 30 45 48 51 52 64 66 69 71 74 79 | **9** | 10 12 18 20 28 64 66 71 74 | 4 |
| #0298140 | 2026-10-05 | 03 10 13 17 18 23 28 30 33 35 39 50 51 60 61 64 65 69 72 80 | **7** | 10 18 28 30 51 64 69 | 6 |
| #0298141 | 2026-10-05 | 06 20 24 26 27 31 33 34 37 38 39 40 44 49 51 56 58 59 61 70 | **4** | 33 39 51 61 | 2 |
| #0298142 | 2026-10-05 | 01 02 05 14 15 16 19 20 26 29 32 36 39 42 45 53 58 61 79 80 | **5** | 20 26 39 58 61 | 5 |
| #0298143 | 2026-10-05 | 03 04 09 12 14 16 19 21 29 39 47 49 50 54 59 67 71 72 77 80 | **6** | 14 16 19 29 39 80 | 5 |
| #0298144 | 2026-10-05 | 01 03 16 18 23 29 30 34 35 43 45 47 50 65 66 67 70 71 74 80 | **8** | 03 16 29 47 50 67 71 80 | 4 |
| #0298145 | 2026-10-05 | 07 08 11 14 16 17 20 22 25 27 28 30 33 36 42 46 49 51 65 79 | **3** | 16 30 65 | 6 |

TB trùng kỳ trước: 10 kỳ gần 5.00 · 100 kỳ 4.79 · cả lịch sử 4.997 (kỳ vọng 5,000; 10 kỳ dao động ±0,6)

## 2. Số ra trong 10 kỳ gần nhất (kỳ vọng 2,5 lần)

- 7 lần (1 số): 20
- 5 lần (4 số): 30 39 50 80
- 4 lần (16 số): 03 11 12 14 16 18 19 28 29 33 47 49 51 61 66 71
- 3 lần (17 số): 05 06 09 10 26 27 35 36 45 54 58 64 65 67 72 74 79
- 2 lần (22 số): 01 02 04 08 15 17 23 24 25 31 32 34 37 42 43 46 52 59 60 69 70 75
- 1 lần (14 số): 07 13 21 22 38 40 41 44 48 53 56 73 76 77
- 0 lần (6 số): 55 57 62 63 68 78

So với ngẫu nhiên (số lượng số ra k lần): 0: 6 (≈4.5) · 1: 14 (≈15.0) · 2: 22 (≈22.5) · 3: 17 (≈20.0) · 4: 16 (≈11.7) · 5: 4 (≈4.7) · 6: 0 (≈1.3) · 7: 1 (≈0.2)

## 3. Luật: số ra nhiều/ít trong 10 kỳ → kỳ kế (kỳ vọng 25,0%)

| Ra trong 10 kỳ trước | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 3 đoạn 100 kỳ | 5000 kỳ | Cả lịch sử |
|---|---|---|---|---|---|---|---|
| ≥5 lần | 31.3% | 21.0% | 23.5% | 24.9% | 24.9% · 26.0% · 24.1% | 25.2% | 25.0% |
| 4 lần | 23.8% | 25.3% | 23.4% | 26.0% | 26.0% · 23.1% · 26.7% | 25.3% | 24.9% |
| 3 lần | 30.3% | 26.5% | 23.9% | 24.4% | 24.4% · 24.8% · 24.0% | 25.1% | 25.0% |
| 2 lần | 21.4% | 23.2% | 25.0% | 23.7% | 23.7% · 25.4% · 24.2% | 24.8% | 25.0% |
| 1 lần | 26.6% | 28.3% | 27.8% | 26.7% | 26.7% · 25.5% · 27.3% | 25.0% | 25.0% |
| 0 lần | 14.2% | 24.6% | 29.0% | 27.0% | 27.0% · 29.2% · 25.0% | 25.0% | 25.0% |

Kết luận: 10 kỳ gần trùng kỳ trước TB 5,00 (đúng kỳ vọng). Số 20 ra 7/10 kỳ: 1 số bất kỳ ra ≥7/10 xác suất 0,35%, nhưng trong 80 số thì ~25% lần có ít nhất 1 số như vậy → bình thường. Luật "ra nhiều/ít trong 10 kỳ → kỳ kế" ở 5000 kỳ và cả lịch sử 24,8–25,3% → không có lặp lại.


# Keno — chép số kỳ trước mua kỳ sau (05/10/2026, anh: "cũng tính là vết")

Phát hiện: kho keno.jsonl có 26 kỳ bị ghi 2 dòng (cùng mã kỳ) → lần chạy đầu ra 26 lần "trúng 9/9" giả. Đã bỏ trùng trong keno_dauvet/keno_bac/keno_10ky/keno_chep (kết quả cũ gần như không đổi). Script `build/keno_chep.py`.

Dữ liệu 86466 kỳ. Kỳ sau trùng ≥9 số với kỳ trước: thực tế 1750 lần, lý thuyết 1818

| Cách | Bậc | Trúng hết (thực tế / kỳ vọng) | Trúng thiếu 1 (thực tế / kỳ vọng) | TB số trúng (kỳ vọng) | Tiền về |
|---|---|---|---|---|---|
| chép n số đầu kỳ trước | 7 | 1 / 2.11 | 50 / 63.3 | 1.750 (1.75) | 48% |
| chép n số đầu kỳ trước | 8 | 1 / 0.38 | 13 / 13.9 | 1.999 (2.00) | 66% |
| chép n số đầu kỳ trước | 9 | 0 / 0.06 | 6 / 2.8 | 2.249 (2.25) | 50% |
| chép n số đầu kỳ trước | 10 | 0 / 0.01 | 0 / 0.5 | 2.499 (2.50) | 41% |
| chép số kỳ trước, ưu tiên số vừa lặp + nóng 10 kỳ | 7 | 0 / 2.11 | 74 / 63.3 | 1.745 (1.75) | 47% |
| chép số kỳ trước, ưu tiên số vừa lặp + nóng 10 kỳ | 8 | 0 / 0.38 | 14 / 13.9 | 1.999 (2.00) | 46% |
| chép số kỳ trước, ưu tiên số vừa lặp + nóng 10 kỳ | 9 | 0 / 0.06 | 1 / 2.8 | 2.247 (2.25) | 46% |
| chép số kỳ trước, ưu tiên số vừa lặp + nóng 10 kỳ | 10 | 0 / 0.01 | 0 / 0.5 | 2.494 (2.50) | 43% |

Kết luận: kỳ sau trùng ≥9 số với kỳ trước 1750 lần (lý thuyết 1818) — không lặp nhiều hơn ngẫu nhiên. Chép số kỳ trước: trúng hết và trúng thiếu 1 ngang kỳ vọng, TB số trúng đúng n/4. Chơi 100 vé bậc 9: cơ hội có 1 lần 9/9 ≈ 1/13.800.


# Keno — anh dừng (06/10/2026)

Vé thử 4 kỳ (#298244, #298246): loại 3 kỳ TB 2,7 số/vé, tâm linh 3,0, kết hợp 3,0 (kỳ vọng 2,25); vé anh mua thật 4/9 → hoàn 10k (hòa vốn). Anh: "bỏ keno đi, khó nhai" → ngừng.


# Max 3D Pro — lộn ĐB theo độ trễ (06/10/2026, anh hỏi "lộn ngay sau kỳ trước á")

| Lộn ĐB của kỳ cách | Cả lịch sử | 300 kỳ gần |
|---|---|---|
| 1 kỳ (kỳ trước) | 2,43% ×1,22 (38 lần) | ×1,68 |
| 2 kỳ | 2,94% ×1,48 (46 lần) | ×1,26 |
| 3 kỳ | 2,30% ×1,16 | ×1,26 |
| 4 kỳ | 1,60% ×0,81 | ×0,42 |
| 5 kỳ | 1,41% ×0,71 | ×0,59 |

Bộ lộn của ĐB hay ra trong 1–3 kỳ sau, sau đó ra ít. Chia đều 1,98%/bộ.


# Loto — số May Mắn theo khoảng 3/4/6 (06/10/2026, anh)

Script `build/loto_mm_khoang.py`.

## Chia 3 khoảng: 1–4 · 5–8 · 9–12 (chia đều 33.3%)

Cả lịch sử mỗi khoảng: 1–4: 33.5% · 5–8: 32.3% · 9–12: 34.2%
100 kỳ gần: 36% · 32% · 32%

| Cách chọn 1 khoảng | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 200 kỳ | 3 đoạn 100 kỳ (gần→xa) | Cả LS | Kỳ tới |
|---|---|---|---|---|---|---|---|---|
| Khoảng kỳ trước (lặp lại) | 60% | 35% | 28% | 29% | 34% | 29% · 39% · 42% | 33% | 1–4 |
| Khoảng kỳ t−2 | 30% | 35% | 32% | 36% | 35% | 36% · 34% · 28% | 33% | 1–4 |
| Nhiều nhất 10 kỳ | 40% | 30% | 30% | 38% | 34% | 38% · 29% · 39% | 33% | 1–4 |
| Nhiều nhất 20 kỳ | 50% | 45% | 42% | 38% | 34% | 38% · 30% · 30% | 33% | 1–4 |
| Nhiều nhất 50 kỳ | 50% | 45% | 30% | 33% | 30% | 33% · 26% · 29% | 33% | 1–4 |
| Nhiều nhất 100 kỳ | 40% | 40% | 30% | 34% | 28% | 34% · 23% · 32% | 33% | 1–4 |
| Ít nhất 10 kỳ | 30% | 45% | 40% | 35% | 34% | 35% · 32% · 31% | 31% | 9–12 |
| Ít nhất 20 kỳ | 20% | 25% | 34% | 30% | 31% | 30% · 32% · 30% | 32% | 9–12 |
| Ít nhất 50 kỳ | 20% | 30% | 38% | 36% | 36% | 36% · 35% · 45% | 36% | 9–12 |
| Vắng lâu nhất | 30% | 40% | 40% | 36% | 32% | 36% · 28% · 33% | 34% | 5–8 |
| Hay theo sau khoảng kỳ trước (200 kỳ) | 20% | 30% | 26% | 27% | 33% | 27% · 39% · 29% | 34% | 9–12 |
| Nhiều nhất cùng phiên (13h/21h) | 30% | 15% | 22% | 35% | 32% | 35% · 30% · 26% | 31% | 5–8 |

## Chia 4 khoảng: 1–3 · 4–6 · 7–9 · 10–12 (chia đều 25.0%)

Cả lịch sử mỗi khoảng: 1–3: 25.9% · 4–6: 22.7% · 7–9: 26.0% · 10–12: 25.3%
100 kỳ gần: 29% · 23% · 23% · 25%

| Cách chọn 1 khoảng | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 200 kỳ | 3 đoạn 100 kỳ (gần→xa) | Cả LS | Kỳ tới |
|---|---|---|---|---|---|---|---|---|
| Khoảng kỳ trước (lặp lại) | 30% | 20% | 28% | 28% | 28% | 28% · 29% · 34% | 27% | 1–3 |
| Khoảng kỳ t−2 | 30% | 30% | 22% | 23% | 26% | 23% · 28% · 23% | 24% | 1–3 |
| Nhiều nhất 10 kỳ | 30% | 35% | 26% | 28% | 27% | 28% · 26% · 31% | 26% | 1–3 |
| Nhiều nhất 20 kỳ | 40% | 35% | 28% | 29% | 29% | 29% · 29% · 21% | 24% | 1–3 |
| Nhiều nhất 50 kỳ | 40% | 40% | 30% | 25% | 24% | 25% · 22% · 19% | 23% | 1–3 |
| Nhiều nhất 100 kỳ | 60% | 50% | 32% | 29% | 28% | 29% · 27% · 15% | 26% | 1–3 |
| Ít nhất 10 kỳ | 50% | 30% | 30% | 25% | 24% | 25% · 23% · 26% | 26% | 10–12 |
| Ít nhất 20 kỳ | 10% | 15% | 24% | 21% | 20% | 21% · 19% · 17% | 22% | 4–6 |
| Ít nhất 50 kỳ | 30% | 20% | 26% | 22% | 22% | 22% · 22% · 20% | 22% | 7–9 |
| Vắng lâu nhất | 30% | 30% | 32% | 31% | 28% | 31% · 26% · 21% | 27% | 7–9 |
| Hay theo sau khoảng kỳ trước (200 kỳ) | 40% | 25% | 26% | 26% | 28% | 26% · 29% · 21% | 27% | 1–3 |
| Nhiều nhất cùng phiên (13h/21h) | 30% | 20% | 12% | 16% | 19% | 16% · 22% · 15% | 23% | 7–9 |

## Chia 6 khoảng: 1–2 · 3–4 · 5–6 · 7–8 · 9–10 · 11–12 (chia đều 16.7%)

Cả lịch sử mỗi khoảng: 1–2: 16.8% · 3–4: 16.7% · 5–6: 15.2% · 7–8: 17.1% · 9–10: 17.5% · 11–12: 16.7%
100 kỳ gần: 20% · 16% · 16% · 16% · 15% · 17%

| Cách chọn 1 khoảng | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 200 kỳ | 3 đoạn 100 kỳ (gần→xa) | Cả LS | Kỳ tới |
|---|---|---|---|---|---|---|---|---|
| Khoảng kỳ trước (lặp lại) | 10% | 5% | 8% | 10% | 14% | 10% · 19% · 32% | 17% | 3–4 |
| Khoảng kỳ t−2 | 20% | 20% | 12% | 17% | 18% | 17% · 18% · 19% | 18% | 1–2 |
| Nhiều nhất 10 kỳ | 10% | 10% | 18% | 21% | 18% | 21% · 16% · 15% | 17% | 1–2 |
| Nhiều nhất 20 kỳ | 0% | 10% | 14% | 14% | 14% | 14% · 13% · 17% | 16% | 3–4 |
| Nhiều nhất 50 kỳ | 10% | 10% | 14% | 13% | 16% | 13% · 18% · 13% | 18% | 3–4 |
| Nhiều nhất 100 kỳ | 30% | 20% | 18% | 17% | 18% | 17% · 19% · 11% | 17% | 1–2 |
| Ít nhất 10 kỳ | 20% | 25% | 30% | 25% | 20% | 25% · 14% · 18% | 18% | 5–6 |
| Ít nhất 20 kỳ | 20% | 15% | 22% | 20% | 16% | 20% · 13% · 15% | 16% | 9–10 |
| Ít nhất 50 kỳ | 20% | 30% | 28% | 23% | 16% | 23% · 10% · 20% | 17% | 11–12 |
| Vắng lâu nhất | 30% | 35% | 30% | 26% | 22% | 26% · 17% · 18% | 18% | 9–10 |
| Hay theo sau khoảng kỳ trước (200 kỳ) | 10% | 20% | 24% | 16% | 17% | 16% · 18% · 22% | 17% | 5–6 |
| Nhiều nhất cùng phiên (13h/21h) | 10% | 20% | 20% | 16% | 18% | 16% · 21% · 14% | 18% | 3–4 |

Ngẫu nhiên: khung 100 kỳ dao động ±5 (3 khoảng) · ±4 (4 khoảng) · ±4 (6 khoảng) điểm; 10 kỳ ±15 điểm.

Kết luận: không có cách chọn khoảng nào trên mức ở cả 3 đoạn 100 kỳ. Tần suất từng khoảng cả lịch sử sát chia đều (3 khoảng 32–34%, 4 khoảng 23–26%, 6 khoảng 15–18%). Đáng chú ý nhẹ: 6 khoảng — MM ít lặp lại khoảng kỳ trước ở 100 kỳ gần (10%, chia đều 17%) nhưng đoạn xa lại 32% → không ổn định; khớp luật cũ "loại MM vừa ra kỳ trước". Gợi ý thực dụng cho 5 vé: rải 5 MM khác nhau (phủ 5/12 = 42%) thay vì dồn 1 khoảng.


# Theo dõi quẻ ngày tháng (dương, âm, năm) — Power / Mega / Loto

Mỗi số trong nhóm ra % (chia đều = 6/55 Power 10,9% · 6/45 Mega 13,3% · 5/35 Loto 14,3%). "≥2 số" = % kỳ có từ 2 số của nhóm ra, so với ngẫu nhiên.

## POWER — 1003 kỳ (07/03/2020 → 06/10/2026)

| Nhóm | Mỗi số ra: 50 kỳ · 100 kỳ · cả LS | 3 đoạn 100 kỳ | Kỳ có ≥2 số (thực / ngẫu nhiên) | Kỳ có ≥3 số (thực / ngẫu nhiên) |
|---|---|---|---|---|
| Dương: thứ–ngày–tháng | 14.6% · 12.2% · 10.5% | 12.2% · 12.4% · 11.6% | 19 / 26.1 | 1 / 0.7 |
| Dương + năm (26) | 12.4% · 12.3% · 10.7% | 12.3% · 10.9% · 11.1% | 46 / 50.0 | 1 / 2.5 |
| Âm: ngày–tháng | 10.0% · 10.0% · 13.2% | 10.0% · 14.1% · 14.8% | 15 / 9.8 | 0 / 0.0 |
| Âm + năm | 8.8% · 10.2% · 12.6% | 10.2% · 11.6% · 12.7% | 33 / 27.4 | 3 / 0.7 |
| Tất cả (dương + âm + năm) | 11.5% · 11.5% · 11.6% | 11.5% · 12.3% · 11.8% | 116 / 108.1 | 16 / 10.9 |

Chia đều 10.9%. Kỳ gần đây ra ≥3 số ngày tháng: 22/02/2025: 01 02 07 22 23 46; 24/07/2025: 05 10 24 29 30 34; 28/10/2025: 06 08 10 22 25 54; 27/11/2025: 04 05 10 11 28 35; 21/02/2026: 05 07 26 30 41 45
**Kỳ tới 08/10/2026** (âm 28/8): dương 05 08 10 26 · âm 08 26 28

## MEGA — 1003 kỳ (15/03/2020 → 07/10/2026)

| Nhóm | Mỗi số ra: 50 kỳ · 100 kỳ · cả LS | 3 đoạn 100 kỳ | Kỳ có ≥2 số (thực / ngẫu nhiên) | Kỳ có ≥3 số (thực / ngẫu nhiên) |
|---|---|---|---|---|
| Dương: thứ–ngày–tháng | 10.6% · 10.3% · 12.4% | 10.3% · 13.1% · 13.8% | 31 / 38.9 | 2 / 1.2 |
| Dương + năm (26) | 12.2% · 11.6% · 12.5% | 11.6% · 12.1% · 14.0% | 61 / 73.8 | 3 / 4.7 |
| Âm: ngày–tháng | 15.6% · 14.0% · 13.2% | 14.0% · 13.8% · 10.1% | 17 / 14.7 | 0 / 0.0 |
| Âm + năm | 15.2% · 14.0% · 13.0% | 14.0% · 12.2% · 11.1% | 48 / 41.3 | 0 / 1.3 |
| Tất cả (dương + âm + năm) | 12.7% · 12.1% · 12.8% | 12.1% · 12.7% · 12.9% | 160 / 154.9 | 18 / 19.6 |

Chia đều 13.3%. Kỳ gần đây ra ≥3 số ngày tháng: 13/09/2023: 02 04 07 09 12 13; 30/06/2024: 05 23 25 28 30 43; 16/10/2024: 04 14 19 23 24 37; 19/11/2025: 09 12 19 30 40 43; 04/02/2026: 02 12 14 17 39 43
**Kỳ tới 09/10/2026** (âm 29/8): dương 06 09 10 26 · âm 08 26 29

## LOTO — 931 kỳ (29/06/2025 → 07/10/2026 21h)

| Nhóm | Mỗi số ra: 50 kỳ · 100 kỳ · cả LS | 3 đoạn 100 kỳ | Kỳ có ≥2 số (thực / ngẫu nhiên) | Kỳ có ≥3 số (thực / ngẫu nhiên) |
|---|---|---|---|---|
| Dương: thứ–ngày–tháng | 18.7% · 16.3% · 14.7% | 16.3% · 13.8% · 13.4% | 45 / 40.1 | 4 / 1.2 |
| Dương + năm (26) | 14.6% · 14.4% · 14.7% | 14.4% · 13.2% · 14.7% | 83 / 76.0 | 6 / 4.7 |
| Âm: ngày–tháng | 9.2% · 11.7% · 13.6% | 11.7% · 15.7% · 12.8% | 9 / 15.1 | 0 / 0.0 |
| Âm + năm | 6.8% · 11.0% · 14.0% | 11.0% · 14.3% · 15.1% | 37 / 42.1 | 4 / 1.3 |
| Tất cả (dương + âm + năm) | 13.0% · 13.5% · 14.4% | 13.5% · 14.4% · 14.4% | 163 / 164.7 | 21 / 21.1 |

Chia đều 14.3%. Kỳ gần đây ra ≥3 số ngày tháng: 13/08/2026 21h: 01 07 17 26 32; 09/09/2026 13h: 04 07 09 13 33; 28/09/2026 13h: 02 07 09 14 28; 01/10/2026 13h: 01 08 10 24 32; 07/10/2026 21h: 04 07 10 14 17
**Kỳ tới 08/10/2026 13h** (âm 28/8): dương 05 08 10 26 · âm 08 26 28



# Loto — quẻ ngày tháng chi tiết (931 kỳ, 29/06/2025 13h → 07/10/2026 21h)

Mỗi số ra bao nhiêu % (chia đều 14.3%). Số ngoài 1–35 bỏ qua.

| Thành phần | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 3 đoạn 100 kỳ (gần→xa) | Cả LS | 13h (cả LS) | 21h (cả LS) | Kỳ tới |
|---|---|---|---|---|---|---|---|---|---|
| Thứ (T2=2…CN=8) | 10.0% | 15.0% | 20.0% | 13.0% | 13.0% · 12.0% · 8.0% | 14.6% | 15.7% | 13.5% | 05 |
| Ngày dương | 10.0% | 15.0% | 18.0% | 18.0% | 18.0% · 16.0% · 17.0% | 14.0% | 14.2% | 13.7% | 08 |
| Tháng dương | 30.0% | 30.0% | 18.0% | 18.0% | 18.0% · 11.0% · 15.0% | 15.6% | 15.7% | 15.5% | 10 |
| Năm (26) | 10.0% | 5.0% | 2.0% | 9.0% | 9.0% · 11.0% · 19.0% | 15.4% | 15.9% | 14.8% | 26 |
| Ngày âm | 0.0% | 0.0% | 2.0% | 6.0% | 6.0% · 16.0% · 10.0% | 13.1% | 12.7% | 13.5% | 28 |
| Tháng âm | 0.0% | 15.0% | 16.0% | 17.0% | 17.0% · 16.0% · 16.0% | 13.9% | 13.8% | 13.9% | 08 |
| Năm âm (26) | 10.0% | 5.0% | 2.0% | 9.0% | 9.0% · 11.0% · 19.0% | 14.9% | 14.6% | 15.2% | 26 |
| Thứ + ngày | 20.0% | 10.0% | 22.0% | 19.8% | 19.8% · 15.3% · 14.9% | 16.0% | 15.2% | 16.7% | 13 |
| Thứ + tháng | 20.0% | 15.0% | 10.0% | 8.0% | 8.0% · 17.0% · 13.0% | 13.4% | 13.1% | 13.7% | 15 |
| Ngày + tháng | 30.0% | 28.6% | 19.0% | 17.9% | 17.9% · 18.5% · 14.3% | 14.9% | 14.5% | 15.2% | 18 |
| Thứ + ngày + tháng | 20.0% | 14.3% | 9.4% | 12.5% | 12.5% · 9.8% · 15.4% | 14.4% | 15.9% | 13.0% | 23 |
| Ngày âm + tháng âm | 20.0% | 15.0% | 12.0% | 10.2% | 10.2% · 15.3% · 13.0% | 14.3% | 15.1% | 13.5% | — |
| NHÓM dương (thứ, ngày, tháng) | 16.7% | 20.0% | 18.7% | 16.3% | 16.3% · 13.8% · 13.4% | 14.7% | 15.1% | 14.3% | 05 08 10 |
| NHÓM dương + tổng (thứ, ngày, tháng, 3 tổng đôi) | 17.2% | 17.0% | 17.2% | 15.2% | 15.2% · 15.7% · 13.7% | 14.7% | 14.5% | 14.8% | 05 08 10 13 15 18 |
| NHÓM âm (ngày, tháng, tổng) | 6.7% | 10.0% | 10.1% | 11.2% | 11.2% · 15.5% · 12.8% | 13.8% | 13.9% | 13.7% | 08 28 |

## Số May Mắn trùng thứ / ngày / tháng (dương, âm) — chỉ tính số 1–12

| Khung | Trúng thực | Kỳ vọng ngẫu nhiên |
|---|---|---|
| 50 kỳ | 15 | 14.3 |
| 100 kỳ | 28 | 28.7 |
| 200 kỳ | 60 | 57.3 |
| Cả lịch sử | 283 | 267.0 |

**Kỳ tới 08/10/2026 13h** (âm 28/8): MM ngày tháng 05 08 10

Kỳ ra từ 3 số trở lên thuộc nhóm "dương + tổng": 06/07/2025 21h: 06 07 13 28 29; 11/07/2025 13h: 08 11 17 18 20; 05/08/2025 21h: 05 08 10 13 32; 09/08/2025 21h: 09 16 17 26 32; 10/08/2025 13h: 08 16 18 28 34; 26/08/2025 21h: 07 11 26 34 35; 02/09/2025 21h: 05 09 12 32 35; 15/10/2025 13h: 01 04 14 15 32; 18/11/2025 21h: 08 11 17 21 29; 22/12/2025 13h: 08 12 14 24 27; 23/12/2025 13h: 03 23 28 32 35; 23/12/2025 21h: 22 23 26 34 35; 25/12/2025 13h: 05 12 25 28 33; 05/01/2026 21h: 01 02 06 10 17; 20/04/2026 21h: 02 06 15 22 28; 21/04/2026 21h: 04 07 18 19 25; 29/06/2026 21h: 08 22 27 31 35; 08/07/2026 13h: 04 08 11 27 34; 13/07/2026 21h: 02 07 09 13 34; 26/08/2026 13h: 03 10 12 26 30; 02/09/2026 21h: 06 07 09 11 32; 09/09/2026 13h: 04 07 09 13 33; 18/09/2026 21h: 02 06 18 24 35; 20/09/2026 13h: 03 08 09 29 31; 28/09/2026 13h: 02 07 09 14 28; 03/10/2026 13h: 01 10 13 15 17; 07/10/2026 21h: 04 07 10 14 17


# POWER — quẻ ngày tháng chi tiết (1003 kỳ, 07/03/2020 → 06/10/2026)

Mỗi số ra bao nhiêu % (chia đều 10.9%). Số ngoài dải bỏ qua.

| Thành phần | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 3 đoạn 100 kỳ (gần→xa) | Cả LS | 13h (cả LS) | 21h (cả LS) | Kỳ tới |
|---|---|---|---|---|---|---|---|---|---|
| Thứ (T2=2…CN=8) | 40.0% | 30.0% | 20.0% | 18.0% | 18.0% · 12.0% · 12.0% | 11.1% | – | – | 05 |
| Ngày dương | 10.0% | 20.0% | 12.0% | 7.0% | 7.0% · 13.0% · 13.0% | 10.5% | – | – | 08 |
| Tháng dương | 10.0% | 15.0% | 10.0% | 10.0% | 10.0% · 12.0% · 9.0% | 9.6% | – | – | 10 |
| Năm (26) | 10.0% | 10.0% | 6.0% | 12.0% | 12.0% · 6.0% · 9.0% | 11.0% | – | – | 26 |
| Ngày âm | 0.0% | 10.0% | 12.0% | 12.0% | 12.0% · 17.0% · 15.0% | 13.0% | – | – | 28 |
| Tháng âm | 0.0% | 5.0% | 8.0% | 8.0% | 8.0% · 12.0% · 14.0% | 13.5% | – | – | 08 |
| Năm âm (26) | 10.0% | 10.0% | 6.0% | 11.0% | 11.0% · 7.0% · 9.0% | 11.2% | – | – | 26 |
| Thứ + ngày | 0.0% | 10.0% | 8.0% | 7.0% | 7.0% · 17.0% · 9.0% | 9.2% | – | – | 13 |
| Thứ + tháng | 0.0% | 5.0% | 6.0% | 8.0% | 8.0% · 8.0% · 9.0% | 8.1% | – | – | 15 |
| Ngày + tháng | 20.0% | 10.0% | 12.0% | 8.0% | 8.0% · 15.0% · 8.0% | 9.3% | – | – | 18 |
| Thứ + ngày + tháng | 10.0% | 5.0% | 10.0% | 11.0% | 11.0% · 10.0% · 9.0% | 11.2% | – | – | 23 |
| Ngày âm + tháng âm | 0.0% | 5.0% | 4.0% | 9.0% | 9.0% · 10.0% · 9.0% | 11.9% | – | – | 36 |
| NHÓM dương (thứ, ngày, tháng) | 20.0% | 21.7% | 14.6% | 12.2% | 12.2% · 12.4% · 11.6% | 10.5% | – | – | 05 08 10 |
| NHÓM dương + tổng (thứ, ngày, tháng, 3 tổng đôi) | 13.6% | 15.1% | 12.1% | 10.3% | 10.3% · 12.5% · 10.4% | 9.9% | – | – | 05 08 10 13 15 18 |
| NHÓM âm (ngày, tháng, tổng) | 0.0% | 6.7% | 8.0% | 9.7% | 9.7% · 12.8% · 12.8% | 12.8% | – | – | 08 28 36 |

**Kỳ tới 08/10/2026** (âm 28/8)

Kỳ ra từ 3 số trở lên thuộc nhóm "dương + tổng" (12 lần gần nhất): 05/07/2022: 05 07 12 26 29 44; 17/06/2023: 07 13 23 34 38 40; 23/03/2024: 03 10 13 30 40 52; 18/05/2024: 12 18 20 25 27 52; 22/02/2025: 01 02 07 22 23 46; 24/06/2025: 03 09 18 20 30 53; 24/07/2025: 05 10 24 29 30 34; 25/04/2026: 04 07 10 29 41 46


# MEGA — quẻ ngày tháng chi tiết (1003 kỳ, 15/03/2020 → 07/10/2026)

Mỗi số ra bao nhiêu % (chia đều 13.3%). Số ngoài dải bỏ qua.

| Thành phần | 10 kỳ | 20 kỳ | 50 kỳ | 100 kỳ | 3 đoạn 100 kỳ (gần→xa) | Cả LS | 13h (cả LS) | 21h (cả LS) | Kỳ tới |
|---|---|---|---|---|---|---|---|---|---|
| Thứ (T2=2…CN=8) | 10.0% | 5.0% | 10.0% | 12.0% | 12.0% · 8.0% · 12.0% | 12.3% | – | – | 06 |
| Ngày dương | 10.0% | 5.0% | 6.0% | 9.0% | 9.0% · 16.0% · 15.0% | 13.2% | – | – | 09 |
| Tháng dương | 20.0% | 20.0% | 16.0% | 11.0% | 11.0% · 14.0% · 12.0% | 11.5% | – | – | 10 |
| Năm (26) | 20.0% | 20.0% | 16.0% | 15.0% | 15.0% · 9.0% · 14.0% | 12.6% | – | – | 26 |
| Ngày âm | 20.0% | 15.0% | 14.0% | 12.0% | 12.0% · 19.0% · 13.0% | 13.9% | – | – | 29 |
| Tháng âm | 0.0% | 0.0% | 16.0% | 15.0% | 15.0% · 9.0% · 7.0% | 12.5% | – | – | 08 |
| Năm âm (26) | 20.0% | 20.0% | 16.0% | 15.0% | 15.0% · 9.0% · 13.0% | 12.5% | – | – | 26 |
| Thứ + ngày | 0.0% | 10.0% | 10.0% | 13.0% | 13.0% · 17.0% · 20.0% | 15.0% | – | – | 15 |
| Thứ + tháng | 20.0% | 15.0% | 8.0% | 13.0% | 13.0% · 9.0% · 19.0% | 14.3% | – | – | 16 |
| Ngày + tháng | 10.0% | 15.0% | 24.0% | 16.0% | 16.0% · 10.0% · 14.0% | 13.2% | – | – | 19 |
| Thứ + ngày + tháng | 0.0% | 10.5% | 14.3% | 13.1% | 13.1% · 13.7% · 14.3% | 13.4% | – | – | 25 |
| Ngày âm + tháng âm | 10.0% | 5.0% | 8.0% | 9.0% | 9.0% · 9.0% · 9.0% | 11.2% | – | – | 37 |
| NHÓM dương (thứ, ngày, tháng) | 13.3% | 10.5% | 10.6% | 10.3% | 10.3% · 13.1% · 13.8% | 12.4% | – | – | 06 09 10 |
| NHÓM dương + tổng (thứ, ngày, tháng, 3 tổng đôi) | 11.7% | 12.3% | 12.5% | 12.3% | 12.3% · 12.6% · 15.8% | 13.4% | – | – | 06 09 10 15 16 19 |
| NHÓM âm (ngày, tháng, tổng) | 10.3% | 6.8% | 13.0% | 12.3% | 12.3% · 12.2% · 9.7% | 12.5% | – | – | 08 29 37 |

**Kỳ tới 09/10/2026** (âm 29/8)

Kỳ ra từ 3 số trở lên thuộc nhóm "dương + tổng" (12 lần gần nhất): 15/01/2023: 08 09 15 21 26 45; 28/07/2023: 07 27 28 30 31 35; 08/09/2023: 06 08 14 29 39 42; 13/09/2023: 02 04 07 09 12 13; 09/08/2024: 06 14 15 24 26 39; 13/10/2024: 07 10 13 17 21 45; 20/11/2024: 04 16 24 29 31 37; 05/02/2025: 04 06 09 14 25 41; 27/04/2025: 08 11 31 35 36 45; 04/05/2025: 06 07 08 09 12 29; 08/10/2025: 08 10 11 18 23 32; 07/01/2026: 01 05 07 28 31 43


# 100 kỳ gần — trùng số ngày tháng mỗi kỳ (07/10/2026)

## POWER — 100 kỳ (14/02/2026 → 06/10/2026), mỗi kỳ nhóm ngày tháng TB 8.1 số

| Trùng | 0 số | 1 số | 2 số | ≥3 số | Tổng số trùng |
|---|---|---|---|---|---|
| Thực tế (số kỳ) | 39 | 43 | 14 | 4 | 83 |
| Ngẫu nhiên | 37 | 42 | 17.5 | 3.7 | 88 |


## MEGA — 100 kỳ (18/02/2026 → 07/10/2026), mỗi kỳ nhóm ngày tháng TB 8.1 số

| Trùng | 0 số | 1 số | 2 số | ≥3 số | Tổng số trùng |
|---|---|---|---|---|---|
| Thực tế (số kỳ) | 36 | 31 | 30 | 3 | 100 |
| Ngẫu nhiên | 28 | 42 | 23.1 | 6.4 | 109 |


## LOTO — 100 kỳ (19/08/2026 13h → 07/10/2026 21h), mỗi kỳ nhóm ngày tháng TB 8.2 số

| Trùng | 0 số | 1 số | 2 số | ≥3 số | Tổng số trùng |
|---|---|---|---|---|---|
| Thực tế (số kỳ) | 34 | 33 | 22 | 11 | 115 |
| Ngẫu nhiên | 24 | 43 | 25.9 | 7.4 | 117 |



# Power / Mega — mua cố định 1 bộ: thử cách chọn bộ (07/10/2026)

## POWER — chọn bộ ở mốc, chấm 100 kỳ sau mốc, 3 mốc (300 kỳ gần). Chọn bừa: TB 0.65 số/kỳ, ≥3 số 4.0 lần/300 kỳ

| Cách chọn bộ cố định | 3 mốc: TB số trúng | ≥3 số (300 kỳ) | Hơn % bộ chọn bừa | Bộ hiện tại (theo toàn bộ dữ liệu) |
|---|---|---|---|---|
| Ra nhiều nhất cả quá khứ | 0.85 · 0.68 · 0.66 | 7 | 96% | 22 34 41 43 48 51 |
| Ra nhiều nhất 100 kỳ gần | 0.76 · 0.67 · 0.68 | 5 | 87% | 01 05 07 08 13 16 |
| Ra ít nhất 100 kỳ gần | 0.66 · 0.56 · 0.74 | 7 | 51% | 06 12 19 35 37 42 |
| Cặp hay đi cùng nhất (gắn kết) | 0.62 · 0.58 · 0.68 | 3 | 25% | 11 22 38 41 43 48 |
| Bộ "trung tâm" (hay trùng ≥3 số với kỳ cũ) | 0.61 · 0.70 · 0.68 | 5 | 59% | 05 11 18 22 43 51 |

## MEGA — chọn bộ ở mốc, chấm 100 kỳ sau mốc, 3 mốc (300 kỳ gần). Chọn bừa: TB 0.80 số/kỳ, ≥3 số 7.2 lần/300 kỳ

| Cách chọn bộ cố định | 3 mốc: TB số trúng | ≥3 số (300 kỳ) | Hơn % bộ chọn bừa | Bộ hiện tại (theo toàn bộ dữ liệu) |
|---|---|---|---|---|
| Ra nhiều nhất cả quá khứ | 0.74 · 0.81 · 0.85 | 9 | 49% | 04 07 10 20 37 41 |
| Ra nhiều nhất 100 kỳ gần | 0.89 · 0.90 · 0.77 | 6 | 87% | 06 16 22 31 36 44 |
| Ra ít nhất 100 kỳ gần | 0.86 · 0.76 · 0.75 | 3 | 39% | 01 05 08 18 34 40 |
| Cặp hay đi cùng nhất (gắn kết) | 0.79 · 0.84 · 0.77 | 7 | 49% | 07 13 20 29 37 44 |
| Bộ "trung tâm" (hay trùng ≥3 số với kỳ cũ) | 0.76 · 0.76 · 0.87 | 4 | 46% | 04 10 13 20 27 37 |

## 08/10/2026 — Cộng/trừ qua nhiều kỳ (Power) → điểm cộng trong goiy.py
- Anh: Power/Mega chỉ xét 100/200/500 kỳ (bi thay liên tục).
- Quét ±d × k kỳ (congtru_*.py, power_ct200.py): bền nhất Power ±1 qua 5 kỳ, ±1/±16 qua 5 kỳ; ±16 đang vào nhịp 200 kỳ gần.
- Gắn vào goiy.py (GOIY_CT/GOIY_CTW): Power mặc định ±1 qua 5 kỳ, +1 điểm. Pool 15: TB 1.80→1.84 (100), 1.75→1.83 (200); ≥3 số 23→24% / 24→28%; ≥4 số 6→7% / 4→7%.
- Mega: số bị luật loại nhưng ±14 (10 kỳ)/±6 (5 kỳ) trỏ tới vẫn ra 14,4–14,8% → đề xuất luật cứu (chưa làm).
- 08/10: Nhân/chia Power (nhanchia.py): ×÷2 qua 3 kỳ ra 12,8% ở 100 kỳ (pool ~13 số, 4 đoạn 25 kỳ đều) nhưng 500 kỳ ≈ TB. Gắn vào goiy (GOIY_NC='2:3', GOIY_NCW): pool 15 không lên (w0 1.78/1.80 → w0.5 1.76/1.75, w1 1.78/1.75 ở 100/200) → để trọng số 0, chỉ theo dõi.
- Power 08/10/2026: 01 07 12 27 31 52 · ĐB 06. Pool 15 trúng 2 (01 27); 5 vé (đã bỏ 07 theo anh) tốt nhất 1; nếu giữ 07: vé 4 trúng 2. Ma trận 12: vé tốt nhất 2. Bộ cố định 01 05 07 08 13 16: 2 (01 07). Luật it100 loại 12 → 12 ra. Tâm linh: 01 27 (6 phiếu), ĐB 06 = số tâm linh 8 phiếu. Cộng/trừ ±1 qua 5 kỳ: 12.
- 08/10: Power thêm 3 luật số lặp (anh duyệt): loại số ra 3 kỳ liền (l3), +1 điểm số ra đúng 2 kỳ liền (l2p), số "ra ít nhất 100 kỳ" vừa ra lại thì không loại 3 kỳ (PIT3). Chấm lùi: pool không tụt, vé ma trận 50/100 kỳ 1.38→1.40/1.39, ≥3 8→10% / 7→8%.
- 08/10 tối: Loto kiểm dấu vết trùng (MM lặp kỳ trước 10–11% > TB 8,3%, 13h/21h như nhau; số chính ra 2 kỳ liền → ra tiếp 15,7–18,8%). Anh: "Bỏ đi. Nó ra vậy đỡ sao được" → không sửa luật Loto, giữ nguyên trạng thái đã bỏ Loto.
- 09/10: Số kép (11 22 33 44 [55]): ~1/2 số kỳ có kép, đa số đi 1 mình (Mega 500 kỳ: 188 kỳ 1 kép, 34 kỳ 2 kép, 4 kỳ 3 kép; Power 170/52/4). Anh: vé tối đa 1 kép. Mega: pool ma trận chỉ giữ 1 kép → vé tốt nhất 100 kỳ 1.63→1.67, ≥3 13→17%. Power: giữ pool cũ (bỏ kép làm tụt 1.39→1.33), luật kép chỉ ưu tiên khi chia nhóm.

## 09/10/2026 — Pipeline Mega học trọng số (build/mega_pipeline.py), ≤200 kỳ
- Tầng cộng/trừ (±0..±5, ±1 qua 5 kỳ, ±13/14) + luật (vắng, nóng, lien2, lt3, zprev, kép, lộn, đuôi), hồi quy logistic học 100 kỳ trước, cập nhật dần.
- Chấm lùi 100 kỳ, pool 12: học trọng số TB 1,50 (≥3: 13%) — cách hiện tại (goiy.py) TB 1,76 (≥3: 25%). Ma trận 6 vé: 1,43 vs 1,67.
- Trộn điểm học vào thứ hạng hiện tại (λ 0,5/1/2): 100 kỳ 1,70/1,66/1,69 vs 1,76 → không thêm gì. Giữ cách hiện tại.
- Trọng số học được nghiêng: vắng 11–15 +, ±13/14 qua 5 kỳ +, kề ±1 kỳ trước +, kép −, số lớn nhất kỳ trước −.
- 09/10 học tiếp: học chậm (lr 0,005, cập nhật 1 lượt/kỳ) và chỉ xếp lại trong top 20 của goiy.py → pool12 100 kỳ 1,77 (≥3: 26%, ≥4: 4%) vs hiện tại 1,76 (25%, ≥4 —). Hai nửa 1,64 · 1,90. Ma trận 6 vé 1,60 vs 1,67. Học nhanh/học trên cả 45 số đều kém (1,46–1,66). Dùng bản này cho ô Máy học Mega, sổ tiến làm lại từ 09/10.
- 09/10 học nhiều vòng (1→300 vòng trên 100 kỳ cũ, thêm cờ từng số): tự do 45 số → kỳ đã học 1,80→2,01 (≥3: 21→33%) nhưng 100 kỳ chưa học 1,52→1,61 (≥3 ~16%). Trong top 20: đã học 1,80→1,82, chưa học 1,75→1,74. Học nhiều vòng chỉ thuộc bài cũ, không đoán kỳ mới tốt hơn → giữ học chậm từng kỳ.
- 09/10 số chung app gợi ý ∩ máy học (pool 12, 100 kỳ): ra 15,3%/số (2 nửa 14,6·16,0) vs chỉ một bên 13,7–13,9%. Gắn điểm cộng vào goiy.py (GOIY_ML): ma trận 6 vé 100 kỳ 0 → 1,67 (≥3 17%), 0,2 → 1,59, 0,5 → 1,64, 1 → 1,58 → để 0, chỉ đánh dấu số chung khi báo anh.

## 09/10/2026 — Cặp số liên tiếp trong 1 kỳ (anh hỏi), ≤200 kỳ
- Kỳ có ≥1 cặp liền (vd 35-36): Mega 50/100/200 kỳ 38/49/50%, ≥2 cặp 4/8/10%; Power 40/35/42%, ≥2 cặp 2/3/6%. 3 số liền: Mega 9, Power 6 kỳ/200 (vé đã chặn ≥3 số liên tiếp).
- Kỳ trước có cặp → kỳ sau có: Mega 49% (không có → 50%), Power 40% (43%). Không báo trước.
- Nhịp: Mega 100 kỳ có cặp / 200; khoảng cách tới kỳ có cặp kế 1:49, 2:24, 3:13, 4:6, 5:4, ≥6:3; chuỗi liền nhau dài nhất 6. Power 84/200; khoảng cách 1:34, 2:26, 3:10, 4:5, 5:3, ≥6:5; chuỗi vắng dài nhất 13.
- Vắng cặp đúng k kỳ → kỳ sau có: Mega 24/50 · 13/26 · 6/13 · 4/7 · 2/3; Power 27/50 · 10/23 · 5/13 · 3/8 · 0/5. ≈ một nửa, không thấy nhịp ra liên tiếp hay cách kỳ đều đặn.
- Dùng: vé tối đa 1 cặp liên tiếp (2 cặp chỉ 2–10% kỳ). Chưa cộng/trừ điểm cho số liền kề trong cùng kỳ.

## 09/10/2026 — Mega trật 0/6 (05 07 12 23 32 41): mổ xẻ
- Hạng trong bảng điểm trước kỳ (bỏ 33,43, linh 15 36): 41 hạng 7 (bị loại "ra kỳ trước & t−3"), 12 hạng 19, 32 hạng 20, 23 hạng 31, 07 hạng 32, 05 hạng 41 (vắng 40 kỳ, "khó ra").
- Luật bị trật: lt3 loại 41 (luật vẫn đúng 51/62 kỳ ở 100 kỳ, 104/124 ở 200); "cùng đuôi −" trừ 07, 23 (đuôi 7, 3 của 37, 43) — số cùng đuôi ra 13,6/12,5/12,1/12,5%/số ở 20/50/100/200 kỳ, luật yếu, 20 kỳ gần ra nhiều hơn mức chia đều.
- Tâm linh có 05, 23, 32 (6–7 phiếu) nhưng không đủ điểm vào pool.
- Pool 12 trúng 0: 11/100 kỳ trong chấm lùi → kỳ trật thường gặp, không đổi luật vì 1 kỳ.

## 10/10/2026 — Mega cộng/trừ & lộn xét ngắn 1/3/5 kỳ (anh: "3 kì thôi")
| Luật (bỏ số kỳ trước) | Số ứng viên/kỳ | Ra %/số 20·50·100·200 kỳ |
|---|---|---|
| ±1, 3 kỳ | 22,5 | 13,5 · 13,2 · 13,1 · 13,5 |
| ±13/14, 3 kỳ | 26 | 13,9 · 14,0 · 13,7 · 13,8 |
| Lộn, 1 kỳ | 2,2 | 8,5 · 11,8 · 13,6 · 14,0 |
| **Lộn, 3 kỳ** | **5,5** | **17,5 · 15,2 · 15,1 · 14,7** (≥2 số ra: 25·20·21·20% kỳ) |
| Lộn, 5 kỳ | 8,3 | 14,6 · 13,5 · 13,9 · 13,6 |
- Lộn trong 3 kỳ: nhóm nhỏ, tỉ lệ ra nhỉnh và đều 4 khung → ứng viên cộng điểm nhỏ (chưa gắn, chờ chấm vé). ±1/±13/14 phủ quá rộng, không lọc được.

## 10/10/2026 — Chéo Mega ↔ Power (anh: Mega 09/10 có 07, 12 của Power 08/10)
| Khung | Mega ra số của Power kỳ ngay trước (%/số · kỳ có ≥2 số) | Power ra số (≤45) của Mega kỳ ngay trước |
|---|---|---|
| 20 | 12,7 · 10% | 13,3 · 15% |
| 50 | 14,6 · 16% | 13,3 · 14% |
| 100 | 14,2 · 15% | 13,2 · 15% |
| 200 | 13,4 · 14% | 12,2 · 14% |
- Mega lặp chính kỳ Mega trước: 13,2 (100) · 12,8 (200). Chéo Power→Mega nhỉnh nhẹ ở 50/100 kỳ nhưng 20 kỳ thấp → theo dõi, chưa cộng điểm.
- Power lặp chính kỳ Power trước: 11,7 (50) · 10,3 (100) · 11,4 (200)%/số → Power ra số của Mega kỳ trước (13,2–13,3% ở 20/50/100, 12,2 ở 200) nhỉnh hơn, khá đều. Ứng viên Power 10/10 từ Mega 09/10: 05 07 12 23 32 41.

## 10/10/2026 — Pool 25 số (anh hỏi: ≥4 số trên 80% kỳ?)
| Game | Khung 20·50·100·200: TB trúng | ≥3 số | ≥4 số | ≥5 số |
|---|---|---|---|---|
| Mega | 3,40·3,46·3,43·3,40 | 75·82·82·79% | 50·48·45·46% | 20·18·17·16% |
| Power | 3,25·2,88·2,95·2,91 | 65·56·59·60% | 40·26·31·30% | 20·12·13·10% |
- ≥4 số trên 80% kỳ: không đạt (Mega ~46%, Power ~30%). Mega pool 25 đạt ~80% ở mức ≥3 số. Chấm bằng `GOIY_RK=25`.
- 10/10 loại trước rồi mới chọn pool 25 (gộp các luật loại trong sổ, chấm 200 kỳ): mỗi luật riêng đúng 88–98% kỳ, nhưng gộp 8 luật ≥90% → loại ~5 số, cả nhóm trúng 0 số chỉ 54–61% kỳ, mất 0,5 số/kỳ; gộp 14–15 luật ≥80% → loại ~9 số, đúng 28–30% kỳ, mất ~1 số/kỳ. Áp lên pool 25: Power ≥4 số 30→26%, Mega 46→40% (pool còn ~23 số). Sai số cộng dồn khi chồng nhiều luật → không tăng tỉ lệ.
- 10/10 nghiên cứu sâu pool 25 (`build/pool25_sau.py`): 35 đặc trưng/số (nhịp vắng, c5–c100, đà, lien2/lt3, max/min kỳ trước, kề ±1, ±1 & ±13/14 trong 3 kỳ, lộn 3 kỳ, chéo game, cùng đuôi, kép, hạng app, hàng chục), hồi quy logistic, học 100 kỳ cũ → kiểm 100 kỳ mới.
  - Mega: cách hiện tại 100 kỳ mới ≥4 45% ≥5 17%; học 1 lần ≥4 42–44%; cuốn chiếu (học lại mỗi 10 kỳ) **≥4 48% ≥5 18%**, TB 3,41.
  - Power: cách hiện tại ≥4 31% ≥5 13%; học 1 lần ≥4 25–26%; cuốn chiếu **≥4 34%** nhưng ≥5 8%.
  - Kỳ đã học lên tới ≥4 53–55% (Mega) nhưng kỳ mới chỉ ~45–48% → phần tăng chủ yếu là "thuộc bài". Trọng số Mega nghiêng: lộn 3 kỳ +, vắng 1 kỳ +, vắng 11–15 +, ±13/14 +, cùng đuôi −, c100 −. Power: hạng app +, vắng ≥26 +, chéo Mega +.
- 10/10 Power pool theo cỡ (cách hiện tại, 100 kỳ): 12 → ≥3 11% ≥4 1% · 15 → 23%/6% · 18 → 32%/12% · 20 → 40%/15% · 25 → 59%/31%. Thử thêm cho ≥4 trong pool 25: cân theo hàng chục 31%, chỉ đánh kỳ máy "tự tin" (30/50 kỳ cao nhất) 30–34% — không tăng.
- 10/10 thử 31 phương pháp chọn pool 25 Power (`build/pool25_pp.py`, bảng đầy đủ `build/pool25_power.md`): ≥4 số ở 100 kỳ mới cao nhất 36% (±1 kỳ trước, chéo Mega 3 kỳ) nhưng 100 kỳ cũ chỉ 25%/21%; ghép tốt nhất chọn trên đoạn cũ (36%) sang đoạn mới 32%. Không cách nào ổn định trên ~30–34%.
- 10/10 quét 2.891 phương pháp pool 25 Power (`build/pool25_quet.py`, kết quả `build/pool25_quet_power.md`): 291 cách đơn (nóng/nguội 14 khung, nóng giảm dần 9 mức, vắng ≈0–30, ±0–20 qua 1–10 kỳ, lộn, chéo Mega, đuôi, hàng chục, lớp chia 2–9, theo sau t−1..3, cặp đi cùng, xác suất theo mức vắng, app) + 2.600 cách ghép. ≥4 số: đoạn cũ cao nhất 47% → sang đoạn gần 31%; không cách nào ≥40% cả hai đoạn; ổn định nhất "±16 qua 5 kỳ + Nguội 75 kỳ + ±1 qua 4 kỳ" 37% · 38%.
- 10/10 xếp riêng theo 100 kỳ gần (Power, 5.491 cách gồm ghép chọn theo 100 kỳ gần): ≥4 số cao nhất 42%, 93 cách ≥40%, không cách nào ≥45%. Nhóm đứng đầu: "Chéo Mega qua 7 kỳ + Vắng ≈24–30 kỳ" — 100 kỳ gần 42% (2 nửa 50 kỳ: 42·42%), khung 10/20/50/100: ≥4 30·35·42·42%, ≥3 90·90·78·72%; nhưng 100 kỳ cũ hơn chỉ 23%.
- 10/10 Pool 25 Power đưa vào app (`build/pool25_power.py`). Loại tiếp theo nhãn hồ sơ (tính tại từng kỳ, 100 kỳ): số trong pool theo nhãn ra Trong nhịp nghỉ 15,7% · Vượt nghỉ dài nhất 12,6% · Bình thường 12,5% · Nghiêng ra 11,1%/số; loại "Trong nhịp nghỉ" làm ≥4 tụt 42→38%, loại "Vượt nghỉ dài nhất" tụt 42→19% → không loại theo nhãn.
- 10/10 loại tiếp trong Pool 25 Power (`build/pool25_loaitiep.py`, 100 kỳ): bỏ 5/7/10 số điểm thấp theo từng cách trong 291 cách → pool 20: ≥4 tối đa 27–28%; pool 18: ~19–20%; pool 15: ~10–13% (gốc 25 số: 42%). Luật sổ kiểm chứng bỏ khỏi pool: tốt nhất "phá nhịp tối thiểu" 41%, "ra nhiều nhất 100 kỳ" 40% (chỉ bỏ ~0,4 số); luật vắng ≥20/25/30 làm tụt mạnh vì pool dựa vào số vắng lâu. Kết luận: chưa có cách loại nào giữ được ≥4 khi thu pool.
- 10/10 anh đặt chuẩn: mỗi lần thu 5 số, sai số ≤5%. Quét 582 cách bỏ 5 số (thấp/cao nhất theo 291 cách) trong pool 25 Power: 5 số bị bỏ không chứa số trúng tốt nhất ~60% kỳ (2 nửa 60·60, trung vị 46%) → sai ~40%; ≥4 sau khi bỏ còn 22–26% (gốc 42%). Chưa đạt chuẩn ≤5%.
- 10/10 học cách loại trong pool 25 Power (`build/pool25_loaihoc.py`: 291 điểm làm đặc trưng cho số trong pool, logistic cuốn chiếu): bỏ 1 số → ≥4 40% (−2 điểm), bỏ sạch 89–90%; bỏ 2 → 37% (−5, đạt chuẩn anh vừa sát); bỏ 3 → 32–33%; bỏ 5 → 21–24%. Cách loại đơn lẻ tốt nhất trước đó chỉ bỏ sạch ~60% với 5 số.
- 10/10 tâm linh để loại trong pool 25 Power (`build/tamlinh_ls.js` lấy phiếu tâm linh 220 kỳ quá khứ từ app): bỏ 1/2/3/5 số phiếu ít nhất → ≥4 37/31/28/21%; bỏ phiếu nhiều nhất 35/31/28/23%. Số trong pool có đúng 3 phiếu ra 8,4% (2 nửa 8,1·8,7%) → bỏ hết (pool còn 19,5) ≥4 30% (−12 điểm), tốt hơn các cách bỏ 5 số khác (22–26%) nhưng chưa đạt chuẩn −5. Toàn bảng 55 số, phiếu 3 ra 10,2% như các mức khác → nhiều khả năng chỉ trùng hợp trong pool.
- 10/10 anh chốt dùng Pool 20 Power = pool 25 bỏ số đúng 3 phiếu tâm linh (≥4 ~30%). Kỳ 10/10: 02 08 09 10 15 19 22 25 28 29 30 33 37 43 44 45 47 49 (18 số). Chấm tiến trong sổ pool25_power_log.jsonl (trung20).
