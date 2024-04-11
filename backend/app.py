from flask import Flask, request
from flask import jsonify
import json
from flask_cors import CORS
import pandas as pd

from db_control import crud, mymodels, readchatlog

import requests
from datetime import datetime

import openai
from openai import OpenAI
from dotenv import load_dotenv
import os

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
def get_chatsummary():

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

    # systemメッセージを追加する
    system_message_df = pd.DataFrame(
        [
            {
                "role": "system",
                "content": "あなたは終活アドバイザー、終活の専門家です",
            }
        ]
    )

    # 繋げたうえで、辞書形式で渡す
    message_df = pd.concat([system_message_df, message_df])
    message_dict = message_df.to_dict(orient="records")

    system_content = """
       
    あなたは終活アドバイザー、終活の専門家です。
    以下の会話から終活に関する特定の情報を抽出し、終活ロードマップに沿った順序でカテゴリー分けし、要約してください。
    各カテゴリーに該当する内容がない場合は「なし」と回答してください。要約はそれぞれ200文字以内で行ってください。
    カテゴリーと順序:
    ライフプラン/自分史（学び、仕事、家族、住まい、趣味、旅行）
    資産・お金（口座情報、銀行名、証券会社名、保険会社名、不動産、支店名、金額、資産区分）
    相続（相続したい人の名前、相続したいものの詳細）
    葬式/お墓（葬儀の種類、葬儀社名、お寺・教会、場所、形態、墓の有無、承継者、法要、無墓希望、費用）
    健康/病気（診療科、病院名、病名、認知症や判断力低下時の希望、病名や余命の告知、緩和ケア、ホスピス入所）
    介護（介護施設名、介護サービス、介護者）
    出力方法：
    各カテゴリーについてはjson形式で出力してください。
    各カテゴリーのキーは以下のものを使ってください。
    "life_plan", "assets_money", "inheritance", "funeral_grave", "health_illness", "caregiving"
    各カテゴリーに該当する内容が複数ある場合は、数字をキーとして複数に分けて出力してください。
    該当する項目がない場合は、{"1": None}と格納してください
    また、一度出力した内容を見直したうえで、該当する項目がない箇所は"none"に修正してください。
    """

    user_content = """
    お父さん、今日はちょっと話があって…。でも、その前にお父さんの好きなコーヒー淹れたよ。おお、それはありがたい。何の話だね？」実は終活の話と、もう一つ…。お父さんが若い頃によく話してくれた、海外旅行の話をもう一度聞きたくて。海外旅行か…。あの頃は冒険だったなあ。でも、なぜ急に？いや、だってお父さんの話、本当に面白いんだもの。でも、その前に終活のこと。遺言や葬儀の希望、遺産の話も含めて、ゆっくり話し合いたいんだ。そうか、終活の話か。それは大事なことだ。遺言については、特に古い家や土地のことをどうしてほしいか書き記しておきたいな。それから、葬儀のスタイルも。お父さんがどんな風に見送られたいのか、具体的に聞いておきたい。シンプルで良いんだ。自然葬を考えている。そういえば、昔、あの旅行で森の中に迷い込んだことがあったな。自然の美しさと厳しさを同時に感じたよ。自然葬か…。お父さんらしいね。そして、その旅行話、また聞かせてよ。ああ、その話か。でも、遺産分割の話も重要だ。みんなで平和に解決したいからね。分かってる。でも、今日はお父さんの楽しい話も聞きたいんだ。終活の話はもちろん大切だけど、お父さんの人生の楽しい部分も、今のうちにたくさん共有したいから。なるほど、そういうことか。じゃあ、あの時の話から始めようか。インドでね、珍しいスパイスを買いに市場へ行ったんだけど…。ええ、それそれ！その話大好きなんだよね。話は長くなるが、いいかい？その後、終活のことも真剣に考えよう。家族の絆って、こういう共有からも深まるんだろうね。うん、終活も家族の思い出話も、全部がお父さんとの大切な時間。ありがとう、お父さん。いや、こちらこそありがとう。今日は良い一日だね。」
    """

    print(message_dict)

    client = OpenAI()

    response = client.chat.completions.create(
        # model="gpt-4",
        # model="gpt-4-1106-preview",
        model="gpt-3.5-turbo",
        response_format={"type": "json_object"},
        # messages=message_dict,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ],
        temperature=0.2,
        max_tokens=500,
    )
    print(response)
    result = response.choices[0].message.content

    # 　Unicodeエスケープしない
    result_json = chatpost_small_df.to_json(orient="records", force_ascii=False)

    return result, 200
