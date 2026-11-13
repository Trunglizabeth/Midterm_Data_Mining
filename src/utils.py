"""Hàm và hằng số dùng chung cho các notebook câu b-e.

Dùng trong notebook:
    import sys; sys.path.append("../src")
    from utils import *
"""
from pathlib import Path

import numpy as np
import pandas as pd

# ---- Đường dẫn -------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"
for _p in (PROCESSED, FIGURES):
    _p.mkdir(parents=True, exist_ok=True)

SEED = 2476

# ---- Lược đồ dữ liệu -------------------------------------------------------
ID_COL = "customer_id"
LABEL_COL = "true_segment"          # chỉ dùng để đánh giá, KHÔNG làm đặc trưng

NUM_COLS = ["age", "tenure_months", "annual_income", "orders_per_year", "avg_order_value",
            "days_since_last_purchase", "return_rate", "discount_usage_rate", "sessions_per_month"]
NOMINAL_COLS = ["gender", "region", "preferred_category"]
ORDINAL_COLS = {"membership_tier": ["Bronze", "Silver", "Gold", "Platinum"]}
INPUT_COLS = ["age", "gender", "region", "membership_tier", "tenure_months", "annual_income",
              "orders_per_year", "avg_order_value", "days_since_last_purchase", "return_rate",
              "discount_usage_rate", "sessions_per_month", "preferred_category"]


def load_raw(name="customers_dirty"):
    """Đọc một file trong data/raw (customers_dirty, customers_clean, injection_log)."""
    return pd.read_csv(RAW / f"{name}.csv")


def check_constraints(df):
    """Đếm số dòng vi phạm từng ràng buộc miền giá trị và ràng buộc logic.

    Giá trị thiếu không bị tính là vi phạm.
    """
    def bad(cond, *cols):
        return (cond & df[list(cols)].notna().all(axis=1)).sum()

    return pd.Series({
        "age ngoai [18,70]": bad(~df.age.between(18, 70), "age"),
        "ty le ngoai [0,1]": bad(~df.return_rate.between(0, 1) | ~df.discount_usage_rate.between(0, 1),
                                 "return_rate", "discount_usage_rate"),
        "AOV <= 0": bad(df.avg_order_value <= 0, "avg_order_value"),
        "income <= 0": bad(df.annual_income <= 0, "annual_income"),
        "orders < 1": bad(df.orders_per_year < 1, "orders_per_year"),
        "sessions < 0": bad(df.sessions_per_month < 0, "sessions_per_month"),
        "recency ngoai [0,365]": bad(~df.days_since_last_purchase.between(0, 365), "days_since_last_purchase"),
        "tenure > (age-16)*12": bad(df.tenure_months > (df.age - 16) * 12, "tenure_months", "age"),
    })


def iqr_bounds(x, k=1.5):
    """Ngưỡng dưới, ngưỡng trên theo quy tắc k × IQR (bỏ qua giá trị thiếu)."""
    q1, q3 = pd.Series(x, dtype=float).quantile([0.25, 0.75])
    r = q3 - q1
    return q1 - k * r, q3 + k * r


def iqr_flags(df, cols=NUM_COLS, k=1.5):
    """Bảng True/False: ô nào nằm ngoài ngưỡng IQR."""
    out = pd.DataFrame(False, index=df.index, columns=cols)
    for col in cols:
        lo, hi = iqr_bounds(df[col], k)
        x = df[col].astype(float)
        out[col] = (x < lo) | (x > hi)
    return out


def savefig(fig, name):
    """Lưu hình vào reports/figures với độ phân giải đủ cho báo cáo."""
    fig.savefig(FIGURES / name, dpi=150, bbox_inches="tight")
