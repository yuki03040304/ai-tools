import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate
from json import JSONDecodeError
import argparse

# .envファイルから環境変数を読み込む
load_dotenv()

# OpenAI APIキーとSerpAPIキーを環境変数から取得
openai_api_key = os.getenv('OPENAI_API_KEY')
serpapi_api_key = os.getenv('SERPAPI_API_KEY')

if not openai_api_key:
    print('OPENAI_API_KEYが設定されていません。.envファイルを確認してください。')
    exit(1)

if not serpapi_api_key:
    print('SERPAPI_API_KEYが設定されていません。.envファイルを確認してください。')
    exit(1)

# OpenAIチャットモデルのインスタンスを作成
llm = ChatOpenAI(api_key=openai_api_key, model="gpt-4o-mini")

# SerpAPIツールの読み込み
tools = load_tools(["serpapi"], serpapi_api_key=serpapi_api_key)

# メモリの初期化
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# エージェントの初期化
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# チャット履歴のJSONファイル名
CHAT_LOG_FILE = "chat.json"

def load_chat_history():
    """JSONファイルからチャット履歴を読み込む"""
    if os.path.exists(CHAT_LOG_FILE):
        with open(CHAT_LOG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def save_chat_history(chat_history):
    """チャット履歴をJSONファイルに保存する（配列形式）"""
    with open(CHAT_LOG_FILE, "w", encoding="utf-8") as file:
        json.dump(chat_history, file, indent=4, ensure_ascii=False)

def label_message(message):
    """メッセージのラベリングを生成AIを使って行う"""
    prompt = f"""
以下のメッセージに適切なカテゴリを付けてください:
メッセージ: "{message}"
カテゴリ例: ["質問", "回答", "指示", "感情", "情報提供", "確認"]
"""
    return llm.predict(prompt).strip()

def extract_elements(message, keys):
    """メッセージから指定されたキーに基づいて要素を抽出し、JSON形式で返す"""
    # JSON出力パーサーの初期化
    parser = JsonOutputParser()

    # プロンプトテンプレートの作成
    prompt_template = PromptTemplate(
        input_variables=["message", "keys"],
        template="""
以下の文章を解析し、指定されたキーに基づいて情報を抽出してください。
出力は以下のJSONフォーマットに従ってください。
JSONフォーマット:
{keys}
最終応答は、上記のJSON形式のみを出力し、他のテキストは一切含めないでください。
文章: "{message}"
"""
    )

    # プロンプトの生成
    prompt = prompt_template.format(message=message, keys=keys)

    # LLMからの応答を取得
    response = llm.predict(prompt).strip()

    try:
        # JSON形式の応答を解析
        return parser.parse(response)
    except JSONDecodeError:
        print("LLMからの出力が有効なJSON形式ではありません。プロンプトやLLMの出力内容を再確認してください。")
        return {}

def main(user_input, json_keys):
    # チャット履歴の読み込み
    chat_history = load_chat_history()

    # ユーザーのメッセージをチャット履歴に追加
    user_label = label_message(user_input)
    user_message = {'role': 'user', 'content': user_input, 'label': user_label}
    chat_history.append(user_message)

    # エージェントを使用して応答を生成
    bot_response = agent.run(input=user_input).strip()
    bot_label = label_message(bot_response)
    bot_message = {'role': 'bot', 'content': bot_response, 'label': bot_label}

    # ボットの応答をチャット履歴に追加
    chat_history.append(bot_message)

    # チャット履歴全体をJSON配列として保存
    save_chat_history(chat_history)

    # 要素の抽出
    extracted_json = extract_elements(bot_response, json_keys)
    if extracted_json:
        # structured_chat.jsonをBOMなしのUTF-8で保存
        with open("structured_chat.json", "w", encoding="utf-8") as file:
            json.dump(extracted_json, file, indent=4, ensure_ascii=False)

    # 応答の表示
    print(f"Bot: {bot_response}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chatbot CLI")
    parser.add_argument("user_input", type=str, help="ユーザーからのメッセージ")
    parser.add_argument("json_keys", type=str, help="抽出するJSONのキーを指定。例: '{\"family\": [{\"name\": \"\", \"relation\": \"\", \"details\": {\"age\": \"\", \"occupation\": \"\", \"hobbies\": []}}]}'")
    args = parser.parse_args()

    main(args.user_input, args.json_keys)
