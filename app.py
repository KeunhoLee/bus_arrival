from flask import Flask, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    # 매 요청 시 현재 시각을 반환
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"remain_time_min": 5})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)