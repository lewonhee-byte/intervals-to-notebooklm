import os
import csv
import requests

API_KEY = os.environ.get("INTERVALS_API_KEY")
ATHLETE_ID = os.environ.get("INTERVALS_ATHLETE_ID")

# 전체 액티비티 싹 가져오는 API
url = f"https://intervals.icu/api/v1/athlete/{ATHLETE_ID}/activities"
response = requests.get(url, auth=("API_KEY", API_KEY))

if response.status_code == 200:
    activities = response.json()
    filename = "intervals_training_log.csv"
    
    if activities and isinstance(activities, list):
        # API가 보내주는 전체 필드 이름을 그대로 CSV 컬럼으로 생성
        headers = list(activities[0].keys())
        
        with open(filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for act in activities:
                writer.writerow(act)
        print(f"Successfully wrote {len(activities)} activities.")
    else:
        print("No activities returned from API.")
else:
    print(f"API Failed: {response.status_code}, {response.text}")
    raise Exception(f"API Error {response.status_code}")
