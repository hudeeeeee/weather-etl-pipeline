import os
import requests
import json
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv

# Tải các biến môi trường (API Key) từ file .env bí mật
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = "Hanoi"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

def extract_weather_data():
    """Step 1: Extract data from public API"""
    print(f"[{datetime.now()}] Starting extraction for {CITY}...")
    try:
        response = requests.get(URL)
        response.raise_for_status() # Báo lỗi nếu API gặp sự cố
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Extraction failed: {e}")
        return None

def transform_weather_data(raw_data):
    """Step 2: Transform and flatten JSON data"""
    if not raw_data:
        return None
    
    print(f"[{datetime.now()}] Transforming data...")
    transformed = {
        "city": raw_data.get("name"),
        "country": raw_data.get("sys", {}).get("country"),
        "temperature": raw_data.get("main", {}).get("temp"),
        "feels_like": raw_data.get("main", {}).get("feels_like"),
        "humidity": raw_data.get("main", {}).get("humidity"),
        "weather_main": raw_data.get("weather", [{}])[0].get("main"),
        "weather_desc": raw_data.get("weather", [{}])[0].get("description"),
        "wind_speed": raw_data.get("wind", {}).get("speed"),
        "extracted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return transformed

def load_to_lake(clean_data):
    """Step 3: Load structured data into partitioned Data Lake"""
    if not clean_data:
        print("No data to load.")
        return
    
    print(f"[{datetime.now()}] Loading data to Data Lake...")
    
    # Tổ chức Data Lake phân cấp theo Thời gian
    now = datetime.now()
    dir_path = f"data/raw/year={now.year}/month={now.strftime('%m')}/day={now.strftime('%d')}"
    os.makedirs(dir_path, exist_ok=True)
    
    # Lưu file dạng JSON
    file_path = os.path.join(dir_path, "weather_data.json")
    
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(clean_data, ensure_ascii=False) + "\n")
        
    print(f"Successfully loaded data into: {file_path}")

if __name__ == "__main__":
    # Chạy luồng ETL
    raw_payload = extract_weather_data()
    if raw_payload:
        clean_payload = transform_weather_data(raw_payload)
        load_to_lake(clean_payload)