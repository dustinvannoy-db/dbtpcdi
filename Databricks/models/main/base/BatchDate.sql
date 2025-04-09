{{
    config(
        materialized = 'streaming_table'
    )
}}

select
    *,
    int(substring(_metadata.file_path FROM (position('/Batch', _metadata.file_path) + 6) FOR 1)) batchid
from STREAM read_files(
  "{{ var('tpcdi_directory') }}sf={{ var('benchmark') }}/Batch*",
  format => "csv",
  inferSchema => False, 
  header => False,
  sep => "|",
  fileNamePattern => "BatchDate.txt", 
  schema => "batchdate DATE"
)

