# SlackCogs Slack Bot

SlackCogsフレームワークを使用したモダンなSlackボットのスターターテンプレートです。

## 🚀 特徴

- **モジュラー設計**: Cog（コグ）システムによる機能の分離
- **ホットリロード**: 開発時にボットを再起動せずにコードを更新
- **型安全性**: Python 3.10+の型ヒントを活用
- **包括的テスト**: pytestを使用した自動テスト
- **Docker対応**: 本番環境での簡単なデプロイ
- **設定管理**: 環境変数による柔軟な設定

## 📁 プロジェクト構成

```
my-slack-bot/
├── 📄 .env.example                 # 環境変数テンプレート
├── 📄 .gitignore                   # Git除外設定
├── 📄 requirements.txt             # 依存関係
├── 📄 docker-compose.yml           # Docker設定
├── 📄 Dockerfile                   # Dockerコンテナ
├── 📄 README.md                    # プロジェクト説明
├── 📄 main.py                      # アプリケーション起動点
├── 📄 config.py                    # 設定管理
│
├── 📂 cogs/                        # Cogディレクトリ
│   ├── __init__.py
│   ├── 📄 general.py               # 基本コマンド（ping, help, status）
│   ├── 📄 admin.py                 # 管理機能（reload, load, unload）
│   └── 📄 example.py               # サンプルCog（カスタム機能例）
│
└── 📂 tests/                       # テスト
    ├── __init__.py
    └── 📄 test_cogs.py             # Cogテスト
```

## 🛠️ セットアップ

### 前提条件

- Python 3.10以上
- Slack App の作成とトークンの取得

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd slack-bot
```

### 2. 仮想環境の作成

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# または
venv\Scripts\activate  # Windows
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定

```bash
cp .env.example .env
```

`.env`ファイルを編集して、必要な環境変数を設定してください：

```env
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret
SLACK_APP_TOKEN=xapp-your-app-token
ENABLE_HOT_RELOAD=true
DEBUG_MODE=true
```

### 5. Slack Appの設定

1. [Slack API](https://api.slack.com/apps)でアプリを作成
2. OAuth & Permissions で Bot Token Scopes を設定
3. Socket Mode を有効化してApp Tokenを取得
4. アプリをワークスペースにインストール

### 6. ボットの起動

```bash
python main.py
```

## 🐳 Docker を使用した起動

### 開発環境

```bash
# ホットリロード有効で起動
docker-compose up --build
```

### 本番環境

```bash
# 本番用設定で起動
docker-compose -f docker-compose.yml up -d --build
```

## 🧪 テストの実行

```bash
# 全テストを実行
pytest

# カバレッジ付きでテスト実行
pytest --cov=cogs --cov-report=html

# 特定のテストファイルを実行
pytest tests/test_cogs.py
```

## 📊 利用可能なコマンド

### 基本コマンド（GeneralCog）

- `/ping` - ボットの応答テスト
- `/help` - ヘルプメッセージを表示
- `/status` - ボットのステータス情報を表示

### 管理者コマンド（AdminCog）

- `/reload [cog名]` - Cogをリロード
- `/load <cog名>` - 指定されたCogを読み込み
- `/unload <cog名>` - 指定されたCogをアンロード
- `/list_cogs` - 読み込まれているCog一覧を表示
- `/admin_help` - 管理者ヘルプを表示

### サンプルコマンド（ExampleCog）

- `/hello [名前]` - 挨拶をします
- `/count` - カウンターを増加
- `/quote` - ランダムな名言を表示
- `/time` - 現在の時刻を表示
- `/user_info [show/reset]` - ユーザー情報の表示・リセット

## 🔧 新しいCogの作成

1. `cogs/`ディレクトリに新しいPythonファイルを作成
2. `BaseCog`を継承したクラスを作成
3. `@slash_command()`デコレータでコマンドを定義
4. テストファイルを`tests/`に追加

### 例: HelloCog

```python
# cogs/hello.py
from slackcogs import BaseCog, slash_command, SlackContext

class HelloCog(BaseCog):
    def __init__(self, app):
        super().__init__(app)
    
    @slash_command()
    async def greet(self, ctx: SlackContext, name: str):
        """挨拶コマンド"""
        await ctx.respond(f"こんにちは、{name}さん！")
```

## 🚀 デプロイ

### Heroku

```bash
# Herokuアプリを作成
heroku create your-slack-bot

# 環境変数を設定
heroku config:set SLACK_BOT_TOKEN=xoxb-your-token
heroku config:set SLACK_SIGNING_SECRET=your-secret
heroku config:set SLACK_APP_TOKEN=xapp-your-token

# デプロイ
git push heroku main
```

### AWS/GCP/Azure

Docker イメージを使用して、任意のクラウドプロバイダーにデプロイできます。

## 🛠️ 開発

### コード品質ツール

```bash
# コードフォーマット
black .

# リンター
flake8 .

# 型チェック
mypy .
```

### ホットリロード

開発環境では、ファイルの変更が自動的に検出され、Cogがリロードされます。

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## ❓ サポート

問題が発生した場合は、[Issues](../../issues)で報告してください。

## 🔗 関連リンク

- [Slack API Documentation](https://api.slack.com/)
- [SlackCogs Framework Documentation](https://slackcogs.readthedocs.io/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
