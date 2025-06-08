{{
    config(
        materialized = 'view',
        partition_by = 'rectype'
    )
}}

select *, substring(value, 16, 3) rectype, to_date(substring(value, 1, 8), 'yyyyMMdd') AS recdate
FROM text.`{{ var('tpcdi_directory') }}sf={{ var('benchmark') }}/Batch1/FINWIRE[0-9][0-9][0-9][0-9]Q[1-4]`;