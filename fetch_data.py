import os
import csv
import requests
from datetime import datetime, timedelta

API_KEY = os.environ.get("INTERVALS_API_KEY")
ATHLETE_ID = os.environ.get("INTERVALS_ATHLETE_ID")

oldest = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
newest = datetime.now().strftime("%Y-%m-%d")

# 캘린더/활동 상세 데이터를 전부 받아오는 API 엔드포인트
url = f"https://intervals.icu/api/v1/athlete/{ATHLETE_ID}/events?oldest={oldest}&newest={newest}"

response = requests.get(url, auth=("API_KEY", API_KEY))

if response.status_code == 200:
    events = response.json()
    filename = "intervals_training_log.csv"
    headers = ["Date", "Name", "Type", "Moving Time(s)", "Distance(m)", "TSS", "NP", "Average Power", "Average HR"]
    
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for item in events:
            # 실체 라이딩/운동(Activity) 데이터만 추출
            if item.get("type") in ["WORKOUT", "NOTE"]:
                continue
                
            writer.writerow([
                str(item.get("start_date_local", ""))[:10],
                item.get("name", "Ride"),
                item.get("type", "Ride"),
                item.get("moving_time", 0),
                item.get("distance", 0),
                item.get("icu_training_load", item.get("load", 0)),
                item.get("icu_weighted_avg_watts", 0),
                item.get("average_watts", 0),
                item.get("average_heartrate", 0)
            ])
    print("Successfully generated intervals_training_log.csv")
else:
    print(f"API Error {response.status_code}: {response.text}")
    raise Exception(f"API Request Failed with status {response.status_code}")
