import os
import math
import requests

from flask import Flask, render_template, jsonify

BUS_NO = os.environ.get("BUS_NO", "6712")
BUFFER_MIN = 1

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/healthcheck')
def healthcheck():
    # 헬스 체크 엔드포인트
    return jsonify({"status": "ok"}), 200

@app.route('/data')
def data():
    # 매 요청 시 현재 시각을 반환
    url = "https://map.naver.com/p/api/pubtrans/realtime/bus/arrivals?stopId=80198"

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'referer': 'https://map.naver.com/p/entry/bus-station/80198?c=16.00,0,0,0,dh',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        return jsonify({"error": "Failed to fetch data"}), 500
    
    bus_info_list = res.json()
    remaining_time = 0
    remaining_time_next = 0
    for bl in bus_info_list:

        if bl["name"] == BUS_NO:
            arrival_info = bl["arrival"]["buses"]
            if not arrival_info:
                return jsonify({"remain_time_min": "도착정보 없음",
                                "remain_time_next_min": ""})
            
            remaining_time = arrival_info[0]["remainingTime"]/60 - BUFFER_MIN
            print(f"버스 {BUS_NO}의 도착 예상 시간: {math.ceil(remaining_time)} 분")
            if len(arrival_info) > 1:
                remaining_time_next = arrival_info[1]["remainingTime"]/60 - BUFFER_MIN
                print(f"버스 {BUS_NO}의 다음 도착 예상 시간: {math.ceil(remaining_time_next)} 분")
            break

    return jsonify({"remain_time_min": f"{math.ceil(remaining_time)} 분",
                    "remain_time_next_min": f"{math.ceil(remaining_time_next)} 분"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)