#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
環境設定とモジュールの動作確認テストスクリプト
"""

import os
import sys

def test_environment():
    """環境設定のテスト"""
    print("=== 環境設定テスト ===")
    
    # .envファイルの存在確認
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        print(f"✅ .envファイルが見つかりました: {env_file}")
    else:
        print(f"❌ .envファイルが見つかりません: {env_file}")
        print("   プロジェクトルートに.envファイルを作成してください")
    
    # 必要なディレクトリの存在確認
    required_dirs = [
        'ai-requests',
        'ai-requests/common',
        'ai-requests/local',
        'ai-requests/flash-lite',
        'prompt-generator',
        'diary-viewer'
    ]
    
    print("\nディレクトリ構造の確認:")
    for dir_path in required_dirs:
        full_path = os.path.join(os.path.dirname(__file__), dir_path)
        if os.path.exists(full_path):
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path}")

def test_modules():
    """モジュールのインポートテスト"""
    print("\n=== モジュールインポートテスト ===")
    
    try:
        # 環境変数モジュールのテスト
        sys.path.append(os.path.join(os.path.dirname(__file__), 'ai-requests', 'common'))
        from env_loader import load_environment, get_project_paths
        
        print("✅ env_loaderモジュールのインポートに成功")
        
        # プロジェクトパスの取得テスト
        paths = get_project_paths()
        print("✅ プロジェクトパスの取得に成功")
        for key, path in paths.items():
            print(f"   {key}: {path}")
            
    except ImportError as e:
        print(f"❌ モジュールのインポートに失敗: {e}")
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")

def test_dependencies():
    """依存パッケージのテスト"""
    print("\n=== 依存パッケージテスト ===")
    
    required_packages = [
        'pandas',
        'tqdm',
        'google.generativeai',
        'dotenv'
    ]
    
    for package in required_packages:
        try:
            if package == 'dotenv':
                import dotenv
            elif package == 'google.generativeai':
                import google.generativeai
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - インストールが必要")
        except Exception as e:
            print(f"⚠️ {package} - エラー: {e}")

def test_csv_files():
    """CSVファイルのテスト"""
    print("\n=== CSVファイルテスト ===")
    
    csv_files = [
        'ai-requests/local/sample_prompts.csv',
        'ai-requests/flash-lite/sample_prompts.csv'
    ]
    
    for csv_file in csv_files:
        full_path = os.path.join(os.path.dirname(__file__), csv_file)
        if os.path.exists(full_path):
            print(f"✅ {csv_file}")
            # ファイルサイズの確認
            size = os.path.getsize(full_path)
            print(f"   サイズ: {size} bytes")
        else:
            print(f"❌ {csv_file}")

def main():
    """メインテスト"""
    print("🔍 コナン日記プロジェクト - セットアップテスト")
    print("=" * 50)
    
    test_environment()
    test_modules()
    test_dependencies()
    test_csv_files()
    
    print("\n" + "=" * 50)
    print("📋 セットアップ完了後の次のステップ:")
    print("1. .envファイルを作成してGEMINI_API_KEYを設定")
    print("2. 必要なパッケージをインストール: pip install -r requirements.txt")
    print("3. ローカル版のテスト: cd ai-requests/local && python run_local_batch.py")
    print("4. Flash Lite版のテスト: cd ai-requests/flash-lite && python run_flash_lite_batch.py")

if __name__ == "__main__":
    main()
