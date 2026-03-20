CREATE OR REPLACE VIEW vw_pick_rate AS
SELECT
  event_time::DATE                                             AS report_date,
  worker_id, shift,
  SUM(items_picked)                                           AS total_items,
  SUM(hours_worked)                                           AS total_hours,
  ROUND(SUM(items_picked) / NULLIF(SUM(hours_worked),0), 2)  AS pick_rate
FROM fact_warehouse_ops
GROUP BY 1,2,3;

CREATE OR REPLACE VIEW vw_order_accuracy AS
SELECT
  event_time::DATE                                            AS report_date,
  worker_id,
  SUM(orders_completed)                                       AS total_orders,
  SUM(errors)                                                 AS total_errors,
  ROUND(100.0 * (SUM(orders_completed) - SUM(errors))
        / NULLIF(SUM(orders_completed),0), 2)                AS accuracy_pct
FROM fact_warehouse_ops
GROUP BY 1,2;

CREATE OR REPLACE VIEW vw_dock_utilization AS
SELECT
  event_time::DATE                                            AS report_date,
  dock_id,
  ROUND(100.0 * AVG(dock_in_use::INT), 2)                   AS utilization_pct
FROM fact_warehouse_ops
GROUP BY 1,2;

CREATE OR REPLACE VIEW vw_labor_productivity AS
SELECT
  event_time::DATE                                            AS report_date,
  worker_id,
  SUM(orders_completed)                                       AS orders_per_worker
FROM fact_warehouse_ops
GROUP BY 1,2;
