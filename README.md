# MyWallets API

WEB+DB PRESS Vol.136 特集記事「Python最新Web開発」の第6章のソースコードです。

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

## その他

本リポジトリはWEB+DB PRESS Vol.136のために用意したものですが、個人のOSS活動の一環として数年前から公開しているサンプルプロジェクト[rhoboro/async-fastapi-sqlalchemy](https://github.com/rhoboro/async-fastapi-sqlalchemy)があります。  
このプロジェクトではWEB+DB PRESS Vol.136ではスペースの都合上解説できなかった、DBマイグレーション管理やPostgreSQLを採用した場合のテスト用DB作成方法などを行っています。ぜひご参考にしてみてください。

