{{
    config(
        materialized = 'streaming_table'
    )
}}

select
    *
from STREAM read_files(
  "{{ var('tpcdi_directory') }}sf={{ var('benchmark') }}/Batch*",
    format => "csv",
    inferSchema => False,
    header => False,
    sep => ",",
    fileNamePattern => "HR.csv",
    schema => 'employeeid string, managerid string, employeefirstname string, employeelastname string, employeemi string, employeejobcode string, employeebranch string, employeeoffice string, employeephone string'
)