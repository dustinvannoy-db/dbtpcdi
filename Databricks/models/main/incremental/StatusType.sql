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
    fileNamePattern => "StatusType.txt",
    schema => "st_id STRING, st_name STRING"
  )
