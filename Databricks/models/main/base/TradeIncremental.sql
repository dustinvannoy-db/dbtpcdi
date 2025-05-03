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
    fileNamePattern => "Trade.txt",
    schema => "cdc_flag string, cdc_dsn bigint, t_id bigint, t_dts timestamp, t_st_id string, t_tt_id string, t_is_cash tinyint, t_s_symb string, t_qty int, t_bid_price double, t_ca_id bigint, t_exec_name string, t_trade_price double, t_chrg double, t_comm double, t_tax double"
  )
