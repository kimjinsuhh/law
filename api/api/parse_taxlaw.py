from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "✅ API is alive and ready!"}

@app.get("/api/parse-taxlaw")
async def parse_taxlaw(
    ntstTlawClCd: str,
    ntstSysClCd: str,
    ntstBscId: str,
    ntstTextUqno: str,
    ntstEnfrDt: str
):
    return {
        "message": "파라미터 정상 수신",
        "params": {
            "ntstTlawClCd": ntstTlawClCd,
            "ntstSysClCd": ntstSysClCd,
            "ntstBscId": ntstBscId,
            "ntstTextUqno": ntstTextUqno,
            "ntstEnfrDt": ntstEnfrDt
        }
    }
