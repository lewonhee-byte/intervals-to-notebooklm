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

# Intervals.icu 인증 규격: username에 "API_KEY", password에 실제 발급받은 키 값 입력
response = requests.get(url, auth=("API_KEY", API_KEY))

if response.status_code == 200:
    activities = response.json()
    filename = "intervals_training_log.csv"
    headers = ["Date", "Name", "Type", "Moving Time(s)", "Distance(m)", "TSS", "NP", "Average Power", "Average HR"]
    
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for act in activities:
            # TSS 키 값이 icu_training_load 또는 icu_load로 들어옴
            tss = act.get("icu_training_load") if act.get("icu_training_load") is not None else act.get("icu_load", 0)
            
            writer.writerow([
                act.get("start_date_local", "")[:10],
                act.get("name", ""),
                act.get("type", ""),
                act.get("moving_time", 0),
                act.get("distance", 0),
                tss,
                act.get("icu_weighted_avg_watts", 0),
                act.get("average_watts", 0),
                act.get("average_heartrate", 0)
            ])
    print("Successfully updated intervals_training_log.csv")
else:
    raise Exception(f"API Error {response.status_code}: {response.text}")
