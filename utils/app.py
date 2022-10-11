# -*- coding: utf-8 -*-
"""
服務主入口
"""
from pathlib import Path
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import Optional
from fastapi import (
    FastAPI, APIRouter, Request, HTTPException
)
from fastapi.responses import JSONResponse, HTMLResponse 
from utils.data import getProduct
from prometheus_client import Counter, Summary

app = FastAPI()


## 路徑問題
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

## Prometheus 監測數據
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
REQUEST_COUNT = Counter('request_count', 'Total webapp request count')
LATENCY = Summary('request_processing_latency_seconds', 'Time for a request')


router = APIRouter()
def reply_response(
    code: int, desc: str, result: Optional[dict] = None):
    msg = {
        'Result':result,
        'Status': {
            'Code': code,
            'Desc':desc
        }
    } 
    return msg

@REQUEST_TIME.time()
@LATENCY.time()
@router.get(f'/pageList', response_class=JSONResponse)
async def pageList(request: Request):
    try:
        data = getProduct()
        msg = reply_response(
            result = data,
            code = 200,
            desc = '呼叫成功'
        )
        return JSONResponse(status_code=200, content=msg)
    except:
        msg = reply_response(
            result = None,
            code = 400,
            desc='呼叫失敗'
        )
        return JSONResponse(status_code=400, content=msg)

#跳轉至畫面
@router.get(f"/page", response_class=HTMLResponse)
async def userpage(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})