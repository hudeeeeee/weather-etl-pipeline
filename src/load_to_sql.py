import os
import json
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import urllib.parse

# ==========================================
# 1. CẤU HÌNH KẾT NỐI DATABASE
# ==========================================
# SỬA LỖI 1: Gọi đúng tên container SQL Server thay vì 127.0.0.1
SERVER = 'weather-dw:1433' 
DATABASE = 'WeatherDW'
USERNAME = 'sa'

# LƯU Ý: Phải đảm bảo mật khẩu này giống y hệt mật khẩu trong file docker-compose.yml
PASSWORD = 'YourStrong!Passw0rd' 

encoded_password = urllib.parse.quote_plus(PASSWORD)
connection_string = f"mssql+pyodbc://{USERNAME}:{encoded_password}@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(connection_string, fast_executemany=True)

# ==========================================
# 2. HÀM THỰC THI CHÍNH (ETL - LOAD)
# ==========================================
def load_json_to_sql():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Bắt đầu tiến trình bơm dữ liệu vào SQL Server...")
    
    now = datetime.now()
    dir_path = f"data/raw/year={now.year}/month={now.strftime('%m')}/day={now.strftime('%d')}"
    file_path = os.path.join(dir_path, "weather_data.json")
    
    if not os.path.exists(file_path):
        print(f"[-] Lỗi: Không tìm thấy file dữ liệu tại {file_path}")
        raise FileNotFoundError(f"Không tìm thấy file: {file_path}") # SỬA LỖI 2: Đánh bật lỗi cho Airflow

    data_list = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data_list.append(json.loads(line.strip()))
                    
        if not data_list:
            print("[-] Thông báo: File JSON rỗng.")
            return
            
        df = pd.DataFrame(data_list)
        print(f"[+] Đã trích xuất thành công {len(df)} dòng dữ liệu từ Data Lake.")
        
    except Exception as e:
        print(f"[-] Lỗi trong quá trình đọc file JSON: {e}")
        raise # SỬA LỖI 2: Đánh bật lỗi cho Airflow
    
    try:
        df.to_sql('Weather_Data', con=engine, if_exists='append', index=False)
        print(f"[+] [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] THÀNH CÔNG! Đã bơm {len(df)} dòng vào bảng Weather_Data.")
    except Exception as e:
        print(f"[-] Lỗi nghiêm trọng khi Insert vào Database:\n{e}")
        raise # SỬA LỖI 2: Đánh bật lỗi cho Airflow để báo màu đỏ

if __name__ == "__main__":
    load_json_to_sql()