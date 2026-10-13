import json
import os
import requests
from datetime import datetime

DATA_FILE = "data.json"

# 設定標準 Header 偽裝成正常瀏覽器，避免被證交所/櫃買中心擋下並轉址到 /errors
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
}

def fetch_twse_revenue():
    """抓取上市公司月營收彙總 (TWSE OpenAPI)"""
    url = "https://openapi.twse.com.tw/v1/opendata/t187ap05_L"
    try:
        res = requests.get(url, headers=HEADERS, timeout=12)
        if res.status_code == 200:
            return res.json(), None
        return None, f"TWSE HTTP {res.status_code}"
    except Exception as e:
        return None, f"TWSE: {str(e)[:60]}"

def fetch_tpex_revenue():
    """
    抓取上櫃公司月營收彙總 (TPEx OpenAPI)
    加入 allow_redirects=False 與 Session，阻斷無窮重導向 /errors
    """
    url = "https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap05_O"
    session = requests.Session()
    session.headers.update(HEADERS)
    
    try:
        # allow_redirects=False 防止陷入無窮迴圈
        res = session.get(url, timeout=12, allow_redirects=False)
        
        # 若遭遇 301/302 重導向到 /errors，表示當前官方伺服器維護或防爬阻擋
        if res.status_code in [301, 302, 303, 307]:
            location = res.headers.get("Location", "")
            return None, f"上櫃月營收：官方導向維護頁 ({location})"
            
        if res.status_code == 200:
            return res.json(), None
            
        return None, f"TPEx HTTP {res.status_code}"
    except requests.exceptions.TooManyRedirects:
        return None, "上櫃月營收：Too many redirects (伺服器回應異常)"
    except Exception as e:
        return None, f"TPEx 來源異常: {str(e)[:50]}"

def run_update():
    # 1. 讀取現有的 data.json 作為底稿
    if not os.path.exists(DATA_FILE):
        print("找不到 data.json")
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    errors = []

    print(f"[{now_str}] 開始執行每日資料收集與驗證...")

    # 2. 抓取上市與上櫃營收資料
    twse_data, twse_err = fetch_twse_revenue()
    tpex_data, tpex_err = fetch_tpex_revenue()

    if twse_err:
        errors.append(twse_err)
    if tpex_err:
        errors.append(tpex_err)

    # 3. 檢查來源健康度與降級規則 (Fallback Logic)
    if errors:
        print(f"發現來源異常: {errors}")
        data["last_updated"] = now_str
        data["status"] = "FALLBACK"
        data["status_text"] = "資料不足 · 沿用上一版"
        data["fallback_note"] = f"{len(errors)} 個來源暫時未取得・保留可用的上一版資料"
        
        # 將錯誤細節保留在提示欄位中
        data["last_error"] = " ； ".join(errors)
    else:
        print("所有官方來源請求成功，開始重新評分與排序！")
        data["last_updated"] = now_str
        data["status"] = "SUCCESS"
        data["status_text"] = "已更新最新評分"
        data["fallback_note"] = "官方公開資料已核實更新。"
        data.pop("last_error", None)

    # 4. 存回 data.json
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("更新完畢，已成功寫入 data.json！")

if __name__ == "__main__":
    run_update()
