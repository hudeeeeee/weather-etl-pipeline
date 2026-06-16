# 🌤️ Weather ETL Pipeline

Dự án này là một hệ thống đường ống dữ liệu (ETL Pipeline) tự động hóa quá trình trích xuất, biến đổi và tải dữ liệu thời tiết thực tế. Dữ liệu được thu thập từ **OpenWeatherMap API**, xử lý thông qua **Python** và được điều phối bằng **Apache Airflow** trước khi lưu trữ vào **SQL Server**. Toàn bộ hệ thống được container hóa bằng **Docker** để đảm bảo tính nhất quán và dễ dàng triển khai.

---

## 🚀 Công nghệ sử dụng

| Thành phần | Công nghệ |
|---|---|
| Ngôn ngữ lập trình | Python |
| Điều phối quy trình | Apache Airflow |
| Cơ sở dữ liệu | SQL Server |
| Nền tảng triển khai | Docker & Docker Compose |
| Nguồn dữ liệu | OpenWeatherMap API |

---

## 🏗️ Kiến trúc hệ thống

- **Extract (Trích xuất):** Kết nối và gọi API từ OpenWeatherMap để lấy dữ liệu thời tiết thô của các khu vực được chỉ định dưới dạng JSON.

- **Transform (Biến đổi):** Sử dụng các thư viện Python để làm sạch dữ liệu, chuẩn hóa định dạng thời gian, chuyển đổi đơn vị nhiệt độ và trích lọc các trường thông tin cần thiết để phân tích.

- **Load (Tải):** Mở kết nối và chèn dữ liệu đã được làm sạch một cách an toàn vào các bảng tương ứng bên trong SQL Server.

- **Automate (Tự động hóa):** Apache Airflow chịu trách nhiệm lên lịch (schedule) và giám sát quá trình thực thi của toàn bộ quy trình ETL theo các chu kỳ cố định.

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
```

### Bước 3: Khởi chạy hệ thống với Docker

```bash
docker-compose up -d
```

### Bước 4: Truy cập và kích hoạt Pipeline

1. Mở trình duyệt và truy cập `http://localhost:8080`
2. Đăng nhập bằng thông tin tài khoản mặc định trong cấu hình
3. Tìm DAG có tên `weather_etl_dag`, gạt nút sang trạng thái **Unpause/Enable** và **Trigger** chạy lần đầu tiên

---

## 📂 Cấu trúc thư mục

```plaintext
weather-etl-pipeline/
├── dags/               # Mã nguồn Python định nghĩa luồng công việc (Airflow DAGs)
├── src/                # Các script Python xử lý logic Extract, Transform, Load
├── sql/                # Các tệp .sql để khởi tạo schema và bảng dữ liệu
├── docker-compose.yml  # Tệp cấu hình khởi tạo các container Docker
├── requirements.txt    # Danh sách các thư viện Python cần thiết
└── README.md           # Tài liệu hướng dẫn dự án
```