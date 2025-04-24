# taxlaw_proxy.py
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def home():
    return "Tax Law Proxy API is running."

@app.route("/taxlaw/summary", methods=["GET"])
def get_taxlaw_summary():
    url = "https://taxlaw.nts.go.kr/is/USEISA003M.do"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 실제 HTML 구조에 맞게 selector 수정 필요
    content = soup.select_one("body")  # 임시 선택자
    if content:
        summary = content.get_text(strip=True)[:1000]
    else:
        summary = "세법 콘텐츠를 찾을 수 없습니다."

    return jsonify({
        "title": "세법 콘텐츠 요약",
        "summary": summary
    })
