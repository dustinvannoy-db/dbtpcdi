{{
    config(
        materialized = 'view'
    )
}}
-- NOTE: Need to create the staging table first using code in helpers directory.
select
    *
from
    {{var('stagingcatalog')}}.{{var('stagingschema')}}.customermgmt

