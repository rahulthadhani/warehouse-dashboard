import pandas as pd
import numpy as np
import os

np.random.seed(42)
n = 5000

workers = [f"W{str(i).zfill(3)}" for i in range(1, 51)]

df = pd.DataFrame({
    'date':             pd.date_range('2023-01-01', periods=n, freq='h'),
    'worker_id':        np.random.choice(workers, n),
    'shift':            np.random.choice(['AM', 'PM', 'Night'], n),
    'dock_id':          np.random.randint(1, 9, n),
    'dock_in_use':      np.random.choice([0, 1], n, p=[0.35, 0.65]),
    'items_picked':     np.random.poisson(45, n),
    'hours_worked':     np.random.uniform(0.5, 1.0, n).round(2),
    'orders_completed': np.random.poisson(8, n),
    'errors':           np.random.poisson(0.3, n),
})

os.makedirs('data', exist_ok=True)
df.to_csv('data/warehouse_ops.csv', index=False)
print(f"Generated {len(df)} rows -> data/warehouse_ops.csv")