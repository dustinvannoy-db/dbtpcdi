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
    fileNamePattern => "Time.txt",
    schema => "sk_timeid bigint, timevalue string, hourid int, hourdesc string, minuteid int, minutedesc int, secondid int, seconddesc int, markethoursflag boolean, officehoursflag boolean"
  )
