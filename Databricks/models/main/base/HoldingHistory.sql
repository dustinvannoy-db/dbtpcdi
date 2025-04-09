{{
    config(
        materialized = 'table'
    )
}}
select
    *,
    1 batchid
from STREAM read_files(
  "{{ var('tpcdi_directory') }}sf={{ var('benchmark') }}/Batch1",
    format => "csv",
    inferSchema => False,
    header => False,
    sep => "|",
    fileNamePattern => "HoldingHistory.txt",
    schema => "hh_h_t_id INT, hh_t_id INT, hh_before_qty INT, hh_after_qty INT"
  )

