# Phân cụm khách hàng sàn thương mại điện tử

Bài thi giữa kỳ môn **Phân tích và khai phá dữ liệu**, Trường Đại học Công nghệ, ĐHQGHN.

- **Sinh viên:** Phạm Thanh Trung, MSSV 24022476
- **Tham số theo MSSV:** a = 1, b = 2, c = 4, suy ra N = 220 bản ghi, ≥ 10 thuộc tính đầu vào, ≥ 13 bản ghi ngoại lai
- **Báo cáo:** [`reports/Bao_Cao_Ket_Qua.pdf`](reports/Bao_Cao_Ket_Qua.pdf) (mã nguồn LaTeX: `reports/Bao_Cao_Ket_Qua.tex`)

## Kết quả chính

| | Trước xử lý | Sau xử lý |
|---|---|---|
| k (do silhouette chọn) | 2 | 3 |
| Kích thước cụm | 217, 3 | 86, 74, 60 |
| ARI với phân khúc thật | 0,011 | **0,751** |
| ARI ở cùng k = 4 | 0,179 | **0,864** |

Trước xử lý, `avg_order_value` chiếm 98,2% phương sai nên K-Means chỉ cô lập 3 khách siêu VIP. Sau xử lý thu được 3 cụm diễn giải được: săn khuyến mãi, khách mới hoặc ít hoạt động, trung thành giá trị cao. Với k = 4 tách thêm được nhóm VIP (13%).

## Pipeline

```
 data/raw/customers_dirty.csv ─────────────────────────────────────────────┐ (kịch bản "trước xử lý")
          │                                                                │
 [01] Sinh dữ liệu ─► [02] Data Understanding ─► [03] Preprocessing ─► [04] Preparation ─► [05] K-Means
   4 phân khúc ẩn       thống kê, Pearson/         NaN ô bất khả,         log1p, bỏ dư thừa,   so sánh trước/sau,
   nhiễu, ngoại lai,    Spearman, χ², IQR, LOF,    KNN k = 20,            StandardScaler,      ARI, NMI,
   giá trị thiếu        Mann-Whitney               giữ cực trị hợp lý     PCA 5 thành phần     hồ sơ cụm
          │                    │                          │                    │                  │
   customers_dirty     b_outlier_candidates     customers_preprocessed  customers_prepared  cluster_assignments

 customers_clean.csv, injection_log.csv, true_segment: CHỈ dùng để đối chiếu (mục cuối câu b, c) và đánh giá (câu e)
```

Hình pipeline đầy đủ có trong báo cáo (Hình 1).

## Cấu trúc thư mục

```
Midterm_Data_Mining/
├── README.md
├── requirements.txt              # thư viện và phiên bản đã dùng (Python 3.13)
├── data/
│   ├── raw/                      # SẢN PHẨM 2: dữ liệu ban đầu và sau khi thêm nhiễu, ngoại lai
│   │   ├── customers_clean.csv   #   trước khi làm bẩn (chỉ dùng đối chiếu)
│   │   ├── customers_dirty.csv   #   sau khi thêm nhiễu, ngoại lai, giá trị thiếu
│   │   └── injection_log.csv     #   nhật ký từng can thiệp (dòng, cột, loại, giá trị cũ/mới)
│   └── processed/                # SẢN PHẨM 3: dữ liệu sau tiền xử lý và chuẩn bị
│       ├── customers_preprocessed.csv   # câu c: 220 × 13 thuộc tính, thang gốc + cột cờ
│       ├── customers_prepared.csv       # câu d: 220 × 5 thành phần chính (đầu vào K-Means)
│       ├── customers_scaled_numeric.csv # câu d: 8 thuộc tính số đã log + chuẩn hóa (để đối chiếu)
│       └── cluster_assignments.csv      # câu e: nhãn cụm của hai kịch bản
├── notebooks/                    # SẢN PHẨM 4: chạy tuần tự 01 → 05
│   ├── 01_cau_a_sinh_du_lieu.ipynb
│   ├── 02_cau_b_data_understanding.ipynb
│   ├── 03_cau_c_preprocessing.ipynb
│   ├── 04_cau_d_preparation.ipynb
│   └── 05_cau_e_clustering.ipynb
├── src/
│   └── utils.py                  # đường dẫn, lược đồ cột, kiểm tra ràng buộc, IQR
├── reports/                      # SẢN PHẨM 1
│   ├── Bao_Cao_Ket_Qua.pdf       #   báo cáo cuối (7 trang)
│   ├── Bao_Cao_Ket_Qua.tex       #   mã nguồn LaTeX
│   ├── expected_findings.md      #   đặc điểm cài sẵn khi sinh dữ liệu (đối chiếu câu b)
│   ├── figures/                  #   hình câu b, c
│   └── tables/                   #   bảng câu b, c
├── outputs/
│   ├── figures/                  #   hình câu d, e
│   └── tables/                   #   bảng câu d, e
└── ai_logs/                      # SẢN PHẨM 5
    ├── AI_DECLARATION.md         #   khai báo công cụ, phiên làm việc, điểm phản biện
    └── (lịch sử hội thoại export)
```

## Cách chạy lại

```bash
pip install -r requirements.txt
cd notebooks
for nb in 01 02 03 04 05; do
  jupyter nbconvert --to notebook --execute --inplace ${nb}_*.ipynb
done
```

Mỗi notebook tự xác định thư mục gốc. Seed cố định `2476`; chạy lại cho dữ liệu giống hệt từng byte (đã kiểm tra).

Biên dịch báo cáo (cần XeLaTeX; dùng Times New Roman nếu có, nếu không dùng Liberation Serif):

```bash
cd reports && xelatex Bao_Cao_Ket_Qua.tex && xelatex Bao_Cao_Ket_Qua.tex
```

## Nguyên tắc chống rò rỉ

- `customers_clean.csv`, `injection_log.csv`, `expected_findings.md` và cột `true_segment` **chỉ dùng để đối chiếu và đánh giá**: không dùng để điền giá trị (câu c), không dùng để chọn thuộc tính, scaler, PCA hay số cụm (câu d, e).
- Mỗi notebook chỉ đọc kết quả của bước trước; không ghi đè `data/raw/` (trừ notebook 01 sinh ra nó).
