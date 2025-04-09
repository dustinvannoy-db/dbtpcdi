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
    sep => ",",
    fileNamePattern => "Prospect.csv",
    schema => "agencyid STRING, lastname STRING, firstname STRING, middleinitial STRING, gender STRING, addressline1 STRING, addressline2 STRING, postalcode STRING, city STRING, state STRING, country STRING, phone STRING, income STRING, numbercars INT, numberchildren INT, maritalstatus STRING, age INT, creditrating INT, ownorrentflag STRING, employer STRING, numbercreditcards INT, networth INT"
  )