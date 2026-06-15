# 1. Chọn hệ điều hành nền tảng có sẵn Python (bản slim cho nhẹ)
FROM python:3.10-slim

# 2. Tạo một thư mục ảo tên là /app bên trong container để làm việc
WORKDIR /app

# 3. Copy danh sách thư viện từ máy bạn vào container và cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy thư mục chứa code (src) vào trong container
COPY src/ ./src/

# 5. Lệnh sẽ được kích hoạt tự động khi container bắt đầu chạy
CMD ["python", "src/pipeline.py"]