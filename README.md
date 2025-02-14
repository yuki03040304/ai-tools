# ai-tools

## インストール方法

このリポジトリをクローンし、仮想環境を作成した後、必要なパッケージをインストールしてください。

# リポジトリをクローン
git clone https://github.com/yuki03040304/ai-tools.git
cd ai-tools

# 仮想環境を作成して有効化
python -m venv venv
source venv/bin/activate  

# 必要なパッケージをインストール
pip install -r requirements.txt
```

## 使用方法
python chatApp.py "家族の詳細情報を教えてください。" '{"family": [{"name": "", "relation": "", "details": {"age": "", "occupation": "", "hobbies": []}}]}'

## 出力結果の例
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
```

