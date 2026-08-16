import os
import csv
import requests
from datetime import datetime, timedelta

API_KEY = os.environ.get("INTERVALS_API_KEY")
ATHLETE_ID = os.environ.get("INTERVALS_ATHLETE_ID")

# 최근 90일간 데이터 추출
oldest = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
newest = datetime.now().strftime("%Y-%m-%d")

# Intervals.icu API 호출 (Basic Auth: username="API_KEY", password=발급받은 키)
url = f"https://intervals.icu/api/v1/athlete/{ATHLETE_ID}/activities?oldest={oldest}&newest={newest}"
response = requests.get(url, auth=("API_KEY", API_KEY))

if response.status_code == 200:
    activities = response.json()
    filename = "intervals_training_log.csv"
    headers = ["Date", "Name", "Type", "Moving Time(s)", "Distance(m)", "TSS", "NP", "Average Power", "Average HR"]
    
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for act in activities:
            if not isinstance(act, dict):
                continue
            
            # TSS / Load 필드 매핑
            tss = act.get("icu_training_load")
            if tss is None or tss == 0:
                tss = act.get("icu_load", 0)
                
            writer.writerow([
                str(act.get("start_date_local", ""))[:10],
                act.get("name", "Workout"),
                act.get("type", "Ride"),
                act.get("moving_time", 0),
                act.get("distance", 0),
                tss,
                act.get("icu_weighted_avg_watts", 0),
                act.get("average_watts", 0),
                act.get("average_heartrate", 0)
            ])
    print("Successfully generated intervals_training_log.csv")
else:
    print(f"API Error {response.status_code}: {response.text}")
    raise Exception(f"API Request Failed with status {response.status_code}")
