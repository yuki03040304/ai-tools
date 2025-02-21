# ai-tools

# リポジトリをクローン
git clone https://github.com/yuki03040304/ai-tools.git
cd ai-tools

# 仮想環境を作成して有効化
python -m venv venv
source venv/bin/activate  

# 必要なパッケージをインストール
pip install -r requirements.txt
```

# 使用方法(json)
python chatApp.py "家族の詳細情報を教えてください。" '{"family": [{"name": "", "relation": "", "details": {"age": "", "occupation": "", "hobbies": []}}]}'

# 使用方法(google ads)
python searchKeyword.py "にんにく" --max_results 10 --location 2392 --language 1005
--max_results 出力上限
--location 2392 場所設定
--language 1005　言語設定

# 出力結果の例(json)
{
    "family": [
        {
            "name": "山田花子",
            "relation": "母",
            "details": {
                "age": "45",
                "occupation": "教師",
                "hobbies": [
                    "ガーデニング",
                    "読書"
                ]
            }
        },
        {
            "name": "山田太郎",
            "relation": "父",
            "details": {
                "age": "50",
                "occupation": "エンジニア",
                "hobbies": [
                    "釣り",
                    "映画鑑賞"
                ]
            }
        },
        {
            "name": "山田一郎",
            "relation": "子供",
            "details": {
                "age": "16",
                "occupation": "高校生",
                "hobbies": [
                    "サッカー",
                    "ゲーム"
                ]
            }
        },
        {
            "name": "山田二郎",
            "relation": "子供",
            "details": {
                "age": "12",
                "occupation": "小学生",
                "hobbies": [
                    "アニメ",
                    "絵画"
                ]
            }
        }
    ]
}

# 出力結果の例(google ads)
KW           | 月間平均検索数 | 競合性    |      下限入札額 |      上限入札額
-------------+---------+--------+------------+-----------
にんにく         |  135000 | MEDIUM |  15.365026 |     59.926
にんにく 卵黄      |    8100 | HIGH   | 138.739926 | 482.030211
黒 にんにく       |   40500 | HIGH   |  23.711519 |   61.42415
にんにく サプリ     |    2400 | HIGH   |  43.384026 | 307.731695
にんにく しじみ     |    1300 | HIGH   |  66.521006 | 223.711848
行者 にんにく      |   40500 | MEDIUM |     8.9889 | 127.157728
やずや にんにく 卵黄  |    5400 | HIGH   |  28.679085 | 100.543692
黒 にんにく サプリ   |    1300 | HIGH   |   28.46485 | 258.210646
伝統 にんにく 卵黄   |     140 | HIGH   |  85.480993 | 953.294568
にんにく 卵黄 ワイルド |    1900 | HIGH   |    32.9593 | 176.876083
```

