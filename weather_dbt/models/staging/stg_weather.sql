with source as (

    select * from {{ source('weather_dw', 'Weather_Data') }}

),

renamed as (

    select
        trim(City)                                  as city_name,
        upper(trim(Country))                        as country_code,

        -- API được gọi với units=metric nên Temperature/Feels_Like đã sẵn là Celsius
        cast(Temperature as decimal(6,2))            as temperature_c,
        cast(Feels_Like as decimal(6,2))             as feels_like_c,
        cast(Humidity as int)                        as humidity_pct,
        cast(Wind_Speed as decimal(6,2))             as wind_speed_ms,

        lower(trim(Weather_Main))                    as weather_main,
        trim(Weather_Desc)                           as weather_description,

        -- Extracted_At được ghi dưới dạng string '%Y-%m-%d %H:%M:%S' trong fetch_weather.py
        cast(Extracted_At as datetime)                as extracted_at,
        cast(cast(Extracted_At as datetime) as date)  as extracted_date

    from source
    where City is not null
      and Extracted_At is not null

),

deduplicated as (

    -- Phòng trường hợp Airflow retry task fetch_weather/load_to_sql trong cùng khung giờ
    select
        *,
        row_number() over (
            partition by city_name, extracted_at
            order by extracted_at desc
        ) as rn
    from renamed

)

select
    city_name,
    country_code,
    temperature_c,
    feels_like_c,
    humidity_pct,
    wind_speed_ms,
    weather_main,
    weather_description,
    extracted_at,
    extracted_date
from deduplicated
where rn = 1
