# taxlaw_proxy.py
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import os

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

    content = soup.select_one("body")
    summary = content.get_text(strip=True)[:1000] if content else "세법 콘텐츠를 찾을 수 없습니다."

    return jsonify({
        "title": "세법 콘텐츠 요약",
        "summary": summary
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
