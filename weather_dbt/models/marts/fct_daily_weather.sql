with stg as (

    select * from {{ ref('stg_weather') }}

),

daily_agg as (

    select
        city_name,
        country_code,
        extracted_date,

        avg(temperature_c)     as avg_temperature_c,
        min(temperature_c)     as min_temperature_c,
        max(temperature_c)     as max_temperature_c,
        avg(feels_like_c)      as avg_feels_like_c,
        avg(humidity_pct)      as avg_humidity_pct,
        avg(wind_speed_ms)     as avg_wind_speed_ms,

        -- Điều kiện thời tiết xuất hiện nhiều nhất trong ngày (DAG chạy @daily nên
        -- thường mỗi ngày chỉ có 1 record, nhưng vẫn xử lý tổng quát phòng khi
        -- lịch chạy được đổi sang nhiều lần/ngày)
        max(weather_main)      as dominant_weather_main,

        count(*)                as observation_count

    from stg
    group by city_name, country_code, extracted_date

)

select
    {{ dbt_utils.generate_surrogate_key(['city_name', 'extracted_date']) }} as daily_weather_id,
    dl.location_id,
    da.city_name,
    da.extracted_date,
    da.avg_temperature_c,
    da.min_temperature_c,
    da.max_temperature_c,
    da.avg_feels_like_c,
    da.avg_humidity_pct,
    da.avg_wind_speed_ms,
    da.dominant_weather_main,
    da.observation_count
from daily_agg da
left join {{ ref('dim_location') }} dl
    on da.city_name = dl.city_name
    and da.country_code = dl.country_code
