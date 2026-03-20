# DAX Measures - Warehouse Operations Dashboard

## Pick Rate
Pick Rate = DIVIDE(SUM(warehouse_ops[items_picked]), SUM(warehouse_ops[hours_worked]), 0)

## Order Accuracy %
Order Accuracy % = DIVIDE(SUM(warehouse_ops[orders_completed]) - SUM(warehouse_ops[errors]), SUM(warehouse_ops[orders_completed]), 0) * 100

## Dock Utilization %
Dock Utilization % = AVERAGE(warehouse_ops[dock_in_use]) * 100

## Labor Productivity
Labor Productivity = DIVIDE(SUM(warehouse_ops[orders_completed]), DISTINCTCOUNT(warehouse_ops[worker_id]), 0)

## Avg Lead Time (days)
Avg Lead Time = AVERAGE(monthly_orders[avg_lead_time])

## Total Supply Chain Orders
Total SC Orders = SUM(monthly_orders[total_orders])

## Total Sales
Total Sales = SUM(monthly_orders[total_sales])
