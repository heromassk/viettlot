# Rà soát dấu vết — 05/10/2026 (`python3 build/rasoat.py <game>`)

Dấu vết = xác suất nghiêng (không cần đúng 100%). ✔ nghiêng ổn định ở cả 2 khung 100 kỳ · ~ nghiêng 1 khung · ✘ không nghiêng / ngược. ● = đang áp dụng (loại hẳn hoặc trọng số nhỏ).

## mega645 — rà soát 35 luật, 100 kỳ gần / 100 kỳ trước (bình quân mỗi số 13.3%)

| Luật | Áp dụng | Ra mỗi số (gần / trước) | Kỳ không mất số (luật loại) | Cỡ nhóm TB | Nhận định |
|---|---|---|---|---|---|
| Bỏ số vắng ≥20 kỳ | ● | 11.5% / 12.7% | 69% / 63% | 2.9 | ✔ ra ít (nghiêng ổn định) |
| Bỏ số vắng ≥25 kỳ |  | 10.5% / 12.3% | 80% / 74% | 1.9 | ✔ ra ít (nghiêng ổn định) |
| Bỏ số vắng ≥30 kỳ |  | 6.8% / 16.4% | 90% / 75% | 1.5 | ~ ít ở 1 khung |
| Bỏ số "lâu lâu mới ra" (200 kỳ ≤85% kỳ vọng) đang vắng ≥15 | ● | 12.3% / 10.5% | 75% / 82% | 2.5 | ✔ ra ít (nghiêng ổn định) |
| Bỏ số vắng lâu nhất |  | 8.0% / 15.0% | 92% / 85% | 1.0 | ~ ít ở 1 khung |
| Bỏ số vắng lâu nhì |  | 9.0% / 15.0% | 91% / 85% | 1.0 | ~ ít ở 1 khung |
| Bỏ số ra 2 kỳ liền | ● | 10.3% / 10.8% | 87% / 88% | 1.2 | ✔ ra ít (nghiêng ổn định) |
| Bỏ số ra 3 lần trong 5 kỳ |  | 8.5% / 8.7% | 88% / 89% | 1.4 | ✔ ra ít (nghiêng ổn định) |
| Bỏ số ra kỳ trước VÀ kỳ t−3 | ● | 11.2% / 12.7% | 84% / 84% | 1.4 | ✔ ra ít (nghiêng ổn định) |
| Bỏ số tái xuất sau vắng ≥15 |  | 10.0% / 9.6% | 87% / 87% | 1.3 | ✔ ra ít (nghiêng ổn định) |
| Bỏ số tái xuất sau vắng ≥10 |  | 13.5% / 12.3% | 78% / 79% | 1.7 | ~ ít ở 1 khung |
| Bỏ số nóng nhất 10 kỳ (≥4 lần) |  | 5.9% / 15.9% | 94% / 84% | 1.0 | ~ ít ở 1 khung |
| Bỏ số ra ít nhất 100 kỳ |  | 15.0% / 5.0% | 85% / 95% | 1.0 | ~ ít ở 1 khung |
| Bỏ số ra nhiều nhất 100 kỳ |  | 10.0% / 12.0% | 90% / 88% | 1.0 | ✔ ra ít (nghiêng ổn định) |
| Bỏ số nhịp "ra – vắng 2 – ra" (vừa ra lại sau đúng 2 kỳ vắng) |  | 11.1% / 10.2% | 86% / 87% | 1.3 | ✔ ra ít (nghiêng ổn định) |
| Bỏ số phá nhịp tối thiểu (100 kỳ: luôn nghỉ ≥x kỳ, mới nghỉ <x) |  | 17.1% / 10.8% | 69% / 78% | 1.8 | ~ ít ở 1 khung |
| Bỏ số phá nhịp tối thiểu (200 kỳ) |  | 9.5% / 11.5% | 89% / 88% | 1.1 | ✔ ra ít (nghiêng ổn định) |
| Bỏ số nhỏ nhất kỳ trước |  | 15.0% / 9.0% | 85% / 91% | 1.0 | ~ ít ở 1 khung |
| Bỏ số lớn nhất kỳ trước | ● | 12.0% / 14.0% | 88% / 86% | 1.0 | ~ ít ở 1 khung |
| Có ≥1 số của 2 kỳ gần nhất | | — | đúng 90 / 92% kỳ | — | khẳng định |
| Có ≥1 số trong 10 số nóng nhất 20 kỳ | | — | đúng 80 / 82% kỳ | — | khẳng định |
| Có ≥1 số trùng hoặc kề ±1 kỳ trước | | — | đúng 95 / 98% kỳ | — | khẳng định |
| Không trùng ≥2 số với kỳ trước | | — | đúng 86 / 90% kỳ | — | khẳng định |
| Nhóm "phá nhịp nghỉ" (100 kỳ: ≥80% lần nghỉ ≥x kỳ, mới nghỉ <x) ra ít hơn bình quân |  | 15.0% / 13.9% |  | 7.1 | ✘ ngược (ra nhiều) |
| Nhóm số của kỳ cách 7 kỳ ra NHIỀU hơn bình quân (dấu vết máy, 100 kỳ) |  | 13.4% / 14.1% |  | 5.3 | ~ nhiều ở 1 khung |
| Nhóm số của kỳ cách 9 kỳ ra NHIỀU hơn bình quân (dấu vết máy, 100 kỳ) |  | 12.5% / 14.3% |  | 5.3 | ~ nhiều ở 1 khung |
| Soi cầu: lô kép (11, 22, 33…) ra NHIỀU hơn bình quân |  | 15.5% / 9.8% |  | 4.0 | ~ nhiều ở 1 khung |
| Soi cầu: số cầu Pascal của kỳ trước ra NHIỀU hơn bình quân |  | 7.1% / 16.3% |  | 1.0 | ~ nhiều ở 1 khung |
| Soi cầu: cầu vị trí đã chạy ≥2 kỳ ra NHIỀU hơn bình quân |  | 14.2% / 13.0% |  | 2.0 | ~ nhiều ở 1 khung |
| Soi cầu: kép liền kề của kép kỳ trước (11↔22↔33) ra NHIỀU hơn bình quân |  | 17.0% / 14.8% |  | 1.9 | ✔ ra nhiều (nghiêng ổn định) |
| Soi cầu: lô kẹp (kỳ trước có a, a+2 → a+1) ra ÍT hơn bình quân |  | 9.6% / 18.9% |  | 1.1 | ~ ít ở 1 khung |
| Nhóm nhịp riêng "lúc vắng thế này chưa từng ra" ra ít hơn bình quân |  | 10.8% / 11.7% |  | 6.7 | ✔ ra ít (nghiêng ổn định) |

## power655 — rà soát 35 luật, 100 kỳ gần / 100 kỳ trước (bình quân mỗi số 10.9%)

| Luật | Áp dụng | Ra mỗi số (gần / trước) | Kỳ không mất số (luật loại) | Cỡ nhóm TB | Nhận định |
|---|---|---|---|---|---|
| Bỏ số vắng ≥20 kỳ | ● | 14.7% / 11.0% | 51% / 52% | 4.4 | ✘ ngược (ra nhiều) |
| Bỏ số vắng ≥25 kỳ |  | 15.7% / 10.4% | 70% / 67% | 2.2 | ✘ ngược (ra nhiều) |
| Bỏ số vắng ≥30 kỳ |  | 20.7% / 11.2% | 72% / 78% | 1.4 | ✘ ngược (ra nhiều) |
| Bỏ số "lâu lâu mới ra" (200 kỳ ≤85% kỳ vọng) đang vắng ≥15 |  | 11.9% / 10.0% | 69% / 69% | 3.0 | ~ ít ở 1 khung |
| Bỏ số vắng lâu nhất |  | 18.0% / 11.0% | 82% / 89% | 1.0 | ✘ ngược (ra nhiều) |
| Bỏ số vắng lâu nhì |  | 12.0% / 10.0% | 88% / 90% | 1.0 | ~ ít ở 1 khung |
| Bỏ số ra 2 kỳ liền |  | 15.0% / 13.5% | 81% / 82% | 1.3 | ✘ ngược (ra nhiều) |
| Bỏ số ra 3 lần trong 5 kỳ |  | 7.0% / 6.9% | 91% / 92% | 1.2 | ✔ ra ít (nghiêng ổn định) |
| Bỏ số ra kỳ trước VÀ kỳ t−3 |  | 8.9% / 13.3% | 88% / 82% | 1.3 | ~ ít ở 1 khung |
| Bỏ số tái xuất sau vắng ≥15 |  | 7.6% / 14.7% | 89% / 78% | 1.6 | ~ ít ở 1 khung |
| Bỏ số tái xuất sau vắng ≥10 |  | 8.0% / 15.3% | 84% / 71% | 2.3 | ~ ít ở 1 khung |
| Bỏ số nóng nhất 10 kỳ (≥4 lần) |  | 17.5% / 11.3% | 82% / 89% | 1.0 | ✘ ngược (ra nhiều) |
| Bỏ số ra ít nhất 100 kỳ | ● | 7.0% / 7.0% | 93% / 93% | 1.0 | ✔ ra ít (nghiêng ổn định) |
| Bỏ số ra nhiều nhất 100 kỳ |  | 10.0% / 12.0% | 90% / 88% | 1.0 | ~ ít ở 1 khung |
| Bỏ số nhịp "ra – vắng 2 – ra" (vừa ra lại sau đúng 2 kỳ vắng) |  | 5.0% / 9.1% | 97% / 89% | 1.3 | ✔ ra ít (nghiêng ổn định) |
| Bỏ số phá nhịp tối thiểu (100 kỳ: luôn nghỉ ≥x kỳ, mới nghỉ <x) |  | 9.0% / 12.5% | 71% / 71% | 3.3 | ~ ít ở 1 khung |
| Bỏ số phá nhịp tối thiểu (200 kỳ) |  | 9.9% / 10.7% | 87% / 85% | 1.3 | ~ ít ở 1 khung |
| Bỏ số nhỏ nhất kỳ trước |  | 10.0% / 13.0% | 90% / 87% | 1.0 | ~ ít ở 1 khung |
| Bỏ số lớn nhất kỳ trước |  | 9.0% / 11.0% | 91% / 89% | 1.0 | ~ ít ở 1 khung |
| Có ≥1 số của 2 kỳ gần nhất | | — | đúng 77 / 77% kỳ | — | khẳng định |
| Có ≥1 số trong 10 số nóng nhất 20 kỳ | | — | đúng 72 / 75% kỳ | — | khẳng định |
| Có ≥1 số trùng hoặc kề ±1 kỳ trước | | — | đúng 86 / 89% kỳ | — | khẳng định |
| Không trùng ≥2 số với kỳ trước | | — | đúng 87 / 85% kỳ | — | khẳng định |
| Nhóm "phá nhịp nghỉ" (100 kỳ: ≥80% lần nghỉ ≥x kỳ, mới nghỉ <x) ra ít hơn bình quân |  | 9.1% / 11.9% |  | 9.6 | ~ ít ở 1 khung |
| Nhóm số của kỳ cách 7 kỳ ra NHIỀU hơn bình quân (dấu vết máy, 100 kỳ) |  | 10.2% / 10.4% |  | 5.3 | ✘ không nghiêng |
| Nhóm số của kỳ cách 9 kỳ ra NHIỀU hơn bình quân (dấu vết máy, 100 kỳ) |  | 9.4% / 10.4% |  | 5.4 | ✘ ngược (ra ít) |
| Soi cầu: lô kép (11, 22, 33…) ra NHIỀU hơn bình quân |  | 11.8% / 13.8% |  | 5.0 | ✔ ra nhiều (nghiêng ổn định) |
| Soi cầu: số cầu Pascal của kỳ trước ra NHIỀU hơn bình quân |  | 17.6% / 14.3% |  | 1.0 | ✔ ra nhiều (nghiêng ổn định) |
| Soi cầu: cầu vị trí đã chạy ≥2 kỳ ra NHIỀU hơn bình quân |  | 15.0% / 13.9% |  | 1.8 | ✔ ra nhiều (nghiêng ổn định) |
| Soi cầu: kép liền kề của kép kỳ trước (11↔22↔33) ra NHIỀU hơn bình quân |  | 10.8% / 15.1% |  | 2.2 | ~ nhiều ở 1 khung |
| Soi cầu: lô kẹp (kỳ trước có a, a+2 → a+1) ra ÍT hơn bình quân |  | 10.3% / 5.6% |  | 1.3 | ✔ ra ít (nghiêng ổn định) |
| Nhóm nhịp riêng "lúc vắng thế này chưa từng ra" ra ít hơn bình quân |  | 11.7% / 11.6% |  | 10.6 | ✘ không nghiêng |

## loto535 — rà soát 35 luật, 100 kỳ gần / 100 kỳ trước (bình quân mỗi số 14.3%)

| Luật | Áp dụng | Ra mỗi số (gần / trước) | Kỳ không mất số (luật loại) | Cỡ nhóm TB | Nhận định |
|---|---|---|---|---|---|
| Bỏ số vắng ≥20 kỳ | ● | 15.0% / 11.1% | 77% / 79% | 1.6 | ~ ít ở 1 khung |
| Bỏ số vắng ≥25 kỳ |  | 14.1% / 13.3% | 84% / 81% | 1.1 | ~ ít ở 1 khung |
| Bỏ số vắng ≥30 kỳ |  | 12.5% / 18.2% | 87% / 82% | 1.0 | ~ ít ở 1 khung |
| Bỏ số "lâu lâu mới ra" (200 kỳ ≤85% kỳ vọng) đang vắng ≥15 | ● | 12.9% / 11.9% | 79% / 81% | 1.7 | ✔ ra ít (nghiêng ổn định) |
| Bỏ số vắng lâu nhất | ● | 11.0% / 10.0% | 89% / 90% | 1.0 | ✔ ra ít (nghiêng ổn định) |
| Bỏ số vắng lâu nhì |  | 21.0% / 10.0% | 79% / 90% | 1.0 | ~ ít ở 1 khung |
| Bỏ số ra 2 kỳ liền |  | 17.5% / 13.7% | 79% / 84% | 1.2 | ~ ít ở 1 khung |
| Bỏ số ra 3 lần trong 5 kỳ | ● | 11.9% / 7.6% | 85% / 90% | 1.2 | ✔ ra ít (nghiêng ổn định) |
| Bỏ số ra kỳ trước VÀ kỳ t−3 |  | 11.0% / 13.3% | 86% / 86% | 1.2 | ✔ ra ít (nghiêng ổn định) |
| Bỏ số tái xuất sau vắng ≥15 | ● | 10.2% / 17.1% | 91% / 81% | 1.1 | ~ ít ở 1 khung |
| Bỏ số tái xuất sau vắng ≥10 |  | 10.4% / 12.6% | 88% / 82% | 1.4 | ✔ ra ít (nghiêng ổn định) |
| Bỏ số nóng nhất 10 kỳ (≥4 lần) |  | 23.5% / 11.1% | 77% / 89% | 1.0 | ~ ít ở 1 khung |
| Bỏ số ra ít nhất 100 kỳ |  | 15.0% / 13.0% | 85% / 87% | 1.0 | ~ ít ở 1 khung |
| Bỏ số ra nhiều nhất 100 kỳ |  | 15.0% / 8.0% | 85% / 92% | 1.0 | ~ ít ở 1 khung |
| Bỏ số nhịp "ra – vắng 2 – ra" (vừa ra lại sau đúng 2 kỳ vắng) |  | 8.8% / 9.5% | 90% / 89% | 1.1 | ✔ ra ít (nghiêng ổn định) |
| Bỏ số phá nhịp tối thiểu (100 kỳ: luôn nghỉ ≥x kỳ, mới nghỉ <x) |  | 12.8% / 7.4% | 82% / 87% | 1.6 | ✔ ra ít (nghiêng ổn định) |
| Bỏ số phá nhịp tối thiểu (200 kỳ) |  | 16.1% / 6.7% | 82% / 92% | 1.1 | ~ ít ở 1 khung |
| Loto: bỏ số vắng ≥20 kỳ CÙNG PHIÊN (13h đúng ~80%, 21h ngược) |  | 14.1% / 15.4% | 79% / 70% | 1.7 | ✘ ngược (ra nhiều) |
| Loto 13h: bỏ số tái xuất trong phiên (ra hôm trước sau vắng ≥10 kỳ 13h) |  | 7.7% / 14.3% | 89% / 82% | 1.4 | ~ ít ở 1 khung |
| Bỏ số nhỏ nhất kỳ trước |  | 14.0% / 15.0% | 86% / 85% | 1.0 | ✘ không nghiêng |
| Bỏ số lớn nhất kỳ trước |  | 13.0% / 15.0% | 87% / 85% | 1.0 | ~ ít ở 1 khung |
| Có ≥1 số của 2 kỳ gần nhất | | — | đúng 81 / 79% kỳ | — | khẳng định |
| Có ≥1 số trong 10 số nóng nhất 20 kỳ | | — | đúng 84 / 81% kỳ | — | khẳng định |
| Có ≥1 số trùng hoặc kề ±1 kỳ trước | | — | đúng 90 / 96% kỳ | — | khẳng định |
| Không trùng ≥2 số với kỳ trước | | — | đúng 91 / 86% kỳ | — | khẳng định |
| Nhóm "phá nhịp nghỉ" (100 kỳ: ≥80% lần nghỉ ≥x kỳ, mới nghỉ <x) ra ít hơn bình quân |  | 13.2% / 13.0% |  | 6.2 | ✔ ra ít (nghiêng ổn định) |
| Nhóm số của kỳ cách 7 kỳ ra NHIỀU hơn bình quân (dấu vết máy, 100 kỳ) |  | 16.7% / 15.7% |  | 4.3 | ✔ ra nhiều (nghiêng ổn định) |
| Nhóm số của kỳ cách 9 kỳ ra NHIỀU hơn bình quân (dấu vết máy, 100 kỳ) |  | 17.5% / 15.0% |  | 4.2 | ✔ ra nhiều (nghiêng ổn định) |
| Loto 21h: nhóm tái xuất trong phiên ra NHIỀU hơn bình quân |  | 8.5% / 20.7% |  | 1.3 | ~ nhiều ở 1 khung |
| Soi cầu: lô kép (11, 22, 33…) ra NHIỀU hơn bình quân |  | 16.7% / 19.0% |  | 3.0 | ✔ ra nhiều (nghiêng ổn định) |
| Soi cầu: số cầu Pascal của kỳ trước ra NHIỀU hơn bình quân |  | 23.3% / 16.0% |  | 1.0 | ✔ ra nhiều (nghiêng ổn định) |
| Soi cầu: cầu vị trí đã chạy ≥2 kỳ ra NHIỀU hơn bình quân |  | 15.3% / 6.6% |  | 1.5 | ~ nhiều ở 1 khung |
| Soi cầu: kép liền kề của kép kỳ trước (11↔22↔33) ra NHIỀU hơn bình quân |  | 18.5% / 20.3% |  | 1.5 | ✔ ra nhiều (nghiêng ổn định) |
| Soi cầu: lô kẹp (kỳ trước có a, a+2 → a+1) ra ÍT hơn bình quân |  | 13.3% / 10.9% |  | 1.1 | ✔ ra ít (nghiêng ổn định) |
| Nhóm nhịp riêng "lúc vắng thế này chưa từng ra" ra ít hơn bình quân |  | 13.5% / 13.1% |  | 3.8 | ✔ ra ít (nghiêng ổn định) |

