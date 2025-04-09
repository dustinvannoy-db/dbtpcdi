{{
    config(
        materialized = 'streaming_table'
    )
}}
select
    *,
    int(substring(_metadata.file_path FROM (position('/Batch', _metadata.file_path) + 6) FOR 1)) batchid
from STREAM read_files(
  "{{ var('tpcdi_directory') }}sf={{ var('benchmark') }}/Batch{2,3}",
    format => "csv",
    inferSchema => False,
    header => False,
    sep => "|",
    fileNamePattern => "HoldingHistory.txt",
    schema => "cdc_flag STRING, cdc_dsn BIGINT, hh_h_t_id INT, hh_t_id INT, hh_before_qty INT, hh_after_qty INT"
  )

