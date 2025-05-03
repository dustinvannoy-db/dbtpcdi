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
    fileNamePattern => "TradeType.txt",
    schema => "tt_id STRING, tt_name STRING, tt_is_sell INT, tt_is_mrkt INT"
  )

