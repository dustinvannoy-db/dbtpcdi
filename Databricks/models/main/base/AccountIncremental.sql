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
    schema => "cdc_flag string, cdc_dsn bigint, accountid bigint, ca_b_id bigint, ca_c_id bigint, accountDesc string, taxstatus tinyint, ca_st_id string"
  )

