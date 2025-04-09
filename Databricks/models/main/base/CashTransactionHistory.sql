{{
    config(
        materialized = 'table'
    )
}}
SELECT
    *,
    1 as batchid
FROM read_files(
    "{{ var('tpcdi_directory') }}sf={{ var('benchmark') }}/Batch1",
    format => "csv",
    inferSchema => False,
    header => False,
    sep => "|",
    fileNamePattern => "CashTransaction.txt",
    schema => "accountid BIGINT, ct_dts TIMESTAMP, ct_amt DOUBLE, ct_name STRING"
  )
