{{
    config(
        materialized = 'streaming_table'
    )
}}
SELECT
    *,
    int(substring(_metadata.file_path FROM (position('/Batch', _metadata.file_path) + 6) FOR 1)) batchid
  FROM STREAM read_files(
    "{{ var('tpcdi_directory') }}sf={{ var('benchmark') }}/Batch{2,3}",
    format => "csv",
    inferSchema => False,
    header => False,
    sep => "|",
    fileNamePattern => "Account.txt",
    schema => "cdc_flag STRING, cdc_dsn BIGINT, accountid BIGINT, brokerid BIGINT, customerid BIGINT, accountdesc STRING, taxstatus TINYINT, status STRING"
  )

