# Khai báo sử dụng AI và công cụ

**Sinh viên:** Phạm Thanh Trung, MSSV 24022476

## 1. Công cụ đã dùng

| Công cụ | Phiên bản / mô hình | Mục đích |
|---|---|---|
| Claude (claude.ai) | Claude Opus 5.5, một đoạn dùng Claude Fable 5.2 | Phân tích đề, đề xuất thiết kế, viết và chạy code, rà soát kết quả |
| Python + Jupyter | Xem `requirements.txt` | Sinh dữ liệu, phân tích, phân cụm |
| *(bổ sung nếu dùng thêm)* | | |

## 2. Các phiên làm việc

| Phiên | Thời gian | Nội dung chính | File export |
|---|---|---|---|
| 1 | 13/11/2026, từ 10:28 | Phân tích đề; tính tham số; thiết kế thuộc tính và cơ chế sinh; làm câu a; tổ chức thư mục; làm câu b | *(điền tên file export)* |

## 3. Những chỗ sinh viên phản biện, điều chỉnh đề xuất của AI

*(Sinh viên tự điền. Gợi ý từ phiên 1:)*

- Yêu cầu AI giải thích lý do chọn từng phân phối và tính phù hợp với bài toán; sau đó AI tự sửa Poisson thành Negative Binomial và cho recency phụ thuộc tần suất mua.
- Chọn giữ `gender` (AI đề xuất bỏ) để có phép thử về thuộc tính không mang cấu trúc cụm.
- Chọn sửa dòng có sẵn để giữ N = 220; giữ tỷ lệ phân khúc 30/70/60/60, kèm điều kiện kiểm chứng ảnh hưởng ở câu e.
- Yêu cầu thêm nhiễu riêng cho recency để không dư thừa hoàn toàn với số đơn.
- Đưa giáo trình *Data understanding* vào để AI căn chỉnh thiết kế theo nội dung đã học.
- Chất vấn rủi ro AI thiên vị khi vừa sinh dữ liệu vừa phân tích; yêu cầu làm câu b đầy đủ, có LOF và Mann-Whitney.

## 4. Những chỗ AI tự phát hiện và sửa khi kiểm chứng

- Ngoại lai logic ban đầu (recency = 300 ngày) vượt ngưỡng IQR, trái ý đồ "IQR không bắt được"; đã sửa thành 180 ngày và thêm `assert`.
- Tương quan income và AOV đo được (0,82) cao hơn ước tính ban đầu (≈ 0,6); đã ghi nhận.
- `region` cho p = 0,037 dù được sinh độc lập; giữ nguyên, ghi chú là liên hệ giả do N nhỏ.

- Câu b: ràng buộc "≥ 50 đơn nhưng ≥ 120 ngày chưa mua" ban đầu được xếp là bất khả; khi đối chiếu thấy nó gắn cờ nhầm một khách thật đang rời bỏ (C0091), nên đã hạ thành ràng buộc mềm ("đáng ngờ").
- Câu b: giả thuyết "LOF bắt được ngoại lai logic" sai (0/3); kết luận MAR của income không đạt ý nghĩa sau hiệu chỉnh Holm. Cả hai được ghi lại thay vì chỉnh phân tích cho khớp.
- Câu b phát hiện lỗi thiết kế ở câu a: ngoại lai logic C0205 không phân biệt được với hành vi "ngừng mua" mà câu a cố ý sinh ra.

## 5. Cam kết

Sinh viên đã rà soát, chạy lại và chịu trách nhiệm về toàn bộ mã nguồn, dữ liệu và báo cáo.
