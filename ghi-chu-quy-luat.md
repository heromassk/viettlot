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
