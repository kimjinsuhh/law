# main.py
from fastapi import FastAPI
from clrwing.py import crawl

app = FastAPI()

@app.get("/crawl-taxlaw")
def crawl_taxlaw(limit: int = 10):
    file_path = crawl(limit=limit)
    return {"file_path": file_path}
