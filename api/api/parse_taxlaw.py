from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from bs4 import BeautifulSoup
import httpx

app = FastAPI()
@app.get("/")
async def root():
    return {"status": "✅ API is alive and running!"}

@app.get("/api/parse-taxlaw")
async def parse_taxlaw(
    ntstTlawClCd: str,
    ntstSysClCd: str,
    ntstBscId: str,
    ntstTextUqno: str,
    ntstEnfrDt: str
):
    url = "https://taxlaw.nts.go.kr/st/USESTA002M.do"
    params = {
        "ntstTlawClCd": ntstTlawClCd,
        "ntstSysClCd": ntstSysClCd,
        "ntstBscId": ntstBscId,
        "ntstTextUqno": ntstTextUqno,
        "ntstEnfrDt": ntstEnfrDt
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

        result = {}
        divs = soup.find_all("div")

        for i in range(len(divs) - 1):
            label = divs[i].get_text(strip=True)
            value = divs[i + 1].get_text(strip=True)
            if any(key in label for key in ["문서번호", "해석내용", "작성일", "적용사례", "제목", "소득세"]):
                result[label] = value

        return result or {"message": "데이터 없음"}

    except httpx.RequestError as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
