{{
    config(
        materialized = 'table'
    )
}}
SELECT
    *
FROM read_files(
    "{{ var('tpcdi_directory') }}sf={{ var('benchmark') }}/Batch1",
    format => "csv",
    inferSchema => False,
    header => False,
    sep => "|",
    fileNamePattern => "CashTransaction.txt",
    schema => "ct_ca_id bigint, ct_dts timestamp, ct_amt double, ct_name string"
  )
