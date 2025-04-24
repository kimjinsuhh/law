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
    # ✅ 소득세 관련 법령 고정 URL
    url = "https://taxlaw.nts.go.kr/law/read/read.do?articleKey=1001000001"  # 이 값은 실제 소득세 관련 문서 URL로 바꾸세요

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # ✅ 실제 페이지 구조 확인 후 태그 선택자 수정 필요
    content = soup.select_one("div#contentsArea")  # 또는 div.lawDetail, div#content 등 개발자도구(F12)로 확인 필요
    summary = content.get_text(strip=True)[:1000] if content else "소득세 콘텐츠를 찾을 수 없습니다."

    return jsonify({
        "title": "소득세 요약",
        "summary": summary
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
