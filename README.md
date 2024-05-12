# LifePlanApp

## 概要

- 宿題パッケージと同じ形で作成
- バックエンドをFlask, フロントエンドをNext.jsで作成

## 準備

- バックエンドの準備

  - python仮想環境に対して、requirements.txtの内容をインストール
    - pip install -r requirements.txt
  - /backend直下に、.envファイルを作成する
    - 環境変数　OPENAI_API_KEY=XXXXXX

- フロントエンドの準備
  - /frontendにおいて、"npm install"を実行し、package.jsonの内容をインストール
  - /frontend直下に、.env.localファイルを置く
    - 環境変数　NEXT_PUBLIC_API_ENDPOINT=http://127.0.0.1:5000

## 実行方法

- アプリの実行方法（MVP動画作成時）
  - バックエンド
    - /backendにおいて、"flask --app app run"でサーバーを立ち上げる
  - フロントエンド
    - /frontendにおいて、"npm run dev"でサーバーを立ち上げる
  - フロントエンドのサーバーをインターネットブラウザで開く
    - Web Speech APIが使える必要がある Chrom, Safariなど
  - DBにダミーデータが入っており、表示できるのは以下のページ
    - /roadmap/1/2　：ロードマップ
    - /roadmap/1/2/[item_name]　：各詳細ページ
      - [item_name]は以下の６つのいずれか
      - ”life_plan", "assets_money", "inheritance", "funeral_grave","health_illness", "caregiving"
    - /roadmap/1/2/chat　：チャット画面
    - /roadmap/1/2/chatlog　：チャット履歴

## 補足など

- DBの初期化方法

  - 実行するとデータが蓄積され続けるため、DBを元に戻したい時には以下を実行してください

  1. /backend/db_control/LifePlan.dbを削除（DBの削除）
  2. /backend/db_control/create_tables.pyを実行（新規DBの作成）
  3. /backend/make_dummy_db.pyの実行（新規DBにダミーデータを追加）

  - ダミーデータに関してのメモ
    - 現在のプログラムではChatSummaries, ManualSummariesにダミーデータが必須（データが０の時エラーがでる）。アプリを完成させる際には、親データを作成するタイミングで、ダミーデータの挿入まで行う必要がある。
    - ChatSummariesのダミーデータは、他のデータが挿入されるとユーザーに表示されないようにしているので、削除せずに残しておいて問題ない。
    - ManualSummariesは、一つのデータを編集・更新する設計なので、その通りにすればよい

- GPTプロンプトについて

  - GPTプロンプト用のDBは使用しておらず、すべて以下のファイルに記載しています。
    - /backend/dummy_message_and_prompt.py
  - MVP動画の際に入力したテキストは上記のファイルに記載しています
    - 同ファイルの52行目　（１行になっているため見ずらいです）

- 使用したformatterとその設定
  - prettier：python以外（デフォルトで使用）
    - frontend\.prettierrc.yaml :prettierの設定ファイル
  - Black Formatter: python
    - black formatterの設定は以下のもの
    - "black-formatter.args": ["--line-length=200", "--skip-string-normalization"],
