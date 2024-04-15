from flask import Flask, request
from flask import jsonify
import json
from flask_cors import CORS
import pandas as pd

from db_control import crud, mymodels, readchatlog, updateroadmap

import requests
from datetime import datetime
import pytz

import openai
from openai import OpenAI
from dotenv import load_dotenv
import os

import textwrap  # テキストの分割
import dummy_message_and_prompt  # 　プロンプト検討用

# Azure Database for MySQL
# REST APIでありCRUDを持っている
app = Flask(__name__)
CORS(app)

# 環境変数を使用する
openai.api_key = os.getenv('OPENAI_API_KEY')

os.getenv("")


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

    # ユーザーとGPTのチャット履歴を時間順に並べてすべて取得する
    chatposts_all_df = readchatlog.readchalogall(values)

    # 　Unicodeエスケープしない
    result_json = chatposts_all_df.to_json(orient="records", force_ascii=False)

    return result_json, 200


# ChatPostsから会話の開始と終了を読み込んで、ChatRawDatasの内容を整理してjson形式で返す
# countで指定された数だけ返す
@app.route("/chatlogsmall", methods=["POST"])
def get_chatrawdatasmall():

    values_all = request.get_json()
    # values = {
    #     "parent_user_id": XX,
    #     "child_user_id": YY,
    #     "count": Z,
    # }
    print(values_all)

    values = {
        "parent_user_id": values_all.get("parent_user_id"),
        "child_user_id": values_all.get("child_user_id"),
    }
    count = values_all.get("count")

    # ユーザーとGPTのチャット履歴を時間順に並べて、最新ものをcount数だけ取得する
    chatpost_small_df = readchatlog.readchalogsmall(values, count)

    # 　Unicodeエスケープしない
    result_json = chatpost_small_df.to_json(orient="records", force_ascii=False)

    return result_json, 200


# ChatPostsから会話の開始と終了を読み込んで、ChatRawDatasの内容を整理してjson形式で返す
# countで指定された数だけ返す
@app.route("/chatsummary", methods=["POST"])
def set_chatsummary():

    values_all = request.get_json()
    # values = {
    #     "parent_user_id": XX,
    #     "child_user_id": YY,
    #     "count": Z,
    # }
    print(values_all)

    values = {
        "parent_user_id": values_all.get("parent_user_id"),
        "child_user_id": values_all.get("child_user_id"),
    }
    count = values_all.get("count")

    # ユーザーとGPTのチャット履歴を時間順に並べて、最新ものをcount数だけ取得する
    chatpost_small_df = readchatlog.readchalogsmall(values, count)
    # "role"と"content"だけ抜き出す
    message_df = chatpost_small_df[["role", "content"]]

    # GPT用要約時の"system"のプロンプトをダミーファイルから読み込み、syteメッセージを作成する
    system_content = dummy_message_and_prompt.make_dummy_message()
    # systemメッセージを追加する
    system_message_df = pd.DataFrame([{"role": "system", "content": dummy_message_and_prompt.make_system_message()}])
    system_message2_df = pd.DataFrame([{"role": "system", "content": dummy_message_and_prompt.make_system_message2()}])

    # 繋げたうえで、辞書形式にしてから、openAIのAPIへ渡す
    # 回答を安定させるために、systemメッセージで挟み込む
    message_df = pd.concat([system_message_df, message_df, system_message2_df])
    message_dict = message_df.to_dict(orient="records")

    # GPT要約の部分
    # client = OpenAI()
    # response = client.chat.completions.create(
    #     # model="gpt-4",
    #     # model="gpt-4-1106-preview",
    #     model="gpt-3.5-turbo",
    #     response_format={"type": "json_object"},

    #     # チャット履歴から渡す時はこちら
    #     # messages=message_dict,

    #     # 親子会話をダミーデータから渡す時はこちら
    #     messages=[
    #         {"role": "system", "content": dummy_message_and_prompt.make_system_message()},
    #         {"role": "user", "content": dummy_message_and_prompt.make_dummy_message()},
    #         {"role": "system", "content": dummy_message_and_prompt.make_system_message2()},
    #     ],
    #     temperature=0.2,
    #     max_tokens=500,
    # )

    # gpt_summaries = response.choices[0].message.content
    # GPT要約の部分ここまで

    # GPTのダミー回答（動作確認する際はこちらを使う）
    gpt_summaries = {
        "life_plan": {"1": "海外旅行の話を再度聞きたい", "2": "遺言や葬儀の希望、遺産の話をゆっくり話し合いたい"},
        "assets_money": {"1": "古い家や土地の遺産分割について"},
        "inheritance": {"1": "遺言に古い家や土地の処分方法を記載", "2": "遺産分割を家族で平和に解決したい"},
        "funeral_grave": {"1": "自然葬を希望", "2": "葬儀のスタイルについて具体的に話し合い"},
        "health_illness": {"1": "none"},
        "caregiving": {"1": "none"},
    }
    gpt_summaries = json.dumps(gpt_summaries, indent=4, ensure_ascii=False)
    # GPTのダミー回答ここまで

    gpt_summaries = json.loads(gpt_summaries)
    print(gpt_summaries)

    # 要約結果をChatSummariesへ格納
    for category, details in gpt_summaries.items():

        item_id = crud.get_item_id(mymodels.Items, category)
        for key, content in details.items():
            if content in ["none", "なし"]:  # 該当がない時
                break
            else:
                values = {
                    "parent_user_id": values_all.get("parent_user_id"),
                    "child_user_id": values_all.get("child_user_id"),
                    "item_id": item_id,
                    "content": content,
                }

                result = crud.insert_chatsummaris(mymodels.ChatSummaries, values)
                if result == "error":
                    return "error"

    # 　Unicodeエスケープしない
    result_json = chatpost_small_df.to_json(orient="records", force_ascii=False)

    # 要約格納後にRoadmapsの更新を行う
    updateroadmap.update_roadmaps(values_all.get("parent_user_id"))

    return gpt_summaries, 200


# ロードマップの読み込み
@app.route("/roadmaps", methods=["GET"])
def get_roadmaps():
    parent_user_id = request.args.get("parent_user_id")  # クエリパラメータ
    result_df = crud.read_roadmaps(mymodels.Roadmaps, parent_user_id)

    result_df = result_df[["item_id", "item_input_num", "item_state", "item_updated_at"]]
    # UTCからJST（日本時間）への変換
    result_df['item_updated_at'] = result_df['item_updated_at'].dt.tz_localize('UTC').dt.tz_convert('Asia/Tokyo')
    # 日付を文字列に変換（例: '2024-04-13 09:00'）
    result_df['item_updated_at'] = result_df['item_updated_at'].dt.strftime('%Y-%m-%d %H:%M')

    result_json = result_df.to_json(orient="records", force_ascii=False)

    return result_json, 200


# 終活項目のidと項目名の対応を読み込む
@app.route("/items", methods=["GET"])
def get_items():
    result_df = crud.read_items(mymodels.Items)
    result_json = result_df.to_json(orient="records", force_ascii=False)

    return result_json, 200


# 終活項目の詳細ページに必要な項目
@app.route("/roadmapdetails", methods=["GET"])
def get_roadmapdetails():
    parent_user_id = request.args.get("parent_user_id")  # クエリパラメータ
    child_user_id = request.args.get("child_user_id")  # クエリパラメータ
    item_name = request.args.get("item_name")  # クエリパラメータ

    print(parent_user_id, child_user_id, item_name)
    item_id = crud.get_item_id(mymodels.Items, item_name)

    # item_idに対応するロードマップ情報を取得
    roadmap_item_df = crud.get_select_roadmap(mymodels.Roadmaps, parent_user_id, item_id)
    roadmap_item_df = roadmap_item_df[["item_input_num", "item_state"]]
    roadmap_item_json = roadmap_item_df.to_json(orient="records", force_ascii=False)

    # チャット要約から対応するものを取得
    select_chatsummaries_df = crud.get_select_chatsummaries(mymodels.ChatSummaries, parent_user_id, child_user_id, item_id)
    select_chatsummaries_df = select_chatsummaries_df[["chat_summary_id", "content", "created_at"]]
    # UTCからJST（日本時間）への変換した後に文字列に変換（例: '2024-04-13 09:00'）
    select_chatsummaries_df['created_at'] = select_chatsummaries_df['created_at'].dt.tz_localize('UTC').dt.tz_convert('Asia/Tokyo')
    select_chatsummaries_df['created_at'] = select_chatsummaries_df['created_at'].dt.strftime('%Y-%m-%d %H:%M')

    # 　有効な要約が入っている場合は１行目のダミーデータを取り除く
    if len(select_chatsummaries_df) >= 2:
        select_chatsummaries_df = select_chatsummaries_df.iloc[1:]

    select_chatsummaries_json = select_chatsummaries_df.to_json(orient="records", force_ascii=False)
    # 手動要約から対応するものを取得
    select_manualsummaries_df = crud.get_select_manualsummaries(mymodels.ManualSummaries, parent_user_id, item_id)
    select_manualsummaries_df = select_manualsummaries_df[["manual_summary_id", "content", "updated_at"]]
    # UTCからJST（日本時間）への変換した後に文字列に変換（例: '2024-04-13 09:00'）
    select_manualsummaries_df['updated_at'] = select_manualsummaries_df['updated_at'].dt.tz_localize('UTC').dt.tz_convert('Asia/Tokyo')
    select_manualsummaries_df['updated_at'] = select_manualsummaries_df['updated_at'].dt.strftime('%Y-%m-%d %H:%M')
    select_manualsummaries_json = select_manualsummaries_df.to_json(orient="records", force_ascii=False)

    # 辞書としてまとめからjsonifyで変換する
    result_dict = {
        "roadmap": json.loads(roadmap_item_json),
        "chatsummaries": json.loads(select_chatsummaries_json),
        "manualsummaries": json.loads(select_manualsummaries_json),
    }

    return jsonify(result_dict), 200


# ChatPostsから会話の開始と終了を読み込んで、ChatRawDatasの内容を整理してjson形式で返す
# countで指定された数だけ返す
@app.route("/chatpostgpt", methods=["POST"])
def get_chatpsotgpt():

    values_all = request.get_json()
    # values = {
    #     "parent_user_id": XX,
    #     "child_user_id": YY,
    #     "count": Z,
    # }
    print(values_all)

    values = {
        "parent_user_id": values_all.get("parent_user_id"),
        "child_user_id": values_all.get("child_user_id"),
    }
    count = values_all.get("count")

    # ユーザーとGPTのチャット履歴を時間順に並べて、最新ものをcount数だけ取得する
    chatpost_small_df = readchatlog.readchalogsmall(values, count)
    # "role"と"content"だけ抜き出す
    message_df = chatpost_small_df[["role", "content"]]

    # 質問作成用のsystemメッセージを追加する
    system_message_df = pd.DataFrame([{"role": "system", "content": dummy_message_and_prompt.make_system_message_question()}])

    # 繋げたうえで、辞書形式にしてから、openAIのAPIへ渡す
    # 回答を安定させるために、systemメッセージで挟み込む
    message_df = pd.concat([system_message_df, message_df])
    message_dict = message_df.to_dict(orient="records")

    # GPTへ指示を出す部分
    client = OpenAI()
    response = client.chat.completions.create(
        # model="gpt-4",
        # model="gpt-4-1106-preview",
        model="gpt-3.5-turbo",
        messages=message_dict,
        temperature=0.2,
        max_tokens=500,
    )

    question = response.choices[0].message.content
    # GPTへ指示を出す部分ここまで

    # 返答内容をchatpostgptへ格納する
    values = {
        "parent_user_id": values_all.get("parent_user_id"),
        "child_user_id": values_all.get("child_user_id"),
        "content": question,
    }

    result = crud.insert_chatpostgpt(mymodels.ChatPostsGPT, values)

    # # 　Unicodeエスケープしない
    # result_json = chatpost_small_df.to_json(orient="records", force_ascii=False)

    return result, 200


# チャットの生データを挿入する
@app.route("/chatposttext", methods=["POST"])
def create_chattext():
    values = request.get_json()
    # values = {
    #     "parent_user_id": XX,
    #     "child_user_id": YY,
    #     "content": "テキスト（長文）",
    # }
    print(values)

    parent_user_id = values.get("parent_user_id")
    child_user_id = values.get("child_user_id")
    content = values.get("content")

    # ChatPostへ投稿用の開始時間の取得
    recording_start = datetime.utcnow()

    content_list = textwrap.wrap(content, 50)  # 文章を50文字毎に分割
    for part_of_contennt in content_list:
        values = {"parent_user_id": parent_user_id, "child_user_id": child_user_id, "content": part_of_contennt}

        result = crud.chatrawinsert(mymodels.ChatRawDatas, values)

    # ChatPostへ投稿用の終了時間の取得
    recording_end = datetime.utcnow()

    values = {
        "parent_user_id": parent_user_id,
        "child_user_id": child_user_id,
        "recording_start_datetime": recording_start,
        "recording_end_datetime": recording_end,
    }

    result = crud.chatpostinsert_rawdatetime(mymodels.ChatPosts, values)

    return result, 200
