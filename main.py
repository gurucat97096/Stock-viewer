from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import yfinance as yf
import os
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def format_date(value):
    try:
        if isinstance(value, (int, float)) and value > 1000000000:
            return datetime.fromtimestamp(value).strftime('%Y年%m月%d日')
        elif isinstance(value, datetime):
            return value.strftime('%Y年%m月%d日')
        return value
    except:
        return value

def get_stock_info(code: str):
    try:
        stock = yf.Ticker(f"{code}.TW")
        info = stock.info
        price = stock.fast_info.get("lastPrice", "N/A")
        return {
            "名稱": info.get("longName", "N/A"),
            "代碼": code,
            "當前價格": f"{price} 元",
            "產業": info.get("sector", "N/A"),
            "市值": info.get("marketCap", "N/A"),
            "本益比": info.get("trailingPE", "N/A"),
            "股息殖利率": f"{round(info.get('dividendYield', 0) * 100, 2)}%" if info.get("dividendYield") else "N/A",
            "除息日": format_date(info.get("exDividendDate"))
        }
    except Exception as e:
        return {"錯誤": str(e)}

@app.get("/", response_class=HTMLResponse)
def home(request: Request, code: str = Query(default="")):
    info = get_stock_info(code) if code else None
    return templates.TemplateResponse("stock.html", {"request": request, "query": code, "info": info})
