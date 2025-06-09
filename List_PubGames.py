from google_play_scraper import search, app
import pandas as pd
import time
import sys

def get_app_list(search_term, lang='ja', country='jp', num_results=50):
    """
    Google Playストアから検索ワードに基づくアプリ一覧を取得
    
    Parameters:
    search_term (str): 検索キーワード
    lang (str): 言語 (デフォルト: 'ja')
    country (str): 国 (デフォルト: 'jp')
    num_results (int): 取得するアプリの最大数 (デフォルト: 50)
    
    Returns:
    DataFrame: アプリ情報のリスト
    """
    try:
        # 検索を実行
        results = search(
            search_term,
            lang=lang,      # 言語設定
            country=country, # 国設定
            n_hits=num_results # 結果の最大数
        )
        
        # データを整理
        app_data = []
        for apl in results:

            # リクエスト間隔を設けてレート制限を回避
            time.sleep(0.5)

            # アプリの詳細情報を取得
            app_details = app(apl['appId'], lang=lang, country=country)

            # 必要な情報を抽出
            app_info = {
                'アプリ名': apl['title'],
                'スコア': apl['score'],
                'リリース日': app_details['released'] if 'released' in app_details else 'N/A',
                'url': app_details['url'] if 'url' in app_details else 'N/A',
                '内容': app_details['summary'] if 'summary' in app_details else 'N/A',
            }
            app_data.append(app_info)
        
        # DataFrameに変換
        df = pd.DataFrame(app_data).sort_values(by='リリース日')
        return df
    
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None

# 使用例
if __name__ == "__main__":
    pub = sys.argv[1]  # パブリッシャー名
    search_word = f"pub:{pub}" # 検索キーワード
    apps_df = get_app_list(search_word)
    
    if apps_df is not None:
        print(f"製作スタジオ: {pub}")
        print(apps_df)
        
        # CSVに保存（オプション）
        apps_df.to_csv(f"list_{pub}.csv", index=False, encoding='shift-jis')
        print(f"結果を list_{pub}.csv に保存しました。")
