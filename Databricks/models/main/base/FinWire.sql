{{
    config(
        materialized = 'view',
        partition_by = 'rectype'
    )
}}

select *, substring(value, 16, 3) rectype from 
FROM text.`{{ var('tpcdi_directory') }}sf={{ var('benchmark') }}/Batch1/FINWIRE[0-9][0-9][0-9][0-9]Q[1-4]`;