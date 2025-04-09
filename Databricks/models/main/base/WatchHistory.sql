{{
    config(
        materialized = 'table'
    )
}}
select
    *,
    1 as batchid
from STREAM read_files(
  "{{ var('tpcdi_directory') }}sf={{ var('benchmark') }}/Batch1",
      format => "csv",
      inferSchema => False,
      header => False,
      sep => "|",
      fileNamePattern => "WatchHistory.txt",
      schema => "w_c_id BIGINT, w_s_symb STRING, w_dts TIMESTAMP, w_action STRING"
    )
