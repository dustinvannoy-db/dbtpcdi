{{
    config(
        materialized = 'view'
    )
}}
select
    *
from
    {{var('stagingcatalog')}}.{{var('stagingschema')}}.customermgmt

