---
name: suyluan
description: Suy luận dấu vết Vietlott (power / mega / loto) từ dữ liệu quá khứ — tìm luật LOẠI số, luật khẳng định, tín hiệu cộng/trừ điểm; chấm theo từng kỳ, ưu tiên 100 kỳ gần, kiểm độ ổn định; đề xuất đưa vào skill power/mega/loto. Dùng khi anh nói "suy luận", "suyluan", "tìm dấu vết", "kiểm tra kĩ mega/power/loto", "có cách nào loại/thu hẹp", "có bổ sung suy luận gì không".
---

# suyluan — suy luận dấu vết

Xưng hô: gọi người dùng là **anh**, tự xưng **em**, trả lời tiếng Việt, ngắn gọn, dùng bảng.

## Cách anh nghĩ (bắt buộc hiểu đúng)
- **Dấu vết = xác suất NGHIÊNG, không phải đúng 100% (anh nhắc nhiều lần, 05/10/2026).** Một cách luận số chỉ cần làm tỉ lệ ra lệch khỏi bình thường một cách ỔN ĐỊNH (dù chỉ 1–3 điểm %) là dấu vết, dùng được để nhích xác suất / gọn pool. Khi báo: ✔ = nghiêng ổn định (cả các khung) · ~ = có nghiêng nhưng chưa ổn định / ít mẫu → theo dõi · ✘ = không nghiêng (ngang bình thường). TUYỆT ĐỐI không bác một cách vì "không đúng 100%" hay "chỉ nhích nhẹ"; nhích nhẹ ổn định = có giá trị, cho trọng số nhỏ thay vì bỏ.
- **Chơi bền, không chơi ăn ngay (anh, 04/10/2026):** không đổi luật/pool theo kết quả 1 kỳ; có kỳ trúng kỳ trật là bình thường. Khi có kết quả: chấm sổ và báo; chỉ đề xuất sửa luật khi số liệu cộng dồn nhiều kỳ (sổ kiểm chứng) cho thấy luật yếu đi, và phải kiểm trên 100–200 kỳ trước.
- **Cốt lõi (anh, 04/10/2026):** luật loại được chấm trên CHUỖI kỳ dài, không phán theo 1 kỳ. Số "lâu lâu mới ra" có ra 1 kỳ thì chỉ thua kỳ đó; sau đó nó lại vắng theo nhịp cũ → các kỳ sau vẫn loại đúng → cộng dồn vẫn thắng. Không bỏ luật vì 1 kỳ sai; chỉ xem lại khi tỉ lệ cộng dồn trong sổ kiểm chứng tụt dần nhiều kỳ (tính cách số đổi / bộ bi đổi).
- Anh **chơi mọi kỳ, lâu dài**. Một luật chỉ cần **đúng ở phần lớn các kỳ và ổn định**; sai vài kỳ chỉ thua đúng vài kỳ đó, còn những kỳ đúng thì pool gọn, vé tập trung → lợi lâu dài lớn. Ví dụ gốc: bỏ số vắng lâu — dù nó có về thì chỉ thua 1–2 kỳ.
- Mốc tiềm năng: **đúng ≥70% số kỳ** ("10 kỳ đúng 7 là ok"); mạnh khi ≥85%.
- **Không so với bốc ngẫu nhiên / bỏ bừa.** Chấm luật bằng chính nó: % kỳ đúng, độ ổn định giữa các đoạn, xu hướng gần đây. Phương pháp phải có quy luật, cơ sở, suy luận và **cố định cách tính qua các kỳ**.
- Cột **"vé giữ lại"** (phần vé còn lại sau khi lọc theo luật) chỉ để đo độ thu hẹp; luật có dấu vết thật khi **% đúng ≥ % vé giữ lại**. Nói nhẹ, không gọi là "so ngẫu nhiên".
- **Bộ bi có thể đổi** (Power/Mega quay lồng cầu, bi vật lý; giả thuyết trọng lượng bi) → **ưu tiên 100 kỳ gần nhất**, so với 100 kỳ trước đó để xem ổn định. Loto quay máy tính → không dùng lý thuyết bi.
- **Tâm linh / linh cảm được tôn trọng**: số tâm linh mạnh bị luật loại thì nêu ra để cân nhắc, không loại im lặng.
- Luôn **xác nhận lại ý anh** trước khi kết luận nếu yêu cầu mới; báo kết quả trung thực (luật nào không đứng được thì nói thẳng là bỏ).

## Bắt đầu: HỎI GAME TRƯỚC
Việc đầu tiên khi chạy skill: dùng AskUserQuestion hỏi **áp dụng cho game nào** (Power 6/55 · Mega 6/45 · Loto 5/35; cho chọn nhiều nếu anh muốn). **Chọn xong mới chạy tiếp.** Nếu anh đã nói rõ game trong câu lệnh thì xác nhận lại 1 câu rồi chạy.

## 3 mục tiêu (luôn làm đủ, mỗi lần tự tìm thêm suy luận mới — xem hiệu quả có đáng đánh đổi không)
1. **Thu hẹp pool toàn dãy** gọn nhất có thể mà vẫn an toàn trên phần lớn kỳ (luật loại số, khẳng định, tín hiệu cộng/trừ điểm). Kiểm quá khứ để chứng minh.
2. **Thu hẹp pool từng vị trí** u, v, w, x, y, z (dãy xếp tăng dần): khoảng cho từng vị trí, loại trừ được số nào ở vị trí nào; % kỳ đúng từng vị trí và đúng CẢ dãy.
3. **Hình dạng dãy**: to/nhỏ, chẵn/lẻ, tổng, cặp liền nhau, hàng chục, độ trải, khe lớn nhất, AC, cùng đuôi… → tự nghiên cứu, gộp thành **khuôn tối ưu** (đúng nhiều kỳ, vé giữ lại ít).
Với mỗi mục: đưa con số "đánh đổi" — % kỳ đúng (an toàn) đổi lấy bao nhiêu thu hẹp (số bị bỏ / vé giữ lại). Đề xuất mức em thấy đáng nhất.

## Tự nghĩ thêm (bắt buộc mỗi lần chạy)
Ngoài các luật có sẵn, tự đặt câu hỏi theo kiểu anh hay nghĩ và thử luôn:
- **Nhịp riêng từng số** (khoảng cách giữa các lần ra của CHÍNH số đó; ra – vắng k – ra; chu kỳ đều) → kỳ nào nó hay "nghỉ"?
- **Nhịp của nhóm** (hàng chục, chẵn/lẻ, đuôi) theo kỳ; số vắng/nóng theo từng vị trí u…z.
- Mỗi suy luận: đổi thành luật cố định, đo **% kỳ đúng** (số bỏ ít thì mới đúng nhiều kỳ) và **tỉ lệ ra của nhóm bị bỏ so với các số còn lại** — đây mới là phần "lợi" thật; loại 1 số bất kỳ vốn đã đúng ~86–89% kỳ.

## Tìm ý mới từ suy luận dãy số nói chung (không riêng xổ số)
Được phép (và nên) mượn các cách tìm quy luật / "ẩn số x" của dãy số tổng quát, rồi **kiểm bằng dữ liệu quá khứ, chấm theo từng kỳ** trước khi tin:
- Sai phân bậc 1–2 (dãy hiệu), tìm công thức truy hồi / hồi quy tuyến tính theo kỳ trước (tự hồi quy AR), trung bình trượt, hồi về trung bình.
- Chuỗi Markov / ma trận chuyển (giá trị hoặc trạng thái kỳ này → kỳ sau), đếm theo đồng dư (mod 2, 3, 5, 9, 10…), chữ số, tổng chữ số.
- Chu kỳ / tuần hoàn: tự tương quan, phổ tần (FFT), khoảng lặp; phát hiện đổi chế độ (CUSUM, so 2 đoạn); kiểm loạt (runs test), entropy.
- Cấu trúc tổ hợp: AC (số hiệu khác nhau), khe giữa các số, độ trải, cặp/bộ ba hay đi cùng, đối xứng (n ↔ N+1−n).
Mỗi ý mới: viết luật cố định → chạy tiến trên 100 kỳ gần + 100 kỳ trước → giữ nếu đứng được, bỏ nếu không (nói thẳng).

## Công cụ (đều chạy tiến: mỗi kỳ chỉ dùng dữ liệu trước kỳ đó)
| Script | Dùng để |
|---|---|
| `python3 build/suyluan.py <game> [--W 100]` | **Mặc định.** Luật loại chấm theo từng kỳ ở W kỳ gần + W kỳ trước (vắng ≥10…30, khó ra, ít ra nhất, ra 2 kỳ liền, quá nóng, lệch bền, các luật gộp), cột Đánh giá ✔/~/✘, hiện trạng (ra ít/nhiều, vắng lâu, lệch bền 4 đoạn 25 kỳ) và **"Áp vào kỳ tới"** (số bị loại theo từng luật). |
| `python3 build/vitri.py <game> [--W 100] [--q 85]` | **Mục tiêu 2.** Khoảng từng vị trí u…z (A: theo giá trị, B: theo chênh lệch so với kỳ trước): % kỳ đúng từng vị trí, đúng CẢ dãy, vé giữ lại, khoảng áp kỳ tới. Đổi `--q` để cân an toàn ↔ gọn. |
| `python3 build/hinhdang.py <game> [--W 100] [--q 85] [--floor 60]` | **Mục tiêu 3.** Từng đặc trưng hình dạng + gộp tham lam thành khuôn (mỗi bước giảm vé giữ lại nhiều nhất mà % kỳ đúng gộp ≥ floor). In khuôn áp kỳ tới. (~10 giây) |
| `python3 build/loai_nho.py <game> [--W 100]` | **Luật loại nhỏ kiểu "bỏ số vắng lâu"** (mỗi kỳ bỏ ~1 số có lý do): vắng lâu nhất/nhì, ra 2 kỳ liền, ra 3 lần/5 kỳ, ra kỳ trước & t−3, tái xuất, ra ít/nhiều nhất 100 kỳ, u/z kỳ trước… 3 đoạn 100 kỳ + vé giữ lại + số bị loại kỳ tới. Thêm luật vào `RULES`. |
| `python3 build/nhip.py <game> [--W 200]` | **Nhịp riêng từng số** (ý anh: số ra kỳ 1, 5, 9… thì kỳ 2, 3, 6, 7, 8 loại đúng): theo lịch sử của chính số đó, ở đúng số kỳ đang vắng hiện tại nó đã gặp ≥m lần mà tỉ lệ ra ≤ ngưỡng → loại. Báo % kỳ đúng, số bỏ/kỳ, tỉ lệ ra nhóm bỏ vs còn lại. |
| `python3 build/nhip_min.py <game>` | **Nhịp tối thiểu từng số**: luôn nghỉ ≥x kỳ giữa 2 lần ra (cửa sổ 100/200 kỳ) mà hiện mới nghỉ <x → loại. |
| `python3 build/thu_hep.py <game> [--min 60]` | **Gộp luật loại để thu hẹp pool** (dùng mọi luật trong `theodoi.RULES`): thêm dần luật ít "tốn" an toàn nhất trên mỗi số bỏ thêm; mỗi bước: bỏ TB/kỳ, pool còn, % kỳ không mất số (100 gần / 100 trước), số trúng mất/kỳ, số bị bỏ kỳ tới. |
| `python3 build/dauvet_may.py` | Dấu vết máy (Loto) khung 100/200 kỳ: lặp theo độ trễ k=1..14, số nhiều/ít giữ sang kỳ kế, vị trí dính kỳ trước, tính cách phiên/thứ. |
| `python3 build/phien.py` | Loto: tách phiên 13h / 21h thành 2 dãy riêng, khung 100/200 kỳ của chính phiên: lặp theo ngày, nóng/lạnh, loại vắng ≥10/15/20 trong phiên, pool nóng cùng phiên, MM. |
| `python3 build/phien2.py` | Loto theo phiên: 13h→21h cùng ngày, 21h→13h hôm sau, luật loại/tái xuất/vắng tính trong phiên, hồi về trung vị theo phiên. |
| `python3 build/soicau.py <game>` | Các cách "luận số / soi cầu" trên mạng: cầu vị trí (chạy k ngày), cầu Pascal, lô kép, lô rơi, lô gan, đầu/đuôi câm. |
| `python3 build/khia_canh.py <game> [--W 100]` | Khía cạnh mới: nhóm số (lộn, chạm tổng, ±2, t−2/t−3, nguyên tố, chia 3, cùng vị trí, tái xuất, hàng chục…) 3 đoạn; hồi về trung vị (tổng, lẻ, u, z, số nhỏ) có cột vé giữ lại; hình dạng (chia 3, nguyên tố, khe nhỏ nhất, tổng đuôi, mod 9, đối xứng). Thêm ý mới vào `GROUPS` / `FEAT` / `SH`. |
| `python3 build/khang_dinh.py <game>` | Khẳng định về kỳ tới (≥1 số của 2 kỳ gần, ≥1 số nóng, chẵn/lẻ, nhỏ/lớn, hàng chục…): % kỳ đúng 3 khúc + vé giữ lại. |
| `python3 build/loai_tru.py <game>` | Tỉ lệ ra của nhóm bị loại so với nhóm còn lại (cấp số), luật loại vé (cấp vé). |
| `python3 build/thu_them.py <game>` | Theo thứ quay, số "đến hạn", cặp số, số cùng thứ tuần trước. |
| `python3 build/loto_dauvet.py` | Riêng Loto: phiên 13h/21h, chuyển kỳ, số May Mắn. |
| `python3 build/goiy.py <game> [--cu]` + biến `GOIY_W`, `GOIY_WT`, `--G` | Đo pool 10/15/20 trước/sau khi thêm luật (TB số trúng, % kỳ ≥1/≥2/≥3). |

Muốn thử ý mới: thêm luật vào `RULES` trong `build/suyluan.py` (hàm `(t, gap, counts) -> tập số bị loại`) hoặc viết script nhỏ cùng khuôn (chạy tiến, chia đoạn, chấm theo từng kỳ).

## Quy trình
1. **Hỏi game** (AskUserQuestion) → chờ anh chọn. Xác nhận khung kỳ (mặc định 100 gần + 100 trước).
2. Chạy `build/suyluan.py`, `build/vitri.py`, `build/hinhdang.py` cho game đó (+ các script khác nếu cần). Tự nghĩ thêm 2–4 giả thuyết (từ cách nghĩ của anh và từ suy luận dãy số tổng quát) và thử luôn.
3. Trình bày:
   - Theo 3 mục tiêu: (1) pool toàn dãy, (2) pool từng vị trí, (3) khuôn hình dạng — mỗi mục có bảng + "áp kỳ tới".
   - Bảng luật: **% kỳ đúng (100 gần / 100 trước)**, số bị bỏ TB/kỳ, vé giữ lại, đánh giá. Nhấn luật ✔ (đúng ≥85% gần, ≥80% trước, ≥ vé giữ lại).
   - **Không nên loại** gì (luật thất bại, nhóm hay quay lại).
   - **Áp vào kỳ tới**: số cụ thể bị loại / nên giữ; nêu xung đột với lõi vé, với tâm linh mạnh.
   - Đề xuất thay đổi cho skill `power` / `mega` / `loto` (luật, trọng số) + đo pool trước/sau bằng `goiy.py`.
4. **Luật mới nào cũng đưa vào sổ kiểm chứng** (`build/theodoi.py`: thêm vào RULES/CLAIMS, `snap`) để chấm dần từ kỳ tới — kể cả luật chưa áp dụng. **Chỉ áp vào skill gợi ý khi anh đồng ý** (và thêm id vào `APPLIED`). Khi áp: sửa `build/goiy.py` (tín hiệu + `SIGS`, nhãn trong `rows`/`why`), cập nhật SKILL.md của trò đó, chạy lại gợi ý kỳ đang chờ (thay dòng tương ứng trong `build/goiy_log.jsonl`), `build/chup.js` gửi ảnh bảng, `build/assemble.py` → `build/check_page.js` → đăng app cùng URL.
5. Ghi kết quả vào `ghi-chu-quy-luat.md` (mục mới, ngày, script, số liệu, luật dùng/bỏ). Commit + push.

## Đã biết (cập nhật khi có nghiên cứu mới)
- **Mega vị trí/hình dạng (04/10/2026):** khoảng 85% từng vị trí → đúng cả 6 vị trí 59% kỳ (100 gần) / 51% (100 trước), vé giữ lại 49%. Khuôn hình dạng gộp (số nhỏ 2–4, hàng chục 3–4, cặp liền 0–1, số lẻ 2–4): đúng 70% / 64%, vé giữ lại 52%.
- **Mega (100 kỳ, 04/10/2026):** bỏ vắng ≥30 đúng 94% kỳ; bỏ số ra 2 kỳ liền 92%; gộp 2 luật 87%; bỏ vắng ≥20 chỉ 72%; không nên bỏ số khó ra / ít ra nhất / ít ra cả 4 đoạn (chúng hay quay lại); số nhiều ra cả 4 đoạn 25 kỳ (16 31 36) đáng giữ. Khẳng định có dấu vết: ≥1 số của 2 kỳ gần (86–91%), ≥1 số trong 10 số nóng.
- **Power:** số vắng 11–15 kỳ ra nhiều hơn; vắng 6–10 ít hơn; số kỳ cùng thứ tuần trước ít hơn; đà tổng có dấu vết; rải ≥4 hàng chục.
- **Loto:** phiên 13h/21h có tính cách riêng; chuyển kỳ; số vừa ra kỳ trước ít hơn; số vắng lâu không nên loại; số May Mắn cân bằng (chọn vắng lâu).
- **Khía cạnh mới (04/10):** Mega số kỳ t−3 ra ít (3/3), hồi về trung vị của tổng (77/76/71% vs vé giữ 69%), tổng mod 9 (theo dõi); Power tổng mod 9 (theo dõi); Loto số "tái xuất" ra ít (3/3) → loại, hồi về trung vị số nhỏ. Bẫy: "hồi về trung vị" phải tính kỳ bằng nhau là sai + luôn so vé giữ lại.
- **Loto 2 phiên ngược nhau (05/10):** 13h "lạnh giữ lạnh" (vắng ≥20 trong phiên và tái xuất trong phiên đều ra ít → loại); 21h "cân bằng" (vắng lâu & tái xuất trong phiên ra nhiều → giữ).
- Không có dấu vết: số lộn, chạm tổng, cách ±2, nguyên tố/chia 3 (nhóm số), cùng vị trí ±1, cặp số, theo thứ quay, số "đến hạn", đuôi số (Loto), đà tổng (Loto).
