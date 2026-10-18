# Kiểm tra lại mọi phương pháp + pool chuẩn — 13/10/2026 (anh: "thử lại tất cả phương pháp app đang có kể cả tâm linh, chấm trên 100 và 200 kỳ gần nhất, chọn phương pháp ổn định tỉ lệ trúng cao để lọc pool chuẩn")

Chạy lại: `python build/kiemtra_app.py 400` (lấy 16 PP pool + 20 PP tâm linh từ code app) → `python build/kiemtra_pp.py power|mega|loto` → `python build/kiemtra_max3d.py`.
Dữ liệu đến: Power 03/10, Mega 04/10, Loto 05/10 13h, Max 3D 05/10, Pro 03/10/2026. Mỗi kỳ chỉ dùng dữ liệu trước nó.

Cách chấm (chính phương pháp, không so bốc ngẫu nhiên): luật loại = % kỳ đúng + số bị loại ra ≤ BQ; chọn số = tỉ lệ ra mỗi số so với BQ; khẳng định = % kỳ đúng.
Đạt = ổn định ở cả 100 kỳ gần và 100 kỳ trước (2 nửa của 200 kỳ). Ít mẫu (kỳ vọng <10 lần trúng) không xét.
Pool chuẩn: loại hẳn = các luật loại đạt, thêm dần từ mạnh nhất miễn CẢ NHÓM vẫn đúng ≥70% kỳ; luật loại đạt còn lại → trừ điểm;
chọn số đạt → cộng điểm (hệ số ra 200 kỳ − 1). **Kiểm chéo**: chọn phương pháp + trọng số chỉ từ 200 kỳ cũ hơn (−400…−200), chấm trên 200 kỳ gần — đây là con số gần với thực tế khi dùng tiếp.

## Kết luận
- Pool chuẩn chấm trên chính 200 kỳ dùng để chọn: ×1.12–1.26 BQ (3 game số), ×1.03–1.09 (Max 3D+).
- Kiểm chéo (chưa thấy kỳ chấm): Power ×0.95–0.96, Mega ×1.02–1.06, Loto ×1.04–1.11, Max 3D+ ×1.00–1.07, Pro ×0.94–1.08 — ngang pool app hiện tại (×1.05–1.10). Phần lớn mức hơn ở trên là do chọn trên cùng dữ liệu.
- Lỗi đã sửa trong cùng đợt: `theodoi.py` chấm nhóm rỗng thành SAI/ĐÚNG (giờ = không xét), cờ ● luật nhóm, chấm luật nhóm bằng tỉ lệ ra cộng dồn; `rasoat` chạy lại (`ra-soat-dau-vet.md`).

## power655 — 82 phương pháp, chấm trên 100 / 200 kỳ gần nhất (đến 03/10/2026), BQ mỗi số ra 10.9%/kỳ

Đạt = ổn định ở cả 100 kỳ gần và 100 kỳ trước đó. Luật loại: đúng ≥70% + số bị loại ra ≤ BQ · Chọn số: ra > BQ · Ra ít: ra < BQ · Khẳng định: đúng ≥70%.


### Luật loại số (21)

| Phương pháp | Nhóm | Bỏ TB | Đúng 100 / 200 kỳ | Số bị loại ra (100 / 200 / 100 trước) | Đạt |
|---|---|---|---|---|---|
| Bỏ số ra ít nhất 100 kỳ | Luật loại (sổ) | 1.0 | 93% / 93% | ×0.64 / ×0.64 / ×0.64 | ✔ đạt |
| Bỏ số nhịp "ra – vắng 2 – ra" (vừa ra lại sau đúng 2 kỳ vắng) | Luật loại (sổ) | 1.3 | 97% / 93% | ×0.46 / ×0.65 / ×0.83 | ✔ đạt |
| Bỏ số ra 3 lần trong 5 kỳ | Luật loại (sổ) | 1.3 | 91% / 92% | ×0.64 / ×0.64 / ×0.64 | ✔ đạt |
| Bỏ số lớn nhất kỳ trước | Luật loại (sổ) | 1.0 | 91% / 90% | ×0.82 / ×0.92 / ×1.01 | ✘ |
| Bỏ số vắng lâu nhì | Luật loại (sổ) | 1.0 | 88% / 89% | ×1.10 / ×1.01 / ×0.92 | ✘ |
| Bỏ số ra nhiều nhất 100 kỳ | Luật loại (sổ) | 1.0 | 90% / 89% | ×0.92 / ×1.01 / ×1.10 | ✘ |
| Bỏ số nhỏ nhất kỳ trước | Luật loại (sổ) | 1.0 | 90% / 88% | ×0.92 / ×1.05 / ×1.19 | ✘ |
| Bỏ số nóng nhất 10 kỳ (≥4 lần) | Luật loại (sổ) | 1.0 | 82% / 86% | ×1.61 / ×1.31 / ×1.03 | ✘ |
| Bỏ số vắng lâu nhất | Luật loại (sổ) | 1.0 | 82% / 86% | ×1.65 / ×1.33 / ×1.01 | ✘ |
| Bỏ số ra kỳ trước VÀ kỳ t−3 | Luật loại (sổ) | 1.3 | 88% / 85% | ×0.81 / ×1.01 / ×1.22 | ✘ |
| Bỏ số tái xuất sau vắng ≥15 | Luật loại (sổ) | 1.7 | 89% / 84% | ×0.70 / ×1.03 / ×1.35 | ✘ |
| Bỏ số ra 2 kỳ liền | Luật loại (sổ) | 1.3 | 81% / 82% | ×1.38 / ×1.30 / ×1.24 | ✘ |
| Bỏ số tái xuất sau vắng ≥10 | Luật loại (sổ) | 2.2 | 84% / 77% | ×0.73 / ×1.06 / ×1.40 | ✘ |
| Bỏ số vắng ≥30 kỳ | Luật loại (sổ) | 1.8 | 72% / 75% | ×1.90 / ×1.32 / ×1.03 | ✘ |
| Bỏ số phá nhịp tối thiểu (100 kỳ: luôn nghỉ ≥x kỳ, mới nghỉ <x) | Luật loại (sổ) | 3.0 | 71% / 71% | ×0.83 / ×0.97 / ×1.15 | ✘ |
| Bỏ số phá nhịp tối thiểu (khung dài: Power 100, Mega 100, Loto 200 kỳ) | Luật loại (sổ) | 3.0 | 71% / 71% | ×0.83 / ×0.97 / ×1.15 | ✘ |
| Bỏ số vắng ≥25 kỳ | Luật loại (sổ) | 2.7 | 70% / 69% | ×1.44 / ×1.15 / ×0.96 | ✘ |
| Bỏ số "lâu lâu mới ra" (khung gần: Power 100, Mega 100, Loto 200 kỳ; ≤85% kỳ vọng) đang vắng ≥15 | Luật loại (sổ) | 5.1 | 54% / 56% | ×1.22 / ×1.04 / ×0.90 | ✘ |
| Bỏ số vắng ≥20 kỳ | Luật loại (sổ) | 5.1 | 51% / 52% | ×1.35 / ×1.16 / ×1.01 | ✘ |
| Loto: bỏ số vắng ≥20 kỳ CÙNG PHIÊN (13h đúng ~80%, 21h ngược) | Luật loại (sổ) | 0.0 | — / — | — / — / — | ít mẫu |
| Loto 13h: bỏ số tái xuất trong phiên (ra hôm trước sau vắng ≥10 kỳ 13h) | Luật loại (sổ) | 0.0 | — / — | — / — / — | ít mẫu |

### Chọn số (+) (48)

| Phương pháp | Nhóm | Cỡ TB | Ra so với BQ: 100 / 200 kỳ (100 trước) | Kỳ có ≥1 số trúng 100 / 200 | Đạt |
|---|---|---|---|---|---|
| Soi cầu: số cầu Pascal của kỳ trước ra NHIỀU hơn bình quân | Khẳng định / nhóm (sổ) | 1.0 | ×1.62 / ×1.47 (×1.31) | 18% / 16% | ít mẫu |
| Soi cầu: cầu vị trí đã chạy ≥2 kỳ ra NHIỀU hơn bình quân | Khẳng định / nhóm (sổ) | 1.8 | ×1.38 / ×1.32 (×1.27) | 24% / 22% | ít mẫu |
| Soi cầu: kép liền kề của kép kỳ trước (11↔22↔33) ra NHIỀU hơn bình quân | Khẳng định / nhóm (sổ) | 2.1 | ×0.99 / ×1.20 (×1.38) | 21% / 25% | ✘ |
| Soi cầu: lô kép (11, 22, 33…) ra NHIỀU hơn bình quân | Khẳng định / nhóm (sổ) | 5.0 | ×1.08 / ×1.17 (×1.27) | 43% / 48% | ✔ đạt |
| Bóng âm dương | Tâm linh (bắt số dân gian) | 13.1 | ×1.08 / ×1.12 (×1.17) | 84% / 85% | ✔ đạt |
| Tarot (3 lá) | Tâm linh (Tarot, Mai Hoa, Kỳ Môn, Tứ trụ) | 4.0 | ×1.16 / ×1.12 (×1.08) | 45% / 42% | ✔ đạt |
| Lộn + kép | Tâm linh (bắt số dân gian) | 8.2 | ×1.09 / ×1.12 (×1.15) | 66% / 67% | ✔ đạt |
| Nhị thập bát tú | Tâm linh (ngày giờ quay) | 5.5 | ×1.14 / ×1.09 (×1.05) | 56% / 55% | ✔ đạt |
| Huyền Không Phi Tinh | Tâm linh (ngày giờ quay) | 11.6 | ×1.13 / ×1.09 (×1.05) | 85% / 82% | ✔ đạt |
| Kề ±1 kỳ trước | Tín hiệu gợi ý | 10.2 | ×1.05 / ×1.06 (×1.08) | 73% / 74% | ✔ đạt |
| PP18t Tích lũy đang tăng | Pool app (top 17) | 17.0 | ×1.04 / ×1.06 (×1.08) | 95% / 95% | ✔ đạt |
| Ngũ hành nạp âm | Tâm linh (ngày giờ quay) | 11.0 | ×1.02 / ×1.05 (×1.08) | 76% / 77% | ✔ đạt |
| PP27 Gộp: 5 phương pháp tốt nhất 50 kỳ gần nhất | Pool app (top 17) | 17.0 | ×1.07 / ×1.04 (×1.01) | 92% / 93% | ✔ đạt |
| PP20b Số kề kỳ trước (±2) | Pool app (top 17) | 17.0 | ×1.05 / ×1.04 (×1.04) | 92% / 91% | ✔ đạt |
| Vắng 11–15 kỳ "chín" | Tín hiệu gợi ý | 6.8 | ×1.06 / ×1.04 (×1.02) | 58% / 57% | ✔ đạt |
| PP16 Gan (lâu chưa ra nhất) | Pool app (top 17) | 17.0 | ×1.11 / ×1.04 (×0.97) | 90% / 90% | ✘ |
| Tổng phiếu 20 phương pháp tâm linh, top 17 | Tâm linh (tổng phiếu) | 17.0 | ×1.04 / ×1.03 (×1.02) | 93% / 94% | ✔ đạt |
| Chạm đầu đuôi | Tâm linh (bắt số dân gian) | 26.8 | ×1.07 / ×1.03 (×1.00) | 98% / 99% | ✘ |
| Thần số học | Tâm linh (người chơi) | 18.0 | ×1.06 / ×1.03 (×0.99) | 94% / 94% | ✘ |
| PP18 Tích lũy đang giảm (sắp hồi) | Pool app (top 17) | 17.0 | ×1.04 / ×1.02 (×1.00) | 96% / 92% | ✔ đạt |
| PP20 Số kề kỳ trước (±1) | Pool app (top 17) | 17.0 | ×1.07 / ×1.02 (×0.97) | 89% / 88% | ✘ |
| Bát trạch (cung mệnh) | Tâm linh (người chơi) | 12.0 | ×1.00 / ×1.01 (×1.02) | 81% / 82% | ✔ đạt |
| PP15 Nóng 30 kỳ (ra nhiều nhất) | Pool app (top 17) | 17.0 | ×1.03 / ×1.01 (×0.99) | 94% / 92% | ✘ |
| PP23 Cặp hay đi cùng kỳ trước | Pool app (top 17) | 17.0 | ×1.01 / ×1.01 (×1.01) | 92% / 94% | ✔ đạt |
| PP24 Cùng giờ / cùng thứ 60 kỳ | Pool app (top 17) | 17.0 | ×1.04 / ×1.01 (×0.97) | 90% / 92% | ✘ |
| PP21 Tần suất theo vị trí (500 kỳ) | Pool app (top 17) | 17.0 | ×1.00 / ×1.00 (×1.00) | 89% / 88% | ✔ đạt |
| Hoàng đạo / Hắc đạo | Tâm linh (ngày giờ quay) | 4.6 | ×1.10 / ×1.00 (×0.90) | 47% / 42% | ✘ |
| PP26 Bóng đối xứng (N+1−n) kỳ trước | Pool app (top 17) | 17.0 | ×1.09 / ×0.99 (×0.89) | 93% / 90% | ✘ |
| PP22 Markov số → số | Pool app (top 17) | 17.0 | ×0.97 / ×0.99 (×1.01) | 89% / 90% | ✘ |
| Nóng (c10≥3 hoặc c20≥2×kỳ vọng) | Tín hiệu gợi ý | 6.4 | ×1.03 / ×0.99 (×0.96) | 52% / 54% | ✘ |
| PP17 Đến chu kỳ trung bình | Pool app (top 17) | 17.0 | ×0.99 / ×0.98 (×0.98) | 95% / 94% | ✘ |
| PP17b Chu kỳ hay gặp (khoảng chưa ra đúng bằng chu kỳ cũ) | Pool app (top 17) | 17.0 | ×0.91 / ×0.98 (×1.06) | 87% / 90% | ✘ |
| Bạc nhớ | Tâm linh (bắt số dân gian) | 17.0 | ×0.96 / ×0.98 (×1.00) | 87% / 90% | ✘ |
| Tử vi (Mệnh, Cục, sao Tử Vi) | Tâm linh (người chơi) | 15.0 | ×0.93 / ×0.98 (×1.03) | 82% / 86% | ✘ |
| Tổng chạm | Tâm linh (bắt số dân gian) | 5.4 | ×0.94 / ×0.98 (×1.01) | 46% / 49% | ✘ |
| Tứ trụ (dụng thần) | Tâm linh (Tarot, Mai Hoa, Kỳ Môn, Tứ trụ) | 11.0 | ×0.95 / ×0.98 (×1.00) | 75% / 75% | ✘ |
| PP19 Cấp số của các lần ra | Pool app (top 17) | 17.0 | ×1.04 / ×0.97 (×0.90) | 91% / 89% | ✘ |
| Thái Ất (thời kế, rút gọn) | Tâm linh (ngày giờ quay) | 10.5 | ×0.93 / ×0.96 (×0.99) | 71% / 73% | ✘ |
| PP24c Cùng ngày âm | Pool app (top 17) | 17.0 | ×1.03 / ×0.96 (×0.88) | 88% / 91% | ✘ |
| Nhóm số của kỳ cách 7 kỳ ra NHIỀU hơn bình quân (dấu vết máy, 100 kỳ) | Khẳng định / nhóm (sổ) | 5.3 | ×0.93 / ×0.95 (×0.96) | 45% / 48% | ✘ |
| Tiểu Lục Nhâm | Tâm linh (ngày giờ quay) | 16.3 | ×0.97 / ×0.94 (×0.92) | 88% / 88% | ✘ |
| Kỳ Môn Độn Giáp | Tâm linh (Tarot, Mai Hoa, Kỳ Môn, Tứ trụ) | 7.7 | ×1.11 / ×0.92 (×0.73) | 65% / 58% | ✘ |
| Xin xăm (100 quẻ) | Tâm linh (người chơi) | 6.8 | ×0.71 / ×0.91 (×1.13) | 45% / 54% | ✘ |
| Đại Lục Nhâm (rút gọn) | Tâm linh (ngày giờ quay) | 12.8 | ×0.93 / ×0.91 (×0.89) | 76% / 76% | ✘ |
| Nhóm số của kỳ cách 9 kỳ ra NHIỀU hơn bình quân (dấu vết máy, 100 kỳ) | Khẳng định / nhóm (sổ) | 5.4 | ×0.87 / ×0.91 (×0.95) | 39% / 45% | ✘ |
| Bóng dễ ra (z>1) | Tín hiệu gợi ý | 6.5 | ×0.88 / ×0.86 (×0.83) | 51% / 47% | ✘ |
| Mai Hoa (giờ quay) | Tâm linh (Tarot, Mai Hoa, Kỳ Môn, Tứ trụ) | 2.9 | ×0.74 / ×0.83 (×0.92) | 22% / 25% | ✘ |
| Loto 21h: nhóm tái xuất trong phiên ra NHIỀU hơn bình quân | Khẳng định / nhóm (sổ) | 0.0 | — / — (—) | — / — | ít mẫu |

### Tín hiệu ra ít (−) (6)

| Phương pháp | Nhóm | Cỡ TB | Ra so với BQ: 100 / 200 kỳ (100 trước) | Kỳ có ≥1 số trúng 100 / 200 | Đạt |
|---|---|---|---|---|---|
| Soi cầu: lô kẹp (kỳ trước có a, a+2 → a+1) ra ÍT hơn bình quân | Khẳng định / nhóm (sổ) | 1.3 | ×0.95 / ×0.74 (×0.51) | — / — | ít mẫu |
| Số kỳ cùng thứ tuần trước | Tín hiệu gợi ý | 5.2 | ×0.77 / ×0.84 (×0.91) | — / — | ✔ đạt |
| Bóng khó ra (z<−1.5) | Tín hiệu gợi ý | 3.2 | ×1.09 / ×0.91 (×0.76) | — / — | ✘ |
| Nhóm "phá nhịp nghỉ" (100 kỳ: ≥80% lần nghỉ ≥x kỳ, mới nghỉ <x) ra ít hơn bình quân | Khẳng định / nhóm (sổ) | 8.7 | ×0.84 / ×0.95 (×1.09) | — / — | ✘ |
| Vắng 6–10 kỳ | Tín hiệu gợi ý | 12.5 | ×1.00 / ×0.99 (×0.98) | — / — | ✘ |
| Nhóm nhịp riêng "lúc vắng thế này chưa từng ra" ra ít hơn bình quân | Khẳng định / nhóm (sổ) | 10.7 | ×1.07 / ×1.07 (×1.06) | — / — | ✘ |

### Khẳng định (7)

| Phương pháp | Nhóm | Đúng 100 / 200 kỳ (100 trước) | Đạt |
|---|---|---|---|
| Có ≥1 số trùng hoặc kề ±1 kỳ trước | Khẳng định / nhóm (sổ) | 86% / 88% (89%) | ✔ đạt |
| Không trùng ≥2 số với kỳ trước | Khẳng định / nhóm (sổ) | 87% / 86% (85%) | ✔ đạt |
| Nhỏ/lớn cân (3±1) | Khẳng định vé (gợi ý) | 83% / 80% (78%) | ✔ đạt |
| Rải ≥4 hàng chục | Khẳng định vé (gợi ý) | 80% / 80% (80%) | ✔ đạt |
| Chẵn/lẻ cân (3±1) | Khẳng định vé (gợi ý) | 79% / 79% (79%) | ✔ đạt |
| Có ≥1 số của 2 kỳ gần nhất | Khẳng định / nhóm (sổ) | 77% / 77% (77%) | ✔ đạt |
| Có ≥1 số trong 10 số nóng nhất 20 kỳ | Khẳng định / nhóm (sổ) | 72% / 74% (75%) | ✔ đạt |

### Pool chuẩn — dùng 28 phương pháp đạt

- Loại hẳn (cả nhóm đúng ≥70% kỳ): Bỏ số ra 3 lần trong 5 kỳ, Bỏ số ra ít nhất 100 kỳ, Bỏ số nhịp "ra – vắng 2 – ra" (vừa ra lại sau đúng 2 kỳ vắng) · TB bỏ 2.0 số/kỳ, kỳ có số trúng bị loại nhầm: 11% (100 kỳ) / 13% (200 kỳ)
- Cộng điểm: Soi cầu: lô kép (11, 22, 33…) ra NHIỀU hơn bình quân (×1.17), Kề ±1 kỳ trước (×1.06), Vắng 11–15 kỳ "chín" (×1.04), PP18 Tích lũy đang giảm (sắp hồi) (×1.02), PP18t Tích lũy đang tăng (×1.06), PP20b Số kề kỳ trước (±2) (×1.04), PP23 Cặp hay đi cùng kỳ trước (×1.01), PP21 Tần suất theo vị trí (500 kỳ) (×1.00), PP27 Gộp: 5 phương pháp tốt nhất 50 kỳ gần nhất (×1.04), Huyền Không Phi Tinh (×1.09), Nhị thập bát tú (×1.09), Ngũ hành nạp âm (×1.05), Bóng âm dương (×1.12), Lộn + kép (×1.12), Tarot (3 lá) (×1.12), Bát trạch (cung mệnh) (×1.01), Tổng phiếu 20 phương pháp tâm linh, top 17 (×1.03)
- Trừ điểm: Số kỳ cùng thứ tuần trước (×0.84)
- Khẳng định đạt (dùng lọc vé, không lọc số): Có ≥1 số của 2 kỳ gần nhất, Có ≥1 số trong 10 số nóng nhất 20 kỳ, Có ≥1 số trùng hoặc kề ±1 kỳ trước, Không trùng ≥2 số với kỳ trước, Chẵn/lẻ cân (3±1), Nhỏ/lớn cân (3±1), Rải ≥4 hàng chục

| Cỡ pool | Pool chuẩn: TB trúng 100 / 200 kỳ | Kỳ ≥1/≥2/≥3 số (200 kỳ) | Ra so với BQ | Kiểm chéo (chọn từ 200 kỳ cũ): TB 100 / 200 · ×BQ | Pool app hiện tại: TB 100 / 200 · ×BQ |
|---|---|---|---|---|---|
| 10 | **1.20 / 1.27** | 79% / 39% / 8% | ×1.17 | 1.17 / 1.03 · ×0.95 | 1.26 / 1.17 · ×1.07 |
| 12 | **1.45 / 1.52** | 86% / 48% / 15% | ×1.16 | 1.33 / 1.25 · ×0.96 | 1.44 / 1.38 · ×1.05 |
| 15 | **1.84 / 1.94** | 93% / 65% / 28% | ×1.19 | 1.58 / 1.57 · ×0.96 | 1.80 / 1.75 · ×1.07 |
| 18 | **2.30 / 2.35** | 96% / 76% / 42% | ×1.19 | 1.82 / 1.87 · ×0.95 | 2.15 / 2.11 · ×1.07 |
| 20 | **2.48 / 2.55** | 97% / 82% / 50% | ×1.17 | 2.03 / 2.10 · ×0.96 | 2.34 / 2.31 · ×1.06 |

**Kỳ tới** — bị loại: 06 13 18  ·  xếp hạng: 11 44 08 33 55 10 14 22 15 45 53 43 46 03 19 16 09 20 25 28


## mega645 — 82 phương pháp, chấm trên 100 / 200 kỳ gần nhất (đến 04/10/2026), BQ mỗi số ra 13.3%/kỳ

Đạt = ổn định ở cả 100 kỳ gần và 100 kỳ trước đó. Luật loại: đúng ≥70% + số bị loại ra ≤ BQ · Chọn số: ra > BQ · Ra ít: ra < BQ · Khẳng định: đúng ≥70%.


### Luật loại số (21)

| Phương pháp | Nhóm | Bỏ TB | Đúng 100 / 200 kỳ | Số bị loại ra (100 / 200 / 100 trước) | Đạt |
|---|---|---|---|---|---|
| Bỏ số ra ít nhất 100 kỳ | Luật loại (sổ) | 1.0 | 85% / 90% | ×1.12 / ×0.75 / ×0.38 | ✘ |
| Bỏ số nóng nhất 10 kỳ (≥4 lần) | Luật loại (sổ) | 1.0 | 94% / 89% | ×0.44 / ×0.82 / ×1.19 | ✘ |
| Bỏ số ra nhiều nhất 100 kỳ | Luật loại (sổ) | 1.0 | 90% / 89% | ×0.75 / ×0.83 / ×0.90 | ✔ đạt |
| Bỏ số ra 3 lần trong 5 kỳ | Luật loại (sổ) | 1.3 | 88% / 89% | ×0.64 / ×0.64 / ×0.65 | ✔ đạt |
| Bỏ số vắng lâu nhất | Luật loại (sổ) | 1.0 | 92% / 88% | ×0.60 / ×0.86 / ×1.12 | ✘ |
| Bỏ số vắng lâu nhì | Luật loại (sổ) | 1.0 | 91% / 88% | ×0.67 / ×0.90 / ×1.12 | ✘ |
| Bỏ số nhỏ nhất kỳ trước | Luật loại (sổ) | 1.0 | 85% / 88% | ×1.12 / ×0.90 / ×0.67 | ✘ |
| Bỏ số ra 2 kỳ liền | Luật loại (sổ) | 1.2 | 87% / 87% | ×0.77 / ×0.79 / ×0.81 | ✔ đạt |
| Bỏ số lớn nhất kỳ trước | Luật loại (sổ) | 1.0 | 88% / 87% | ×0.90 / ×0.98 / ×1.05 | ✘ |
| Bỏ số tái xuất sau vắng ≥15 | Luật loại (sổ) | 1.3 | 87% / 87% | ×0.75 / ×0.73 / ×0.72 | ✔ đạt |
| Bỏ số nhịp "ra – vắng 2 – ra" (vừa ra lại sau đúng 2 kỳ vắng) | Luật loại (sổ) | 1.3 | 86% / 86% | ×0.83 / ×0.80 / ×0.76 | ✔ đạt |
| Bỏ số ra kỳ trước VÀ kỳ t−3 | Luật loại (sổ) | 1.3 | 84% / 84% | ×0.84 / ×0.89 / ×0.95 | ✔ đạt |
| Bỏ số vắng ≥30 kỳ | Luật loại (sổ) | 1.5 | 90% / 83% | ×0.51 / ×0.84 / ×1.23 | ✘ |
| Bỏ số tái xuất sau vắng ≥10 | Luật loại (sổ) | 1.7 | 78% / 78% | ×1.01 / ×0.97 / ×0.92 | ✘ |
| Bỏ số vắng ≥25 kỳ | Luật loại (sổ) | 2.0 | 80% / 77% | ×0.79 / ×0.86 / ×0.92 | ✔ đạt |
| Bỏ số phá nhịp tối thiểu (100 kỳ: luôn nghỉ ≥x kỳ, mới nghỉ <x) | Luật loại (sổ) | 2.1 | 69% / 74% | ×1.29 / ×1.00 / ×0.81 | ✘ |
| Bỏ số phá nhịp tối thiểu (khung dài: Power 100, Mega 100, Loto 200 kỳ) | Luật loại (sổ) | 2.1 | 69% / 74% | ×1.29 / ×1.00 / ×0.81 | ✘ |
| Bỏ số "lâu lâu mới ra" (khung gần: Power 100, Mega 100, Loto 200 kỳ; ≤85% kỳ vọng) đang vắng ≥15 | Luật loại (sổ) | 3.0 | 70% / 71% | ×0.89 / ×0.79 / ×0.70 | ✘ |
| Bỏ số vắng ≥20 kỳ | Luật loại (sổ) | 3.0 | 69% / 66% | ×0.86 / ×0.91 / ×0.95 | ✘ |
| Loto: bỏ số vắng ≥20 kỳ CÙNG PHIÊN (13h đúng ~80%, 21h ngược) | Luật loại (sổ) | 0.0 | — / — | — / — / — | ít mẫu |
| Loto 13h: bỏ số tái xuất trong phiên (ra hôm trước sau vắng ≥10 kỳ 13h) | Luật loại (sổ) | 0.0 | — / — | — / — / — | ít mẫu |

### Chọn số (+) (49)

| Phương pháp | Nhóm | Cỡ TB | Ra so với BQ: 100 / 200 kỳ (100 trước) | Kỳ có ≥1 số trúng 100 / 200 | Đạt |
|---|---|---|---|---|---|
| Soi cầu: kép liền kề của kép kỳ trước (11↔22↔33) ra NHIỀU hơn bình quân | Khẳng định / nhóm (sổ) | 1.7 | ×1.28 / ×1.21 (×1.11) | 28% / 25% | ít mẫu |
| Vắng 11–15 kỳ "chín" | Tín hiệu gợi ý | 4.6 | ×1.29 / ×1.11 (×0.94) | 56% / 51% | ✘ |
| Ra nhiều cả 4 đoạn 25 kỳ | Tín hiệu gợi ý | 2.4 | ×1.18 / ×1.11 (×1.05) | 35% / 35% | ✔ đạt |
| Tarot (3 lá) | Tâm linh (Tarot, Mai Hoa, Kỳ Môn, Tứ trụ) | 3.8 | ×1.10 / ×1.11 (×1.12) | 44% / 46% | ✔ đạt |
| Tổng chạm | Tâm linh (bắt số dân gian) | 4.4 | ×1.17 / ×1.10 (×1.02) | 54% / 52% | ✔ đạt |
| Đại Lục Nhâm (rút gọn) | Tâm linh (ngày giờ quay) | 10.4 | ×1.16 / ×1.08 (×1.01) | 83% / 82% | ✔ đạt |
| Bạc nhớ | Tâm linh (bắt số dân gian) | 14.0 | ×0.99 / ×1.07 (×1.15) | 90% / 93% | ✘ |
| Bóng âm dương | Tâm linh (bắt số dân gian) | 11.4 | ×1.10 / ×1.06 (×1.02) | 89% / 88% | ✔ đạt |
| PP16 Gan (lâu chưa ra nhất) | Pool app (top 14) | 14.0 | ×1.07 / ×1.04 (×1.01) | 93% / 94% | ✔ đạt |
| Tử vi (Mệnh, Cục, sao Tử Vi) | Tâm linh (người chơi) | 13.0 | ×0.98 / ×1.04 (×1.10) | 85% / 86% | ✘ |
| Xin xăm (100 quẻ) | Tâm linh (người chơi) | 5.8 | ×1.09 / ×1.04 (×0.99) | 65% / 63% | ✘ |
| Bóng dễ ra (z>1) | Tín hiệu gợi ý | 8.6 | ×0.99 / ×1.04 (×1.07) | 71% / 76% | ✘ |
| PP26 Bóng đối xứng (N+1−n) kỳ trước | Pool app (top 14) | 14.0 | ×1.08 / ×1.04 (×1.00) | 94% / 94% | ✘ |
| PP24 Cùng giờ / cùng thứ 60 kỳ | Pool app (top 14) | 14.0 | ×1.08 / ×1.04 (×1.00) | 89% / 89% | ✘ |
| PP15 Nóng 30 kỳ (ra nhiều nhất) | Pool app (top 14) | 14.0 | ×0.97 / ×1.03 (×1.10) | 90% / 90% | ✘ |
| Nhóm số của kỳ cách 7 kỳ ra NHIỀU hơn bình quân (dấu vết máy, 100 kỳ) | Khẳng định / nhóm (sổ) | 5.2 | ×1.00 / ×1.03 (×1.05) | 56% / 56% | ✔ đạt |
| Kề ±1 kỳ trước | Tín hiệu gợi ý | 10.0 | ×0.98 / ×1.02 (×1.07) | 81% / 82% | ✘ |
| PP27 Gộp: 5 phương pháp tốt nhất 50 kỳ gần nhất | Pool app (top 14) | 14.0 | ×1.02 / ×1.02 (×1.01) | 97% / 94% | ✔ đạt |
| Kỳ Môn Độn Giáp | Tâm linh (Tarot, Mai Hoa, Kỳ Môn, Tứ trụ) | 7.3 | ×1.02 / ×1.02 (×1.01) | 71% / 68% | ✔ đạt |
| Soi cầu: cầu vị trí đã chạy ≥2 kỳ ra NHIỀU hơn bình quân | Khẳng định / nhóm (sổ) | 1.9 | ×1.06 / ×1.02 (×0.97) | 26% / 25% | ✘ |
| PP17 Đến chu kỳ trung bình | Pool app (top 14) | 14.0 | ×0.95 / ×1.02 (×1.08) | 92% / 93% | ✘ |
| PP18t Tích lũy đang tăng | Pool app (top 14) | 14.0 | ×0.99 / ×1.02 (×1.04) | 92% / 92% | ✘ |
| PP20 Số kề kỳ trước (±1) | Pool app (top 14) | 14.0 | ×1.01 / ×1.01 (×1.02) | 92% / 92% | ✔ đạt |
| Nhóm số của kỳ cách 9 kỳ ra NHIỀU hơn bình quân (dấu vết máy, 100 kỳ) | Khẳng định / nhóm (sổ) | 5.2 | ×0.94 / ×1.01 (×1.08) | 54% / 55% | ✘ |
| Chạm đầu đuôi | Tâm linh (bắt số dân gian) | 24.4 | ×1.02 / ×1.01 (×0.99) | 100% / 99% | ✘ |
| PP22 Markov số → số | Pool app (top 14) | 14.0 | ×0.99 / ×1.00 (×1.02) | 91% / 90% | ✘ |
| Tổng phiếu 20 phương pháp tâm linh, top 14 | Tâm linh (tổng phiếu) | 14.0 | ×1.06 / ×1.00 (×0.95) | 94% / 92% | ✘ |
| Lộn + kép | Tâm linh (bắt số dân gian) | 6.6 | ×1.14 / ×1.00 (×0.87) | 68% / 62% | ✘ |
| PP17b Chu kỳ hay gặp (khoảng chưa ra đúng bằng chu kỳ cũ) | Pool app (top 14) | 14.0 | ×1.03 / ×1.00 (×0.97) | 90% / 92% | ✘ |
| Mai Hoa (giờ quay) | Tâm linh (Tarot, Mai Hoa, Kỳ Môn, Tứ trụ) | 2.4 | ×0.93 / ×1.00 (×1.06) | 28% / 28% | ✘ |
| Thần số học | Tâm linh (người chơi) | 15.0 | ×1.04 / ×1.00 (×0.95) | 94% / 92% | ✘ |
| Huyền Không Phi Tinh | Tâm linh (ngày giờ quay) | 9.4 | ×1.01 / ×0.99 (×0.98) | 77% / 77% | ✘ |
| PP24c Cùng ngày âm | Pool app (top 14) | 14.0 | ×1.03 / ×0.99 (×0.96) | 97% / 93% | ✘ |
| Nóng (c10≥3 hoặc c20≥2×kỳ vọng) | Tín hiệu gợi ý | 6.7 | ×0.97 / ×0.99 (×1.01) | 60% / 66% | ✘ |
| PP19 Cấp số của các lần ra | Pool app (top 14) | 14.0 | ×0.97 / ×0.99 (×1.01) | 89% / 90% | ✘ |
| PP20b Số kề kỳ trước (±2) | Pool app (top 14) | 14.0 | ×1.03 / ×0.99 (×0.95) | 91% / 92% | ✘ |
| PP23 Cặp hay đi cùng kỳ trước | Pool app (top 14) | 14.0 | ×1.08 / ×0.99 (×0.89) | 94% / 90% | ✘ |
| PP21 Tần suất theo vị trí (500 kỳ) | Pool app (top 14) | 14.0 | ×1.00 / ×0.99 (×0.98) | 91% / 90% | ✘ |
| Tiểu Lục Nhâm | Tâm linh (ngày giờ quay) | 13.3 | ×1.01 / ×0.97 (×0.93) | 90% / 90% | ✘ |
| Thái Ất (thời kế, rút gọn) | Tâm linh (ngày giờ quay) | 8.5 | ×0.95 / ×0.96 (×0.98) | 69% / 72% | ✘ |
| Bát trạch (cung mệnh) | Tâm linh (người chơi) | 10.0 | ×0.99 / ×0.96 (×0.93) | 79% / 78% | ✘ |
| Soi cầu: lô kép (11, 22, 33…) ra NHIỀU hơn bình quân | Khẳng định / nhóm (sổ) | 4.0 | ×1.16 / ×0.95 (×0.73) | 47% / 42% | ✘ |
| Ngũ hành nạp âm | Tâm linh (ngày giờ quay) | 9.0 | ×0.93 / ×0.95 (×0.97) | 78% / 75% | ✘ |
| Tứ trụ (dụng thần) | Tâm linh (Tarot, Mai Hoa, Kỳ Môn, Tứ trụ) | 9.0 | ×0.93 / ×0.93 (×0.94) | 69% / 71% | ✘ |
| PP18 Tích lũy đang giảm (sắp hồi) | Pool app (top 14) | 14.0 | ×0.94 / ×0.92 (×0.90) | 89% / 88% | ✘ |
| Hoàng đạo / Hắc đạo | Tâm linh (ngày giờ quay) | 3.7 | ×0.94 / ×0.92 (×0.90) | 40% / 39% | ✘ |
| Soi cầu: số cầu Pascal của kỳ trước ra NHIỀU hơn bình quân | Khẳng định / nhóm (sổ) | 1.0 | ×0.54 / ×0.88 (×1.22) | 7% / 12% | ít mẫu |
| Nhị thập bát tú | Tâm linh (ngày giờ quay) | 4.6 | ×0.95 / ×0.83 (×0.70) | 49% / 42% | ✘ |
| Loto 21h: nhóm tái xuất trong phiên ra NHIỀU hơn bình quân | Khẳng định / nhóm (sổ) | 0.0 | — / — (—) | — / — | ít mẫu |

### Tín hiệu ra ít (−) (5)

| Phương pháp | Nhóm | Cỡ TB | Ra so với BQ: 100 / 200 kỳ (100 trước) | Kỳ có ≥1 số trúng 100 / 200 | Đạt |
|---|---|---|---|---|---|
| Nhóm nhịp riêng "lúc vắng thế này chưa từng ra" ra ít hơn bình quân | Khẳng định / nhóm (sổ) | 6.5 | ×0.81 / ×0.84 (×0.88) | — / — | ✔ đạt |
| Cùng đuôi số kỳ trước | Tín hiệu gợi ý | 16.3 | ×0.91 / ×0.94 (×0.97) | — / — | ✔ đạt |
| Bóng khó ra (z<−1.5) | Tín hiệu gợi ý | 3.8 | ×1.26 / ×1.04 (×0.92) | — / — | ✘ |
| Soi cầu: lô kẹp (kỳ trước có a, a+2 → a+1) ra ÍT hơn bình quân | Khẳng định / nhóm (sổ) | 1.1 | ×0.72 / ×1.07 (×1.42) | — / — | ít mẫu |
| Nhóm "phá nhịp nghỉ" (100 kỳ: ≥80% lần nghỉ ≥x kỳ, mới nghỉ <x) ra ít hơn bình quân | Khẳng định / nhóm (sổ) | 7.2 | ×1.13 / ×1.08 (×1.04) | — / — | ✘ |

### Khẳng định (7)

| Phương pháp | Nhóm | Đúng 100 / 200 kỳ (100 trước) | Đạt |
|---|---|---|---|
| Có ≥1 số trùng hoặc kề ±1 kỳ trước | Khẳng định / nhóm (sổ) | 95% / 96% (98%) | ✔ đạt |
| Có ≥1 số của 2 kỳ gần nhất | Khẳng định / nhóm (sổ) | 90% / 91% (92%) | ✔ đạt |
| Không trùng ≥2 số với kỳ trước | Khẳng định / nhóm (sổ) | 86% / 88% (90%) | ✔ đạt |
| Nhỏ/lớn cân (3±1) | Khẳng định vé (gợi ý) | 87% / 86% (85%) | ✔ đạt |
| Chẵn/lẻ cân (3±1) | Khẳng định vé (gợi ý) | 86% / 86% (85%) | ✔ đạt |
| Có ≥1 số trong 10 số nóng nhất 20 kỳ | Khẳng định / nhóm (sổ) | 80% / 81% (82%) | ✔ đạt |
| Rải ≥4 hàng chục | Khẳng định vé (gợi ý) | 73% / 73% (73%) | ✔ đạt |

### Pool chuẩn — dùng 26 phương pháp đạt

- Loại hẳn (cả nhóm đúng ≥70% kỳ): Bỏ số ra 3 lần trong 5 kỳ, Bỏ số tái xuất sau vắng ≥15, Bỏ số ra 2 kỳ liền, Bỏ số nhịp "ra – vắng 2 – ra" (vừa ra lại sau đúng 2 kỳ vắng) · TB bỏ 2.5 số/kỳ, kỳ có số trúng bị loại nhầm: 25% (100 kỳ) / 24% (200 kỳ)
- Cộng điểm: Nhóm số của kỳ cách 7 kỳ ra NHIỀU hơn bình quân (dấu vết máy, 100 kỳ) (×1.03), Ra nhiều cả 4 đoạn 25 kỳ (×1.11), PP16 Gan (lâu chưa ra nhất) (×1.04), PP20 Số kề kỳ trước (±1) (×1.01), PP27 Gộp: 5 phương pháp tốt nhất 50 kỳ gần nhất (×1.02), Đại Lục Nhâm (rút gọn) (×1.08), Bóng âm dương (×1.06), Tổng chạm (×1.10), Tarot (3 lá) (×1.11), Kỳ Môn Độn Giáp (×1.02)
- Trừ điểm: Bỏ số vắng ≥25 kỳ (×0.86), Bỏ số ra kỳ trước VÀ kỳ t−3 (×0.89), Bỏ số ra nhiều nhất 100 kỳ (×0.83), Nhóm nhịp riêng "lúc vắng thế này chưa từng ra" ra ít hơn bình quân (×0.84), Cùng đuôi số kỳ trước (×0.94)
- Khẳng định đạt (dùng lọc vé, không lọc số): Có ≥1 số của 2 kỳ gần nhất, Có ≥1 số trong 10 số nóng nhất 20 kỳ, Có ≥1 số trùng hoặc kề ±1 kỳ trước, Không trùng ≥2 số với kỳ trước, Chẵn/lẻ cân (3±1), Nhỏ/lớn cân (3±1), Rải ≥4 hàng chục

| Cỡ pool | Pool chuẩn: TB trúng 100 / 200 kỳ | Kỳ ≥1/≥2/≥3 số (200 kỳ) | Ra so với BQ | Kiểm chéo (chọn từ 200 kỳ cũ): TB 100 / 200 · ×BQ | Pool app hiện tại: TB 100 / 200 · ×BQ |
|---|---|---|---|---|---|
| 10 | **1.69 / 1.64** | 90% / 55% / 17% | ×1.23 | 1.53 / 1.42 · ×1.06 | 1.46 / 1.44 · ×1.08 |
| 12 | **2.05 / 1.96** | 96% / 68% / 28% | ×1.22 | 1.84 / 1.68 · ×1.05 | 1.78 / 1.74 · ×1.08 |
| 15 | **2.38 / 2.27** | 98% / 78% / 40% | ×1.14 | 2.22 / 2.05 · ×1.02 | 2.21 / 2.11 · ×1.05 |
| 18 | **2.84 / 2.69** | 99% / 88% / 57% | ×1.12 | 2.62 / 2.44 · ×1.02 | 2.61 / 2.55 · ×1.06 |
| 20 | **3.10 / 3.00** | 100% / 94% / 70% | ×1.12 | 2.90 / 2.75 · ×1.03 | 2.87 / 2.81 · ×1.05 |

**Kỳ tới** — bị loại: 20  ·  xếp hạng: 34 36 12 22 24 31 10 17 37 28 04 32 41 19 29 18 45 14 21 01


## loto535 — 82 phương pháp, chấm trên 100 / 200 kỳ gần nhất (đến 05/10/2026 13h), BQ mỗi số ra 14.3%/kỳ

Đạt = ổn định ở cả 100 kỳ gần và 100 kỳ trước đó. Luật loại: đúng ≥70% + số bị loại ra ≤ BQ · Chọn số: ra > BQ · Ra ít: ra < BQ · Khẳng định: đúng ≥70%.


### Luật loại số (21)

| Phương pháp | Nhóm | Bỏ TB | Đúng 100 / 200 kỳ | Số bị loại ra (100 / 200 / 100 trước) | Đạt |
|---|---|---|---|---|---|
| Bỏ số nhịp "ra – vắng 2 – ra" (vừa ra lại sau đúng 2 kỳ vắng) | Luật loại (sổ) | 1.1 | 90% / 90% | ×0.61 / ×0.64 / ×0.67 | ✔ đạt |
| Bỏ số vắng lâu nhất | Luật loại (sổ) | 1.0 | 89% / 90% | ×0.77 / ×0.73 / ×0.70 | ✔ đạt |
| Bỏ số ra nhiều nhất 100 kỳ | Luật loại (sổ) | 1.0 | 85% / 88% | ×1.05 / ×0.81 / ×0.56 | ✘ |
| Bỏ số ra 3 lần trong 5 kỳ | Luật loại (sổ) | 1.2 | 86% / 88% | ×0.82 / ×0.68 / ×0.53 | ✔ đạt |
| Bỏ số phá nhịp tối thiểu (khung dài: Power 100, Mega 100, Loto 200 kỳ) | Luật loại (sổ) | 1.2 | 82% / 88% | ×1.13 / ×0.74 / ×0.47 | ✘ |
| Bỏ số ra kỳ trước VÀ kỳ t−3 | Luật loại (sổ) | 1.2 | 87% / 87% | ×0.76 / ×0.79 / ×0.83 | ✔ đạt |
| Bỏ số tái xuất sau vắng ≥15 | Luật loại (sổ) | 1.1 | 91% / 86% | ×0.70 / ×0.94 / ×1.26 | ✘ |
| Bỏ số ra ít nhất 100 kỳ | Luật loại (sổ) | 1.0 | 86% / 86% | ×0.98 / ×0.98 / ×0.98 | ✔ đạt |
| Bỏ số nhỏ nhất kỳ trước | Luật loại (sổ) | 1.0 | 86% / 86% | ×0.98 / ×0.98 / ×0.98 | ✔ đạt |
| Bỏ số lớn nhất kỳ trước | Luật loại (sổ) | 1.0 | 87% / 86% | ×0.91 / ×0.98 / ×1.05 | ✘ |
| Loto 13h: bỏ số tái xuất trong phiên (ra hôm trước sau vắng ≥10 kỳ 13h) | Luật loại (sổ) | 1.3 | 89% / 85% | ×0.56 / ×0.76 / ×0.96 | ✔ đạt |
| Bỏ số vắng ≥30 kỳ | Luật loại (sổ) | 1.0 | 87% / 85% | ×0.88 / ×1.06 / ×1.24 | ✘ |
| Bỏ số vắng lâu nhì | Luật loại (sổ) | 1.0 | 80% / 84% | ×1.40 / ×1.08 / ×0.77 | ✘ |
| Bỏ số phá nhịp tối thiểu (100 kỳ: luôn nghỉ ≥x kỳ, mới nghỉ <x) | Luật loại (sổ) | 1.8 | 82% / 84% | ×0.90 / ×0.69 / ×0.52 | ✔ đạt |
| Bỏ số tái xuất sau vắng ≥10 | Luật loại (sổ) | 1.4 | 87% / 84% | ×0.79 / ×0.84 / ×0.89 | ✔ đạt |
| Bỏ số vắng ≥25 kỳ | Luật loại (sổ) | 1.3 | 84% / 83% | ×0.98 / ×0.95 / ×0.93 | ✔ đạt |
| Bỏ số nóng nhất 10 kỳ (≥4 lần) | Luật loại (sổ) | 1.0 | 77% / 82% | ×1.62 / ×1.23 / ×0.78 | ✘ |
| Bỏ số ra 2 kỳ liền | Luật loại (sổ) | 1.2 | 79% / 82% | ×1.22 / ×1.08 / ×0.96 | ✘ |
| Bỏ số "lâu lâu mới ra" (khung gần: Power 100, Mega 100, Loto 200 kỳ; ≤85% kỳ vọng) đang vắng ≥15 | Luật loại (sổ) | 1.6 | 81% / 81% | ×0.85 / ×0.87 / ×0.88 | ✔ đạt |
| Bỏ số vắng ≥20 kỳ | Luật loại (sổ) | 1.8 | 78% / 78% | ×1.00 / ×0.90 / ×0.82 | ✔ đạt |
| Loto: bỏ số vắng ≥20 kỳ CÙNG PHIÊN (13h đúng ~80%, 21h ngược) | Luật loại (sổ) | 1.8 | 80% / 75% | ×0.94 / ×1.04 / ×1.13 | ✘ |

### Chọn số (+) (49)

| Phương pháp | Nhóm | Cỡ TB | Ra so với BQ: 100 / 200 kỳ (100 trước) | Kỳ có ≥1 số trúng 100 / 200 | Đạt |
|---|---|---|---|---|---|
| Soi cầu: số cầu Pascal của kỳ trước ra NHIỀU hơn bình quân | Khẳng định / nhóm (sổ) | 1.0 | ×1.69 / ×1.40 (×1.08) | 24% / 20% | ít mẫu |
| Soi cầu: kép liền kề của kép kỳ trước (11↔22↔33) ra NHIỀU hơn bình quân | Khẳng định / nhóm (sổ) | 1.5 | ×1.27 / ×1.31 (×1.34) | 27% / 27% | ít mẫu |
| Soi cầu: lô kép (11, 22, 33…) ra NHIỀU hơn bình quân | Khẳng định / nhóm (sổ) | 3.0 | ×1.14 / ×1.24 (×1.33) | 44% / 46% | ✔ đạt |
| Hoàng đạo / Hắc đạo | Tâm linh (ngày giờ quay) | 2.9 | ×1.32 / ×1.23 (×1.14) | 43% / 43% | ✔ đạt |
| Lộn + kép | Tâm linh (bắt số dân gian) | 4.7 | ×1.20 / ×1.19 (×1.18) | 64% / 61% | ✔ đạt |
| Nhóm số của kỳ cách 7 kỳ ra NHIỀU hơn bình quân (dấu vết máy, 100 kỳ) | Khẳng định / nhóm (sổ) | 4.4 | ×1.17 / ×1.13 (×1.10) | 55% / 54% | ✔ đạt |
| Nhóm số của kỳ cách 9 kỳ ra NHIỀU hơn bình quân (dấu vết máy, 100 kỳ) | Khẳng định / nhóm (sổ) | 4.3 | ×1.24 / ×1.13 (×1.02) | 57% / 56% | ✔ đạt |
| Xin xăm (100 quẻ) | Tâm linh (người chơi) | 4.8 | ×1.20 / ×1.11 (×1.01) | 61% / 56% | ✔ đạt |
| PP16 Gan (lâu chưa ra nhất) | Pool app (top 11) | 11.0 | ×1.04 / ×1.07 (×1.11) | 94% / 92% | ✔ đạt |
| Loto 21h: nhóm tái xuất trong phiên ra NHIỀU hơn bình quân | Khẳng định / nhóm (sổ) | 1.4 | ×0.60 / ×1.07 (×1.45) | 11% / 21% | ít mẫu |
| PP17 Đến chu kỳ trung bình | Pool app (top 11) | 11.0 | ×1.06 / ×1.07 (×1.07) | 89% / 88% | ✔ đạt |
| PP27 Gộp: 5 phương pháp tốt nhất 50 kỳ gần nhất | Pool app (top 11) | 11.0 | ×1.03 / ×1.06 (×1.09) | 89% / 88% | ✔ đạt |
| Thái Ất (thời kế, rút gọn) | Tâm linh (ngày giờ quay) | 6.2 | ×1.02 / ×1.06 (×1.10) | 65% / 70% | ✔ đạt |
| PP24c Cùng ngày âm | Pool app (top 11) | 11.0 | ×1.20 / ×1.06 (×0.92) | 95% / 90% | ✘ |
| Bóng âm dương | Tâm linh (bắt số dân gian) | 8.1 | ×1.14 / ×1.05 (×0.97) | 87% / 78% | ✘ |
| Nóng (c10≥3 hoặc c20≥2×kỳ vọng) | Tín hiệu gợi ý | 6.1 | ×1.15 / ×1.05 (×0.94) | 68% / 62% | ✘ |
| PP23 Cặp hay đi cùng kỳ trước | Pool app (top 11) | 11.0 | ×1.08 / ×1.05 (×1.01) | 92% / 90% | ✔ đạt |
| Kề ±1 kỳ trước | Tín hiệu gợi ý | 8.2 | ×0.95 / ×1.04 (×1.14) | 72% / 78% | ✘ |
| PP20b Số kề kỳ trước (±2) | Pool app (top 11) | 11.0 | ×0.93 / ×1.04 (×1.15) | 87% / 92% | ✘ |
| Tarot (3 lá) | Tâm linh (Tarot, Mai Hoa, Kỳ Môn, Tứ trụ) | 3.5 | ×1.03 / ×1.04 (×1.05) | 39% / 42% | ✔ đạt |
| PP22 Markov số → số | Pool app (top 11) | 11.0 | ×1.08 / ×1.04 (×1.00) | 91% / 90% | ✘ |
| Bóng dễ ra (z>1) | Tín hiệu gợi ý | 6.2 | ×1.05 / ×1.03 (×1.02) | 67% / 65% | ✔ đạt |
| Huyền Không Phi Tinh | Tâm linh (ngày giờ quay) | 7.4 | ×1.04 / ×1.03 (×1.02) | 72% / 72% | ✔ đạt |
| PP21 Tần suất theo vị trí (500 kỳ) | Pool app (top 11) | 11.0 | ×1.01 / ×1.03 (×1.05) | 85% / 88% | ✔ đạt |
| PP20 Số kề kỳ trước (±1) | Pool app (top 11) | 11.0 | ×0.93 / ×1.02 (×1.11) | 85% / 88% | ✘ |
| Chuyển kỳ, top 8 | Tín hiệu gợi ý | 8.0 | ×1.06 / ×1.01 (×0.97) | 73% / 73% | ✘ |
| Kỳ Môn Độn Giáp | Tâm linh (Tarot, Mai Hoa, Kỳ Môn, Tứ trụ) | 6.5 | ×1.03 / ×1.01 (×1.00) | 68% / 68% | ✔ đạt |
| Đại Lục Nhâm (rút gọn) | Tâm linh (ngày giờ quay) | 7.5 | ×1.01 / ×1.01 (×1.01) | 75% / 70% | ✔ đạt |
| PP18 Tích lũy đang giảm (sắp hồi) | Pool app (top 11) | 11.0 | ×0.96 / ×1.00 (×1.04) | 86% / 90% | ✘ |
| PP15 Nóng 30 kỳ (ra nhiều nhất) | Pool app (top 11) | 11.0 | ×1.05 / ×1.00 (×0.95) | 89% / 87% | ✘ |
| Thần số học | Tâm linh (người chơi) | 11.0 | ×0.95 / ×1.00 (×1.05) | 85% / 86% | ✘ |
| Ngũ hành nạp âm | Tâm linh (ngày giờ quay) | 7.0 | ×0.95 / ×0.99 (×1.03) | 71% / 71% | ✘ |
| Tiểu Lục Nhâm | Tâm linh (ngày giờ quay) | 10.3 | ×1.06 / ×0.99 (×0.91) | 89% / 86% | ✘ |
| PP18t Tích lũy đang tăng | Pool app (top 11) | 11.0 | ×1.06 / ×0.99 (×0.92) | 85% / 84% | ✘ |
| PP24 Cùng giờ / cùng thứ 60 kỳ | Pool app (top 11) | 11.0 | ×0.98 / ×0.99 (×1.00) | 84% / 84% | ✘ |
| Chạm đầu đuôi | Tâm linh (bắt số dân gian) | 21.7 | ×0.94 / ×0.98 (×1.03) | 99% / 98% | ✘ |
| Bát trạch (cung mệnh) | Tâm linh (người chơi) | 8.0 | ×0.95 / ×0.98 (×1.01) | 72% / 76% | ✘ |
| Nóng cùng phiên 100 kỳ, top 8 | Tín hiệu gợi ý | 8.0 | ×1.00 / ×0.97 (×0.95) | 71% / 70% | ✘ |
| Nhị thập bát tú | Tâm linh (ngày giờ quay) | 3.5 | ×0.88 / ×0.96 (×1.05) | 40% / 43% | ✘ |
| PP19 Cấp số của các lần ra | Pool app (top 11) | 11.0 | ×0.97 / ×0.96 (×0.95) | 85% / 86% | ✘ |
| Tử vi (Mệnh, Cục, sao Tử Vi) | Tâm linh (người chơi) | 10.0 | ×0.99 / ×0.96 (×0.92) | 85% / 82% | ✘ |
| Bạc nhớ | Tâm linh (bắt số dân gian) | 11.0 | ×0.98 / ×0.96 (×0.94) | 89% / 90% | ✘ |
| Tổng phiếu 20 phương pháp tâm linh, top 11 | Tâm linh (tổng phiếu) | 11.0 | ×0.94 / ×0.95 (×0.97) | 84% / 84% | ✘ |
| PP17b Chu kỳ hay gặp (khoảng chưa ra đúng bằng chu kỳ cũ) | Pool app (top 11) | 11.0 | ×0.96 / ×0.93 (×0.89) | 90% / 88% | ✘ |
| Tứ trụ (dụng thần) | Tâm linh (Tarot, Mai Hoa, Kỳ Môn, Tứ trụ) | 7.0 | ×0.88 / ×0.93 (×0.97) | 69% / 69% | ✘ |
| PP26 Bóng đối xứng (N+1−n) kỳ trước | Pool app (top 11) | 11.0 | ×0.88 / ×0.90 (×0.92) | 84% / 84% | ✘ |
| Tổng chạm | Tâm linh (bắt số dân gian) | 3.3 | ×0.84 / ×0.90 (×0.95) | 34% / 38% | ✘ |
| Soi cầu: cầu vị trí đã chạy ≥2 kỳ ra NHIỀU hơn bình quân | Khẳng định / nhóm (sổ) | 1.6 | ×1.07 / ×0.76 (×0.46) | 18% / 15% | ít mẫu |
| Mai Hoa (giờ quay) | Tâm linh (Tarot, Mai Hoa, Kỳ Môn, Tứ trụ) | 1.7 | ×0.71 / ×0.72 (×0.72) | 17% / 17% | ✘ |

### Tín hiệu ra ít (−) (5)

| Phương pháp | Nhóm | Cỡ TB | Ra so với BQ: 100 / 200 kỳ (100 trước) | Kỳ có ≥1 số trúng 100 / 200 | Đạt |
|---|---|---|---|---|---|
| Soi cầu: lô kẹp (kỳ trước có a, a+2 → a+1) ra ÍT hơn bình quân | Khẳng định / nhóm (sổ) | 1.1 | ×0.82 / ×0.85 (×0.89) | — / — | ít mẫu |
| Nhóm nhịp riêng "lúc vắng thế này chưa từng ra" ra ít hơn bình quân | Khẳng định / nhóm (sổ) | 4.1 | ×0.95 / ×0.92 (×0.89) | — / — | ✔ đạt |
| Nhóm "phá nhịp nghỉ" (100 kỳ: ≥80% lần nghỉ ≥x kỳ, mới nghỉ <x) ra ít hơn bình quân | Khẳng định / nhóm (sổ) | 6.0 | ×0.92 / ×0.92 (×0.91) | — / — | ✔ đạt |
| Số vừa ra kỳ trước | Tín hiệu gợi ý | 5.0 | ×0.88 / ×0.95 (×1.02) | — / — | ✘ |
| Bóng khó ra (z<−1.5) | Tín hiệu gợi ý | 4.2 | ×1.14 / ×0.98 (×0.86) | — / — | ✘ |

### Khẳng định (7)

| Phương pháp | Nhóm | Đúng 100 / 200 kỳ (100 trước) | Đạt |
|---|---|---|---|
| Có ≥1 số trùng hoặc kề ±1 kỳ trước | Khẳng định / nhóm (sổ) | 90% / 93% (96%) | ✔ đạt |
| Không trùng ≥2 số với kỳ trước | Khẳng định / nhóm (sổ) | 91% / 88% (86%) | ✔ đạt |
| Rải ≥3 hàng chục | Khẳng định vé (gợi ý) | 90% / 87% (84%) | ✔ đạt |
| Có ≥1 số trong 10 số nóng nhất 20 kỳ | Khẳng định / nhóm (sổ) | 84% / 82% (81%) | ✔ đạt |
| Có ≥1 số của 2 kỳ gần nhất | Khẳng định / nhóm (sổ) | 81% / 80% (79%) | ✔ đạt |
| Nhỏ/lớn cân (2±1) | Khẳng định vé (gợi ý) | 71% / 68% (64%) | ✘ |
| Chẵn/lẻ cân (2±1) | Khẳng định vé (gợi ý) | 62% / 64% (67%) | ✘ |

### Pool chuẩn — dùng 36 phương pháp đạt

- Loại hẳn (cả nhóm đúng ≥70% kỳ): Bỏ số nhịp "ra – vắng 2 – ra" (vừa ra lại sau đúng 2 kỳ vắng), Bỏ số ra 3 lần trong 5 kỳ, Bỏ số phá nhịp tối thiểu (100 kỳ: luôn nghỉ ≥x kỳ, mới nghỉ <x), Loto 13h: bỏ số tái xuất trong phiên (ra hôm trước sau vắng ≥10 kỳ 13h) · TB bỏ 2.8 số/kỳ, kỳ có số trúng bị loại nhầm: 28% (100 kỳ) / 24% (200 kỳ)
- Cộng điểm: Nhóm số của kỳ cách 7 kỳ ra NHIỀU hơn bình quân (dấu vết máy, 100 kỳ) (×1.13), Nhóm số của kỳ cách 9 kỳ ra NHIỀU hơn bình quân (dấu vết máy, 100 kỳ) (×1.13), Soi cầu: lô kép (11, 22, 33…) ra NHIỀU hơn bình quân (×1.24), Bóng dễ ra (z>1) (×1.03), PP16 Gan (lâu chưa ra nhất) (×1.07), PP17 Đến chu kỳ trung bình (×1.07), PP23 Cặp hay đi cùng kỳ trước (×1.05), PP21 Tần suất theo vị trí (500 kỳ) (×1.03), PP27 Gộp: 5 phương pháp tốt nhất 50 kỳ gần nhất (×1.06), Đại Lục Nhâm (rút gọn) (×1.01), Thái Ất (thời kế, rút gọn) (×1.06), Huyền Không Phi Tinh (×1.03), Hoàng đạo / Hắc đạo (×1.23), Lộn + kép (×1.19), Xin xăm (100 quẻ) (×1.11), Tarot (3 lá) (×1.04), Kỳ Môn Độn Giáp (×1.01)
- Trừ điểm: Bỏ số vắng ≥20 kỳ (×0.90), Bỏ số vắng ≥25 kỳ (×0.95), Bỏ số "lâu lâu mới ra" (khung gần: Power 100, Mega 100, Loto 200 kỳ; ≤85% kỳ vọng) đang vắng ≥15 (×0.87), Bỏ số vắng lâu nhất (×0.73), Bỏ số ra kỳ trước VÀ kỳ t−3 (×0.79), Bỏ số tái xuất sau vắng ≥10 (×0.84), Bỏ số ra ít nhất 100 kỳ (×0.98), Bỏ số nhỏ nhất kỳ trước (×0.98), Nhóm "phá nhịp nghỉ" (100 kỳ: ≥80% lần nghỉ ≥x kỳ, mới nghỉ <x) ra ít hơn bình quân (×0.92), Nhóm nhịp riêng "lúc vắng thế này chưa từng ra" ra ít hơn bình quân (×0.92)
- Khẳng định đạt (dùng lọc vé, không lọc số): Có ≥1 số của 2 kỳ gần nhất, Có ≥1 số trong 10 số nóng nhất 20 kỳ, Có ≥1 số trùng hoặc kề ±1 kỳ trước, Không trùng ≥2 số với kỳ trước, Rải ≥3 hàng chục

| Cỡ pool | Pool chuẩn: TB trúng 100 / 200 kỳ | Kỳ ≥1/≥2/≥3 số (200 kỳ) | Ra so với BQ | Kiểm chéo (chọn từ 200 kỳ cũ): TB 100 / 200 · ×BQ | Pool app hiện tại: TB 100 / 200 · ×BQ |
|---|---|---|---|---|---|
| 6 | **1.07 / 1.07** | 72% / 30% / 4% | ×1.25 | 0.94 / 0.95 · ×1.11 | 0.96 / 0.92 · ×1.07 |
| 8 | **1.47 / 1.44** | 86% / 44% / 13% | ×1.26 | 1.16 / 1.23 · ×1.07 | 1.31 / 1.23 · ×1.08 |
| 10 | **1.81 / 1.74** | 91% / 58% / 22% | ×1.22 | 1.43 / 1.49 · ×1.04 | 1.65 / 1.56 · ×1.10 |
| 12 | **2.08 / 2.02** | 95% / 70% / 32% | ×1.18 | 1.71 / 1.81 · ×1.06 | 1.93 / 1.87 · ×1.09 |
| 15 | **2.51 / 2.44** | 99% / 84% / 46% | ×1.14 | 2.21 / 2.31 · ×1.08 | 2.38 / 2.33 · ×1.09 |

**Kỳ tới** — bị loại: 09 14 35  ·  xếp hạng: 11 22 34 33 23 10 06 08 24 28 13 32 01 30 20

### Số May Mắn (BQ 3 số / 12 = 25%)

| Cách | Trúng 100 kỳ | 100 trước | 200 kỳ |
|---|---|---|---|
| 3 số vắng lâu nhất (đang dùng) | 31% | 27% | 29% |
| MM kỳ trước + 2 vắng lâu (đề xuất cũ) | 33% | 26% | 30% |


## Max 3D+ — chấm trên 100 / 200 kỳ gần nhất (đến 05/10/2026), BQ mỗi bộ ra 2%/kỳ

| Phương pháp | Loại / chọn | Cỡ TB (bộ) | Ra so với BQ: 100 / 200 kỳ (100 trước) | Kỳ có ≥1 bộ ĐB rơi vào (200 kỳ) | Đạt |
|---|---|---|---|---|---|
| Tâm linh: Ngày + tháng âm (25/8 → 258, 825) | chọn | 2 | ×2.01 / ×2.01 (×2.01) | 0% | ít mẫu |
| Tâm linh: Bóng âm dương 2 số ĐB kỳ trước | chọn | 2 | ×0.75 / ×1.50 (×2.25) | 1% | ít mẫu |
| Tâm linh: Ngày + tháng dương (05/10 → 050, 005…) | chọn | 2 | ×1.25 / ×1.38 (×1.51) | 0% | ít mẫu |
| Tâm linh: Tam hoa theo thần số học ngày | chọn | 1 | ×2.50 / ×1.25 (×0.00) | 0% | ít mẫu |
| Quanh ±1 một chữ số của 20 bộ kỳ trước | chọn | 112 | ×1.08 / ×1.04 (×1.00) | 24% | ✘ |
| Pool app hiện tại (340 bộ) | chọn | 340 | ×1.02 / ×1.04 (×1.06) | 56% | ✔ đạt |
| 340 bộ chữ số nặng nhất (50 kỳ), không loại gì | chọn | 340 | ×1.00 / ×1.02 (×1.05) | 58% | ✔ đạt |
| Tâm linh: Lộn 2 số ĐB kỳ trước | chọn | 2 | ×0.83 / ×0.97 (×1.11) | 0% | ít mẫu |
| 20 bộ kỳ trước (lặp lại) | chọn | 20 | ×0.81 / ×0.77 (×0.73) | 3% | ✘ |
| 2 bộ ĐB kỳ trước | chọn | 2 | ×0.75 / ×0.50 (×0.25) | 0% | ít mẫu |
| Bỏ tam hoa (000…999) | loại | 10 | ×1.15 / ×1.15 (×1.15) | 2% | ✘ |
| Bỏ dạng 00x | loại | 10 | ×0.90 / ×1.10 (×1.30) | 1% | ✘ |
| Bỏ bộ ra trong 30 kỳ gần | loại | 451 | ×1.03 / ×1.02 (×1.00) | 70% | ✘ |
| Bỏ bộ ra trong 10 kỳ gần | loại | 182 | ×0.98 / ×0.98 (×0.98) | 35% | ✔ đạt |
| Bộ có chữ số nhẹ nhất 100 kỳ ở mọi hàng (đang theo dõi) | loại | 271 | ×0.97 / ×0.97 (×0.97) | 46% | ✔ đạt |
| Bỏ bộ ra trong 5 kỳ gần | loại | 96 | ×0.96 / ×0.95 (×0.93) | 16% | ✔ đạt |
| Bộ kép kẹp (aba) — app trừ điểm nhẹ | loại | 90 | ×0.92 / ×0.89 (×0.86) | 18% | ✔ đạt |
| Bỏ bộ tiến liên tiếp (012…789) | loại | 8 | ×0.75 / ×0.78 (×0.81) | 2% | ✔ đạt |

**17 phương pháp tâm linh** (tỉ số ra so với BQ, 100 kỳ gần / 100 trước): Tiểu Lục Nhâm ×1.02/×0.98 · Đại Lục Nhâm (rút gọn) ×0.98/×0.98 · Thái Ất (thời kế, rút gọn) ×1.03/×1.00 ✔ · Huyền Không Phi Tinh ×0.95/×1.06 · Nhị thập bát tú ×1.06/×1.05 ✔ · Hoàng đạo / Hắc đạo ×1.06/×1.06 ✔ · Ngũ hành nạp âm ×1.00/×1.10 ✔ · Thần số học ×1.00/×0.99 · Tử vi (Mệnh, Cục, sao Tử Vi) ×0.99/×0.99 · Xin xăm (100 quẻ) ×0.99/×1.01 · Tarot (3 lá) ×1.08/×0.89 · Mai Hoa (giờ quay) ×1.30/×1.04 (ít mẫu) · Kỳ Môn Độn Giáp ×0.94/×1.24 · Tứ trụ (dụng thần) ×1.01/×1.04 ✔ · Bát trạch (cung mệnh) ×1.03/×1.00 · Bóng âm dương 2 số ĐB kỳ trước ×1.38/×1.75 (ít mẫu) · Lộn 2 số ĐB kỳ trước ×0.75/×1.00 (ít mẫu)

**Pool chuẩn** — loại: Bỏ bộ ra trong 5 kỳ gần, Bỏ bộ ra trong 10 kỳ gần, Bỏ bộ tiến liên tiếp (012…789), Bộ kép kẹp (aba) — app trừ điểm nhẹ, Bộ có chữ số nhẹ nhất 100 kỳ ở mọi hàng (đang theo dõi) (TB bỏ 468 bộ); cộng điểm: Pool app hiện tại (340 bộ), 340 bộ chữ số nặng nhất (50 kỳ), không loại gì; hòa điểm xếp theo chữ số nặng.

| Cỡ pool | Pool chuẩn: ×BQ 100 / 200 kỳ | Kỳ có ≥1 ĐB trong pool (200 kỳ) / kỳ vọng theo cỡ | Kiểm chéo (chọn từ 200 kỳ cũ): ×BQ 100 / 200 |
|---|---|---|---|
| 100 | **×1.08 / ×1.09** | 24% / 19% | ×1.03 / ×1.07 |
| 200 | **×1.03 / ×1.05** | 41% / 36% | ×1.02 / ×1.06 |
| 340 | **×1.04 / ×1.05** | 56% / 56% | ×1.01 / ×1.03 |
| 400 | **×1.04 / ×1.05** | 64% / 64% | ×1.00 / ×1.03 |
| 500 | **×1.03 / ×1.03** | 80% / 75% | ×1.02 / ×1.03 |

## Max 3D Pro — chấm trên 100 / 200 kỳ gần nhất (đến 03/10/2026), BQ mỗi bộ ra 2%/kỳ

| Phương pháp | Loại / chọn | Cỡ TB (bộ) | Ra so với BQ: 100 / 200 kỳ (100 trước) | Kỳ có ≥1 bộ ĐB rơi vào (200 kỳ) | Đạt |
|---|---|---|---|---|---|
| Tâm linh: Lộn 2 số ĐB kỳ trước | chọn | 2 | ×1.96 / ×1.66 (×1.37) | 1% | ít mẫu |
| Tâm linh: Tam hoa theo thần số học ngày | chọn | 1 | ×1.00 / ×1.25 (×1.50) | 0% | ít mẫu |
| 2 bộ ĐB kỳ trước | chọn | 2 | ×1.25 / ×1.12 (×1.00) | 0% | ít mẫu |
| Pool app hiện tại (400 bộ) | chọn | 400 | ×1.00 / ×1.03 (×1.07) | 67% | ✘ |
| Tâm linh: Ngày + tháng âm (25/8 → 258, 825) | chọn | 2 | ×1.26 / ×1.01 (×0.75) | 0% | ít mẫu |
| 400 bộ chữ số nặng nhất (100 kỳ), không loại gì | chọn | 400 | ×0.96 / ×0.99 (×1.02) | 56% | ✘ |
| Quanh ±1 một chữ số của 20 bộ kỳ trước | chọn | 112 | ×1.05 / ×0.99 (×0.92) | 20% | ✘ |
| 20 bộ kỳ trước (lặp lại) | chọn | 20 | ×0.88 / ×0.91 (×0.93) | 3% | ✘ |
| Tâm linh: Ngày + tháng dương (05/10 → 050, 005…) | chọn | 2 | ×0.75 / ×0.75 (×0.75) | 0% | ít mẫu |
| Tâm linh: Bóng âm dương 2 số ĐB kỳ trước | chọn | 2 | ×0.75 / ×0.62 (×0.50) | 0% | ít mẫu |
| Bỏ dạng 00x | loại | 10 | ×1.10 / ×1.17 (×1.25) | 1% | ✘ |
| Bộ có chữ số nhẹ nhất 100 kỳ ở mọi hàng (đang theo dõi) | loại | 271 | ×1.00 / ×1.03 (×1.07) | 49% | ✘ |
| Bộ kép kẹp (aba) — app trừ điểm nhẹ | loại | 90 | ×1.13 / ×1.01 (×0.89) | 16% | ✘ |
| Bỏ bộ ra trong 30 kỳ gần | loại | 457 | ×0.97 / ×0.96 (×0.94) | 65% | ✔ đạt |
| Bỏ bộ ra trong 5 kỳ gần | loại | 96 | ×0.98 / ×0.95 (×0.92) | 14% | ✔ đạt |
| Bỏ bộ ra trong 10 kỳ gần | loại | 182 | ×0.98 / ×0.94 (×0.91) | 26% | ✔ đạt |
| Bỏ tam hoa (000…999) | loại | 10 | ×0.90 / ×0.87 (×0.85) | 2% | ✔ đạt |
| Bỏ bộ tiến liên tiếp (012…789) | loại | 8 | ×0.69 / ×0.81 (×0.94) | 2% | ✔ đạt |

**17 phương pháp tâm linh** (tỉ số ra so với BQ, 100 kỳ gần / 100 trước): Tiểu Lục Nhâm ×0.98/×1.00 · Đại Lục Nhâm (rút gọn) ×1.00/×0.99 · Thái Ất (thời kế, rút gọn) ×0.96/×0.95 · Huyền Không Phi Tinh ×1.02/×1.01 ✔ · Nhị thập bát tú ×0.99/×1.08 · Hoàng đạo / Hắc đạo ×0.90/×1.12 · Ngũ hành nạp âm ×0.96/×0.99 · Thần số học ×1.01/×0.96 · Tử vi (Mệnh, Cục, sao Tử Vi) ×1.03/×0.98 · Xin xăm (100 quẻ) ×0.97/×0.99 · Tarot (3 lá) ×0.60/×0.59 · Mai Hoa (giờ quay) ×1.04/×1.31 (ít mẫu) · Kỳ Môn Độn Giáp ×1.32/×0.94 · Tứ trụ (dụng thần) ×0.93/×0.99 · Bát trạch (cung mệnh) ×1.04/×0.93 · Bóng âm dương 2 số ĐB kỳ trước ×1.12/×0.88 (ít mẫu) · Lộn 2 số ĐB kỳ trước ×2.00/×1.25 (ít mẫu)

**Pool chuẩn** — loại: Bỏ bộ ra trong 5 kỳ gần, Bỏ bộ ra trong 10 kỳ gần, Bỏ bộ ra trong 30 kỳ gần, Bỏ bộ tiến liên tiếp (012…789), Bỏ tam hoa (000…999) (TB bỏ 467 bộ); cộng điểm: —; hòa điểm xếp theo chữ số nặng.

| Cỡ pool | Pool chuẩn: ×BQ 100 / 200 kỳ | Kỳ có ≥1 ĐB trong pool (200 kỳ) / kỳ vọng theo cỡ | Kiểm chéo (chọn từ 200 kỳ cũ): ×BQ 100 / 200 |
|---|---|---|---|
| 100 | **×0.92 / ×1.02** | 18% / 19% | ×1.05 / ×1.08 |
| 200 | **×0.97 / ×1.03** | 34% / 36% | ×0.96 / ×1.00 |
| 340 | **×0.99 / ×1.03** | 58% / 56% | ×0.94 / ×0.98 |
| 400 | **×1.02 / ×1.04** | 67% / 64% | ×0.96 / ×0.99 |
| 500 | **×1.04 / ×1.04** | 76% / 75% | ×0.95 / ×0.98 |



# Tăng % kỳ về ≥4 số trong pool — 13/10/2026 (`python build/pool_hoc.py <game>`, rải vé: `python build/rai_ve.py <game>`)

## power655 — tăng % kỳ có ≥4 số về trong pool (chạy tiến, mọi số liệu là kỳ chưa thấy; dữ liệu đến 03/10/2026)

93 đặc trưng/số: luật sổ, tín hiệu gợi ý, 16 PP pool app, 20 PP tâm linh + tổng phiếu, Markov trễ 1–3 & bậc 2–3, vắng, số lần ra.


### Pool 10 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Điểm theo tỉ lệ ra 100 kỳ gần | 8% · 10% | **3% · 4%** | 0% · 0.0% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 7% · 8% | **2% · 2%** | 0% · 0.5% |
| Pool app đang dùng | 11% · 10% | **3% · 2%** | 0% · 0.0% |
| Markov bậc 2 (học 50 kỳ) | 11% · 11% | **1% · 2%** | 0% · 0.5% |
| Gộp tất cả cách trên | 11% · 10% | **3% · 2%** | 0% · 0.0% |
| Tự chọn cách tốt nhất 50 kỳ trước | 10% · 10% | **2% · 2%** | 0% · 0.0% |
| Markov bậc 2 (học 100 kỳ) | 7% · 8% | **1% · 2%** | 1% · 0.5% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 8% · 6% | **2% · 2%** | 0% · 0.5% |
| Hồi quy logistic học 200 kỳ | 14% · 12% | **0% · 1%** | 0% · 0.0% |
| Gộp: app + logistic 200 + Markov bậc 2 | 10% · 9% | **2% · 1%** | 0% · 0.0% |
| Cây tăng cường học 200 kỳ | 7% · 6% | **2% · 1%** | 0% · 0.0% |
| Hồi quy logistic học 100 kỳ | 11% · 8% | **0% · 0%** | 0% · 0.0% |
| Markov bậc 3 (học 50 kỳ) | 7% · 8% | **1% · 0%** | 0% · 0.0% |

### Pool 12 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Điểm theo tỉ lệ ra 100 kỳ gần | 12% · 12% | **4% · 4%** | 1% · 0.5% |
| Hồi quy logistic học 200 kỳ | 18% · 15% | **4% · 3%** | 0% · 0.0% |
| Gộp: app + logistic 200 + Markov bậc 2 | 18% · 15% | **5% · 3%** | 1% · 0.5% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 11% · 14% | **3% · 3%** | 1% · 1.0% |
| Pool app đang dùng | 14% · 14% | **4% · 3%** | 1% · 0.5% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 14% · 12% | **5% · 3%** | 0% · 0.5% |
| Markov bậc 2 (học 50 kỳ) | 19% · 16% | **2% · 2%** | 0% · 0.5% |
| Cây tăng cường học 200 kỳ | 8% · 9% | **3% · 2%** | 0% · 0.0% |
| Markov bậc 2 (học 100 kỳ) | 16% · 16% | **1% · 2%** | 1% · 1.0% |
| Gộp tất cả cách trên | 16% · 14% | **3% · 2%** | 1% · 0.5% |
| Tự chọn cách tốt nhất 50 kỳ trước | 17% · 14% | **2% · 2%** | 0% · 0.0% |
| Hồi quy logistic học 100 kỳ | 16% · 14% | **0% · 1%** | 0% · 0.0% |
| Markov bậc 3 (học 50 kỳ) | 15% · 14% | **1% · 1%** | 0% · 0.0% |

### Pool 15 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Markov bậc 2 (học 50 kỳ) | 25% · 25% | **9% · 8%** | 1% · 1.0% |
| Hồi quy logistic học 200 kỳ | 24% · 24% | **9% · 7%** | 2% · 1.0% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 23% · 23% | **9% · 7%** | 3% · 2.5% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 22% · 20% | **8% · 6%** | 1% · 1.0% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 27% · 26% | **8% · 6%** | 2% · 1.5% |
| Markov bậc 3 (học 50 kỳ) | 22% · 22% | **5% · 6%** | 0% · 0.0% |
| Gộp: app + logistic 200 + Markov bậc 2 | 21% · 24% | **7% · 6%** | 2% · 1.0% |
| Markov bậc 2 (học 100 kỳ) | 25% · 28% | **4% · 5%** | 1% · 1.0% |
| Tự chọn cách tốt nhất 50 kỳ trước | 22% · 22% | **6% · 5%** | 0% · 0.0% |
| Pool app đang dùng | 23% · 24% | **6% · 4%** | 3% · 2.0% |
| Gộp tất cả cách trên | 25% · 24% | **3% · 4%** | 2% · 1.5% |
| Hồi quy logistic học 100 kỳ | 28% · 24% | **4% · 4%** | 0% · 0.0% |
| Cây tăng cường học 200 kỳ | 19% · 20% | **3% · 4%** | 0% · 0.0% |

### Pool 18 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Markov bậc 2 (học 50 kỳ) | 35% · 36% | **14% · 14%** | 2% · 1.5% |
| Hồi quy logistic học 200 kỳ | 32% · 35% | **14% · 14%** | 3% · 1.5% |
| Markov bậc 3 (học 50 kỳ) | 39% · 37% | **13% · 13%** | 4% · 2.5% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 35% · 34% | **15% · 13%** | 4% · 2.5% |
| Markov bậc 2 (học 100 kỳ) | 38% · 41% | **12% · 12%** | 1% · 1.5% |
| Tự chọn cách tốt nhất 50 kỳ trước | 36% · 34% | **14% · 12%** | 3% · 1.5% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 36% · 34% | **12% · 10%** | 3% · 2.5% |
| Pool app đang dùng | 33% · 36% | **13% · 10%** | 5% · 3.0% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 37% · 36% | **13% · 10%** | 2% · 2.0% |
| Gộp: app + logistic 200 + Markov bậc 2 | 31% · 32% | **11% · 10%** | 3% · 2.0% |
| Hồi quy logistic học 100 kỳ | 37% · 38% | **11% · 9%** | 1% · 1.0% |
| Cây tăng cường học 200 kỳ | 27% · 28% | **8% · 9%** | 0% · 0.0% |
| Gộp tất cả cách trên | 40% · 38% | **8% · 8%** | 2% · 1.5% |

### Pool 20 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Markov bậc 2 (học 100 kỳ) | 43% · 48% | **18% · 20%** | 1% · 2.0% |
| Markov bậc 3 (học 50 kỳ) | 45% · 42% | **21% · 19%** | 5% · 3.5% |
| Markov bậc 2 (học 50 kỳ) | 39% · 42% | **17% · 18%** | 5% · 3.0% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 41% · 40% | **19% · 17%** | 6% · 4.5% |
| Tự chọn cách tốt nhất 50 kỳ trước | 40% · 40% | **19% · 16%** | 4% · 2.5% |
| Hồi quy logistic học 200 kỳ | 33% · 38% | **17% · 16%** | 5% · 3.5% |
| Gộp: app + logistic 200 + Markov bậc 2 | 41% · 40% | **17% · 14%** | 3% · 3.0% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 45% · 43% | **16% · 14%** | 2% · 2.5% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 43% · 43% | **16% · 14%** | 4% · 3.0% |
| Cây tăng cường học 200 kỳ | 38% · 37% | **14% · 14%** | 0% · 0.0% |
| Hồi quy logistic học 100 kỳ | 44% · 44% | **14% · 13%** | 1% · 1.5% |
| Pool app đang dùng | 42% · 44% | **15% · 12%** | 5% · 3.0% |
| Gộp tất cả cách trên | 48% · 48% | **12% · 12%** | 3% · 2.5% |


## mega645 — tăng % kỳ có ≥4 số về trong pool (chạy tiến, mọi số liệu là kỳ chưa thấy; dữ liệu đến 04/10/2026)

96 đặc trưng/số: luật sổ, tín hiệu gợi ý, 16 PP pool app, 20 PP tâm linh + tổng phiếu, Markov trễ 1–3 & bậc 2–3, vắng, số lần ra.


### Pool 10 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Gộp tất cả cách trên | 14% · 14% | **3% · 2%** | 0% · 0.0% |
| Pool app đang dùng | 19% · 16% | **2% · 2%** | 0% · 0.0% |
| Gộp: app + logistic 200 + Markov bậc 2 | 11% · 12% | **3% · 2%** | 0% · 0.0% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 11% · 12% | **2% · 2%** | 0% · 0.0% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 10% · 12% | **1% · 2%** | 0% · 0.0% |
| Tự chọn cách tốt nhất 50 kỳ trước | 10% · 12% | **1% · 2%** | 1% · 0.5% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 11% · 10% | **1% · 2%** | 0% · 0.0% |
| Markov bậc 3 (học 50 kỳ) | 11% · 10% | **2% · 2%** | 0% · 0.0% |
| Markov bậc 2 (học 100 kỳ) | 6% · 8% | **1% · 2%** | 0% · 0.0% |
| Cây tăng cường học 200 kỳ | 12% · 12% | **1% · 1%** | 0% · 0.0% |
| Hồi quy logistic học 200 kỳ | 11% · 10% | **2% · 1%** | 0% · 0.0% |
| Markov bậc 2 (học 50 kỳ) | 8% · 10% | **1% · 1%** | 0% · 0.0% |
| Hồi quy logistic học 100 kỳ | 7% · 8% | **2% · 1%** | 1% · 0.5% |

### Pool 12 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Gộp tất cả cách trên | 19% · 18% | **6% · 6%** | 0% · 0.5% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 17% · 20% | **6% · 5%** | 0% · 0.0% |
| Markov bậc 2 (học 50 kỳ) | 16% · 16% | **3% · 4%** | 0% · 0.0% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 17% · 16% | **5% · 4%** | 0% · 0.0% |
| Gộp: app + logistic 200 + Markov bậc 2 | 17% · 18% | **5% · 4%** | 0% · 0.0% |
| Pool app đang dùng | 26% · 24% | **5% · 4%** | 0% · 0.5% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 21% · 19% | **2% · 4%** | 0% · 0.0% |
| Tự chọn cách tốt nhất 50 kỳ trước | 15% · 17% | **3% · 3%** | 1% · 0.5% |
| Hồi quy logistic học 100 kỳ | 15% · 16% | **3% · 3%** | 1% · 0.5% |
| Markov bậc 3 (học 50 kỳ) | 13% · 16% | **3% · 3%** | 0% · 0.0% |
| Cây tăng cường học 200 kỳ | 20% · 19% | **3% · 2%** | 1% · 0.5% |
| Hồi quy logistic học 200 kỳ | 16% · 17% | **4% · 2%** | 1% · 0.5% |
| Markov bậc 2 (học 100 kỳ) | 12% · 15% | **2% · 2%** | 0% · 0.0% |

### Pool 15 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Gộp tất cả cách trên | 31% · 30% | **14% · 14%** | 3% · 2.5% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 36% · 36% | **12% · 11%** | 3% · 1.5% |
| Hồi quy logistic học 100 kỳ | 28% · 34% | **9% · 10%** | 1% · 0.5% |
| Gộp: app + logistic 200 + Markov bậc 2 | 35% · 34% | **10% · 10%** | 0% · 0.5% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 32% · 32% | **11% · 10%** | 1% · 0.5% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 32% · 34% | **11% · 10%** | 4% · 2.0% |
| Pool app đang dùng | 44% · 40% | **10% · 8%** | 1% · 1.0% |
| Markov bậc 2 (học 50 kỳ) | 28% · 30% | **7% · 8%** | 0% · 1.5% |
| Tự chọn cách tốt nhất 50 kỳ trước | 35% · 32% | **7% · 8%** | 1% · 0.5% |
| Cây tăng cường học 200 kỳ | 38% · 36% | **7% · 7%** | 1% · 0.5% |
| Markov bậc 3 (học 50 kỳ) | 22% · 26% | **4% · 7%** | 1% · 0.5% |
| Hồi quy logistic học 200 kỳ | 29% · 27% | **8% · 6%** | 2% · 1.0% |
| Markov bậc 2 (học 100 kỳ) | 24% · 27% | **5% · 6%** | 0% · 0.5% |

### Pool 18 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 45% · 44% | **22% · 22%** | 6% · 4.5% |
| Gộp tất cả cách trên | 42% · 44% | **22% · 22%** | 7% · 5.0% |
| Pool app đang dùng | 55% · 53% | **22% · 20%** | 4% · 3.0% |
| Markov bậc 2 (học 50 kỳ) | 35% · 42% | **13% · 19%** | 2% · 3.5% |
| Gộp: app + logistic 200 + Markov bậc 2 | 46% · 46% | **17% · 18%** | 3% · 3.0% |
| Cây tăng cường học 200 kỳ | 55% · 52% | **20% · 18%** | 2% · 2.5% |
| Hồi quy logistic học 100 kỳ | 47% · 52% | **13% · 18%** | 3% · 1.5% |
| Tự chọn cách tốt nhất 50 kỳ trước | 53% · 50% | **18% · 18%** | 3% · 2.0% |
| Hồi quy logistic học 200 kỳ | 45% · 46% | **20% · 17%** | 3% · 2.0% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 51% · 48% | **16% · 16%** | 2% · 2.5% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 45% · 44% | **15% · 16%** | 4% · 3.5% |
| Markov bậc 3 (học 50 kỳ) | 35% · 42% | **11% · 16%** | 1% · 2.5% |
| Markov bậc 2 (học 100 kỳ) | 41% · 42% | **10% · 12%** | 1% · 2.0% |

### Pool 20 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Gộp tất cả cách trên | 51% · 52% | **27% · 28%** | 8% · 6.5% |
| Hồi quy logistic học 100 kỳ | 57% · 63% | **22% · 28%** | 4% · 2.0% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 48% · 50% | **28% · 28%** | 6% · 5.5% |
| Hồi quy logistic học 200 kỳ | 55% · 56% | **27% · 26%** | 4% · 4.5% |
| Cây tăng cường học 200 kỳ | 61% · 60% | **29% · 26%** | 5% · 7.0% |
| Gộp: app + logistic 200 + Markov bậc 2 | 54% · 55% | **24% · 26%** | 5% · 4.5% |
| Pool app đang dùng | 64% · 62% | **26% · 26%** | 10% · 6.5% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 56% · 54% | **25% · 25%** | 4% · 5.0% |
| Markov bậc 2 (học 50 kỳ) | 45% · 52% | **17% · 24%** | 4% · 7.5% |
| Tự chọn cách tốt nhất 50 kỳ trước | 59% · 57% | **24% · 24%** | 6% · 4.0% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 59% · 56% | **22% · 22%** | 5% · 4.5% |
| Markov bậc 3 (học 50 kỳ) | 46% · 52% | **15% · 20%** | 3% · 5.0% |
| Markov bậc 2 (học 100 kỳ) | 52% · 52% | **18% · 20%** | 4% · 4.0% |


## loto535 — tăng % kỳ có ≥4 số về trong pool (chạy tiến, mọi số liệu là kỳ chưa thấy; dữ liệu đến 05/10/2026 13h)

96 đặc trưng/số: luật sổ, tín hiệu gợi ý, 16 PP pool app, 20 PP tâm linh + tổng phiếu, Markov trễ 1–3 & bậc 2–3, vắng, số lần ra.


### Pool 10 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Pool app đang dùng | 20% · 18% | **5% · 4%** | 0% · 0.5% |
| Gộp tất cả cách trên | 16% · 16% | **4% · 3%** | 0% · 0.0% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 14% · 14% | **3% · 3%** | 0% · 0.0% |
| Cây tăng cường học 200 kỳ | 7% · 12% | **2% · 3%** | 0% · 0.0% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 17% · 16% | **2% · 2%** | 1% · 0.5% |
| Tự chọn cách tốt nhất 50 kỳ trước | 15% · 14% | **4% · 2%** | 0% · 0.5% |
| Markov bậc 3 (học 50 kỳ) | 15% · 14% | **2% · 2%** | 0% · 0.0% |
| Hồi quy logistic học 200 kỳ | 12% · 12% | **3% · 2%** | 0% · 0.0% |
| Markov bậc 2 (học 50 kỳ) | 14% · 15% | **2% · 2%** | 1% · 0.5% |
| Markov bậc 2 (học 100 kỳ) | 11% · 12% | **3% · 2%** | 0% · 0.0% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 14% · 12% | **2% · 2%** | 0% · 0.0% |
| Gộp: app + logistic 200 + Markov bậc 2 | 20% · 18% | **1% · 1%** | 0% · 0.0% |
| Hồi quy logistic học 100 kỳ | 10% · 10% | **0% · 0%** | 0% · 0.0% |

### Pool 12 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Markov bậc 3 (học 50 kỳ) | 24% · 25% | **8% · 8%** | 0% · 0.0% |
| Gộp: app + logistic 200 + Markov bậc 2 | 30% · 30% | **8% · 6%** | 2% · 1.5% |
| Pool app đang dùng | 29% · 28% | **9% · 6%** | 0% · 1.0% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 26% · 25% | **8% · 6%** | 2% · 1.0% |
| Tự chọn cách tốt nhất 50 kỳ trước | 23% · 22% | **9% · 6%** | 1% · 1.0% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 20% · 22% | **6% · 6%** | 0% · 0.0% |
| Markov bậc 2 (học 50 kỳ) | 21% · 24% | **5% · 6%** | 1% · 0.5% |
| Cây tăng cường học 200 kỳ | 21% · 24% | **3% · 5%** | 0% · 0.5% |
| Gộp tất cả cách trên | 22% · 22% | **5% · 5%** | 0% · 0.5% |
| Markov bậc 2 (học 100 kỳ) | 21% · 22% | **5% · 4%** | 0% · 0.0% |
| Hồi quy logistic học 200 kỳ | 21% · 20% | **4% · 4%** | 0% · 0.0% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 22% · 18% | **5% · 4%** | 0% · 0.0% |
| Hồi quy logistic học 100 kỳ | 19% · 19% | **0% · 2%** | 0% · 0.0% |

### Pool 15 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 49% · 46% | **19% · 16%** | 2% · 1.0% |
| Gộp: app + logistic 200 + Markov bậc 2 | 42% · 42% | **16% · 14%** | 4% · 2.5% |
| Markov bậc 2 (học 50 kỳ) | 36% · 39% | **13% · 14%** | 2% · 1.5% |
| Pool app đang dùng | 48% · 46% | **16% · 14%** | 4% · 3.0% |
| Markov bậc 3 (học 50 kỳ) | 39% · 43% | **14% · 13%** | 2% · 2.0% |
| Gộp tất cả cách trên | 37% · 42% | **11% · 12%** | 2% · 1.5% |
| Cây tăng cường học 200 kỳ | 36% · 42% | **11% · 12%** | 0% · 0.5% |
| Markov bậc 2 (học 100 kỳ) | 42% · 41% | **14% · 12%** | 2% · 2.0% |
| Tự chọn cách tốt nhất 50 kỳ trước | 47% · 42% | **15% · 11%** | 3% · 2.0% |
| Hồi quy logistic học 200 kỳ | 42% · 40% | **12% · 11%** | 0% · 0.0% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 48% · 44% | **10% · 10%** | 2% · 1.5% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 34% · 32% | **8% · 8%** | 1% · 0.5% |
| Hồi quy logistic học 100 kỳ | 33% · 38% | **4% · 6%** | 0% · 0.0% |

### Pool 18 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Pool app đang dùng | 59% · 60% | **27% · 28%** | 8% · 5.0% |
| Gộp: app + logistic 200 + Markov bậc 2 | 60% · 62% | **25% · 28%** | 5% · 4.5% |
| Gộp tất cả cách trên | 58% · 58% | **28% · 26%** | 3% · 3.0% |
| Cây tăng cường học 200 kỳ | 55% · 60% | **20% · 26%** | 2% · 3.0% |
| Markov bậc 3 (học 50 kỳ) | 60% · 57% | **23% · 26%** | 2% · 3.0% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 64% · 64% | **27% · 25%** | 5% · 3.0% |
| Tự chọn cách tốt nhất 50 kỳ trước | 64% · 62% | **24% · 24%** | 6% · 4.5% |
| Markov bậc 2 (học 100 kỳ) | 55% · 55% | **21% · 24%** | 3% · 4.0% |
| Hồi quy logistic học 200 kỳ | 54% · 56% | **22% · 23%** | 5% · 5.0% |
| Markov bậc 2 (học 50 kỳ) | 52% · 56% | **22% · 22%** | 5% · 5.0% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 62% · 57% | **26% · 22%** | 4% · 3.5% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 54% · 52% | **17% · 16%** | 4% · 2.5% |
| Hồi quy logistic học 100 kỳ | 54% · 55% | **15% · 15%** | 0% · 0.5% |

### Pool 20 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 69% · 74% | **34% · 35%** | 8% · 7.0% |
| Cây tăng cường học 200 kỳ | 66% · 70% | **27% · 35%** | 6% · 7.5% |
| Gộp tất cả cách trên | 66% · 68% | **35% · 35%** | 7% · 6.5% |
| Gộp: app + logistic 200 + Markov bậc 2 | 70% · 72% | **33% · 34%** | 6% · 6.5% |
| Pool app đang dùng | 66% · 68% | **30% · 34%** | 11% · 8.5% |
| Markov bậc 3 (học 50 kỳ) | 72% · 70% | **33% · 33%** | 4% · 5.5% |
| Tự chọn cách tốt nhất 50 kỳ trước | 70% · 72% | **28% · 32%** | 7% · 5.5% |
| Markov bậc 2 (học 100 kỳ) | 66% · 68% | **27% · 32%** | 5% · 6.5% |
| Hồi quy logistic học 200 kỳ | 66% · 65% | **31% · 30%** | 5% · 6.0% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 70% · 64% | **34% · 30%** | 5% · 4.0% |
| Markov bậc 2 (học 50 kỳ) | 68% · 72% | **30% · 30%** | 9% · 8.0% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 65% · 64% | **27% · 28%** | 7% · 4.0% |
| Hồi quy logistic học 100 kỳ | 67% · 66% | **24% · 25%** | 2% · 3.0% |



# Chạy lại có thêm ~300 phương pháp của app chính index.html — 13/10/2026 (thay bảng ngay trên)

Lưu ý: index.html chưa tính lại tập số các phương pháp dựa lịch sử (Nóng, Lạnh, Markov…) cho các kỳ thêm sau bằng add_result.py (vd "Nóng 5" Power giữ nguyên 3 kỳ cuối).

## power655 — tăng % kỳ có ≥4 số về trong pool (chạy tiến, mọi số liệu là kỳ chưa thấy; dữ liệu đến 03/10/2026)

387 đặc trưng/số: luật sổ, tín hiệu gợi ý, 16 PP pool app, 20 PP tâm linh + tổng phiếu, Markov trễ 1–3 & bậc 2–3, vắng, số lần ra.


### Pool 10 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Gộp: app + logistic 200 + Markov bậc 2 | 7% · 7% | **5% · 2%** | 0% · 0.0% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 4% · 6% | **1% · 2%** | 1% · 0.5% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 9% · 6% | **4% · 2%** | 0% · 0.0% |
| Gộp: app + top 50 PP + Markov bậc 2 | 15% · 12% | **3% · 2%** | 0% · 0.0% |
| Pool app đang dùng | 11% · 10% | **3% · 2%** | 0% · 0.0% |
| Markov bậc 2 (học 50 kỳ) | 11% · 11% | **1% · 2%** | 0% · 0.5% |
| Markov bậc 2 (học 100 kỳ) | 7% · 8% | **1% · 2%** | 1% · 0.5% |
| Hồi quy logistic học 200 kỳ | 4% · 6% | **2% · 2%** | 1% · 0.5% |
| Tự chọn cách tốt nhất 50 kỳ trước | 9% · 8% | **2% · 1%** | 1% · 0.5% |
| Gộp tất cả cách trên | 10% · 7% | **1% · 1%** | 0% · 0.0% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 8% · 6% | **1% · 1%** | 0% · 0.0% |
| Hồi quy logistic học 100 kỳ | 10% · 6% | **2% · 1%** | 0% · 0.0% |
| Markov bậc 3 (học 50 kỳ) | 7% · 8% | **1% · 0%** | 0% · 0.0% |
| App chính: top 100 PP (100 kỳ) bầu phiếu | 7% · 8% | **1% · 0%** | 0% · 0.0% |
| App chính: top 50 PP (100 kỳ) bầu phiếu | 7% · 5% | **1% · 0%** | 0% · 0.0% |
| Top 50 PP (200 kỳ), phiếu theo tỉ lệ ra | 4% · 4% | **1% · 0%** | 0% · 0.0% |
| Cây tăng cường học 200 kỳ | 6% · 8% | **0% · 0%** | 0% · 0.0% |

### Pool 12 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Gộp: app + top 50 PP + Markov bậc 2 | 15% · 13% | **5% · 4%** | 0% · 0.0% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 10% · 10% | **6% · 4%** | 1% · 0.5% |
| Pool app đang dùng | 14% · 14% | **4% · 3%** | 1% · 0.5% |
| Gộp: app + logistic 200 + Markov bậc 2 | 12% · 13% | **5% · 3%** | 2% · 1.0% |
| App chính: top 100 PP (100 kỳ) bầu phiếu | 10% · 12% | **3% · 3%** | 0% · 0.0% |
| Markov bậc 2 (học 50 kỳ) | 19% · 16% | **2% · 2%** | 0% · 0.5% |
| Gộp tất cả cách trên | 18% · 15% | **3% · 2%** | 0% · 0.5% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 8% · 10% | **1% · 2%** | 1% · 1.0% |
| Markov bậc 2 (học 100 kỳ) | 16% · 16% | **1% · 2%** | 1% · 1.0% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 14% · 12% | **2% · 2%** | 0% · 0.0% |
| Cây tăng cường học 200 kỳ | 9% · 12% | **1% · 2%** | 0% · 0.0% |
| Hồi quy logistic học 100 kỳ | 14% · 11% | **3% · 2%** | 0% · 0.0% |
| Hồi quy logistic học 200 kỳ | 9% · 10% | **2% · 2%** | 2% · 1.0% |
| Markov bậc 3 (học 50 kỳ) | 15% · 14% | **1% · 1%** | 0% · 0.0% |
| Tự chọn cách tốt nhất 50 kỳ trước | 15% · 13% | **2% · 1%** | 1% · 0.5% |
| App chính: top 50 PP (100 kỳ) bầu phiếu | 12% · 10% | **1% · 0%** | 0% · 0.0% |
| Top 50 PP (200 kỳ), phiếu theo tỉ lệ ra | 9% · 8% | **1% · 0%** | 1% · 0.5% |

### Pool 15 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Markov bậc 2 (học 50 kỳ) | 25% · 25% | **9% · 8%** | 1% · 1.0% |
| Gộp: app + logistic 200 + Markov bậc 2 | 25% · 25% | **5% · 6%** | 2% · 1.5% |
| Markov bậc 3 (học 50 kỳ) | 22% · 22% | **5% · 6%** | 0% · 0.0% |
| Gộp tất cả cách trên | 24% · 22% | **7% · 6%** | 0% · 0.5% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 21% · 20% | **8% · 6%** | 1% · 0.5% |
| Gộp: app + top 50 PP + Markov bậc 2 | 24% · 22% | **6% · 6%** | 1% · 0.5% |
| Hồi quy logistic học 100 kỳ | 22% · 20% | **8% · 6%** | 0% · 0.0% |
| Markov bậc 2 (học 100 kỳ) | 25% · 28% | **4% · 5%** | 1% · 1.0% |
| Hồi quy logistic học 200 kỳ | 22% · 22% | **4% · 5%** | 2% · 1.0% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 22% · 22% | **6% · 5%** | 1% · 1.0% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 22% · 21% | **5% · 5%** | 1% · 0.5% |
| Pool app đang dùng | 23% · 24% | **6% · 4%** | 3% · 2.0% |
| Tự chọn cách tốt nhất 50 kỳ trước | 22% · 24% | **5% · 4%** | 1% · 0.5% |
| Cây tăng cường học 200 kỳ | 16% · 23% | **3% · 4%** | 1% · 0.5% |
| App chính: top 100 PP (100 kỳ) bầu phiếu | 22% · 23% | **3% · 4%** | 1% · 0.5% |
| App chính: top 50 PP (100 kỳ) bầu phiếu | 24% · 20% | **3% · 4%** | 0% · 0.0% |
| Top 50 PP (200 kỳ), phiếu theo tỉ lệ ra | 20% · 16% | **5% · 3%** | 1% · 0.5% |

### Pool 18 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Markov bậc 2 (học 50 kỳ) | 35% · 36% | **14% · 14%** | 2% · 1.5% |
| Markov bậc 3 (học 50 kỳ) | 39% · 37% | **13% · 13%** | 4% · 2.5% |
| Markov bậc 2 (học 100 kỳ) | 38% · 41% | **12% · 12%** | 1% · 1.5% |
| Hồi quy logistic học 200 kỳ | 37% · 37% | **14% · 12%** | 4% · 2.0% |
| Gộp: app + logistic 200 + Markov bậc 2 | 33% · 36% | **10% · 11%** | 4% · 2.5% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 33% · 33% | **13% · 11%** | 1% · 1.0% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 33% · 30% | **10% · 11%** | 3% · 2.5% |
| Tự chọn cách tốt nhất 50 kỳ trước | 36% · 36% | **12% · 10%** | 4% · 2.5% |
| Pool app đang dùng | 33% · 36% | **13% · 10%** | 5% · 3.0% |
| Gộp tất cả cách trên | 35% · 34% | **10% · 10%** | 2% · 2.0% |
| Cây tăng cường học 200 kỳ | 25% · 32% | **9% · 10%** | 1% · 0.5% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 32% · 30% | **12% · 10%** | 2% · 1.0% |
| App chính: top 50 PP (100 kỳ) bầu phiếu | 32% · 29% | **6% · 10%** | 1% · 1.0% |
| Hồi quy logistic học 100 kỳ | 29% · 28% | **13% · 9%** | 0% · 0.0% |
| Gộp: app + top 50 PP + Markov bậc 2 | 31% · 31% | **11% · 8%** | 1% · 1.0% |
| App chính: top 100 PP (100 kỳ) bầu phiếu | 26% · 30% | **6% · 8%** | 1% · 1.0% |
| Top 50 PP (200 kỳ), phiếu theo tỉ lệ ra | 28% · 26% | **10% · 6%** | 1% · 0.5% |

### Pool 20 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Markov bậc 2 (học 100 kỳ) | 43% · 48% | **18% · 20%** | 1% · 2.0% |
| Hồi quy logistic học 200 kỳ | 41% · 41% | **21% · 20%** | 4% · 2.5% |
| Markov bậc 3 (học 50 kỳ) | 45% · 42% | **21% · 19%** | 5% · 3.5% |
| Markov bậc 2 (học 50 kỳ) | 39% · 42% | **17% · 18%** | 5% · 3.0% |
| Tự chọn cách tốt nhất 50 kỳ trước | 43% · 46% | **21% · 18%** | 4% · 3.0% |
| Gộp: app + logistic 200 + Markov bậc 2 | 41% · 40% | **15% · 16%** | 4% · 4.0% |
| App chính: top 50 PP (100 kỳ) bầu phiếu | 43% · 38% | **10% · 14%** | 1% · 2.0% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 39% · 38% | **15% · 14%** | 2% · 2.0% |
| Cây tăng cường học 200 kỳ | 31% · 38% | **12% · 13%** | 2% · 2.0% |
| Gộp tất cả cách trên | 48% · 45% | **13% · 12%** | 2% · 2.5% |
| Pool app đang dùng | 42% · 44% | **15% · 12%** | 5% · 3.0% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 38% · 38% | **16% · 12%** | 4% · 2.5% |
| Hồi quy logistic học 100 kỳ | 38% · 37% | **16% · 12%** | 3% · 1.5% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 38% · 35% | **12% · 12%** | 4% · 3.0% |
| Gộp: app + top 50 PP + Markov bậc 2 | 39% · 39% | **15% · 12%** | 4% · 2.5% |
| App chính: top 100 PP (100 kỳ) bầu phiếu | 39% · 42% | **10% · 10%** | 2% · 2.0% |
| Top 50 PP (200 kỳ), phiếu theo tỉ lệ ra | 31% · 36% | **15% · 10%** | 2% · 1.5% |

### 294 phương pháp của app chính (index.html) — tỉ lệ ra so với BQ

- Đạt (ra nhiều hơn BQ ở cả 100 kỳ gần và 100 kỳ trước): **47** · ít mẫu (chọn quá ít số): 32 · không đạt: 215
- Top đạt: Can tháng ×1.65/×1.56 (1.0 số/kỳ), DxMxY cộng ×1.38/×1.56 (1.0 số/kỳ), Thứ ngày ×1.65/×1.19 (1.0 số/kỳ), Tithi số ×1.47/×1.38 (1.0 số/kỳ), Số 8 ×1.56/×1.19 (1.0 số/kỳ), Pascal lộn ×1.47/×1.17 (1.0 số/kỳ), MHdương chủ ×1.28/×1.19 (1.0 số/kỳ), ÂmDxM mod ×1.19/×1.28 (1.0 số/kỳ), ÂmDMY cộng ×1.19/×1.28 (1.0 số/kỳ), Tổng ngày ×1.19/×1.19 (1.0 số/kỳ), Số 13 ×1.28/×1.10 (1.0 số/kỳ), Pers55 tách ×1.15/×1.24 (2.0 số/kỳ), Sinh2025 cộng ×1.28/×1.10 (1.0 số/kỳ), Chi lụchợp ×1.04/×1.26 (4.6 số/kỳ), Nhị thập ×1.28/×1.01 (1.0 số/kỳ)


## mega645 — tăng % kỳ có ≥4 số về trong pool (chạy tiến, mọi số liệu là kỳ chưa thấy; dữ liệu đến 04/10/2026)

387 đặc trưng/số: luật sổ, tín hiệu gợi ý, 16 PP pool app, 20 PP tâm linh + tổng phiếu, Markov trễ 1–3 & bậc 2–3, vắng, số lần ra.


### Pool 10 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Gộp tất cả cách trên | 15% · 14% | **2% · 2%** | 2% · 1.0% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 11% · 12% | **3% · 2%** | 0% · 0.0% |
| Pool app đang dùng | 19% · 16% | **2% · 2%** | 0% · 0.0% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 12% · 14% | **2% · 2%** | 0% · 0.0% |
| Cây tăng cường học 200 kỳ | 10% · 8% | **3% · 2%** | 0% · 0.0% |
| Hồi quy logistic học 100 kỳ | 16% · 12% | **3% · 2%** | 0% · 0.0% |
| Markov bậc 3 (học 50 kỳ) | 11% · 10% | **2% · 2%** | 0% · 0.0% |
| Tự chọn cách tốt nhất 50 kỳ trước | 9% · 10% | **2% · 2%** | 0% · 0.0% |
| App chính: top 50 PP (100 kỳ) bầu phiếu | 8% · 9% | **2% · 2%** | 1% · 0.5% |
| Hồi quy logistic học 200 kỳ | 10% · 8% | **2% · 2%** | 1% · 0.5% |
| Markov bậc 2 (học 100 kỳ) | 6% · 8% | **1% · 2%** | 0% · 0.0% |
| Gộp: app + logistic 200 + Markov bậc 2 | 14% · 12% | **1% · 1%** | 0% · 0.0% |
| Markov bậc 2 (học 50 kỳ) | 8% · 10% | **1% · 1%** | 0% · 0.0% |
| Top 50 PP (200 kỳ), phiếu theo tỉ lệ ra | 7% · 10% | **0% · 1%** | 0% · 0.0% |
| App chính: top 100 PP (100 kỳ) bầu phiếu | 8% · 9% | **0% · 1%** | 0% · 0.0% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 8% · 7% | **1% · 1%** | 0% · 0.0% |
| Gộp: app + top 50 PP + Markov bậc 2 | 14% · 13% | **0% · 0%** | 0% · 0.0% |

### Pool 12 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Điểm theo tỉ lệ ra 200 kỳ gần | 19% · 20% | **5% · 6%** | 1% · 0.5% |
| Gộp tất cả cách trên | 18% · 19% | **7% · 6%** | 2% · 1.0% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 19% · 20% | **4% · 5%** | 1% · 0.5% |
| Markov bậc 2 (học 50 kỳ) | 16% · 16% | **3% · 4%** | 0% · 0.0% |
| Hồi quy logistic học 200 kỳ | 20% · 16% | **6% · 4%** | 1% · 1.0% |
| Hồi quy logistic học 100 kỳ | 22% · 20% | **6% · 4%** | 1% · 0.5% |
| Pool app đang dùng | 26% · 24% | **5% · 4%** | 0% · 0.5% |
| Gộp: app + logistic 200 + Markov bậc 2 | 24% · 20% | **4% · 4%** | 0% · 0.0% |
| Gộp: app + top 50 PP + Markov bậc 2 | 18% · 20% | **4% · 4%** | 0% · 0.0% |
| App chính: top 100 PP (100 kỳ) bầu phiếu | 15% · 16% | **4% · 4%** | 0% · 0.0% |
| Top 50 PP (200 kỳ), phiếu theo tỉ lệ ra | 12% · 18% | **1% · 3%** | 0% · 0.0% |
| Cây tăng cường học 200 kỳ | 16% · 16% | **3% · 3%** | 0% · 0.0% |
| Markov bậc 3 (học 50 kỳ) | 13% · 16% | **3% · 3%** | 0% · 0.0% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 15% · 15% | **3% · 3%** | 0% · 0.5% |
| App chính: top 50 PP (100 kỳ) bầu phiếu | 12% · 14% | **4% · 3%** | 1% · 0.5% |
| Tự chọn cách tốt nhất 50 kỳ trước | 18% · 18% | **4% · 2%** | 0% · 0.0% |
| Markov bậc 2 (học 100 kỳ) | 12% · 15% | **2% · 2%** | 0% · 0.0% |

### Pool 15 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Gộp tất cả cách trên | 24% · 28% | **13% · 12%** | 3% · 1.5% |
| Gộp: app + top 50 PP + Markov bậc 2 | 36% · 34% | **11% · 11%** | 0% · 1.0% |
| Gộp: app + logistic 200 + Markov bậc 2 | 38% · 32% | **12% · 10%** | 0% · 0.5% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 29% · 32% | **8% · 10%** | 2% · 1.5% |
| Cây tăng cường học 200 kỳ | 29% · 31% | **9% · 9%** | 1% · 1.0% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 28% · 29% | **10% · 9%** | 3% · 2.0% |
| Hồi quy logistic học 100 kỳ | 29% · 29% | **10% · 9%** | 3% · 1.5% |
| Pool app đang dùng | 44% · 40% | **10% · 8%** | 1% · 1.0% |
| App chính: top 100 PP (100 kỳ) bầu phiếu | 28% · 30% | **7% · 8%** | 1% · 0.5% |
| App chính: top 50 PP (100 kỳ) bầu phiếu | 24% · 25% | **8% · 8%** | 3% · 2.0% |
| Tự chọn cách tốt nhất 50 kỳ trước | 32% · 32% | **9% · 8%** | 1% · 0.5% |
| Markov bậc 2 (học 50 kỳ) | 28% · 30% | **7% · 8%** | 0% · 1.5% |
| Hồi quy logistic học 200 kỳ | 33% · 28% | **9% · 7%** | 2% · 1.5% |
| Markov bậc 3 (học 50 kỳ) | 22% · 26% | **4% · 7%** | 1% · 0.5% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 25% · 31% | **7% · 6%** | 2% · 2.0% |
| Top 50 PP (200 kỳ), phiếu theo tỉ lệ ra | 27% · 30% | **3% · 6%** | 0% · 0.0% |
| Markov bậc 2 (học 100 kỳ) | 24% · 27% | **5% · 6%** | 0% · 0.5% |

### Pool 18 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Pool app đang dùng | 55% · 53% | **22% · 20%** | 4% · 3.0% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 41% · 45% | **20% · 20%** | 4% · 2.5% |
| Gộp: app + top 50 PP + Markov bậc 2 | 47% · 44% | **17% · 20%** | 3% · 3.0% |
| Hồi quy logistic học 100 kỳ | 47% · 46% | **23% · 20%** | 6% · 3.5% |
| Markov bậc 2 (học 50 kỳ) | 35% · 42% | **13% · 19%** | 2% · 3.5% |
| Cây tăng cường học 200 kỳ | 43% · 46% | **18% · 18%** | 4% · 3.5% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 48% · 45% | **19% · 18%** | 5% · 4.0% |
| Hồi quy logistic học 200 kỳ | 44% · 44% | **21% · 18%** | 3% · 2.5% |
| Gộp tất cả cách trên | 40% · 40% | **15% · 16%** | 5% · 3.5% |
| Tự chọn cách tốt nhất 50 kỳ trước | 47% · 49% | **16% · 16%** | 3% · 2.0% |
| App chính: top 100 PP (100 kỳ) bầu phiếu | 40% · 40% | **14% · 16%** | 1% · 1.5% |
| Markov bậc 3 (học 50 kỳ) | 35% · 42% | **11% · 16%** | 1% · 2.5% |
| Gộp: app + logistic 200 + Markov bậc 2 | 49% · 46% | **16% · 15%** | 0% · 1.0% |
| Top 50 PP (200 kỳ), phiếu theo tỉ lệ ra | 45% · 47% | **11% · 14%** | 1% · 1.0% |
| App chính: top 50 PP (100 kỳ) bầu phiếu | 37% · 40% | **12% · 14%** | 4% · 3.5% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 38% · 42% | **13% · 12%** | 5% · 3.5% |
| Markov bậc 2 (học 100 kỳ) | 41% · 42% | **10% · 12%** | 1% · 2.0% |

### Pool 20 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Gộp: app + top 50 PP + Markov bậc 2 | 55% · 54% | **28% · 30%** | 6% · 5.5% |
| Cây tăng cường học 200 kỳ | 60% · 59% | **24% · 28%** | 7% · 5.5% |
| Hồi quy logistic học 100 kỳ | 57% · 55% | **29% · 27%** | 13% · 9.0% |
| Hồi quy logistic học 200 kỳ | 49% · 52% | **30% · 26%** | 7% · 6.5% |
| Pool app đang dùng | 64% · 62% | **26% · 26%** | 10% · 6.5% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 46% · 50% | **26% · 26%** | 9% · 6.0% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 56% · 54% | **26% · 25%** | 9% · 6.5% |
| Gộp: app + logistic 200 + Markov bậc 2 | 55% · 56% | **23% · 24%** | 5% · 4.5% |
| Markov bậc 2 (học 50 kỳ) | 45% · 52% | **17% · 24%** | 4% · 7.5% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 47% · 52% | **23% · 22%** | 6% · 5.0% |
| Tự chọn cách tốt nhất 50 kỳ trước | 59% · 61% | **21% · 21%** | 8% · 5.0% |
| Gộp tất cả cách trên | 50% · 53% | **17% · 20%** | 5% · 4.5% |
| Top 50 PP (200 kỳ), phiếu theo tỉ lệ ra | 51% · 55% | **15% · 20%** | 2% · 3.0% |
| App chính: top 100 PP (100 kỳ) bầu phiếu | 48% · 49% | **20% · 20%** | 4% · 5.0% |
| Markov bậc 3 (học 50 kỳ) | 46% · 52% | **15% · 20%** | 3% · 5.0% |
| Markov bậc 2 (học 100 kỳ) | 52% · 52% | **18% · 20%** | 4% · 4.0% |
| App chính: top 50 PP (100 kỳ) bầu phiếu | 50% · 50% | **16% · 18%** | 6% · 5.0% |

### 291 phương pháp của app chính (index.html) — tỉ lệ ra so với BQ

- Đạt (ra nhiều hơn BQ ở cả 100 kỳ gần và 100 kỳ trước): **57** · ít mẫu (chọn quá ít số): 23 · không đạt: 211
- Top đạt: Ngày-tháng ×1.06/×1.78 (1.0 số/kỳ), Tiết khí ×1.12/×1.57 (1.0 số/kỳ), Sinh2025 mod ×1.20/×1.43 (1.0 số/kỳ), Ngày năm ×1.12/×1.43 (1.0 số/kỳ), ÂmDMY cộng ×1.28/×1.20 (1.0 số/kỳ), Tuần ISO ×1.05/×1.42 (1.0 số/kỳ), DMY đầu2 ×1.12/×1.28 (1.0 số/kỳ), DDMMYYYY mod ×1.05/×1.35 (1.0 số/kỳ), Chaldean Nguyệt ×1.11/×1.28 (5.0 số/kỳ), NgàyNăm tách ×1.16/×1.22 (3.4 số/kỳ), Chi ngày ×1.05/×1.28 (1.0 số/kỳ), Chạm đầu ×1.19/×1.13 (4.5 số/kỳ), MHdương hậuthiên ×1.24/×1.05 (2.0 số/kỳ), Life 9 ×1.14/×1.12 (5.0 số/kỳ), Hợp Rồng ×1.05/×1.18 (4.0 số/kỳ)


## loto535 — tăng % kỳ có ≥4 số về trong pool (chạy tiến, mọi số liệu là kỳ chưa thấy; dữ liệu đến 05/10/2026 13h)

401 đặc trưng/số: luật sổ, tín hiệu gợi ý, 16 PP pool app, 20 PP tâm linh + tổng phiếu, Markov trễ 1–3 & bậc 2–3, vắng, số lần ra.


### Pool 10 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Pool app đang dùng | 20% · 18% | **5% · 4%** | 0% · 0.5% |
| Gộp: app + top 50 PP + Markov bậc 2 | 16% · 16% | **2% · 3%** | 0% · 0.0% |
| Gộp: app + logistic 200 + Markov bậc 2 | 14% · 16% | **2% · 2%** | 0% · 0.5% |
| Hồi quy logistic học 100 kỳ | 13% · 13% | **4% · 2%** | 0% · 0.0% |
| Top 50 PP (200 kỳ), phiếu theo tỉ lệ ra | 12% · 12% | **4% · 2%** | 1% · 0.5% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 17% · 18% | **2% · 2%** | 0% · 0.0% |
| Markov bậc 3 (học 50 kỳ) | 15% · 14% | **2% · 2%** | 0% · 0.0% |
| Tự chọn cách tốt nhất 50 kỳ trước | 13% · 14% | **3% · 2%** | 0% · 0.5% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 14% · 13% | **2% · 2%** | 0% · 0.0% |
| Markov bậc 2 (học 50 kỳ) | 14% · 15% | **2% · 2%** | 1% · 0.5% |
| Markov bậc 2 (học 100 kỳ) | 11% · 12% | **3% · 2%** | 0% · 0.0% |
| Gộp tất cả cách trên | 12% · 14% | **2% · 1%** | 0% · 0.0% |
| Hồi quy logistic học 200 kỳ | 12% · 14% | **1% · 1%** | 0% · 0.0% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 16% · 15% | **0% · 0%** | 0% · 0.0% |
| App chính: top 50 PP (100 kỳ) bầu phiếu | 11% · 10% | **0% · 0%** | 0% · 0.0% |
| Cây tăng cường học 200 kỳ | 16% · 14% | **0% · 0%** | 0% · 0.0% |
| App chính: top 100 PP (100 kỳ) bầu phiếu | 14% · 12% | **0% · 0%** | 0% · 0.0% |

### Pool 12 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Markov bậc 3 (học 50 kỳ) | 24% · 25% | **8% · 8%** | 0% · 0.0% |
| Pool app đang dùng | 29% · 28% | **9% · 6%** | 0% · 1.0% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 29% · 31% | **6% · 6%** | 0% · 0.0% |
| Markov bậc 2 (học 50 kỳ) | 21% · 24% | **5% · 6%** | 1% · 0.5% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 23% · 22% | **5% · 5%** | 1% · 0.5% |
| Hồi quy logistic học 100 kỳ | 16% · 20% | **4% · 5%** | 0% · 0.0% |
| Gộp: app + top 50 PP + Markov bậc 2 | 25% · 25% | **3% · 4%** | 0% · 0.0% |
| Markov bậc 2 (học 100 kỳ) | 21% · 22% | **5% · 4%** | 0% · 0.0% |
| Gộp tất cả cách trên | 23% · 22% | **3% · 4%** | 0% · 0.0% |
| Top 50 PP (200 kỳ), phiếu theo tỉ lệ ra | 21% · 20% | **4% · 4%** | 1% · 0.5% |
| Tự chọn cách tốt nhất 50 kỳ trước | 15% · 19% | **5% · 4%** | 0% · 0.5% |
| Gộp: app + logistic 200 + Markov bậc 2 | 19% · 24% | **3% · 4%** | 1% · 1.0% |
| Cây tăng cường học 200 kỳ | 20% · 20% | **2% · 4%** | 0% · 0.0% |
| App chính: top 50 PP (100 kỳ) bầu phiếu | 16% · 16% | **4% · 4%** | 0% · 0.0% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 22% · 23% | **3% · 3%** | 0% · 0.5% |
| Hồi quy logistic học 200 kỳ | 18% · 20% | **1% · 2%** | 0% · 0.0% |
| App chính: top 100 PP (100 kỳ) bầu phiếu | 17% · 17% | **2% · 2%** | 0% · 0.0% |

### Pool 15 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Markov bậc 2 (học 50 kỳ) | 36% · 39% | **13% · 14%** | 2% · 1.5% |
| Pool app đang dùng | 48% · 46% | **16% · 14%** | 4% · 3.0% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 43% · 44% | **14% · 14%** | 1% · 0.5% |
| Markov bậc 3 (học 50 kỳ) | 39% · 43% | **14% · 13%** | 2% · 2.0% |
| Markov bậc 2 (học 100 kỳ) | 42% · 41% | **14% · 12%** | 2% · 2.0% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 35% · 40% | **11% · 12%** | 1% · 1.5% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 37% · 39% | **14% · 12%** | 5% · 2.5% |
| Cây tăng cường học 200 kỳ | 35% · 36% | **11% · 12%** | 0% · 0.0% |
| Top 50 PP (200 kỳ), phiếu theo tỉ lệ ra | 31% · 34% | **9% · 10%** | 1% · 0.5% |
| Gộp: app + top 50 PP + Markov bậc 2 | 42% · 43% | **6% · 10%** | 1% · 1.0% |
| Hồi quy logistic học 100 kỳ | 31% · 38% | **7% · 10%** | 0% · 0.0% |
| Gộp: app + logistic 200 + Markov bậc 2 | 35% · 40% | **8% · 9%** | 1% · 1.5% |
| Gộp tất cả cách trên | 38% · 42% | **7% · 8%** | 0% · 1.0% |
| Tự chọn cách tốt nhất 50 kỳ trước | 29% · 34% | **7% · 8%** | 1% · 1.0% |
| App chính: top 50 PP (100 kỳ) bầu phiếu | 34% · 34% | **7% · 8%** | 0% · 0.5% |
| App chính: top 100 PP (100 kỳ) bầu phiếu | 28% · 29% | **4% · 6%** | 2% · 2.0% |
| Hồi quy logistic học 200 kỳ | 31% · 34% | **4% · 6%** | 0% · 0.0% |

### Pool 18 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Pool app đang dùng | 59% · 60% | **27% · 28%** | 8% · 5.0% |
| Markov bậc 3 (học 50 kỳ) | 60% · 57% | **23% · 26%** | 2% · 3.0% |
| Gộp: app + top 50 PP + Markov bậc 2 | 61% · 61% | **18% · 25%** | 3% · 3.0% |
| Điểm theo tỉ lệ ra 100 kỳ gần | 54% · 56% | **23% · 24%** | 5% · 5.5% |
| Markov bậc 2 (học 100 kỳ) | 55% · 55% | **21% · 24%** | 3% · 4.0% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 59% · 60% | **24% · 24%** | 5% · 3.5% |
| Gộp: app + logistic 200 + Markov bậc 2 | 58% · 58% | **22% · 22%** | 4% · 4.5% |
| Markov bậc 2 (học 50 kỳ) | 52% · 56% | **22% · 22%** | 5% · 5.0% |
| Cây tăng cường học 200 kỳ | 57% · 56% | **16% · 21%** | 3% · 4.0% |
| Gộp tất cả cách trên | 62% · 60% | **21% · 20%** | 2% · 2.5% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 56% · 56% | **23% · 20%** | 6% · 4.0% |
| Hồi quy logistic học 100 kỳ | 50% · 56% | **15% · 20%** | 1% · 1.5% |
| Tự chọn cách tốt nhất 50 kỳ trước | 51% · 52% | **14% · 20%** | 1% · 1.5% |
| Top 50 PP (200 kỳ), phiếu theo tỉ lệ ra | 53% · 53% | **16% · 19%** | 3% · 2.5% |
| Hồi quy logistic học 200 kỳ | 48% · 52% | **18% · 18%** | 1% · 1.0% |
| App chính: top 50 PP (100 kỳ) bầu phiếu | 54% · 52% | **17% · 16%** | 2% · 1.5% |
| App chính: top 100 PP (100 kỳ) bầu phiếu | 46% · 46% | **15% · 16%** | 3% · 4.0% |

### Pool 20 — % kỳ về ≥3 / ≥4 / ≥5 số trong pool (100 kỳ gần · 200 kỳ gần)

| Cách | ≥3 số | **≥4 số** | ≥5 số |
|---|---|---|---|
| Điểm theo tỉ lệ ra 100 kỳ gần | 66% · 70% | **34% · 34%** | 7% · 7.0% |
| Pool app đang dùng | 66% · 68% | **30% · 34%** | 11% · 8.5% |
| Markov bậc 3 (học 50 kỳ) | 72% · 70% | **33% · 33%** | 4% · 5.5% |
| Gộp: app + logistic 200 + Markov bậc 2 | 68% · 69% | **33% · 32%** | 8% · 8.0% |
| Gộp: app + tỉ lệ ra 200 + Markov bậc 2 | 68% · 70% | **33% · 32%** | 8% · 7.5% |
| Gộp tất cả cách trên | 70% · 72% | **32% · 32%** | 3% · 6.5% |
| Cây tăng cường học 200 kỳ | 70% · 70% | **24% · 32%** | 6% · 8.5% |
| Markov bậc 2 (học 100 kỳ) | 66% · 68% | **27% · 32%** | 5% · 6.5% |
| Gộp: app + top 50 PP + Markov bậc 2 | 77% · 74% | **29% · 31%** | 4% · 5.5% |
| Tự chọn cách tốt nhất 50 kỳ trước | 66% · 66% | **28% · 30%** | 3% · 3.5% |
| Markov bậc 2 (học 50 kỳ) | 68% · 72% | **30% · 30%** | 9% · 8.0% |
| Top 50 PP (200 kỳ), phiếu theo tỉ lệ ra | 64% · 64% | **25% · 29%** | 6% · 5.5% |
| Hồi quy logistic học 200 kỳ | 61% · 64% | **29% · 28%** | 4% · 4.0% |
| Hồi quy logistic học 100 kỳ | 62% · 65% | **23% · 27%** | 7% · 6.0% |
| Điểm theo tỉ lệ ra 200 kỳ gần | 62% · 62% | **29% · 26%** | 9% · 7.0% |
| App chính: top 100 PP (100 kỳ) bầu phiếu | 59% · 60% | **22% · 24%** | 4% · 6.0% |
| App chính: top 50 PP (100 kỳ) bầu phiếu | 66% · 63% | **22% · 21%** | 3% · 3.5% |

### 305 phương pháp của app chính (index.html) — tỉ lệ ra so với BQ

- Đạt (ra nhiều hơn BQ ở cả 100 kỳ gần và 100 kỳ trước): **66** · ít mẫu (chọn quá ít số): 30 · không đạt: 209
- Top đạt: DDMM đầu2 ×1.40/×1.20 (0.8 số/kỳ), NgàyNăm cộng ×1.40/×1.19 (1.0 số/kỳ), Sinh 27 ×1.33/×1.26 (1.0 số/kỳ), Sinh27 mod ×1.33/×1.26 (1.0 số/kỳ), Sinh27 cộng ×1.33/×1.26 (1.0 số/kỳ), Ngày+tháng ×1.25/×1.29 (0.8 số/kỳ), DDMM cộng ×1.33/×1.19 (1.0 số/kỳ), Tiết khí ×1.05/×1.47 (1.0 số/kỳ), Số 13 ×1.47/×1.05 (1.0 số/kỳ), DxMxY cộng ×1.05/×1.47 (1.0 số/kỳ), Luân48 mod ×1.47/×1.05 (1.0 số/kỳ), Soul13 mod ×1.47/×1.05 (1.0 số/kỳ), Soul13 cộng ×1.47/×1.05 (1.0 số/kỳ), DxMxY mod ×1.05/×1.40 (1.0 số/kỳ), Hợp Trâu ×1.26/×1.17 (3.0 số/kỳ)



# Thử phương pháp mới tra được + Markov nhiều bậc để thu hẹp pool — 14/10/2026 (`python build/pool_moi.py <game>`)

## power655 — pool mới (chạy tiến, tự chọn phương pháp theo 100 kỳ trước mỗi kỳ) so với pool đang dùng, đến 13/10/2026

Loại hẳn TB **4.2 số/kỳ** (10 kỳ gần 4.3) · kỳ không loại nhầm số nào: 60% / 65% / 62% / 61% (khung 10/20/50/100)

| Pool | Cách | Kỳ ≥3 số: 10 / 20 / 50 / 100 kỳ | Kỳ ≥4 số: 10 / 20 / 50 / 100 kỳ | TB số trúng (100 kỳ) |
|---|---|---|---|---|
| 10 | Pool mới (gộp hết) | 10% / 5% / 4% / 5% | 0% / 0% / 0% / 0% | 1.25 |
| 10 | (C) đang dùng + loại ≥70% | 0% / 5% / 6% / 10% | 0% / 0% / 0% / 0% | 1.19 |
| 10 | (D) đang dùng + loại ≥80% | 0% / 5% / 8% / 11% | 0% / 0% / 0% / 1% | 1.23 |
| 10 | Pool đang dùng | 0% / 5% / 6% / 9% | 0% / 0% / 0% / 1% | 1.26 |
| 15 | Pool mới (gộp hết) | 30% / 20% / 16% / 20% | 10% / 5% / 4% / 2% | 1.70 |
| 15 | (C) đang dùng + loại ≥70% | 30% / 30% / 22% / 23% | 0% / 10% / 4% / 8% | 1.83 |
| 15 | (D) đang dùng + loại ≥80% | 30% / 30% / 24% / 25% | 0% / 10% / 4% / 9% | 1.88 |
| 15 | Pool đang dùng | 30% / 25% / 20% / 23% | 0% / 10% / 4% / 9% | 1.82 |
| 18 | Pool mới (gộp hết) | 30% / 35% / 28% / 30% | 10% / 5% / 4% / 6% | 1.99 |
| 18 | (C) đang dùng + loại ≥70% | 40% / 40% / 28% / 35% | 0% / 10% / 6% / 12% | 2.14 |
| 18 | (D) đang dùng + loại ≥80% | 40% / 40% / 30% / 37% | 0% / 10% / 6% / 13% | 2.20 |
| 18 | Pool đang dùng | 30% / 35% / 30% / 36% | 10% / 15% / 6% / 13% | 2.19 |

**Luật loại được chọn nhiều nhất** (số kỳ/100): Luật: Bỏ số ra 3 lần trong 5 kỳ (100) · Luật: Bỏ số nhịp "ra – vắng 2 – ra" (vừa ra lại sau đúng 2 kỳ vắng) (98) · Chuỗi ra/vắng bậc 5, chung, học 100 — điểm ≤60% TB (83) · Luật: Bỏ số ra ít nhất 100 kỳ (42) · Luật: Bỏ số nhỏ nhất kỳ trước (32) · Luật: Bỏ số tái xuất sau vắng ≥15 (29) · Chuỗi ra/vắng bậc 4, chung, học 100 — điểm ≤60% TB (23) · Chuỗi ra/vắng bậc 4, chung, học 50 — điểm ≤60% TB (22)

**Phương pháp cộng điểm được chọn nhiều nhất** (số kỳ/100): Markov bộ số bậc 4, học 100 (100) · Chuỗi ra/vắng bậc 10, chung, học 50 (100) · Chuỗi ra/vắng bậc 3, chung, học 100 (99) · Markov bộ số bậc 4, học 50 (99) · Chuỗi ra/vắng bậc 5, chung, học 100 (95) · Markov bộ số bậc 2, học 100 (91) · Pool app đang dùng (điểm goiy) (89) · Markov bộ số bậc 2, học 50 (85) · Chuỗi ra/vắng bậc 2, chung, học 100 (85) · Chuỗi ra/vắng bậc 4, chung, học 100 (85) · Markov bộ số bậc 3, học 50 (82) · Chuỗi ra/vắng bậc 5, chung, học 50 (78)

**Riêng các phương pháp mới tra được** — top 15 ra mỗi số (10 / 20 / 50 / 100 kỳ), được chọn bao nhiêu kỳ:
- 連休回数 riêng từng số (cả lịch sử): 10.7% / 12.3% / 11.5% / 10.8% (TB 10.9%) · chọn 1 kỳ
- 連休回数 chung mọi số (100 kỳ): 12.0% / 12.3% / 12.5% / 12.0% (TB 10.9%) · chọn 69 kỳ
- Tỉ lệ vắng/vắng TB (cao = đến hạn): 10.7% / 12.7% / 13.1% / 12.2% (TB 10.9%) · chọn 62 kỳ
- Tỉ lệ vắng/vắng TB (thấp = vừa ra): 12.0% / 11.3% / 10.8% / 10.3% (TB 10.9%) · chọn 37 kỳ
- KNN 5 đặc trưng vắng: 12.7% / 11.3% / 11.7% / 11.3% (TB 10.9%) · chọn 13 kỳ
- HMM 2 trạng thái nóng/nguội: 12.7% / 12.0% / 9.6% / 9.9% (TB 10.9%) · chọn 0 kỳ
- 斜连 số chéo: 16.0% / 14.3% / 12.3% / 11.5% (TB 10.9%) · chọn 15 kỳ
- 隔号 cách số kỳ trước ±2: 14.7% / 12.3% / 12.3% / 11.3% (TB 10.9%) · chọn 32 kỳ

**Kỳ tới**: loại hẳn 06 07 24 27 40 50 53 · pool 18: 14 05 09 03 21 17 04 08 39 13 23 25 19 33 22 11 55 15


## mega645 — pool mới (chạy tiến, tự chọn phương pháp theo 100 kỳ trước mỗi kỳ) so với pool đang dùng, đến 11/10/2026

Loại hẳn TB **3.8 số/kỳ** (10 kỳ gần 4.9) · kỳ không loại nhầm số nào: 60% / 65% / 64% / 62% (khung 10/20/50/100)

| Pool | Cách | Kỳ ≥3 số: 10 / 20 / 50 / 100 kỳ | Kỳ ≥4 số: 10 / 20 / 50 / 100 kỳ | TB số trúng (100 kỳ) |
|---|---|---|---|---|
| 10 | Pool mới (gộp hết) | 10% / 5% / 12% / 7% | 10% / 5% / 4% / 2% | 1.30 |
| 10 | (C) đang dùng + loại ≥70% | 30% / 25% / 18% / 19% | 0% / 0% / 4% / 3% | 1.49 |
| 10 | (D) đang dùng + loại ≥80% | 30% / 20% / 16% / 18% | 0% / 0% / 4% / 2% | 1.45 |
| 10 | Pool đang dùng | 20% / 15% / 14% / 18% | 0% / 0% / 4% / 2% | 1.45 |
| 15 | Pool mới (gộp hết) | 30% / 30% / 30% / 27% | 10% / 20% / 16% / 11% | 2.03 |
| 15 | (C) đang dùng + loại ≥70% | 50% / 40% / 42% / 42% | 0% / 5% / 6% / 9% | 2.11 |
| 15 | (D) đang dùng + loại ≥80% | 50% / 40% / 42% / 42% | 0% / 5% / 8% / 9% | 2.14 |
| 15 | Pool đang dùng | 50% / 40% / 40% / 44% | 0% / 10% / 12% / 10% | 2.18 |
| 18 | Pool mới (gộp hết) | 30% / 40% / 40% / 41% | 30% / 30% / 26% / 19% | 2.46 |
| 18 | (C) đang dùng + loại ≥70% | 60% / 55% / 52% / 51% | 30% / 25% / 22% / 21% | 2.52 |
| 18 | (D) đang dùng + loại ≥80% | 60% / 50% / 50% / 50% | 20% / 15% / 20% / 20% | 2.52 |
| 18 | Pool đang dùng | 70% / 55% / 54% / 54% | 20% / 20% / 22% / 21% | 2.56 |

**Luật loại được chọn nhiều nhất** (số kỳ/100): Luật: Bỏ số ra 3 lần trong 5 kỳ (74) · Luật: Bỏ số nhịp "ra – vắng 2 – ra" (vừa ra lại sau đúng 2 kỳ vắng) (73) · Luật: Bỏ số nóng nhất 10 kỳ (≥4 lần) (71) · Luật: Bỏ số vắng ≥30 kỳ (43) · Luật: Bỏ số ra nhiều nhất 100 kỳ (41) · Luật: Bỏ số ra 2 kỳ liền (36) · Markov bộ số bậc 1, học 50 — điểm 0 (34) · Luật: Bỏ số ra ít nhất 100 kỳ (32)

**Phương pháp cộng điểm được chọn nhiều nhất** (số kỳ/100): Tỉ lệ vắng/vắng TB (cao = đến hạn) (86) · Pool app đang dùng (điểm goiy) (79) · KNN 5 đặc trưng vắng (71) · 連休回数 riêng từng số (cả lịch sử) (66) · Chuỗi ra/vắng bậc 9, riêng, học 100 (66) · Chuỗi ra/vắng bậc 2, riêng, học 100 (64) · Chuỗi ra/vắng bậc 9, riêng, học 50 (57) · Chuỗi ra/vắng bậc 10, riêng, học 100 (57) · Chuỗi ra/vắng bậc 10, riêng, học 50 (52) · Chuỗi ra/vắng bậc 1, riêng, học 50 (47) · Chuỗi ra/vắng bậc 10, chung, học 100 (47) · Markov trễ 2 kỳ, học 50 (45)

**Riêng các phương pháp mới tra được** — top 15 ra mỗi số (10 / 20 / 50 / 100 kỳ), được chọn bao nhiêu kỳ:
- 連休回数 riêng từng số (cả lịch sử): 14.0% / 12.7% / 15.1% / 13.9% (TB 13.3%) · chọn 66 kỳ
- 連休回数 chung mọi số (100 kỳ): 16.7% / 15.7% / 13.7% / 13.7% (TB 13.3%) · chọn 26 kỳ
- Tỉ lệ vắng/vắng TB (cao = đến hạn): 14.7% / 13.3% / 13.6% / 14.3% (TB 13.3%) · chọn 86 kỳ
- Tỉ lệ vắng/vắng TB (thấp = vừa ra): 12.7% / 13.3% / 13.5% / 13.3% (TB 13.3%) · chọn 16 kỳ
- KNN 5 đặc trưng vắng: 14.7% / 14.0% / 14.4% / 13.8% (TB 13.3%) · chọn 71 kỳ
- HMM 2 trạng thái nóng/nguội: 14.0% / 12.7% / 12.7% / 13.0% (TB 13.3%) · chọn 0 kỳ
- 斜连 số chéo: 13.3% / 13.7% / 12.4% / 12.9% (TB 13.3%) · chọn 1 kỳ
- 隔号 cách số kỳ trước ±2: 15.3% / 14.3% / 14.5% / 13.7% (TB 13.3%) · chọn 38 kỳ

**Kỳ tới**: loại hẳn 08 15 41 42 · pool 18: 03 45 16 21 18 11 12 22 43 38 39 05 27 09 02 31 17 25


## loto535 — pool mới (chạy tiến, tự chọn phương pháp theo 100 kỳ trước mỗi kỳ) so với pool đang dùng, đến 13/10/2026 21h

Loại hẳn TB **3.6 số/kỳ** (10 kỳ gần 2.3) · kỳ không loại nhầm số nào: 60% / 50% / 54% / 56% (khung 10/20/50/100)

| Pool | Cách | Kỳ ≥3 số: 10 / 20 / 50 / 100 kỳ | Kỳ ≥4 số: 10 / 20 / 50 / 100 kỳ | TB số trúng (100 kỳ) |
|---|---|---|---|---|
| 10 | Pool mới (gộp hết) | 0% / 5% / 12% / 13% | 0% / 0% / 0% / 0% | 1.38 |
| 10 | (C) đang dùng + loại ≥70% | 10% / 10% / 18% / 17% | 0% / 0% / 4% / 5% | 1.63 |
| 10 | (D) đang dùng + loại ≥80% | 10% / 10% / 20% / 18% | 0% / 0% / 4% / 5% | 1.63 |
| 10 | Pool đang dùng | 10% / 10% / 18% / 19% | 0% / 0% / 4% / 5% | 1.65 |
| 15 | Pool mới (gộp hết) | 10% / 15% / 34% / 36% | 10% / 10% / 14% / 9% | 2.01 |
| 15 | (C) đang dùng + loại ≥70% | 30% / 25% / 46% / 46% | 10% / 5% / 16% / 16% | 2.35 |
| 15 | (D) đang dùng + loại ≥80% | 30% / 25% / 46% / 44% | 10% / 5% / 18% / 17% | 2.35 |
| 15 | Pool đang dùng | 40% / 30% / 46% / 47% | 10% / 5% / 18% / 17% | 2.37 |
| 18 | Pool mới (gộp hết) | 50% / 40% / 46% / 48% | 10% / 15% / 24% / 21% | 2.49 |
| 18 | (C) đang dùng + loại ≥70% | 50% / 50% / 60% / 55% | 30% / 20% / 36% / 29% | 2.76 |
| 18 | (D) đang dùng + loại ≥80% | 50% / 50% / 62% / 58% | 30% / 20% / 36% / 27% | 2.77 |
| 18 | Pool đang dùng | 60% / 50% / 62% / 58% | 30% / 20% / 36% / 29% | 2.78 |

**Luật loại được chọn nhiều nhất** (số kỳ/100): Luật: Bỏ số nhịp "ra – vắng 2 – ra" (vừa ra lại sau đúng 2 kỳ vắng) (98) · Markov bộ số bậc 2, học 100 — điểm 0 (76) · Luật: Bỏ số tái xuất sau vắng ≥15 (59) · Chuỗi ra/vắng bậc 4, chung, học 100 — điểm ≤60% TB (56) · Luật: Loto 13h: bỏ số tái xuất trong phiên (ra hôm trước sau vắng ≥10 kỳ 13h) (54) · Luật: Bỏ số ra 3 lần trong 5 kỳ (53) · Chuỗi ra/vắng bậc 4, chung, học 200 — điểm ≤60% TB (50) · Chuỗi ra/vắng bậc 5, chung, học 100 — điểm ≤60% TB (47)

**Phương pháp cộng điểm được chọn nhiều nhất** (số kỳ/100): Markov bộ số bậc 3, học 50 (96) · Pool app đang dùng (điểm goiy) (91) · Markov bộ số bậc 2, học 50 (90) · Chuỗi ra/vắng bậc 7, riêng, học 50 (85) · Chuỗi ra/vắng bậc 5, riêng, học 50 (84) · Tỉ lệ vắng/vắng TB (cao = đến hạn) (81) · Markov bộ số bậc 4, học 100 (81) · Markov bộ số bậc 4, học 50 (79) · Chuỗi ra/vắng bậc 1, riêng, học 100 (77) · Chuỗi ra/vắng bậc 10, chung, học 100 (75) · Chuỗi ra/vắng bậc 10, chung, học 200 (73) · Chuỗi ra/vắng bậc 2, chung, học 100 (72)

**Riêng các phương pháp mới tra được** — top 15 ra mỗi số (10 / 20 / 50 / 100 kỳ), được chọn bao nhiêu kỳ:
- 連休回数 riêng từng số (cả lịch sử): 14.7% / 14.0% / 14.5% / 13.8% (TB 14.3%) · chọn 0 kỳ
- 連休回数 chung mọi số (100 kỳ): 11.3% / 12.0% / 13.3% / 13.7% (TB 14.3%) · chọn 47 kỳ
- Tỉ lệ vắng/vắng TB (cao = đến hạn): 12.0% / 13.0% / 15.2% / 14.3% (TB 14.3%) · chọn 81 kỳ
- Tỉ lệ vắng/vắng TB (thấp = vừa ra): 15.3% / 15.0% / 13.5% / 14.3% (TB 14.3%) · chọn 0 kỳ
- KNN 5 đặc trưng vắng: 14.0% / 13.0% / 14.5% / 14.9% (TB 14.3%) · chọn 52 kỳ
- HMM 2 trạng thái nóng/nguội: 14.0% / 15.0% / 14.5% / 14.9% (TB 14.3%) · chọn 52 kỳ
- 斜连 số chéo: 14.7% / 13.7% / 14.8% / 14.3% (TB 14.3%) · chọn 11 kỳ
- 隔号 cách số kỳ trước ±2: 14.0% / 14.0% / 15.7% / 14.6% (TB 14.3%) · chọn 35 kỳ

**Kỳ tới**: loại hẳn 01 32 34 · pool 18: 14 08 18 07 20 21 17 11 12 04 16 06 10 02 33 19 15 03



# Thử TỪNG phương pháp gắn vào pool đang dùng — 14/10/2026 (`python build/pool_moi.py <game> --tung`)
## power655 — thử TỪNG phương pháp gắn vào pool đang dùng (187 lần thử)

Ô = % kỳ ≥3 số · % kỳ ≥4 số, theo khung 10 / 20 / 50 / 100 kỳ.

| Phương pháp | Cách gắn | Pool 15 | Pool 18 | Hơn pool đang dùng ở (cả khung 50 & 100) | Ghi chú |
|---|---|---|---|---|---|
| **Pool đang dùng** | — | 30·0 / 25·10 / 20·4 / 23·9 | 30·10 / 35·15 / 30·6 / 36·13 | — | |
| Chuỗi ra/vắng bậc 5, chung, học 100 | gộp 50/50 | 40·10 / 30·15 / 28·12 / 26·10 | 50·20 / 40·20 / 44·16 / 38·13 | P10 ≥3, P10 ≥4, P15 ≥3, P15 ≥4, P18 ≥3 |  |
| Markov trễ 2 kỳ, học 50 | riêng | 60·20 / 35·10 / 30·6 / 29·7 | 60·40 / 40·25 / 34·14 / 37·14 | P10 ≥3, P10 ≥4, P15 ≥3, P18 ≥3, P18 ≥4 |  |
| Chuỗi ra/vắng bậc 5, chung, học 50 | gộp 50/50 | 40·10 / 40·25 / 30·14 / 27·10 | 60·30 / 55·35 / 42·18 / 36·13 | P10 ≥3, P10 ≥4, P15 ≥3, P15 ≥4 |  |
| Chuỗi ra/vắng bậc 5, chung, học 100 | riêng | 50·20 / 35·10 / 34·8 / 27·8 | 70·30 / 50·15 / 46·16 / 40·13 | P10 ≥3, P10 ≥4, P15 ≥3, P18 ≥3 |  |
| Chuỗi ra/vắng bậc 7, chung, học 100 | gộp 50/50 | 30·10 / 30·15 / 28·10 / 27·9 | 50·20 / 45·20 / 38·14 / 32·14 | P10 ≥3, P10 ≥4, P15 ≥3, P18 ≥4 |  |
| Chuỗi ra/vắng bậc 4, chung, học 100 | gộp 50/50 | 40·0 / 35·5 / 24·4 / 26·7 | 50·30 / 50·25 / 40·18 / 38·14 | P10 ≥3, P15 ≥3, P18 ≥3, P18 ≥4 |  |
| Chuỗi ra/vắng bậc 6, chung, học 100 | gộp 50/50 | 40·10 / 35·10 / 28·8 / 27·10 | 40·10 / 45·15 / 36·12 / 36·12 | P10 ≥3, P10 ≥4, P15 ≥3, P15 ≥4 |  |
| Markov bộ số bậc 4, học 50 | gộp 50/50 | 30·10 / 25·5 / 28·4 / 29·7 | 40·20 / 40·15 / 36·10 / 41·11 | P10 ≥3, P10 ≥4, P15 ≥3, P18 ≥3 |  |
| Markov trễ 2 kỳ, học 100 | riêng | 40·20 / 35·10 / 22·6 / 26·7 | 40·30 / 40·15 / 36·12 / 39·17 | P10 ≥3, P15 ≥3, P18 ≥3, P18 ≥4 |  |
| Markov trễ 2 kỳ, học 50 | gộp 50/50 | 50·20 / 35·10 / 24·4 / 26·7 | 60·40 / 45·25 / 34·10 / 39·16 | P10 ≥3, P15 ≥3, P18 ≥3, P18 ≥4 |  |
| Markov bộ số bậc 4, học 100 — điểm 0 | loại | 10·10 / 25·10 / 22·4 / 25·9 | 30·10 / 40·10 / 36·6 / 39·13 | P10 ≥3, P10 ≥4, P15 ≥3, P18 ≥3 | bỏ 23.8 số/kỳ, loại nhầm 96/100 kỳ |
| Chuỗi ra/vắng bậc 5, riêng, học 100 | gộp 50/50 | 40·10 / 35·15 / 22·10 / 24·10 | 50·10 / 40·15 / 30·14 / 33·14 | P10 ≥4, P15 ≥3, P15 ≥4, P18 ≥4 |  |
| Chuỗi ra/vắng bậc 3, chung, học 50 | gộp 50/50 | 60·20 / 45·15 / 32·8 / 27·8 | 70·30 / 65·25 / 58·14 / 50·13 | P10 ≥3, P15 ≥3, P18 ≥3 |  |
| Chuỗi ra/vắng bậc 3, chung, học 100 | gộp 50/50 | 60·20 / 45·15 / 32·6 / 27·8 | 60·30 / 60·20 / 56·12 / 52·11 | P10 ≥3, P15 ≥3, P18 ≥3 |  |
| Chuỗi ra/vắng bậc 5, chung, học 50 | riêng | 60·30 / 45·15 / 32·10 / 25·8 | 70·30 / 50·20 / 46·16 / 36·13 | P10 ≥3, P10 ≥4, P15 ≥3 |  |
| 連休回数 chung mọi số (100 kỳ) | gộp 50/50 | 40·20 / 35·15 / 26·10 / 26·8 | 60·30 / 55·20 / 42·16 / 37·12 | P10 ≥3, P15 ≥3, P18 ≥3 |  |
| Chuỗi ra/vắng bậc 4, riêng, học 100 | gộp 50/50 | 40·10 / 40·15 / 30·10 / 28·5 | 50·10 / 45·20 / 36·14 / 37·13 | P10 ≥4, P15 ≥3, P18 ≥3 |  |
| Tỉ lệ vắng/vắng TB (cao = đến hạn) | riêng | 20·0 / 25·0 / 30·4 / 26·8 | 30·0 / 35·5 / 42·14 / 38·16 | P15 ≥3, P18 ≥3, P18 ≥4 |  |
| Chuỗi ra/vắng bậc 3, riêng, học 100 — điểm ≤60% TB | loại | 30·10 / 30·15 / 26·6 / 27·8 | 40·10 / 45·15 / 36·10 / 38·12 | P10 ≥3, P15 ≥3, P18 ≥3 | bỏ 9.1 số/kỳ, loại nhầm 65/100 kỳ |
| Chuỗi ra/vắng bậc 2, riêng, học 100 | gộp 50/50 | 20·10 / 30·10 / 26·4 / 24·5 | 30·10 / 40·10 / 36·12 / 35·13 | P10 ≥3, P10 ≥4, P15 ≥3 |  |
| Chuỗi ra/vắng bậc 3, riêng, học 100 | gộp 50/50 | 30·10 / 35·10 / 28·6 / 25·5 | 40·10 / 40·15 / 36·10 / 36·10 | P10 ≥3, P10 ≥4, P15 ≥3 |  |
| Chuỗi ra/vắng bậc 2, riêng, học 100 — điểm ≤60% TB | loại | 30·10 / 30·15 / 28·6 / 28·10 | 40·10 / 40·15 / 34·8 / 36·13 | P10 ≥3, P15 ≥3, P15 ≥4 | bỏ 6.2 số/kỳ, loại nhầm 56/100 kỳ |
| Chuỗi ra/vắng bậc 10, chung, học 50 | gộp 50/50 | 20·0 / 30·5 / 24·6 / 26·5 | 50·20 / 50·20 / 38·16 / 37·12 | P10 ≥3, P15 ≥3, P18 ≥3 |  |
| Chuỗi ra/vắng bậc 7, riêng, học 50 — điểm ≤60% TB | loại | 20·10 / 35·15 / 26·6 / 30·7 | 40·10 / 50·20 / 34·10 / 37·12 | P10 ≥3, P15 ≥3, P18 ≥3 | bỏ 12.5 số/kỳ, loại nhầm 80/100 kỳ |
| Chuỗi ra/vắng bậc 4, riêng, học 100 — điểm ≤60% TB | loại | 30·10 / 30·15 / 22·6 / 27·9 | 40·10 / 40·15 / 30·10 / 36·13 | P10 ≥3, P10 ≥4, P15 ≥3 | bỏ 9.6 số/kỳ, loại nhầm 69/100 kỳ |

Số phương pháp hơn pool đang dùng ít nhất 1 chỉ số (ở cả khung 50 & 100): 127/187

## mega645 — thử TỪNG phương pháp gắn vào pool đang dùng (187 lần thử)

Ô = % kỳ ≥3 số · % kỳ ≥4 số, theo khung 10 / 20 / 50 / 100 kỳ.

| Phương pháp | Cách gắn | Pool 15 | Pool 18 | Hơn pool đang dùng ở (cả khung 50 & 100) | Ghi chú |
|---|---|---|---|---|---|
| **Pool đang dùng** | — | 50·0 / 40·10 / 40·12 / 44·10 | 70·20 / 55·20 / 54·22 / 54·21 | — | |
| Chuỗi ra/vắng bậc 6, riêng, học 50 — điểm ≤60% TB | loại | 40·10 / 40·15 / 42·16 / 45·12 | 50·10 / 50·20 / 56·22 / 57·21 | P10 ≥4, P15 ≥3, P15 ≥4, P18 ≥3 | bỏ 15.1 số/kỳ, loại nhầm 93/100 kỳ |
| Chuỗi ra/vắng bậc 10, riêng, học 50 | gộp 50/50 | 50·20 / 40·10 / 50·10 / 48·11 | 60·40 / 50·30 / 58·26 / 55·27 | P15 ≥3, P18 ≥3, P18 ≥4 |  |
| 連休回数 riêng từng số (cả lịch sử) | gộp 50/50 | 40·20 / 30·10 / 42·16 / 38·14 | 50·20 / 45·15 / 60·22 / 56·23 | P10 ≥4, P15 ≥4, P18 ≥3 |  |
| Markov bộ số bậc 4, học 50 | gộp 50/50 | 60·20 / 30·10 / 36·16 / 36·14 | 70·30 / 55·25 / 60·30 / 57·30 | P15 ≥4, P18 ≥3, P18 ≥4 |  |
| Markov bộ số bậc 4, học 100 — điểm 0 | loại | 40·10 / 30·15 / 32·14 / 37·13 | 60·30 / 50·25 / 56·24 / 57·22 | P15 ≥4, P18 ≥3, P18 ≥4 | bỏ 8.1 số/kỳ, loại nhầm 67/100 kỳ |
| Chuỗi ra/vắng bậc 5, riêng, học 100 — điểm ≤60% TB | loại | 40·10 / 35·15 / 34·16 / 36·11 | 40·30 / 45·25 / 46·26 / 50·19 | P10 ≥3, P10 ≥4, P15 ≥4 | bỏ 9.4 số/kỳ, loại nhầm 71/100 kỳ |
| Chuỗi ra/vắng bậc 8, riêng, học 50 | gộp 50/50 | 30·10 / 35·5 / 40·10 / 40·11 | 50·30 / 50·20 / 60·28 / 61·28 | P18 ≥3, P18 ≥4 |  |
| Chuỗi ra/vắng bậc 8, riêng, học 100 | gộp 50/50 | 50·20 / 55·10 / 50·10 / 49·13 | 50·40 / 55·25 / 56·22 / 58·27 | P15 ≥3, P18 ≥3 |  |
| 連休回数 riêng từng số (cả lịch sử) — điểm ≤60% TB | loại | 60·10 / 45·15 / 42·16 / 39·14 | 70·20 / 60·25 / 58·26 / 53·23 | P15 ≥4, P18 ≥4 | bỏ 5.9 số/kỳ, loại nhầm 53/100 kỳ |
| Chuỗi ra/vắng bậc 10, riêng, học 100 | gộp 50/50 | 30·20 / 30·15 / 36·10 / 38·12 | 60·30 / 50·25 / 64·24 / 59·27 | P18 ≥3, P18 ≥4 |  |
| Chuỗi ra/vắng bậc 10, chung, học 50 | gộp 50/50 | 70·30 / 55·20 / 38·18 / 41·14 | 70·60 / 60·40 / 50·28 / 55·24 | P15 ≥4, P18 ≥4 |  |
| Chuỗi ra/vắng bậc 6, riêng, học 100 — điểm ≤60% TB | loại | 50·20 / 45·20 / 42·18 / 39·11 | 70·20 / 60·25 / 52·24 / 52·17 | P10 ≥4, P15 ≥4 | bỏ 10.5 số/kỳ, loại nhầm 78/100 kỳ |
| Chuỗi ra/vắng bậc 9, riêng, học 50 | gộp 50/50 | 30·10 / 30·5 / 44·8 / 44·8 | 50·30 / 40·20 / 60·24 / 60·26 | P18 ≥3, P18 ≥4 |  |
| Chuỗi ra/vắng bậc 5, riêng, học 50 — điểm ≤60% TB | loại | 30·0 / 30·5 / 38·14 / 39·11 | 40·20 / 40·20 / 52·24 / 57·21 | P10 ≥4, P15 ≥4 | bỏ 14.1 số/kỳ, loại nhầm 85/100 kỳ |
| Chuỗi ra/vắng bậc 7, riêng, học 50 — điểm ≤60% TB | loại | 30·10 / 35·15 / 40·16 / 40·13 | 30·20 / 40·25 / 52·24 / 52·22 | P15 ≥4, P18 ≥4 | bỏ 14.8 số/kỳ, loại nhầm 87/100 kỳ |
| Chuỗi ra/vắng bậc 5, riêng, học 100 | gộp 50/50 | 30·10 / 30·10 / 38·12 / 37·11 | 40·40 / 40·30 / 46·30 / 49·23 | P10 ≥4, P18 ≥4 |  |
| Chuỗi ra/vắng bậc 8, riêng, học 100 | riêng | 50·30 / 45·30 / 36·18 / 35·12 | 50·30 / 55·30 / 52·22 / 53·20 | P10 ≥4, P15 ≥4 |  |
| Chuỗi ra/vắng bậc 10, riêng, học 50 — điểm ≤60% TB | loại | 50·10 / 40·15 / 40·14 / 38·13 | 60·40 / 55·35 / 54·24 / 50·22 | P15 ≥4, P18 ≥4 | bỏ 10.9 số/kỳ, loại nhầm 72/100 kỳ |
| Chuỗi ra/vắng bậc 2, chung, học 100 | gộp 50/50 | 40·10 / 40·10 / 32·10 / 34·9 | 70·50 / 70·35 / 56·34 / 51·25 | P10 ≥4, P18 ≥4 |  |
| Markov bộ số bậc 4, học 50 — điểm 0 | loại | 30·20 / 30·15 / 36·20 / 32·16 | 50·20 / 45·15 / 46·24 / 43·20 | P10 ≥4, P15 ≥4 | bỏ 18.7 số/kỳ, loại nhầm 94/100 kỳ |
| Chuỗi ra/vắng bậc 5, chung, học 100 | gộp 50/50 | 50·30 / 45·15 / 36·14 / 37·13 | 60·40 / 60·25 / 54·24 / 54·22 | P15 ≥4, P18 ≥4 |  |
| Chuỗi ra/vắng bậc 9, riêng, học 50 | riêng | 10·10 / 20·15 / 24·16 / 34·15 | 40·10 / 35·20 / 40·18 / 46·22 | P10 ≥4, P15 ≥4 |  |
| Chuỗi ra/vắng bậc 3, riêng, học 50 | gộp 50/50 | 40·20 / 30·15 / 30·18 / 29·13 | 50·20 / 50·15 / 44·20 / 43·16 | P10 ≥4, P15 ≥4 |  |
| Chuỗi ra/vắng bậc 2, riêng, học 100 | gộp 50/50 | 30·10 / 25·10 / 30·14 / 29·11 | 40·10 / 50·15 / 48·18 / 45·16 | P10 ≥4, P15 ≥4 |  |
| HMM — xác suất ≤60% TB | loại | 50·0 / 40·10 / 40·12 / 44·10 | 70·20 / 60·20 / 58·22 / 56·19 | P18 ≥3 | bỏ 3.9 số/kỳ, loại nhầm 40/100 kỳ |

Số phương pháp hơn pool đang dùng ít nhất 1 chỉ số (ở cả khung 50 & 100): 63/187

## loto535 — thử TỪNG phương pháp gắn vào pool đang dùng (246 lần thử)

Ô = % kỳ ≥3 số · % kỳ ≥4 số, theo khung 10 / 20 / 50 / 100 kỳ.

| Phương pháp | Cách gắn | Pool 15 | Pool 18 | Hơn pool đang dùng ở (cả khung 50 & 100) | Ghi chú |
|---|---|---|---|---|---|
| **Pool đang dùng** | — | 40·10 / 30·5 / 46·18 / 47·17 | 60·30 / 50·20 / 62·36 / 58·29 | — | |
| Luật: Loto: bỏ số vắng ≥20 kỳ CÙNG PHIÊN (13h đúng ~80%, 21h ngược) | loại | 50·10 / 35·5 / 50·22 / 49·19 | 50·30 / 45·20 / 60·36 / 57·29 | P10 ≥3, P10 ≥4, P15 ≥3, P15 ≥4 | bỏ 1.6 số/kỳ, loại nhầm 22/100 kỳ |
| Chuỗi ra/vắng bậc 10, riêng, học 200 — điểm ≤60% TB | loại | 40·10 / 35·10 / 48·24 / 44·20 | 50·20 / 50·20 / 64·36 / 58·28 | P10 ≥3, P10 ≥4, P15 ≥4 | bỏ 5.6 số/kỳ, loại nhầm 52/100 kỳ |
| Chuỗi ra/vắng bậc 9, riêng, học 200 — điểm ≤60% TB | loại | 40·0 / 35·5 / 52·22 / 46·19 | 50·10 / 50·15 / 62·34 / 55·28 | P10 ≥3, P15 ≥4 | bỏ 5.1 số/kỳ, loại nhầm 51/100 kỳ |
| Chuỗi ra/vắng bậc 10, riêng, học 50 — điểm ≤60% TB | loại | 40·0 / 30·0 / 50·16 / 50·16 | 70·20 / 55·15 / 68·34 / 62·27 | P15 ≥3, P18 ≥3 | bỏ 4.3 số/kỳ, loại nhầm 49/100 kỳ |
| Chuỗi ra/vắng bậc 10, chung, học 200 — điểm ≤60% TB | loại | 50·10 / 35·5 / 46·20 / 47·16 | 50·20 / 50·15 / 60·32 / 57·30 | P10 ≥3, P10 ≥4 | bỏ 3.0 số/kỳ, loại nhầm 35/100 kỳ |
| Chuỗi ra/vắng bậc 7, chung, học 200 — điểm ≤60% TB | loại | 40·10 / 30·5 / 46·20 / 47·18 | 40·30 / 40·20 / 58·32 / 56·27 | P10 ≥3, P15 ≥4 | bỏ 1.0 số/kỳ, loại nhầm 14/100 kỳ |
| Markov bộ số bậc 2, học 100 | gộp 50/50 | 50·10 / 45·15 / 46·22 / 43·18 | 70·20 / 55·25 / 58·34 / 58·30 | P10 ≥4, P15 ≥4 |  |
| Luật: Bỏ số ra nhiều nhất 100 kỳ | loại | 30·10 / 25·5 / 46·20 / 43·19 | 60·20 / 50·15 / 62·32 / 56·26 | P10 ≥4, P15 ≥4 | bỏ 1.0 số/kỳ, loại nhầm 17/100 kỳ |
| Chuỗi ra/vắng bậc 6, chung, học 200 — điểm ≤60% TB | loại | 40·10 / 30·5 / 48·16 / 48·16 | 50·30 / 40·20 / 58·32 / 56·26 | P10 ≥3, P15 ≥3 | bỏ 0.6 số/kỳ, loại nhầm 10/100 kỳ |
| 連休回数 riêng từng số (cả lịch sử) — điểm ≤60% TB | loại | 50·10 / 30·5 / 46·20 / 42·20 | 60·30 / 50·20 / 62·30 / 56·27 | P10 ≥4, P15 ≥4 | bỏ 3.7 số/kỳ, loại nhầm 44/100 kỳ |
| Chuỗi ra/vắng bậc 10, riêng, học 100 | gộp 50/50 | 20·10 / 30·10 / 44·22 / 39·17 | 30·20 / 40·15 / 54·28 / 55·28 | P10 ≥3, P10 ≥4 |  |
| Chuỗi ra/vắng bậc 2, riêng, học 50 — điểm ≤60% TB | loại | 40·10 / 30·5 / 44·22 / 45·18 | 40·20 / 40·15 / 50·32 / 52·26 | P10 ≥3, P15 ≥4 | bỏ 7.2 số/kỳ, loại nhầm 68/100 kỳ |
| Markov bộ số bậc 4, học 100 — điểm 0 | loại | 30·30 / 25·15 / 48·16 / 48·14 | 40·30 / 35·15 / 56·24 / 56·21 | P10 ≥3, P15 ≥3 | bỏ 7.4 số/kỳ, loại nhầm 63/100 kỳ |
| Luật: Loto 13h: bỏ số tái xuất trong phiên (ra hôm trước sau vắng ≥10 kỳ 13h) | loại | 40·10 / 30·5 / 48·18 / 48·17 | 60·30 / 50·20 / 62·36 / 59·29 | P15 ≥3 | bỏ 0.5 số/kỳ, loại nhầm 6/100 kỳ |
| Chuỗi ra/vắng bậc 8, riêng, học 200 — điểm ≤60% TB | loại | 30·10 / 30·5 / 50·24 / 46·20 | 50·20 / 45·10 / 58·30 / 59·26 | P15 ≥4 | bỏ 4.5 số/kỳ, loại nhầm 58/100 kỳ |
| Luật: Bỏ số ra kỳ trước VÀ kỳ t−3 | loại | 40·10 / 30·5 / 46·18 / 47·17 | 60·30 / 50·20 / 62·36 / 58·29 | P10 ≥4 | bỏ 0.7 số/kỳ, loại nhầm 7/100 kỳ |
| Chuỗi ra/vắng bậc 9, riêng, học 50 — điểm ≤60% TB | loại | 40·20 / 30·10 / 48·20 / 46·19 | 60·30 / 50·25 / 60·36 / 58·29 | P15 ≥4 | bỏ 5.0 số/kỳ, loại nhầm 49/100 kỳ |
| Chuỗi ra/vắng bậc 3, chung, học 50 — điểm ≤60% TB | loại | 40·10 / 30·5 / 46·18 / 46·17 | 60·30 / 50·20 / 62·36 / 58·29 | P10 ≥4 | bỏ 0.6 số/kỳ, loại nhầm 8/100 kỳ |
| Chuỗi ra/vắng bậc 4, chung, học 200 — điểm ≤60% TB | loại | 40·10 / 30·5 / 46·18 / 47·16 | 60·30 / 50·20 / 62·36 / 59·28 | P10 ≥3 | bỏ 0.6 số/kỳ, loại nhầm 7/100 kỳ |
| Chuỗi ra/vắng bậc 6, chung, học 100 — điểm ≤60% TB | loại | 40·10 / 30·5 / 46·18 / 46·15 | 60·30 / 55·20 / 64·34 / 60·26 | P18 ≥3 | bỏ 1.1 số/kỳ, loại nhầm 14/100 kỳ |
| Chuỗi ra/vắng bậc 1, riêng, học 100 — điểm ≤60% TB | loại | 40·10 / 30·5 / 46·18 / 46·17 | 60·30 / 50·20 / 62·36 / 57·28 | P10 ≥3 | bỏ 2.9 số/kỳ, loại nhầm 35/100 kỳ |
| Markov bộ số bậc 1, học 50 — điểm 0 | loại | 40·10 / 30·5 / 46·20 / 47·18 | 50·30 / 45·20 / 60·36 / 57·29 | P15 ≥4 | bỏ 0.5 số/kỳ, loại nhầm 7/100 kỳ |
| Markov bộ số bậc 2, học 100 — điểm 0 | loại | 40·10 / 30·5 / 46·18 / 46·18 | 50·30 / 45·20 / 60·36 / 56·29 | P10 ≥3 | bỏ 0.4 số/kỳ, loại nhầm 7/100 kỳ |
| Chuỗi ra/vắng bậc 7, chung, học 50 — điểm ≤60% TB | loại | 40·10 / 35·5 / 46·20 / 48·15 | 50·30 / 45·25 / 56·36 / 57·27 | P10 ≥3 | bỏ 2.6 số/kỳ, loại nhầm 31/100 kỳ |
| Luật: Bỏ số nhịp "ra – vắng 2 – ra" (vừa ra lại sau đúng 2 kỳ vắng) | loại | 30·10 / 25·5 / 44·18 / 46·17 | 50·30 / 45·20 / 60·36 / 58·29 | P10 ≥3 | bỏ 0.6 số/kỳ, loại nhầm 7/100 kỳ |

Số phương pháp hơn pool đang dùng ít nhất 1 chỉ số (ở cả khung 50 & 100): 64/246

