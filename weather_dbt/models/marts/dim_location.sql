with stg as (

    select * from {{ ref('stg_weather') }}

),

distinct_locations as (

    select distinct
        city_name,
        country_code
    from stg

)

select
    -- Hiện tại pipeline chỉ theo dõi 1 thành phố (Hanoi), nhưng tạo surrogate key
    -- để model sẵn sàng mở rộng nếu sau này fetch_weather.py hỗ trợ nhiều CITY
    {{ dbt_utils.generate_surrogate_key(['city_name', 'country_code']) }} as location_id,
    city_name,
    country_code
from distinct_locations
