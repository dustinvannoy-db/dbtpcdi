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
    fileNamePattern => "Industry.txt",
    schema => "in_id STRING, in_name STRING, in_sc_id STRING"
  )

