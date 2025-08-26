# コナン日記プロジェクト (Conan Diary Project)

江戸川コナンの日記をAIで生成し、Web上で表示・管理するための包括的なシステムです。

## 🎯 プロジェクト概要

このプロジェクトは以下の3つの主要コンポーネントで構成されています：

1. **📝 Prompt Generator** - プロンプト作成・CSV成形
2. **🤖 AI Requests** - AIによる日記生成（ローカル版・Flash Lite版）
3. **🌐 Diary Viewer** - HTMLでの日記表示・閲覧

## 📁 プロジェクト構造

```
conan-diary/
├── prompt-generator/          # プロンプト作成・CSV成形
├── ai-requests/              # AIによる日記生成
│   ├── common/               # 共通モジュール
│   ├── local/                # ローカル版日記生成
│   └── flash-lite/           # Flash Lite版日記生成
├── diary-viewer/             # HTMLでの日記表示
├── .env                      # 環境変数設定（要作成）
└── README.md                 # このファイル
```

## 🚀 セットアップ

### 1. 必要なパッケージのインストール

```bash
pip install python-dotenv pandas tqdm google-generativeai
```

### 2. 環境変数の設定

プロジェクトルートに`.env`ファイルを作成し、以下の内容を記述してください：

```env
# Gemini API設定（Flash Lite版で使用）
GEMINI_API_KEY=your-actual-api-key-here

# その他の設定
DEBUG=True
ENVIRONMENT=development
```

**重要**: `your-actual-api-key-here`の部分を、実際のGemini APIキーに置き換えてください。

### 3. Gemini APIキーの取得

1. [Google AI Studio](https://makersuite.google.com/app/apikey) にアクセス
2. Googleアカウントでログイン
3. "Create API Key"をクリック
4. 生成されたAPIキーをコピーして`.env`ファイルに設定

## 📋 使用方法

### 1. プロンプト作成・CSV成形

```bash
cd prompt-generator
python create_prompts.py
```

**機能:**
- エピソード情報からプロンプトを自動生成
- CSVファイルの成形・整理
- 日記生成用のデータ準備

### 2. AIによる日記生成

#### ローカル版（APIキー不要）

```bash
cd ai-requests/local
python run_local_batch.py
```

**特徴:**
- 高速処理
- オフライン対応
- テンプレートベースの生成

#### Flash Lite版（高品質）

```bash
cd ai-requests/flash-lite
python run_flash_lite_batch.py
```

**特徴:**
- 高品質な日記生成
- 自然な日本語
- Gemini 2.5 Flash Lite使用

### 3. 日記の表示・閲覧

```bash
cd diary-viewer
# index.htmlをブラウザで開く
```

**機能:**
- カレンダー表示
- リスト表示
- 検索・フィルタリング
- 日記詳細表示

## 🔧 設定のカスタマイズ

### 日記生成の設定

各AIリクエストディレクトリ内のスクリプトで以下の設定を変更できます：

- **処理間隔**: `DELAY_SECONDS`
- **API制限**: `REQUESTS_PER_MINUTE`
- **モデル**: `MODEL_NAME`（Flash Lite版）

### テンプレートのカスタマイズ

ローカル版の日記テンプレートは`ai-requests/local/run_local_batch.py`内で編集できます。

## 📊 データフロー

```
1. エピソード情報 → prompt-generator → prompts.csv
2. prompts.csv → ai-requests → results.csv
3. results.csv → diary-viewer → Web表示
```

## ⚠️ 注意事項

### API制限
- Flash Lite版: 15リクエスト/分
- 大量のプロンプト処理時は時間がかかります

### ファイル形式
- 入力: CSV形式（UTF-8エンコーディング推奨）
- 出力: CSV形式（生成結果付き）

### エラー処理
- バックアップファイルの自動生成
- エラー時の復旧機能
- 処理の継続性

## 🚨 トラブルシューティング

### よくある問題

1. **環境変数が読み込まれない**
   - `.env`ファイルが正しい場所にあるか確認
   - `python-dotenv`がインストールされているか確認

2. **APIキーエラー**
   - `.env`ファイルの`GEMINI_API_KEY`を確認
   - APIキーが有効か確認

3. **ファイルが見つからない**
   - ファイルパスを確認
   - ファイルの権限を確認

## 📚 関連ドキュメント

- [AI Requests README](ai-requests/README.md) - 日記生成システムの詳細
- [Prompt Generator README](prompt-generator/README.md) - プロンプト作成の詳細
- [Diary Viewer README](diary-viewer/README.md) - Web表示の詳細

## 🔄 更新履歴

- **v2.0.0**: 完全リニューアル
  - 3つのプロジェクトに分割
  - モダンなアーキテクチャ
  - 改善されたエラー処理
  - 包括的なドキュメント

## 📄 ライセンス

このプロジェクトは教育・研究目的で作成されています。

## 🤝 貢献

バグ報告や機能要望は、GitHubのIssueでお知らせください。

---

**There is only one truth!** 🕵️‍♂️
