import os
import json
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import urllib.parse

# ==========================================
# 1. CẤU HÌNH KẾT NỐI DATABASE (SỬ DỤNG PYMSSQL)
# ==========================================
SERVER = 'weather-dw:1433' 
DATABASE = 'WeatherDW'
USERNAME = 'sa'
PASSWORD = 'YourStrong!Passw0rd' 

encoded_password = urllib.parse.quote_plus(PASSWORD)

# Sử dụng pymssql để không phụ thuộc vào driver của Linux
connection_string = f"mssql+pymssql://{USERNAME}:{encoded_password}@{SERVER}/{DATABASE}"
engine = create_engine(connection_string)

# ==========================================
# 2. HÀM THỰC THI CHÍNH (ETL - LOAD)
# ==========================================
def load_json_to_sql():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Bắt đầu tiến trình bơm dữ liệu vào SQL Server...")
    
    now = datetime.now()
    # Đường dẫn tuyệt đối chuẩn xác cho môi trường Docker
    dir_path = f"/opt/airflow/data/raw/year={now.year}/month={now.strftime('%m')}/day={now.strftime('%d')}"
    file_path = os.path.join(dir_path, "weather_data.json")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Không tìm thấy file: {file_path}")

    data_list = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data_list.append(json.loads(line.strip()))
                    
        if not data_list:
            print("[-] File JSON rỗng.")
            return
            
        df = pd.DataFrame(data_list)
        
    except Exception as e:
        print(f"[-] Lỗi đọc file JSON: {e}")
        raise
    
    try:
        # Bơm dữ liệu vào SQL Server
        df.to_sql('Weather_Data', con=engine, if_exists='append', index=False)
        print(f"[+] THÀNH CÔNG! Đã bơm {len(df)} dòng vào bảng Weather_Data.")
    except Exception as e:
        print(f"[-] Lỗi Insert Database:\n{e}")
        raise

if __name__ == "__main__":
    load_json_to_sql()