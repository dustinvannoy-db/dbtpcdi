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
    fileNamePattern => "Trade.txt",
    schema => "tradeid BIGINT, t_dts TIMESTAMP, status STRING, t_tt_id STRING, cashflag TINYINT, t_s_symb STRING, quantity INT, bidprice DOUBLE, t_ca_id BIGINT, executedby STRING, tradeprice DOUBLE, fee DOUBLE, commission DOUBLE, tax DOUBLE"
  )
