#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flash Lite版日記生成スクリプト
Gemini 2.5 Flash Liteを使用して日記生成を行います
"""

import os
import sys
import time
import pandas as pd
from tqdm import tqdm
import google.generativeai as genai

# プロジェクトルートのパスを追加して環境変数モジュールをインポート
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)
from ai_requests.common.env_loader import get_gemini_api_key, load_environment

# --- スクリプト自身の場所を基準にファイルのパスを自動設定 ---
script_dir = os.path.dirname(os.path.abspath(__file__))

# --- 設定項目 ---
INPUT_CSV_FILE = os.path.join(script_dir, 'prompts.csv')
OUTPUT_CSV_FILE = os.path.join(script_dir, 'results.csv')
BACKUP_CSV_FILE = os.path.join(script_dir, 'backup.csv')

# API設定
MODEL_NAME = 'gemini-2.5-flash-lite'
REQUESTS_PER_MINUTE = 15
DELAY_SECONDS = 60 / REQUESTS_PER_MINUTE

# --- ここからスクリプト本体 ---

def configure_api():
    """APIキーを設定します。"""
    try:
        # 環境変数を読み込み
        load_environment()
        # APIキーを取得
        api_key = get_gemini_api_key()
        genai.configure(api_key=api_key)
        print("Gemini APIキーの設定が完了しました。")
        print(f"使用モデル: {MODEL_NAME}")
    except Exception as e:
        print(f"APIキーの設定中にエラーが発生しました: {e}")
        print("環境変数ファイル(.env)にGEMINI_API_KEYが正しく設定されているか確認してください。")
        exit()

def generate_diary_with_gemini(prompt, model):
    """
    Gemini APIを使用して日記を生成します
    
    Args:
        prompt: 生成プロンプト
        model: Geminiモデルインスタンス
    
    Returns:
        str: 生成された日記
    """
    try:
        # 日記生成用のプロンプトを構築
        enhanced_prompt = f"""
以下のプロンプトに基づいて、江戸川コナンの日記を生成してください。
日記は自然で読みやすく、コナンの視点から書かれたものにしてください。

プロンプト: {prompt}

要求事項:
- 日本語で書く
- コナンの視点から書く
- 自然な日記の文体にする
- 200-500文字程度にする
- 日付は含めない（後で追加する）

日記:
"""
        
        response = model.generate_content(enhanced_prompt)
        result_text = response.text.strip()
        
        # 日付を追加
        current_date = time.strftime("%Y年%m月%d日")
        result_text = f"{current_date}\n{result_text}"
        
        return result_text
        
    except Exception as e:
        return f"APIエラー: {e}"

def process_prompts():
    """CSVファイルを読み込み、プロンプトを処理して結果を保存します。"""
    
    try:
        # 出力ファイルが存在する場合は読み込み
        if os.path.exists(OUTPUT_CSV_FILE):
            df_output = pd.read_csv(OUTPUT_CSV_FILE)
            print(f"'{OUTPUT_CSV_FILE}' を読み込みました。続きから処理を再開します。")
        else:
            # 入力ファイルから新規作成
            if os.path.exists(INPUT_CSV_FILE):
                df_input = pd.read_csv(INPUT_CSV_FILE)
                df_input['生成結果'] = ''
                df_output = df_input
                print(f"入力ファイル '{INPUT_CSV_FILE}' を基に、'{OUTPUT_CSV_FILE}' を新規作成します。")
            else:
                print(f"エラー: 入力ファイル '{INPUT_CSV_FILE}' が見つかりません。")
                print(f"スクリプトが探しているパス: {INPUT_CSV_FILE}")
                return

        # 未処理のプロンプトを特定
        rows_to_process = [index for index, row in df_output.iterrows() 
                          if pd.isna(row.get('生成結果', float('nan'))) or row.get('生成結果', '') == '']

        if not rows_to_process:
            print("すべてのプロンプトが処理済みです。")
            return

        print(f"未処理のプロンプトが {len(rows_to_process)} 件見つかりました。処理を開始します。")

        # 処理前のバックアップを作成
        df_output.to_csv(BACKUP_CSV_FILE, index=False)
        print(f"バックアップを作成しました: {BACKUP_CSV_FILE}")

        # Geminiモデルを初期化
        model = genai.GenerativeModel(MODEL_NAME)
        
        # 各プロンプトを処理
        for index in tqdm(rows_to_process, desc="日記を生成中"):
            prompt = df_output.loc[index, '生成プロンプト']

            if pd.isna(prompt):
                df_output.loc[index, '生成結果'] = "エラー: プロンプトが空です"
                continue

            try:
                # Gemini APIを使用して日記を生成
                result_text = generate_diary_with_gemini(prompt, model)
                df_output.loc[index, '生成結果'] = result_text
                
                # 進捗を表示
                print(f"\n行 {index + 1}: 生成完了")
                print(f"プロンプト: {prompt[:50]}...")
                print(f"結果: {result_text[:100]}...")
                
            except Exception as e:
                result_text = f"APIエラー: {e}"
                df_output.loc[index, '生成結果'] = result_text
                print(f"\n行 {index + 1} でエラーが発生しました: {e}")

            # 定期的に保存
            if (index + 1) % 5 == 0:
                df_output.to_csv(OUTPUT_CSV_FILE, index=False)
                print(f"中間保存完了: {index + 1}件処理済み")
            
            # API制限に従って遅延
            time.sleep(DELAY_SECONDS)

        # 最終保存
        df_output.to_csv(OUTPUT_CSV_FILE, index=False)
        print("\nすべての処理が完了しました。")

    except Exception as e:
        print(f"処理中にエラーが発生しました: {e}")
        # エラーが発生した場合はバックアップから復旧を試行
        if os.path.exists(BACKUP_CSV_FILE):
            print("バックアップからの復旧を試行します...")
            try:
                df_backup = pd.read_csv(BACKUP_CSV_FILE)
                df_backup.to_csv(OUTPUT_CSV_FILE, index=False)
                print("バックアップから復旧しました。")
            except Exception as restore_error:
                print(f"復旧に失敗しました: {restore_error}")

def main():
    """メイン処理"""
    print("=== Flash Lite版日記生成スクリプト ===")
    print(f"使用モデル: {MODEL_NAME}")
    print(f"API制限: {REQUESTS_PER_MINUTE} リクエスト/分")
    print()
    
    # API設定
    configure_api()
    
    # プロンプト処理
    process_prompts()

if __name__ == "__main__":
    main()
