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
    fileNamePattern => "DailyMarket.txt",
    schema => "cdc_flag STRING, cdc_dsn BIGINT, dm_date DATE, dm_s_symb STRING, dm_close DOUBLE, dm_high DOUBLE, dm_low DOUBLE, dm_vol INT"
  )
