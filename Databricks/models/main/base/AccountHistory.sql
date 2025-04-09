{{
    config(
        materialized = 'table'
    )
}}
SELECT
    *,
    1 as batchid
  FROM STREAM read_files(
    "{{ var('tpcdi_directory') }}sf={{ var('benchmark') }}/Batch1",
    format => "csv",
    inferSchema => False,
    header => False,
    sep => "|",
    fileNamePattern => "Account.txt",
    schema => "accountid BIGINT, brokerid BIGINT, customerid BIGINT, accountdesc STRING, taxstatus TINYINT, status STRING"
  )

