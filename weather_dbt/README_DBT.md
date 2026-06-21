# dbt Layer cho Weather ETL Pipeline

Bổ sung lớp **transformation** bằng dbt vào DAG `weather_pipeline_v1` hiện có.

## Kiến trúc sau khi thêm dbt

```
OpenWeatherMap API
        │  task: fetch_weather  (src/fetch_weather.py - giữ nguyên)
        ▼
   data/raw/year=.../month=.../day=.../weather_data.json
        │  task: load_to_sql  (src/load_to_sql.py - giữ nguyên)
        ▼
   dbo.Weather_Data  (SQL Server, database WeatherDW)
        │  task MỚI: run_dbt_transform
        ▼
   ┌─────────────────────────────┐
   │  staging.stg_weather         │  clean, chuẩn hoá, dedupe
   │       │                      │
   │       ▼                      │
   │  marts.dim_location          │
   │  marts.fct_daily_weather     │  tổng hợp theo ngày
   └─────────────────────────────┘
```

## Thay đổi cần làm

`src/fetch_weather.py` và `src/load_to_sql.py` **không cần sửa** — dbt đọc thẳng
từ bảng `Weather_Data` mà 2 script này đang ghi vào, không cần đổi schema.

Chỉ cần thêm 1 task mới vào `dags/weather_dag.py`:

```python
run_dbt_transform = BashOperator(
    task_id='run_dbt_transform',
    bash_command='cd /opt/airflow/weather_dbt && dbt run && dbt test'
)

fetch_weather >> load_to_sql >> run_dbt_transform
```

Thêm vào `requirements.txt` (hoặc Dockerfile nếu Airflow build riêng):

```
dbt-core==1.8.*
dbt-sqlserver==1.8.*
```

Thêm biến môi trường để dbt kết nối SQL Server (đặt trong `.env`, không hardcode
như `load_to_sql.py` đang làm):

```ini
DBT_SQLSERVER_USER=sa
DBT_SQLSERVER_PASSWORD=YourStrong!Passw0rd
```

## Cách chạy thử local

```bash
pip install dbt-core dbt-sqlserver
cd weather_dbt
dbt deps          # cài dbt_utils
dbt run           # build stg_weather, dim_location, fct_daily_weather
dbt test          # chạy data quality tests
dbt docs generate && dbt docs serve   # xem lineage graph
```

## Cấu trúc thư mục

```
weather_dbt/
├── dbt_project.yml
├── packages.yml
├── profiles.yml.example
└── models/
    ├── staging/
    │   ├── _weather_sources.yml   # khai báo bảng dbo.Weather_Data
    │   ├── _stg_weather.yml       # tests cho staging
    │   └── stg_weather.sql        # clean + dedupe theo (city_name, extracted_at)
    └── marts/
        ├── _marts.yml             # tests cho marts
        ├── dim_location.sql       # dimension (city_name, country_code)
        └── fct_daily_weather.sql  # fact tổng hợp theo ngày
```

## Lưu ý quan trọng từ code hiện tại

- Bảng `Weather_Data` chỉ đang lưu 1 thành phố (`CITY = "Hanoi"` hardcode trong
  `fetch_weather.py`). Model `dim_location` vẫn được thiết kế tổng quát để sẵn
  sàng mở rộng nếu sau này bạn cho `fetch_weather.py` chạy với nhiều thành phố.
- `Temperature`/`Feels_Like` trong `Weather_Data` đã là Celsius (do gọi API với
  `units=metric`), nên `stg_weather.sql` **không** trừ 273.15 như bản nháp trước —
  nếu trừ sẽ làm sai dữ liệu.
- `Extracted_At` được lưu dạng string, dbt cast lại thành `datetime`/`date` để
  group theo ngày trong `fct_daily_weather`.

## Cập nhật mô tả project (CV / README chính)

> **Technologies Used:** Python (Pandas, requests, pymssql), SQL Server, Apache Airflow,
> **dbt (Data Build Tool)**, Docker, OpenWeatherMap API.
>
> **Key Features:**
> - **Data Transformation:** Implemented a dbt transformation layer (staging → marts)
>   on top of the existing Airflow-orchestrated extract/load pipeline, replacing
>   ad-hoc downstream processing with version-controlled, testable SQL models.
> - **Data Quality:** Added automated dbt tests (not_null, accepted ranges, unique
>   combinations, referential integrity) to validate data before it reaches reporting tables.
> - **Documentation & Lineage:** Generated auto-documentation and lineage graphs via `dbt docs`.
