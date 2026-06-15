import os
import json
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import urllib.parse

# ==========================================
# 1. CẤU HÌNH KẾT NỐI DATABASE
# ==========================================
SERVER = '127.0.0.1:1433'
DATABASE = 'WeatherDW'
USERNAME = 'sa'
PASSWORD = 'Strong@Passw0rd2026!'

# Mã hóa mật khẩu để xử lý an toàn các ký tự đặc biệt (ví dụ: @, !)
encoded_password = urllib.parse.quote_plus(PASSWORD)

# Khởi tạo Engine kết nối (Sử dụng Driver 17 chuẩn và bật tính năng tăng tốc Insert)
connection_string = f"mssql+pyodbc://{USERNAME}:{encoded_password}@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(connection_string, fast_executemany=True)

# ==========================================
# 2. HÀM THỰC THI CHÍNH (ETL - LOAD)
# ==========================================
def load_json_to_sql():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Bắt đầu tiến trình bơm dữ liệu vào SQL Server...")
    
    # Định vị thư mục Data Lake của ngày hôm nay
    now = datetime.now()
    dir_path = f"data/raw/year={now.year}/month={now.strftime('%m')}/day={now.strftime('%d')}"
    file_path = os.path.join(dir_path, "weather_data.json")
    
    # Kiểm tra xem file có tồn tại không
    if not os.path.exists(file_path):
        print(f"[-] Lỗi: Không tìm thấy file dữ liệu tại {file_path}")
        print("    Vui lòng chạy luồng thu thập dữ liệu (pipeline.py) trước khi bơm.")
        return

    # Đọc dữ liệu từ file JSON Lines
    data_list = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():  # Bỏ qua các dòng trống nếu có
                    data_list.append(json.loads(line.strip()))
                    
        if not data_list:
            print("[-] Thông báo: File JSON rỗng, không có dữ liệu để xử lý.")
            return
            
        df = pd.DataFrame(data_list)
        print(f"[+] Đã trích xuất thành công {len(df)} dòng dữ liệu từ Data Lake.")
        
    except Exception as e:
        print(f"[-] Lỗi trong quá trình đọc file JSON: {e}")
        return
    
    # Bơm dữ liệu DataFrame thẳng vào SQL Server
    try:
        df.to_sql('Weather_Data', con=engine, if_exists='append', index=False)
        print(f"[+] [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] THÀNH CÔNG! Đã bơm {len(df)} dòng vào bảng Weather_Data.")
    except Exception as e:
        print(f"[-] Lỗi nghiêm trọng khi Insert vào Database:\n{e}")

# Kích hoạt chạy script
if __name__ == "__main__":
    load_json_to_sql()