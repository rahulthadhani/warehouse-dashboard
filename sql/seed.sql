INSERT INTO dim_docks (dock_id, dock_type, capacity) VALUES
  (1, 'inbound',  4), (2, 'inbound',  4),
  (3, 'inbound',  4), (4, 'inbound',  4),
  (5, 'outbound', 6), (6, 'outbound', 6),
  (7, 'outbound', 6), (8, 'outbound', 6)
ON CONFLICT DO NOTHING;

CREATE TEMP TABLE staging_ops (
  event_time        TIMESTAMP,
  worker_id         VARCHAR(10),
  shift             VARCHAR(10),
  dock_id           INT,
  dock_in_use       SMALLINT,
  items_picked      INT,
  hours_worked      NUMERIC(4,2),
  orders_completed  INT,
  errors            INT
);

\copy staging_ops FROM 'C:/Users/noodl/OneDrive/Desktop/projects/warehouse-dashboard/data/warehouse_ops.csv' DELIMITER ',' CSV HEADER;

INSERT INTO dim_workers (worker_id, department, hire_date)
SELECT DISTINCT
  worker_id,
  'Operations' AS department,
  '2020-01-01'::DATE AS hire_date
FROM staging_ops
ON CONFLICT DO NOTHING;

INSERT INTO fact_warehouse_ops
  (event_time, worker_id, shift, dock_id, dock_in_use, items_picked, hours_worked, orders_completed, errors)
SELECT
  event_time, worker_id, shift, dock_id, dock_in_use, items_picked, hours_worked, orders_completed, errors
FROM staging_ops;
