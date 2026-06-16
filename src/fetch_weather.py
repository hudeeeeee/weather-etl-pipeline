import os
import json
import requests
from datetime import datetime

# TODO: Hãy thay thế chuỗi YOUR_API_KEY bằng API Key thực tế của bạn
API_KEY = "50b70c52128b65d5255e89669c7d30c4"
CITY = "Hanoi"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

def fetch_weather_data():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Bắt đầu lấy dữ liệu từ OpenWeatherMap...")
    try:
        response = requests.get(URL)
        response.raise_for_status() # Bắt lỗi nếu gọi API thất bại
        data = response.json()
        
        # Khớp dữ liệu với các cột trong SQL Server
        weather_record = {
            "City": data.get("name"),
            "Country": data.get("sys", {}).get("country"),
            "Temperature": data.get("main", {}).get("temp"),
            "Feels_Like": data.get("main", {}).get("feels_like"),
            "Humidity": data.get("main", {}).get("humidity"),
            "Weather_Main": data["weather"][0]["main"] if data.get("weather") else None,
            "Weather_Desc": data["weather"][0]["description"] if data.get("weather") else None,
            "Wind_Speed": data.get("wind", {}).get("speed"),
            "Extracted_At": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # Dùng ĐƯỜNG DẪN TUYỆT ĐỐI cho Docker
        now = datetime.now()
        dir_path = f"/opt/airflow/data/raw/year={now.year}/month={now.strftime('%m')}/day={now.strftime('%d')}"
        os.makedirs(dir_path, exist_ok=True)
        
        file_path = os.path.join(dir_path, "weather_data.json")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(weather_record, ensure_ascii=False) + '\n')
            
        print(f"[+] Thành công lưu dữ liệu vào Data Lake: {file_path}")
        
    except Exception as e:
        print(f"[-] Lỗi khi kéo dữ liệu API: {e}")
        raise # Đánh bật lỗi ra ngoài để Airflow báo đỏ

if __name__ == "__main__":
    fetch_weather_data()