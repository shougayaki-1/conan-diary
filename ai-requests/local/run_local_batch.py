#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ローカル版日記生成スクリプト
Gemini APIを使用せずにローカル環境で日記生成を行います
"""

import os
import sys
import time
import pandas as pd
from datetime import datetime
import random

# プロジェクトルートのパスを追加して環境変数モジュールをインポート
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)
from ai_requests.common.env_loader import load_environment, get_project_paths

# --- スクリプト自身の場所を基準にファイルのパスを自動設定 ---
script_dir = os.path.dirname(os.path.abspath(__file__))

# --- 設定項目 ---
INPUT_CSV_FILE = os.path.join(script_dir, 'prompts.csv')
OUTPUT_CSV_FILE = os.path.join(script_dir, 'results.csv')
BACKUP_CSV_FILE = os.path.join(script_dir, 'backup.csv')

# ローカル生成用の設定
DELAY_SECONDS = 0.1  # ローカルなので高速処理
MAX_RETRIES = 3

# --- ローカル日記生成テンプレート ---
DIARY_TEMPLATES = [
    "今日は{episode}の事件を解決した。{character}が犯人だったとは思わなかった。",
    "{episode}の事件で{character}が活躍していた。さすがだ。",
    "{episode}の事件は複雑だったが、{character}の協力で解決できた。",
    "今日も{episode}の事件に巻き込まれた。{character}の推理が鋭い。",
    "{episode}の事件で{character}が怪しい動きをしていた。",
    "{episode}の事件は{character}の証言が決め手になった。",
    "今日は{episode}の事件で{character}と一緒に捜査した。",
    "{episode}の事件は{character}の行動が謎だった。",
    "{episode}の事件で{character}が重要な手がかりを見つけた。",
    "{episode}の事件は{character}の推理で真相が明らかになった。"
]

def load_environment_local():
    """ローカル環境の設定を読み込みます。"""
    try:
        # 環境変数を読み込み（ローカル用の設定）
        load_environment()
        print("ローカル環境の設定を読み込みました。")
    except Exception as e:
        print(f"環境設定の読み込み中にエラーが発生しました: {e}")
        print("ローカルモードで実行を続行します。")

def generate_local_diary(prompt, episode_info=None):
    """
    ローカルで日記を生成します
    
    Args:
        prompt: 生成プロンプト
        episode_info: エピソード情報（辞書）
    
    Returns:
        str: 生成された日記
    """
    try:
        # プロンプトから情報を抽出
        if episode_info:
            episode = episode_info.get('episode', '謎の事件')
            character = episode_info.get('character', '謎の人物')
        else:
            # プロンプトから簡単な情報を抽出
            episode = "謎の事件"
            character = "謎の人物"
            
            if "コナン" in prompt:
                character = "江戸川コナン"
            if "蘭" in prompt:
                character = "毛利蘭"
            if "小五郎" in prompt:
                character = "毛利小五郎"
            if "博士" in prompt:
                character = "阿笠博士"
        
        # テンプレートからランダムに選択して日記を生成
        template = random.choice(DIARY_TEMPLATES)
        diary = template.format(episode=episode, character=character)
        
        # プロンプトの内容を反映した追加情報
        if "推理" in prompt:
            diary += " 推理が冴えていた一日だった。"
        if "事件" in prompt:
            diary += " 事件解決に集中できた。"
        if "捜査" in prompt:
            diary += " 捜査が順調に進んだ。"
        
        # 日付情報を追加
        current_date = datetime.now().strftime("%Y年%m月%d日")
        diary = f"{current_date}\n{diary}"
        
        return diary
        
    except Exception as e:
        return f"ローカル生成エラー: {e}"

def process_prompts_local():
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

        # 各プロンプトを処理
        for index in rows_to_process:
            prompt = df_output.loc[index, '生成プロンプト']

            if pd.isna(prompt):
                df_output.loc[index, '生成結果'] = "エラー: プロンプトが空です"
                continue

            # エピソード情報を抽出（CSVの列に応じて調整）
            episode_info = None
            if 'エピソード' in df_output.columns:
                episode_info = {
                    'episode': df_output.loc[index, 'エピソード'],
                    'character': df_output.loc[index, '登場人物'] if '登場人物' in df_output.columns else '謎の人物'
                }

            # ローカルで日記を生成
            result_text = generate_local_diary(prompt, episode_info)
            df_output.loc[index, '生成結果'] = result_text
            
            # 進捗を表示
            print(f"行 {index + 1}: ローカル生成完了")
            
            # 定期的に保存
            if (index + 1) % 10 == 0:
                df_output.to_csv(OUTPUT_CSV_FILE, index=False)
                print(f"中間保存完了: {index + 1}件処理済み")
            
            # ローカル処理なので短い遅延
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

if __name__ == "__main__":
    print("=== ローカル版日記生成スクリプト ===")
    print("Gemini APIを使用せずにローカル環境で日記生成を行います。")
    print()
    
    load_environment_local()
    process_prompts_local()
