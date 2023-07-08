# MyWallets API

WEB+DB PRESS Vol.136 特集記事「Python最新Web開発」の第6章のソースコードです

## ブランチ

- main

## 使用するライブラリのインストール

```bash
$ python3 -m venv env --upgrade-deps
$ source env/bin/activate
(env) $ pip install fastapi==0.100.0 \
 'SQLAlchemy[aiosqlite]==2.0.18' \
 'uvicorn[standard]==0.22.0'
```

## 開発サーバーの起動

```bash
(env) $ uvicorn app.main:app --reload
```

## ユニットテストの実行

```bash
(env) $ pip install pytest==7.4.0 httpx==0.24.1
(env) $ pytest app -v
```

