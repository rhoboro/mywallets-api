# MyWallets API

WEB+DB PRESS Vol.136 特集記事「Python最新Web開発」の第6章のソースコードです

## ブランチ

- main
    - ユニットテストの追加し、コード整形を適用した最終的なコード
- step01
    - 「アプリケーション全体に関わる共通処理の実装」節の完了時点
- step02
    - 「エンドポイントの実装」節の完了時点
- step03
    - 「ロジックの実装」節の完了時点

## 使用するライブラリのインストール

```bash
$ python3 -m venv env
$ . env/bin/activate
(env) $ pip install fastapi==0.95.2 \
 'SQLAlchemy[aiosqlite]==2.0.16' \
 'uvicorn[standard]==0.22.0'
```

## 開発サーバーの起動

```bash
(env) $ uvicorn app.main:app --reload
```

## ユニットテストの実行

```bash
(env) $ pip install pytest==7.2 httpx==0.24.1
(env) $ pytest app -v
```

