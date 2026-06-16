<<<<<<< HEAD
🌤️ Weather ETL Pipeline
Dự án này là một hệ thống đường ống dữ liệu (ETL Pipeline) tự động hóa quá trình trích xuất, biến đổi và tải dữ liệu thời tiết thực tế. Dữ liệu được thu thập từ OpenWeatherMap API, xử lý thông qua Python và được điều phối bằng Apache Airflow trước khi lưu trữ vào hệ quản trị cơ sở dữ liệu SQL Server. Toàn bộ hệ thống được container hóa bằng Docker để đảm bảo tính nhất quán và dễ dàng triển khai.
=======

                                            Weather ETL Pipeline

                                                            
>>>>>>> 29b8511d0c6b730a859889348c4b5ec938911f87

🚀 Công nghệ sử dụng
Ngôn ngữ lập trình: Python

<<<<<<< HEAD
Điều phối quy trình (Orchestration): Apache Airflow
=======

1. Tổng quan dự án
Đây là hệ thống trích xuất, chuyển đổi và tải (ETL) dữ liệu thời tiết tự động. Hệ thống thu thập dữ liệu thời tiết theo thời gian thực từ API (như OpenWeatherMap), xử lý các thông số kỹ thuật và lưu trữ vào [Tên cơ sở dữ liệu/kho lưu trữ] để phục vụ phân tích dữ liệu hoặc các ứng dụng dự báo.
>>>>>>> 29b8511d0c6b730a859889348c4b5ec938911f87

Cơ sở dữ liệu lưu trữ: SQL Server

Nền tảng triển khai: Docker & Docker Compose

Nguồn dữ liệu: OpenWeatherMap API

🏗️ Kiến trúc hệ thống
Extract (Trích xuất): Kết nối và gọi API từ OpenWeatherMap để lấy dữ liệu thời tiết thô của các khu vực được chỉ định dưới dạng JSON.

Transform (Biến đổi): Sử dụng các thư viện Python để làm sạch dữ liệu, chuẩn hóa định dạng thời gian, chuyển đổi đơn vị nhiệt độ và trích lọc các trường thông tin cần thiết nhất để phân tích.

Load (Tải): Mở kết nối và chèn dữ liệu đã được làm sạch một cách an toàn vào các bảng tương ứng bên trong SQL Server.

Automate (Tự động hóa): Apache Airflow chịu trách nhiệm lên lịch (schedule) và giám sát quá trình thực thi của toàn bộ quy trình ETL này theo các chu kỳ cố định.

📋 Yêu cầu hệ thống
Để chạy dự án này trên máy cá nhân, hệ thống của bạn cần cài đặt sẵn:

Docker và Docker Compose.

Tài khoản và API Key hợp lệ từ OpenWeatherMap.

🛠️ Hướng dẫn cài đặt và khởi chạy
Bước 1: Sao chép kho lưu trữ (Clone repository)

Bash
git clone https://github.com/hudeeeeee/weather-etl-pipeline.git
cd weather-etl-pipeline
Bước 2: Thiết lập biến môi trường
Tạo một tệp .env ở thư mục gốc của dự án và cung cấp các thông tin cấu hình, mật khẩu và API key của bạn:

Ini, TOML
OPENWEATHER_API_KEY=your_api_key_here
SQL_SERVER_USER=sa
SQL_SERVER_PASSWORD=your_strong_password
Bước 3: Khởi chạy hệ thống với Docker
Sử dụng Docker Compose để build và khởi động tất cả các dịch vụ (Airflow, SQL Server):

Bash
docker-compose up -d
Bước 4: Truy cập và kích hoạt Pipeline

Mở trình duyệt web và truy cập vào giao diện quản lý của Airflow (thông thường là http://localhost:8080).

Đăng nhập bằng thông tin tài khoản mặc định được định nghĩa trong cấu hình.

Tìm DAG có tên weather_etl_dag, gạt nút chuyển đổi sang trạng thái Unpause/Enable và kích hoạt (Trigger) chạy lần đầu tiên.

📂 Cấu trúc thư mục dự kiến
Plaintext
weather-etl-pipeline/
├── dags/                  # Chứa mã nguồn Python định nghĩa luồng công việc (Airflow DAGs)
├── src/                   # Các script Python xử lý logic Extract, Transform và Load
├── sql/                   # Chứa các tệp .sql để khởi tạo schema và bảng dữ liệu
├── docker-compose.yml     # Tệp cấu hình để khởi tạo các container Docker
├── requirements.txt       # Danh sách các thư viện Python (packages) cần thiết
└── README.md              # Tài liệu hướng dẫn dự án
