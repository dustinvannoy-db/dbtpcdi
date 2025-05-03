{{
    config(
        materialized = 'table'
    )
}}
select
    *
FROM read_files(
    "{{ var('tpcdi_directory') }}sf={{ var('benchmark') }}/Batch1",
    format => "csv",
    inferSchema => False,
    header => False,
    sep => "|",
    fileNamePattern => "TaxRate.txt",
    schema => "tx_id STRING, tx_name STRING, tx_rate FLOAT"
  )
