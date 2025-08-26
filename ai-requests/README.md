# AI Requests - 日記生成システム

このディレクトリには、江戸川コナンの日記を生成するための2つのシステムが含まれています。

## 📁 ディレクトリ構成

```
ai-requests/
├── common/                    # 共通モジュール
│   └── env_loader.py         # 環境変数読み込み
├── local/                     # ローカル版日記生成
│   └── run_local_batch.py    # ローカル生成スクリプト
├── flash-lite/               # Flash Lite版日記生成
│   └── run_flash_lite_batch.py # Gemini API使用スクリプト
└── README.md                 # このファイル
```

## 🚀 使用方法

### 1. 環境設定

プロジェクトルート（`conan-diary`）に`.env`ファイルを作成し、以下の内容を記述してください：

```env
# Gemini API設定（Flash Lite版で使用）
GEMINI_API_KEY=your-actual-api-key-here

# その他の設定
DEBUG=True
ENVIRONMENT=development
```

**重要**: `your-actual-api-key-here`の部分を、実際のGemini APIキーに置き換えてください。

### 2. 必要なパッケージのインストール

```bash
pip install python-dotenv pandas tqdm google-generativeai
```

### 3. ローカル版での日記生成

Gemini APIを使用せずにローカル環境で日記生成を行います：

```bash
cd ai-requests/local
python run_local_batch.py
```

**特徴:**
- APIキー不要
- 高速処理
- テンプレートベースの生成
- オフライン対応

**入力ファイル:** `prompts.csv`
**出力ファイル:** `results.csv`

### 4. Flash Lite版での日記生成

Gemini 2.5 Flash Liteを使用して高品質な日記生成を行います：

```bash
cd ai-requests/flash-lite
python run_flash_lite_batch.py
```

**特徴:**
- 高品質な日記生成
- 自然な日本語
- コナンの視点からの文章
- API制限対応（15リクエスト/分）

**入力ファイル:** `prompts.csv`
**出力ファイル:** `results.csv`

## 📊 入力CSVファイルの形式

`prompts.csv`ファイルは以下の列を含む必要があります：

```csv
生成プロンプト,エピソード,登場人物
"今日は推理が冴えていた",第1話,江戸川コナン
"事件解決に集中できた",第2話,毛利蘭
```

**必須列:**
- `生成プロンプト`: 日記生成のためのプロンプト

**オプション列:**
- `エピソード`: エピソード情報
- `登場人物`: 登場人物情報

## 🔧 設定のカスタマイズ

### ローカル版の設定

`run_local_batch.py`内の以下の設定を変更できます：

```python
# ローカル生成用の設定
DELAY_SECONDS = 0.1  # 処理間隔
MAX_RETRIES = 3      # 最大リトライ回数

# 日記テンプレート
DIARY_TEMPLATES = [
    "今日は{episode}の事件を解決した。{character}が犯人だったとは思わなかった。",
    # 他のテンプレート...
]
```

### Flash Lite版の設定

`run_flash_lite_batch.py`内の以下の設定を変更できます：

```python
# API設定
MODEL_NAME = 'gemini-2.5-flash-lite'
REQUESTS_PER_MINUTE = 15
DELAY_SECONDS = 60 / REQUESTS_PER_MINUTE
```

## 📝 出力ファイル

両方のシステムで以下のファイルが生成されます：

- **`results.csv`**: 生成された日記の結果
- **`backup.csv`**: 処理前のバックアップ
- **`prompts.csv`**: 入力プロンプト（既存の場合）

## ⚠️ 注意事項

### ローカル版
- テンプレートベースの生成のため、多様性に制限があります
- プロンプトの内容を反映した生成を行いますが、AIほどの柔軟性はありません

### Flash Lite版
- Gemini APIキーが必要です
- API制限（15リクエスト/分）に従って処理されます
- インターネット接続が必要です
- 処理時間はAPIの応答速度に依存します

## 🚨 トラブルシューティング

### エラー: "GEMINI_API_KEY環境変数が設定されていません"

**解決方法:**
1. `.env`ファイルが`conan-diary`直下に存在することを確認
2. `GEMINI_API_KEY`が正しく設定されていることを確認
3. `python-dotenv`パッケージがインストールされていることを確認

### エラー: "入力ファイルが見つかりません"

**解決方法:**
1. `prompts.csv`ファイルが正しいディレクトリに配置されていることを確認
2. ファイル名のスペルを確認
3. ファイルの権限を確認

### 処理が途中で止まる

**解決方法:**
1. バックアップファイル（`backup.csv`）から復旧を試行
2. エラーログを確認
3. ネットワーク接続を確認（Flash Lite版の場合）

## 📚 関連ファイル

- **`common/env_loader.py`**: 環境変数の読み込みと管理
- **`prompts.csv`**: 日記生成用のプロンプト
- **`results.csv`**: 生成された日記の結果

## 🔄 更新履歴

- **v1.0.0**: 初期バージョン
  - ローカル版とFlash Lite版の実装
  - 共通環境変数管理の実装
  - バックアップ・復旧機能の実装
