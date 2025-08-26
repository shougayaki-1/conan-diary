#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
環境変数読み込みモジュール
conan-diary直下の.envファイルを自動的に読み込みます
"""

import os
from dotenv import load_dotenv
from pathlib import Path

def load_environment(env_file='.env'):
    """
    環境変数を読み込む
    
    Args:
        env_file: 環境変数ファイル名
    
    Returns:
        str: 読み込まれた.envファイルのパス
    """
    # プロジェクトルート（conan-diary）の.envファイルを読み込み
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    env_path = os.path.join(current_dir, env_file)
    
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print(f"環境変数ファイルを読み込みました: {env_path}")
        return env_path
    else:
        # フォールバック: 現在の作業ディレクトリから.envを探す
        load_dotenv()
        print("現在の作業ディレクトリの.envファイルを読み込みました")
        return os.path.join(os.getcwd(), env_file)

def get_env_var(key, default=None, required=False):
    """
    環境変数を取得する
    
    Args:
        key: 環境変数名
        default: デフォルト値
        required: 必須かどうか
    
    Returns:
        str: 環境変数の値
    
    Raises:
        ValueError: 必須の環境変数が設定されていない場合
    """
    value = os.getenv(key, default)
    
    if required and not value:
        raise ValueError(f"環境変数 {key} が設定されていません")
    
    return value

def get_gemini_api_key():
    """
    Gemini APIキーを取得する
    
    Returns:
        str: APIキー
    
    Raises:
        ValueError: APIキーが設定されていない場合
    """
    return get_env_var('GEMINI_API_KEY', required=True)

def get_debug_mode():
    """
    デバッグモードを取得する
    
    Returns:
        bool: デバッグモード
    """
    return get_env_var('DEBUG', 'False').lower() == 'true'

def get_environment():
    """
    環境設定を取得する
    
    Returns:
        str: 環境設定
    """
    return get_env_var('ENVIRONMENT', 'production')

def get_project_paths():
    """
    プロジェクトのパス情報を取得する
    
    Returns:
        dict: プロジェクトパスの辞書
    """
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return {
        'root': current_dir,
        'ai_requests': os.path.join(current_dir, 'ai-requests'),
        'local': os.path.join(current_dir, 'ai-requests', 'local'),
        'flash_lite': os.path.join(current_dir, 'ai-requests', 'flash-lite'),
        'diary_viewer': os.path.join(current_dir, 'diary-viewer'),
        'prompt_generator': os.path.join(current_dir, 'prompt-generator')
    }
