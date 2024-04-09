from flask import Flask, request
from flask import jsonify
import json
from flask_cors import CORS
import pandas as pd

from db_control import crud, mymodels

import requests

from datetime import datetime

# Azure Database for MySQL
# REST APIでありCRUDを持っている
app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "<p>Flask top page!</p>"


# チャットの生データを挿入する
@app.route("/chatrawdatas", methods=["POST"])
def create_chatrawdata():
    values = request.get_json()
    # values = {
    #     "parent_user_id": XX,
    #     "child_user_id": YY,
    #     "content": "会話したテキスト",
    # }
    print(values)

    result = crud.chatrawinsert(mymodels.ChatRawDatas, values)
    return result, 200


# サーバー時刻を返す
@app.route("/chatposts", methods=["GET"])
def get_chatpost():

    current_utc_datetime = datetime.utcnow().strftime(('%Y-%m-%d %H:%M:%S.%f'))
    result = {
        "created_at": current_utc_datetime,
    }

    return result, 200


# 投稿管理テーブルへ挿入する
@app.route("/chatposts", methods=["POST"])
def create_chatpost():
    values = request.get_json()
    # values = {
    #     "parent_user_id": 1,
    #     "child_user_id": 2,
    #     "recording_start_datetime": ('%Y-%m-%d %H:%M:%S.%f'),
    #     "recording_end_datetime": ('%Y-%m-%d %H:%M:%S.%f'),
    # }
    print(values)

    result = crud.chatpostinsert(mymodels.ChatPosts, values)
    return result, 200


# ChatPostsから会話の開始と終了を読み込んで、ChatRawDatasの内容を整理してjson形式で返す
@app.route("/chatlogall", methods=["POST"])
def get_chatrawdata():

    values = request.get_json()
    # values = {
    #     "parent_user_id": XX,
    #     "child_user_id": YY,
    # }
    print(values)

    # ChatPostsから録音開始時間と録音終了時間をすべて取り込む
    chatposts_df = crud.read_chatposts(mymodels.ChatPosts, values)

    # ChatPostsGPTからGPTからの投稿内容と作成時間を取り込む
    chatposts_gpt_df = crud.read_chatpostsgpt(mymodels.ChatPostsGPT, values)
    # 使いたいカラムだけ取り出す
    chatposts_gpt_df = chatposts_gpt_df[["chatpost_created_at", "content"]]
    # "post_user"カラムを追加して、GPTの発言と分かるように"gpt"を入れておく
    chatposts_gpt_df["post_user"] = "gpt"

    result_dict_list = []  # 　整理後の履歴を格納する

    # 開始時間と終了時間を使って、生データを整理する
    for i, chatpost_df in chatposts_df.iterrows():
        chatrawdatas_df = crud.read_chatrawdatas(mymodels.ChatRawDatas, chatpost_df)

        contents = ""  # 初期化
        for ii, chatrawdata_df in chatrawdatas_df.iterrows():
            contents = contents + chatrawdata_df["content"]

        # content以外は必要なものだけ取り出す

        # parent_user_id = chatpost_df["parent_user_id"]
        # child_user_id = chatpost_df["child_user_id"]
        # 特に録音停止時間をチャット投稿時間とする
        chatpost_created_at = chatpost_df["recording_end_datetime"]

        result_dict_list.append({"chatpost_created_at": chatpost_created_at, "content": contents, "post_user": "user"})
    # 整理したユーザー投稿内容をdfへ変換する
    chatposts_user_df = pd.DataFrame(result_dict_list)

    # ユーザー投稿とGPT投稿を一つにまとめて、投稿順に並べ替える
    chatposts_all_df = pd.concat([chatposts_user_df, chatposts_gpt_df]).sort_values(by="chatpost_created_at")
    # Datatimeを文字列に直す
    chatposts_all_df["chatpost_created_at"] = chatposts_all_df["chatpost_created_at"].dt.strftime('%Y-%m-%d %H:%M:%S.%f')

    # 　Unicodeエスケープしない
    result_json = chatposts_all_df.to_json(orient="records", force_ascii=False)

    return result_json, 200
