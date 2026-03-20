import pandas as pd

df = pd.read_csv('data/warehouse_ops.csv', parse_dates=['date'])

# Derived columns
df['pick_rate']  = df['items_picked'] / df['hours_worked']
df['accuracy']   = 1 - (df['errors'] / df['orders_completed'].replace(0, pd.NA))

# Daily aggregation
daily = df.groupby(df['date'].dt.date).agg(
    avg_pick_rate     = ('pick_rate',         'mean'),
    avg_accuracy_pct  = ('accuracy',          lambda x: x.mean() * 100),
    avg_dock_util_pct = ('dock_in_use',       'mean'),
    total_orders      = ('orders_completed',  'sum'),
    unique_workers    = ('worker_id',          'nunique'),
).reset_index()

daily['avg_dock_util_pct'] *= 100
daily['labor_productivity'] = (
    daily['total_orders'] / daily['unique_workers']
)

# Shift-level breakdown
shift = df.groupby('shift').agg(
    avg_pick_rate    = ('pick_rate',  'mean'),
    avg_accuracy_pct = ('accuracy',  lambda x: x.mean() * 100),
    total_orders     = ('orders_completed', 'sum'),
).reset_index()

daily.to_csv('data/daily_kpis.csv', index=False)
shift.to_csv('data/shift_kpis.csv', index=False)
print("Exported daily_kpis.csv and shift_kpis.csv")
