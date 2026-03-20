import pandas as pd
import os

# ── Simulated warehouse ops ────────────────────────────────
df = pd.read_csv("data/warehouse_ops.csv", parse_dates=["date"])

df["pick_rate"] = df["items_picked"] / df["hours_worked"]
df["accuracy"] = 1 - (df["errors"] / df["orders_completed"].replace(0, pd.NA))

daily = (
    df.groupby(df["date"].dt.date)
    .agg(
        avg_pick_rate=("pick_rate", "mean"),
        avg_accuracy_pct=("accuracy", lambda x: x.mean() * 100),
        avg_dock_util_pct=("dock_in_use", "mean"),
        total_orders=("orders_completed", "sum"),
        unique_workers=("worker_id", "nunique"),
    )
    .reset_index()
)

daily["avg_dock_util_pct"] *= 100
daily["labor_productivity"] = daily["total_orders"] / daily["unique_workers"]
daily["pick_rate_target"] = 45
daily["accuracy_target"] = 97

shift = (
    df.groupby("shift")
    .agg(
        avg_pick_rate=("pick_rate", "mean"),
        avg_accuracy_pct=("accuracy", lambda x: x.mean() * 100),
        total_orders=("orders_completed", "sum"),
    )
    .reset_index()
)

# ── Kaggle supply chain data ───────────────────────────────
kaggle = pd.read_csv("data/DataCo_Supply_Chain.csv", encoding="latin1")

# Parse dates
kaggle["order_date"] = pd.to_datetime(
    kaggle["order date (DateOrders)"], errors="coerce"
)
kaggle["shipping_date"] = pd.to_datetime(
    kaggle["shipping date (DateOrders)"], errors="coerce"
)

# Lead time = days between order and shipping
kaggle["lead_time_days"] = (kaggle["shipping_date"] - kaggle["order_date"]).dt.days

# Drop negatives and nulls
kaggle = kaggle[kaggle["lead_time_days"] >= 0].dropna(subset=["lead_time_days"])

# KPI 1 — Average lead time by shipping mode
lead_by_mode = (
    kaggle.groupby("Shipping Mode")
    .agg(
        avg_lead_time=("lead_time_days", "mean"),
        total_orders=("Order Id", "count"),
    )
    .reset_index()
    .round(2)
)

# KPI 2 — Average lead time by order type
lead_by_type = (
    kaggle.groupby("Type")
    .agg(
        avg_lead_time=("lead_time_days", "mean"),
        total_orders=("Order Id", "count"),
    )
    .reset_index()
    .round(2)
)

# KPI 3 — Monthly order volume trend
kaggle["year_month"] = kaggle["order_date"].dt.strftime("%Y-%m")
monthly_orders = (
    kaggle.groupby("year_month")
    .agg(
        total_orders=("Order Id", "count"),
        avg_lead_time=("lead_time_days", "mean"),
        total_sales=("Sales", "sum"),
    )
    .reset_index()
    .round(2)
)

# ── Export all files ───────────────────────────────────────
os.makedirs("data", exist_ok=True)
daily.to_csv("data/daily_kpis.csv", index=False)
shift.to_csv("data/shift_kpis.csv", index=False)
lead_by_mode.to_csv("data/lead_by_mode.csv", index=False)
lead_by_type.to_csv("data/lead_by_type.csv", index=False)
monthly_orders.to_csv("data/monthly_orders.csv", index=False)

print("Exported -> data/daily_kpis.csv")
print("Exported -> data/shift_kpis.csv")
print("Exported -> data/lead_by_mode.csv")
print("Exported -> data/lead_by_type.csv")
print("Exported -> data/monthly_orders.csv")
