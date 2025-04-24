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
    cookies = {
        'elevisor_for_j2ee_uid': 'b1dp04c4715xs',
        'PCID': 'e11ebd39-0303-549a-19a5-3be7e9970b72-1742542548354',
        'WT_FPC': 'id=2a04e034391bf99be821742446217996:lv=1745383294814:ss=1745383294814',
        'JSESSIONID': 'Wv0zIHhFRuhjD7sjkTMGGkyX1kz6TPn-8QDNDV8F.cpesiwsp02_SE21',
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    response = requests.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 추출할 태그 확인 필요 (개발자 도구 참고)
    content = soup.select_one("div.taxLawContent")  # 실제 구조에 맞게 수정해야 함
    if content:
        summary = content.get_text(strip=True)[:1000]
    else:
        summary = "세법 콘텐츠를 찾을 수 없습니다."

    return jsonify({
        "title": "세법 콘텐츠 요약",
        "summary": summary
    })

if __name__ == "__main__":
    app.run(port=5001)
