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
    fileNamePattern => "Date.txt",
    schema => "sk_dateid bigint, datevalue date, datedesc string, calendaryearid int, calendaryeardesc string, calendarqtrid int, calendarqtrdesc string, calendarmonthid int, calendarmonthdesc string, calendarweekid int, calendarweekdesc string, dayofweeknum int, dayofweekdesc string, fiscalyearid int, fiscalyeardesc string, fiscalqtrid int, fiscalqtrdesc string, holidayflag boolean"
  )
    
