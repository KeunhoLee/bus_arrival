import os
import requests
# URL Decode 하기
import urllib.parse

API_KEY_DECODE = os.environ["API_KEY_DECODE"]
API_KEY_ENCODE = os.environ["API_KEY_DECODE"]
BUS_NO = os.environ["BUS_NO"]

url = f"http://ws.bus.go.kr/api/rest/stationinfo/getStationByUid?serviceKey={API_KEY_ENCODE}&arsld={BUS_NO}&resultType=json" 
res = requests.get(
    url,
)

if res.status_code != 200:
    print("Error:", res.status_code)

else:
    print(res.text)
    #urllib.parse.unquote(res.content[""])