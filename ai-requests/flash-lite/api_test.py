# api_test.py
import os
import sys
import google.generativeai as genai

# プロジェクトルートのパスを追加して環境変数モジュールをインポート
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'ai-requests', 'common'))
from env_loader import get_gemini_api_key, load_environment

try:
    print("1. 環境変数を読み込み中...")
    load_environment()
    api_key = get_gemini_api_key()
    genai.configure(api_key=api_key)
    print("2. APIキーの設定完了。")

    print("3. Geminiモデルに接続中...")
    model = genai.GenerativeModel('gemini-1.5-flash-latest') # テストなのでモデル名を固定
    
    print("4. 簡単なリクエストを送信中...")
    response = model.generate_content("こんにちは")
    
    print("\n✅ テスト成功！ APIからの応答:")
    print(response.text)

except Exception as e:
    print(f"\n❌ テスト中にエラーが発生しました:")
    print(e)