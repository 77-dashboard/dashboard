import json
from datetime import datetime

DATA_FILE = "data.json"

def run_update():
    # 讀取現有備援版本
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        current_data = json.load(f)

    # 模擬抓取公開資料 / 運算條件檢查
    # 規則：檢查合格股票是否達到 5 檔
    qualified_stocks_count = 0  # 模擬資料收集狀態

    if qualified_stocks_count < 5:
        print("資料不足 5 檔，保留原版備援名單，僅刷新資料收集時間。")
        current_data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_data["status"] = "FALLBACK"
    else:
        print("資料充足，重新評分並套用 70% 最強個股 + 30% 平均值公式。")
        # 此處放入評分重新計算邏輯...

    # 寫回 data.json
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(current_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    run_update()