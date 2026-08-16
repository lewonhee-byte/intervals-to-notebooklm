import os
import csv
import requests
from datetime import datetime, timedelta

API_KEY = os.environ.get("INTERVALS_API_KEY")
ATHLETE_ID = os.environ.get("INTERVALS_ATHLETE_ID")

# 최근 90일간 데이터 추출
oldest = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
newest = datetime.now().strftime("%Y-%m-%d")

url = f"https://intervals.icu/api/v1/athlete/{ATHLETE_ID}/activities?oldest={oldest}&newest={newest}"

# Intervals.icu 인증: username은 "API_KEY", password는 실제 발급받은 API 키
auth = ("API_KEY", API_KEY)

response = requests.get(url, auth=auth)

if response.status_code == 200:
    activities = response.json()
    filename = "intervals_training_log.csv"
    headers = ["Date", "Name", "Type", "Moving Time(s)", "Distance(m)", "TSS", "NP", "Average Power", "Average HR"]
    
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for act in activities:
            writer.writerow([
                act.get("start_date_local", "")[:10],
                act.get("name", ""),
                act.get("type", ""),
                act.get("moving_time", 0),
                act.get("distance", 0),
                act.get("icu_training_load", act.get("icu_load", 0)),
                act.get("icu_weighted_avg_watts", 0),
                act.get("average_watts", 0),
                act.get("average_heartrate", 0)
            ])
    print("Successfully updated intervals_training_log.csv")
else:
    print(f"Failed to fetch data: {response.status_code}, {response.text}")
