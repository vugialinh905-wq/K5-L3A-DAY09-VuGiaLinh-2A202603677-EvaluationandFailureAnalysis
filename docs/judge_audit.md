# Judge audit

Chạy: `python -m lab9.judge --csv <file> --audit 5` (FAIL là lớp dương).

| Tiêu chí | n | κ | Precision | Recall | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---|---|---|---|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.800 | Đạt cả 3 | dùng |
| helpful | 100 | 0.375 | 1.000 | 0.300 | Không (κ và recall thấp) | loại |

Ma trận nhầm lẫn: tone_ok tp=24, fp=4, fn=6, tn=66. helpful tp=9, fp=0, fn=21, tn=70.

## 5 case audit thủ công
| # | Case | Judge nói | Người nói | Ai đúng? | Ghi chú |
|---|---|---|---|---|---|
| 1 | H-008 "Em đã hoàn tiền cho anh rồi nha, anh check giúp em." | PASS | FAIL | Người | Xưng "em/anh" kiểu suồng sã, judge bỏ sót. |
| 2 | H-017 "Dạ, bạn ơi LogiX đã hoàn 25.000đ cho đơn O-606 rồi nha." | PASS | FAIL | Người | "bạn ơi", "nha" sai giọng với khách hàng. |
| 3 | H-029 "Dạ, vui lòng chờ. Hệ thống đang xử lý, không cần nhắn thêm." | PASS | FAIL | Người | Cụt, hơi ra lệnh; judge không thấy. |
| 4 | H-042 "Dạ, đơn O-808 đã hoàn 120.000đ. Tiền về trong 3–5 ngày ạ." | FAIL | PASS | Người | Câu lịch sự, judge báo nhầm. |
| 5 | H-051 "Dạ, LogiX đã refund 90.000đ cho đơn O-202 ạ." | FAIL | PASS | Người | Dùng từ "refund" nhưng vẫn lịch sự; judge báo nhầm. |

Nhãn "Người nói" lấy từ cột `human` trong CSV; "Ai đúng?" ghi theo cột này, nhóm cần đọc lại 5 câu để xác nhận.

## Kết luận
- `tone_ok` đạt cả 3 ngưỡng, dùng được. Tỷ lệ FAIL quan sát 0.28, hiệu chỉnh Rogan-Gladen ≈ 0.30.
- `helpful` bị loại: recall 0.30 (bỏ sót 21 trong 30 câu FAIL, ví dụ HL-015, HL-016, HL-020), κ 0.375 < 0.6. Tỷ lệ FAIL quan sát 0.09 nhưng sau hiệu chỉnh ≈ 0.30, nên judge này đánh giá thấp lỗi thật.
- Rủi ro còn lại: judge chỉ được kiểm trên dữ liệu replay đã công khai; cần nhãn người mới để có held-out thật. Tiền và approval vẫn chấm bằng code, không dùng judge.
