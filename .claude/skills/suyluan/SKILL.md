---
name: suyluan
description: Suy luận dấu vết Vietlott (power / mega / loto) từ dữ liệu quá khứ — tìm luật LOẠI số, luật khẳng định, tín hiệu cộng/trừ điểm; chấm theo từng kỳ, ưu tiên 100 kỳ gần, kiểm độ ổn định; đề xuất đưa vào skill power/mega/loto. Dùng khi anh nói "suy luận", "suyluan", "tìm dấu vết", "kiểm tra kĩ mega/power/loto", "có cách nào loại/thu hẹp", "có bổ sung suy luận gì không".
---

# suyluan — suy luận dấu vết

Xưng hô: gọi người dùng là **anh**, tự xưng **em**, trả lời tiếng Việt, ngắn gọn, dùng bảng.

## Cách anh nghĩ (bắt buộc hiểu đúng)
- Anh **chơi mọi kỳ, lâu dài**. Một luật chỉ cần **đúng ở phần lớn các kỳ và ổn định**; sai vài kỳ chỉ thua đúng vài kỳ đó, còn những kỳ đúng thì pool gọn, vé tập trung → lợi lâu dài lớn. Ví dụ gốc: bỏ số vắng lâu — dù nó có về thì chỉ thua 1–2 kỳ.
- Mốc tiềm năng: **đúng ≥70% số kỳ** ("10 kỳ đúng 7 là ok"); mạnh khi ≥85%.
- **Không so với bốc ngẫu nhiên / bỏ bừa.** Chấm luật bằng chính nó: % kỳ đúng, độ ổn định giữa các đoạn, xu hướng gần đây. Phương pháp phải có quy luật, cơ sở, suy luận và **cố định cách tính qua các kỳ**.
- Cột **"vé giữ lại"** (phần vé còn lại sau khi lọc theo luật) chỉ để đo độ thu hẹp; luật có dấu vết thật khi **% đúng ≥ % vé giữ lại**. Nói nhẹ, không gọi là "so ngẫu nhiên".
- **Bộ bi có thể đổi** (Power/Mega quay lồng cầu, bi vật lý; giả thuyết trọng lượng bi) → **ưu tiên 100 kỳ gần nhất**, so với 100 kỳ trước đó để xem ổn định. Loto quay máy tính → không dùng lý thuyết bi.
- **Tâm linh / linh cảm được tôn trọng**: số tâm linh mạnh bị luật loại thì nêu ra để cân nhắc, không loại im lặng.
- Luôn **xác nhận lại ý anh** trước khi kết luận nếu yêu cầu mới; báo kết quả trung thực (luật nào không đứng được thì nói thẳng là bỏ).

## Công cụ (đều chạy tiến: mỗi kỳ chỉ dùng dữ liệu trước kỳ đó)
| Script | Dùng để |
|---|---|
| `python3 build/suyluan.py <game> [--W 100]` | **Mặc định.** Luật loại chấm theo từng kỳ ở W kỳ gần + W kỳ trước (vắng ≥10…30, khó ra, ít ra nhất, ra 2 kỳ liền, quá nóng, lệch bền, các luật gộp), cột Đánh giá ✔/~/✘, hiện trạng (ra ít/nhiều, vắng lâu, lệch bền 4 đoạn 25 kỳ) và **"Áp vào kỳ tới"** (số bị loại theo từng luật). |
| `python3 build/khang_dinh.py <game>` | Khẳng định về kỳ tới (≥1 số của 2 kỳ gần, ≥1 số nóng, chẵn/lẻ, nhỏ/lớn, hàng chục…): % kỳ đúng 3 khúc + vé giữ lại. |
| `python3 build/loai_tru.py <game>` | Tỉ lệ ra của nhóm bị loại so với nhóm còn lại (cấp số), luật loại vé (cấp vé). |
| `python3 build/thu_them.py <game>` | Theo thứ quay, số "đến hạn", cặp số, số cùng thứ tuần trước. |
| `python3 build/loto_dauvet.py` | Riêng Loto: phiên 13h/21h, chuyển kỳ, số May Mắn. |
| `python3 build/goiy.py <game> [--cu]` + biến `GOIY_W`, `GOIY_WT`, `--G` | Đo pool 10/15/20 trước/sau khi thêm luật (TB số trúng, % kỳ ≥1/≥2/≥3). |

Muốn thử ý mới: thêm luật vào `RULES` trong `build/suyluan.py` (hàm `(t, gap, counts) -> tập số bị loại`) hoặc viết script nhỏ cùng khuôn (chạy tiến, chia đoạn, chấm theo từng kỳ).

## Quy trình
1. **Xác nhận ý anh** (1–3 câu): trò nào, loại hay khẳng định, khung kỳ (mặc định 100 gần + 100 trước).
2. Chạy `build/suyluan.py <game>` (+ các script khác nếu cần). Tự nghĩ thêm 2–4 giả thuyết hợp với cách nghĩ của anh và thử luôn.
3. Trình bày:
   - Bảng luật: **% kỳ đúng (100 gần / 100 trước)**, số bị bỏ TB/kỳ, vé giữ lại, đánh giá. Nhấn luật ✔ (đúng ≥85% gần, ≥80% trước, ≥ vé giữ lại).
   - **Không nên loại** gì (luật thất bại, nhóm hay quay lại).
   - **Áp vào kỳ tới**: số cụ thể bị loại / nên giữ; nêu xung đột với lõi vé, với tâm linh mạnh.
   - Đề xuất thay đổi cho skill `power` / `mega` / `loto` (luật, trọng số) + đo pool trước/sau bằng `goiy.py`.
4. **Chỉ áp vào skill gợi ý khi anh đồng ý.** Khi áp: sửa `build/goiy.py` (tín hiệu + `SIGS`, nhãn trong `rows`/`why`), cập nhật SKILL.md của trò đó, chạy lại gợi ý kỳ đang chờ (thay dòng tương ứng trong `build/goiy_log.jsonl`), `build/chup.js` gửi ảnh bảng, `build/assemble.py` → `build/check_page.js` → đăng app cùng URL.
5. Ghi kết quả vào `ghi-chu-quy-luat.md` (mục mới, ngày, script, số liệu, luật dùng/bỏ). Commit + push.

## Đã biết (cập nhật khi có nghiên cứu mới)
- **Mega (100 kỳ, 04/10/2026):** bỏ vắng ≥30 đúng 94% kỳ; bỏ số ra 2 kỳ liền 92%; gộp 2 luật 87%; bỏ vắng ≥20 chỉ 72%; không nên bỏ số khó ra / ít ra nhất / ít ra cả 4 đoạn (chúng hay quay lại); số nhiều ra cả 4 đoạn 25 kỳ (16 31 36) đáng giữ. Khẳng định có dấu vết: ≥1 số của 2 kỳ gần (86–91%), ≥1 số trong 10 số nóng.
- **Power:** số vắng 11–15 kỳ ra nhiều hơn; vắng 6–10 ít hơn; số kỳ cùng thứ tuần trước ít hơn; đà tổng có dấu vết; rải ≥4 hàng chục.
- **Loto:** phiên 13h/21h có tính cách riêng; chuyển kỳ; số vừa ra kỳ trước ít hơn; số vắng lâu không nên loại; số May Mắn cân bằng (chọn vắng lâu).
- Không có dấu vết: cặp số, theo thứ quay, số "đến hạn", đuôi số (Loto), đà tổng (Loto).
