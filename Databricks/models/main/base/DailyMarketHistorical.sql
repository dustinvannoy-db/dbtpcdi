{{
    config(
        materialized = 'streaming_table'
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
    fileNamePattern => "DailyMarket.txt",
    schema => "dm_date DATE, dm_s_symb STRING, dm_close DOUBLE, dm_high DOUBLE, dm_low DOUBLE, dm_vol INT"
  )
