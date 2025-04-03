# Sample API Server

FastAPIを使用したサンプルAPIサーバーです。

## 機能

- アイテムの作成 (Create)
- アイテムの取得 (Read)
- アイテムの更新 (Update)
- アイテムの削除 (Delete)

## セットアップ

1. 依存関係のインストール:
```bash
pip install -r requirements.txt
```

2. サーバーの起動:
```bash
python main.py
```

## API エンドポイント

- GET /: ウェルカムメッセージを返します
- GET /items/: 全てのアイテムを取得
- GET /items/{item_id}: 特定のアイテムを取得
- POST /items/: 新しいアイテムを作成
- PUT /items/{item_id}: 既存のアイテムを更新
- DELETE /items/{item_id}: アイテムを削除

## API ドキュメント

サーバー起動後、以下のURLでSwagger UIによるAPIドキュメントにアクセスできます：
- http://localhost:8000/docs
- http://localhost:8000/redoc
