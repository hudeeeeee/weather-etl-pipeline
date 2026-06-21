# 🌤️ Weather ETL Pipeline

Dự án này là một hệ thống đường ống dữ liệu (ELT Pipeline) tự động hóa quá trình trích xuất, tải và biến đổi dữ liệu thời tiết thực tế. Dữ liệu được thu thập từ **OpenWeatherMap API**, điều phối bằng **Apache Airflow**, lưu trữ vào **SQL Server**, và được biến đổi (transform) thành các bảng phân tích bằng **dbt (Data Build Tool)**. Toàn bộ hệ thống được container hóa bằng **Docker** để đảm bảo tính nhất quán và dễ dàng triển khai.

---

## 🚀 Công nghệ sử dụng

| Thành phần | Công nghệ |
|---|---|
| Ngôn ngữ lập trình | Python |
| Điều phối quy trình | Apache Airflow |
| Biến đổi dữ liệu (Transformation) | dbt (Data Build Tool) |
| Cơ sở dữ liệu | SQL Server |
| Nền tảng triển khai | Docker & Docker Compose |
| Nguồn dữ liệu | OpenWeatherMap API |

---

## 🏗️ Kiến trúc hệ thống

- **Extract (Trích xuất):** Kết nối và gọi API từ OpenWeatherMap để lấy dữ liệu thời tiết thô của các khu vực được chỉ định dưới dạng JSON.

- **Load (Tải thô):** Dữ liệu JSON thô được tải trực tiếp vào bảng `raw_weather` trong SQL Server, chưa qua xử lý.

- **Transform (Biến đổi):** **dbt** đảm nhiệm toàn bộ logic biến đổi bằng SQL, được tổ chức theo các lớp:
  - **Staging (`stg_weather`):** Làm sạch dữ liệu, chuẩn hóa định dạng thời gian, chuyển đổi đơn vị nhiệt độ (Kelvin → Celsius), loại bỏ bản ghi trùng lặp.
  - **Marts (`dim_location`, `fct_daily_weather`):** Mô hình hóa dữ liệu theo dạng dimension/fact, tổng hợp chỉ số thời tiết theo ngày cho từng khu vực, phục vụ trực tiếp cho phân tích/báo cáo.
  - **Data Quality Tests:** dbt tests (not_null, unique, accepted_range, relationships) đảm bảo chất lượng dữ liệu xuyên suốt từng lớp transform.
  - **Documentation & Lineage:** Tự động sinh tài liệu và sơ đồ lineage thông qua `dbt docs`.

- **Automate (Tự động hóa):** Apache Airflow chịu trách nhiệm lên lịch (schedule) và giám sát toàn bộ quy trình, bao gồm cả việc gọi `dbt run` và `dbt test` sau khi dữ liệu thô được load.

---

## 📋 Yêu cầu hệ thống

Để chạy dự án này trên máy cá nhân, hệ thống của bạn cần cài đặt sẵn:

- **Docker** và **Docker Compose**
- Tài khoản và **API Key** hợp lệ từ [OpenWeatherMap](https://openweathermap.org/)

---

## 🛠️ Hướng dẫn cài đặt và khởi chạy

### Bước 1: Sao chép kho lưu trữ

```bash
git clone https://github.com/hudeeeeee/weather-etl-pipeline.git
cd weather-etl-pipeline
```

### Bước 2: Thiết lập biến môi trường

Tạo một tệp `.env` ở thư mục gốc của dự án và điền các thông tin sau:

```ini
OPENWEATHER_API_KEY=your_api_key_here
SQL_SERVER_USER=sa
SQL_SERVER_PASSWORD=your_strong_password
DBT_SQLSERVER_USER=sa
DBT_SQLSERVER_PASSWORD=your_strong_password
```

### Bước 3: Khởi chạy hệ thống với Docker

```bash
docker-compose up -d
```

### Bước 4: Truy cập và kích hoạt Pipeline

1. Mở trình duyệt và truy cập `http://localhost:8080`
2. Đăng nhập bằng thông tin tài khoản mặc định trong cấu hình
3. Tìm DAG có tên `weather_etl_dag`, gạt nút sang trạng thái **Unpause/Enable** và **Trigger** chạy lần đầu tiên
4. DAG sẽ tự động: gọi API → load raw data vào SQL Server → chạy `dbt run` và `dbt test` để build các bảng staging/marts

### Bước 5 (tuỳ chọn): Chạy/kiểm tra dbt độc lập

```bash
pip install dbt-core dbt-sqlserver
cd weather_dbt
dbt deps                              # cài package dbt_utils
dbt run                               # build models staging + marts
dbt test                              # chạy data quality tests
dbt docs generate && dbt docs serve   # xem tài liệu & lineage graph
```

---

## 📂 Cấu trúc thư mục

```plaintext
weather-etl-pipeline/
├── dags/               # Mã nguồn Python định nghĩa luồng công việc (Airflow DAGs)
├── src/                # Các script Python xử lý logic Extract, Load (raw)
├── sql/                # Các tệp .sql để khởi tạo schema và bảng raw
├── weather_dbt/        # dbt project xử lý transform (staging, marts, tests, docs)
│   ├── models/
│   │   ├── staging/    # Làm sạch, chuẩn hóa dữ liệu raw_weather
│   │   └── marts/      # dim_location, fct_daily_weather phục vụ phân tích
│   ├── dbt_project.yml
│   └── packages.yml
├── docker-compose.yml  # Tệp cấu hình khởi tạo các container Docker
├── requirements.txt    # Danh sách các thư viện Python cần thiết
└── README.md           # Tài liệu hướng dẫn dự án
```
