import json
import os
from datetime import datetime

DATA_FILE = "data.json"

def calculate_and_save():
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 這裡放入你每日抓取的股票名單與營收數據 (範例格式)
    latest_payload = {
        "last_updated": now_str,
        "status": "SUCCESS",
        "status_text": "已更新最新評分",
        "stocks": [
            {"code": "2330", "name": "台積電", "sector": "foundry", "score": 92, "revenue_yoy": 53.3, "status": "公開資料已核實"},
            {"code": "2382", "name": "廣達", "sector": "server", "score": 86, "revenue_yoy": 35.2, "status": "公開資料已核實"},
            {"code": "2344", "name": "華邦電", "sector": "memory", "score": 78, "revenue_yoy": 256.6, "status": "公開資料已核實"},
            {"code": "8299", "name": "群聯", "sector": "memory", "score": 75, "revenue_yoy": 12.4, "status": "公開資料已核實"},
            {"code": "2059", "name": "川湖", "sector": "server", "score": 84, "revenue_yoy": 42.1, "status": "公開資料已核實"}
        ]
    }

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(latest_payload, f, ensure_ascii=False, indent=2)
        
    print(f"[{now_str}] data.json 已成功產出並存檔！")

if __name__ == "__main__":
    calculate_and_save()
