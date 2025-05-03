{{
    config(
        materialized = 'table'
    )
}}
select
    *,
    1 as batchid
from read_files(
  "{{ var('tpcdi_directory') }}sf={{ var('benchmark') }}/Batch1",
    format => "csv",
    inferSchema => False,
    header => False,
    sep => "|",
    fileNamePattern => "TradeHistory.txt",
    schema => "th_t_id bigint, th_dts timestamp, th_st_id string"
  )
