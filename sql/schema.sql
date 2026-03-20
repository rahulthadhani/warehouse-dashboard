CREATE TABLE IF NOT EXISTS dim_workers (
    worker_id   VARCHAR(10)  PRIMARY KEY,
    department  VARCHAR(50),
    hire_date   DATE
);

CREATE TABLE IF NOT EXISTS dim_docks (
    dock_id     INT          PRIMARY KEY,
    dock_type   VARCHAR(20),
    capacity    INT
);

CREATE TABLE IF NOT EXISTS fact_warehouse_ops (
    op_id             SERIAL       PRIMARY KEY,
    event_time        TIMESTAMP,
    worker_id         VARCHAR(10)  REFERENCES dim_workers(worker_id),
    dock_id           INT          REFERENCES dim_docks(dock_id),
    shift             VARCHAR(10),
    items_picked      INT,
    hours_worked      NUMERIC(4,2),
    orders_completed  INT,
    errors            INT,
    dock_in_use       SMALLINT     CHECK (dock_in_use IN (0,1))
);
