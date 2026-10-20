import os
from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup

# トレンドを取得するURL（Twittrendの「世界/ワールド」または「日本」）
# ※世界全体のトレンドを取りたい場合は https://twitrend.jp/world/ を指定
URL = "https://twitrend.jp/"


def get_trends():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
    }
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # 現在日時（日本時間）を取得
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    trends = []
    # トレンドの要素を取得（TwittrendのHTML構造に合わせて抽出）
    for item in soup.select(".trend-card .keyword"):
        word = item.get_text(strip=True)
        if word:
            trends.append({"datetime": now, "keyword": word})

    return trends


def save_to_csv(trends):
    csv_file = "trend_log.csv"
    new_df = pd.DataFrame(trends)

    if os.path.exists(csv_file):
        # 既存のCSVがあれば追記
        existing_df = pd.read_csv(csv_file)
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        updated_df.to_csv(csv_file, index=False, encoding="utf-8-sig")
    else:
        # 新しくCSVを作成
        new_df.to_csv(csv_file, index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    trend_data = get_trends()
    if trend_data:
        save_to_csv(trend_data)
        print(f"成功: {len(trend_data)} 件のトレンドをログ化しました。")
    else:
        print("トレンドの取得に失敗しました。")
