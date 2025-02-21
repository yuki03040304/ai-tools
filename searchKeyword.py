import sys
import argparse
import os
import glob
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from dotenv import load_dotenv

def get_next_filename():
    """
    既存の"kewwoard_ideas*.csv"ファイルを検索し、
    インクリメントされたファイル名を生成します。
    """
    files = glob.glob("kewwoard_ideas*.csv")
    max_num = 0
    for f in files:
        base = os.path.basename(f)
        num_str = base[len("kewwoard_ideas"):base.find(".csv")]
        if num_str.isdigit():
            num = int(num_str)
            if num > max_num:
                max_num = num
    return f"kewwoard_ideas{max_num + 1}.csv"

def main(keyword, max_results, location, language):
    # .envファイルから環境変数を読み込む
    load_dotenv()

    # 必要な環境変数を取得（存在しない場合はKeyErrorとなります）
    developer_token = os.environ["DEVELOPER_TOKEN"]
    client_id = os.environ["CLIENT_ID"]
    client_secret = os.environ["CLIENT_SECRET"]
    refresh_token = os.environ["REFRESH_TOKEN"]
    login_customer_id = os.environ["LOGIN_CUSTOMER_ID"]
    customer_id = os.environ["CUSTOMER_ID"]

    # GoogleAdsClientの設定を辞書形式で定義
    config = {
        "developer_token": developer_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "login_customer_id": login_customer_id,
        "use_proto_plus": True,
    }

    # Google Ads APIクライアントの初期化
    client = GoogleAdsClient.load_from_dict(config)

    # サービスの取得
    keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")
    google_ads_service = client.get_service("GoogleAdsService")

    # 言語と地域の定数を取得（デフォルトは日本）
    language_constant = google_ads_service.language_constant_path(language)
    geo_target_constant = google_ads_service.geo_target_constant_path(location)

    # リクエストの組み立て
    request = client.get_type("GenerateKeywordIdeasRequest")
    request.customer_id = customer_id
    request.language = language_constant
    request.geo_target_constants.append(geo_target_constant)
    request.keyword_seed.keywords.append(keyword)
    request.page_size = max_results  # 1ページあたりの取得件数を指定

    try:
        response = keyword_plan_idea_service.generate_keyword_ideas(request=request)
        results = []
        count = 0
        for idea in response:
            if count >= max_results:
                break
            metrics = idea.keyword_idea_metrics
            if metrics:
                avg_searches = metrics.avg_monthly_searches
                competition = metrics.competition.name  # LOW / MEDIUM / HIGH
                low_bid = (metrics.low_top_of_page_bid_micros / 1e6
                           if metrics.low_top_of_page_bid_micros else None)
                high_bid = (metrics.high_top_of_page_bid_micros / 1e6
                            if metrics.high_top_of_page_bid_micros else None)
                results.append([idea.text, avg_searches, competition, low_bid, high_bid])
            count += 1

        # ヘッダーの定義
        header = ["KW", "月間平均検索数", "競合性", "下限入札額", "上限入札額"]
        all_rows = [header] + results

        # 各列の最大幅を計算（全てのセルの文字列長の最大値）
        col_widths = []
        for col in range(len(header)):
            max_width = max(len(str(row[col])) if row[col] is not None else 4 for row in all_rows)
            col_widths.append(max_width)

        # 列ごとのアライメント設定（例：文字列は左寄せ、数値は右寄せ）
        # KW, 競合性 は左寄せ、その他の数値は右寄せ
        alignments = ["<", ">", "<", ">", ">"]

        # 出力ファイル名の生成
        output_filename = get_next_filename()

        with open(output_filename, mode="w", encoding="utf-8") as file:
            # ヘッダー行の作成
            header_line = " | ".join(f"{str(cell):{align}{width}}"
                                     for cell, align, width in zip(header, alignments, col_widths))
            file.write(header_line + "\n")
            # 区切り線（各列の幅分のハイフンを配置）
            separator_line = "-+-".join("-" * width for width in col_widths)
            file.write(separator_line + "\n")
            # データ行の作成
            for row in results:
                formatted_row = []
                for cell in row:
                    formatted_row.append("-" if cell is None else str(cell))
                line = " | ".join(f"{cell:{align}{width}}"
                                  for cell, align, width in zip(formatted_row, alignments, col_widths))
                file.write(line + "\n")

        print(f"結果が '{output_filename}' に保存されました。")

    except GoogleAdsException as ex:
        print("リクエストに失敗しました。")
        print(f"エラーコード: {ex.error.code()}")
        for error in ex.failure.errors:
            print(f"\t詳細: {error.message}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="キーワードプランナーのデータを取得し、固定幅CSV（.csv）に保存します。"
    )
    parser.add_argument("keyword", type=str, help="検索キーワード")
    parser.add_argument("--max_results", type=int, default=10, help="関連ワードの上限数（デフォルト: 10）")
    parser.add_argument("--location", type=int, default=2392, help="地域のID（デフォルト: 2392 - 日本）")
    parser.add_argument("--language", type=int, default=1005, help="言語のID（デフォルト: 1005 - 日本語）")
    args = parser.parse_args()

    main(args.keyword, args.max_results, args.location, args.language)
