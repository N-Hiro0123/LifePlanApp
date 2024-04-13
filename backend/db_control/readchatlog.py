from flask import Flask, request
from flask import jsonify
import json
from flask_cors import CORS
import pandas as pd

# app.pyを基準に指定すればよさそう
from db_control import crud, mymodels

import requests
import pytz

from datetime import datetime


def readchalogall(values):
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
    # "role"カラムを追加して、GPTの発言と分かるように"assistant"を入れておく
    chatposts_gpt_df["role"] = "assistant"

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

        result_dict_list.append({"chatpost_created_at": chatpost_created_at, "content": contents, "role": "user"})
    # 整理したユーザー投稿内容をdfへ変換する
    chatposts_user_df = pd.DataFrame(result_dict_list)

    # ユーザー投稿とGPT投稿を一つにまとめて、投稿順に並べ替える
    chatposts_all_df = pd.concat([chatposts_user_df, chatposts_gpt_df]).sort_values(by="chatpost_created_at")
    # Datatimeを文字列に直す

    # UTCからJST（日本時間）への変換後、文字列に変換
    chatposts_all_df['chatpost_created_at'] = chatposts_all_df['chatpost_created_at'].dt.tz_localize('UTC').dt.tz_convert('Asia/Tokyo')
    chatposts_all_df["chatpost_created_at"] = chatposts_all_df["chatpost_created_at"].dt.strftime('%Y-%m-%d %H:%M')

    return chatposts_all_df


# チャット履歴から最新のものをcount数だけ取得する
def readchalogsmall(values, count):

    # ChatPostsから録音開始時間と録音終了時間をすべて取り込む
    chatposts_df = crud.read_chatposts(mymodels.ChatPosts, values)

    # ChatPostsGPTからGPTからの投稿内容と作成時間を取り込む
    chatposts_gpt_df = crud.read_chatpostsgpt(mymodels.ChatPostsGPT, values)
    # 使いたいカラムだけ取り出す
    chatposts_gpt_df = chatposts_gpt_df[["chatpost_created_at", "content"]]
    # "role"カラムを追加して、GPTの発言と分かるように"assistant"を入れておく
    chatposts_gpt_df["role"] = "assistant"

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

        result_dict_list.append({"chatpost_created_at": chatpost_created_at, "content": contents, "role": "user"})
    # 整理したユーザー投稿内容をdfへ変換する
    chatposts_user_df = pd.DataFrame(result_dict_list)

    # ユーザー投稿とGPT投稿を一つにまとめて、投稿順に並べ替える
    chatposts_all_df = pd.concat([chatposts_user_df, chatposts_gpt_df]).sort_values(by="chatpost_created_at")

    # UTCからJST（日本時間）への変換後、Datatimeを文字列に直す
    chatposts_all_df['chatpost_created_at'] = chatposts_all_df['chatpost_created_at'].dt.tz_localize('UTC').dt.tz_convert('Asia/Tokyo')
    chatposts_all_df["chatpost_created_at"] = chatposts_all_df["chatpost_created_at"].dt.strftime('%Y-%m-%d %H:%M')

    # 末尾のcount行数だけ取り出す
    chatpost_small_df = chatposts_all_df.tail(count)

    return chatpost_small_df
