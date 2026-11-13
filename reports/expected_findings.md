# Các phát hiện kỳ vọng (đo trên dữ liệu sạch, seed = 2476)

| # | Đặc điểm cài sẵn | Giá trị đo được | Công cụ kiểm tra ở câu b |
|---|---|---|---|
| 1 | annual_income lệch phải | mean 270.6 > median 210.8; skewness 1.59 | describe, histogram, boxplot |
| 2 | avg_order_value lệch phải | mean 592.2 > median 407.8; skewness 2.27 | describe, histogram, boxplot |
| 3 | income và AOV tuyến tính trong không gian log | Pearson thang gốc 0.827; Pearson log-log 0.820; Spearman 0.760 | Pearson trước và sau log, Spearman |
| 4 | orders và recency quan hệ nghịch, phi tuyến | Pearson -0.510; Spearman -0.661 | So sánh Pearson với Spearman, scatter |
| 5 | orders và sessions dư thừa | Pearson 0.871; Spearman 0.902 | Ma trận tương quan |
| 6 | preferred_category phụ thuộc phân khúc | chi2 = 53.1, df = 12, p = 3.90e-07 | Kiểm định chi bình phương |
| 7 | gender độc lập với phân khúc | chi2 = 0.73, df = 3, p = 0.867 | Kiểm định chi bình phương |
| 8 | region được sinh độc lập với phân khúc | chi2 = 13.42, df = 6, p = 0.037; p < 0,05 dù sinh độc lập: liên hệ giả do ngẫu nhiên khi N nhỏ, không được diễn giải là có quan hệ thật | Kiểm định chi bình phương |
| 9 | annual_income thiếu theo cơ chế MAR (đo trên dữ liệu bẩn) | median tenure: nhóm thiếu 7.0 tháng, nhóm không thiếu 24.0 tháng; Mann-Whitney p = 1.78e-03; tỷ lệ thiếu theo phân khúc {'DealHunter': 0.071, 'Loyal': 0.017, 'NewInactive': 0.233, 'VIP': 0.067} | So sánh phân phối tenure giữa hai nhóm |
| 10 | Ngoại lai logic không bị IQR đơn biến phát hiện | IQR bắt 0/3 logic; 5/5 lỗi đơn biến; 7/7 hợp lệ; 50/205 dòng bình thường bị gắn cờ | IQR so với kiểm tra ràng buộc |

Xem trước tác động của dữ liệu bẩn lên tương quan (Pearson; Spearman):

- income và AOV: sạch (0.827; 0.760), bẩn (0.972; 0.771)
- orders và sessions: sạch (0.871; 0.902), bẩn (0.290; 0.879)
