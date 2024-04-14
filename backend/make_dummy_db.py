# uname() error回避
import platform

print("platform", platform.uname())


from sqlalchemy import create_engine, insert, delete, update, select
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json
import pandas as pd

from db_control.connect import engine

# from db_control.mymodels import Users

from datetime import date, datetime

import db_control.mymodels as mymodels

from datetime import datetime  # 日時入力用


def InsertValue(mymodel, valuse):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    # 新規データの挿入
    query = insert(mymodel).values(values)

    # データの更新
    # query = update(mymodel).where(mymodel.user_id == values.get("user_id")).values(**values)

    try:
        # トランザクションを開始
        with session.begin():
            # データの挿入
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("挿入に失敗しました")
        session.rollback()

    # セッションを閉じる
    session.close()

    return


##################################################################################
# Users
mymodel = mymodels.Users

birthdate_str = "1980-01-01"
birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()  # dateオブジェクトへ変換

values = {
    # "user_id": 1,
    "user_name": 'AAA-子',
    "name": "AAA 子",
    "birthdate": birthdate,
    "address": "東京都",
    "password": "AAA",
    "parent_child_class": "child",  # "child" or "parent"
    "family_id": 1,
}

InsertValue(mymodel, values)  # DBへ値を挿入

birthdate_str = "1950-01-01"
birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()  # dateオブジェクトへ変換

values = {
    "user_name": 'AAA-親',
    "name": "AAA 親",
    "birthdate": birthdate,
    "address": "東京都",
    "password": "AAA",
    "parent_child_class": "parent",  # "child" or "parent"
    "family_id": 2,
}

InsertValue(mymodel, values)  # DBへ値を挿入


birthdate_str = "1980-02-02"
birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()  # dateオブジェクトへ変換

values = {
    # "user_id": 1,
    "user_name": 'BBB-子',
    "name": "BBB 子",
    "birthdate": birthdate,
    "address": "東京都",
    "password": "BBB",
    "parent_child_class": "child",  # "child" or "parent"
    "family_id": 3,
}

InsertValue(mymodel, values)  # DBへ値を挿入

birthdate_str = "1950-01-01"
birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()  # dateオブジェクトへ変換

values = {
    "user_name": 'BBB-親',
    "name": "BBB 親",
    "birthdate": birthdate,
    "address": "東京都",
    "password": "BBB",
    "parent_child_class": "parent",  # "child" or "parent"
    "family_id": 4,
}

InsertValue(mymodel, values)  # DBへ値を挿入

##################################################################################
# Items

mymodel = mymodels.Items
values = {"item_name": "life_plan"}
InsertValue(mymodel, values)  # DBへ値を挿入

values = {"item_name": "assets_money"}
InsertValue(mymodel, values)  # DBへ値を挿入

values = {"item_name": "inheritance"}
InsertValue(mymodel, values)  # DBへ値を挿入

values = {"item_name": "funeral_grave"}
InsertValue(mymodel, values)  # DBへ値を挿入

values = {"item_name": "health_illness"}
InsertValue(mymodel, values)  # DBへ値を挿入

values = {"item_name": "caregiving"}
InsertValue(mymodel, values)  # DBへ値を挿入

##################################################################################
# Children

mymodel = mymodels.Children
values = {
    "user_id": 1,
    "father_user_id": 2,
    # "mother_user_id": None,
    "relationship": "長男",
}
InsertValue(mymodel, values)  # DBへ値を挿入

values = {
    "user_id": 3,
    # "father_user_id": ,
    "mother_user_id": 4,
    "relationship": "次女",
}
InsertValue(mymodel, values)  # DBへ値を挿入
##################################################################################
# Parents

mymodel = mymodels.Parents
values = {
    "user_id": 2,
    "parent_class": "父",
}
InsertValue(mymodel, values)  # DBへ値を挿入

mymodel = mymodels.Parents
values = {
    "user_id": 4,
    "parent_class": "母",
}
InsertValue(mymodel, values)  # DBへ値を挿入

##################################################################################
# Roadmaps

mymodel = mymodels.Roadmaps

values = {
    # "roadmap_id": ,
    "parent_user_id": 2,
    "item_id": 1,
    "item_input_num": 0,
    "item_state": "unfilled",
    # "item_updated_at": ,
}

for i in range(1, 7):
    values["item_id"] = i
    InsertValue(mymodel, values)  # DBへ値を挿入

values = {
    # "roadmap_id": ,
    "parent_user_id": 4,
    "item_id": 1,
    "item_input_num": 0,
    "item_state": "unfilled",
    # "item_updated_at": ,
}

for i in range(1, 7):
    values["item_id"] = i
    InsertValue(mymodel, values)  # DBへ値を挿入
##################################################################################
# PromtCategories
mymodel = mymodels.PromtCategories
values = {
    "prompt_category_id": 1,
    "prompt_usage": "質問１",
}
InsertValue(mymodel, values)  # DBへ値を挿入

values = {
    "prompt_category_id": 2,
    "prompt_usage": "質問２",
}
InsertValue(mymodel, values)  # DBへ値を挿入
##################################################################################
# GptPrompts

mymodel = mymodels.GptPrompts
values = {
    # "prompt_id": 1,
    "item_id": 1,
    "prompt_category_id": 1,
    "content": "項目Xの要約のためのプロンプト",
}

for i in range(1, 7):
    values["item_id"] = i
    values["content"] = f"項目{i}の要約のプロンプト"
    InsertValue(mymodel, values)  # DBへ値を挿入
##################################################################################
# ChatPostsGPT　１回目

created_at = datetime.utcnow()

mymodel = mymodels.ChatPostsGPT
values = {
    # "post_id": 1,
    "parent_user_id": 2,
    "child_user_id": 1,
    "content": "お父さんも将来について話したいと思っていはずです。頑張って",
    "chatpost_created_at": created_at,
}
InsertValue(mymodel, values)  # DBへ値を挿入

##################################################################################
# ChatRawDatas
recording_start = datetime.utcnow()


mymodel = mymodels.ChatRawDatas
values = {
    # "chat_id": 1,
    "parent_user_id": 2,
    "child_user_id": 1,
    "content": "会話１",
    # "created_at": ,
}

values["content"] = "今日は終活の話を"
InsertValue(mymodel, values)  # DBへ値を挿入
values["content"] = "したいと思ってきました"
InsertValue(mymodel, values)  # DBへ値を挿入
values["content"] = "お父さんはどう思ってる"
InsertValue(mymodel, values)  # DBへ値を挿入
values["content"] = "世間で言われる終活について"
InsertValue(mymodel, values)  # DBへ値を挿入
values["content"] = "単語は聞くけど考えてない"
InsertValue(mymodel, values)  # DBへ値を挿入
values["content"] = "めんどくさい"
InsertValue(mymodel, values)  # DBへ値を挿入

##################################################################################
# ChatPosts

recording_end = datetime.utcnow()

mymodel = mymodels.ChatPosts
values = {
    # "post_id": 2,
    "parent_user_id": 2,
    "child_user_id": 1,
    "recording_start_datetime": recording_start,
    "recording_end_datetime": recording_end,
}
InsertValue(mymodel, values)  # DBへ値を挿入
##################################################################################
# ChatPostsGPT　２回目

created_at = datetime.utcnow()

mymodel = mymodels.ChatPostsGPT
values = {
    # "post_id": 1,
    "parent_user_id": 2,
    "child_user_id": 1,
    "content": "よい会話のスタートが切れましたね",
    "chatpost_created_at": created_at,
}
InsertValue(mymodel, values)  # DBへ値を挿入


##################################################################################
# ChatSummaries

mymodel = mymodels.ChatSummaries
values = {
    # "chat_summary_id": 1,
    "parent_user_id": 2,
    "child_user_id": 1,
    "item_id": 1,
    "content": "要約結果",
    # "created_at": record_datetime,
}

for i in range(1, 7):
    values["item_id"] = i
    values["content"] = "要約なし（ここに要約結果が保存されます）"
    InsertValue(mymodel, values)  # DBへ値を挿入

##################################################################################
# ChatSummaries

mymodel = mymodels.ManualSummaries
values = {
    # "manual_summary_id": 1,
    "parent_user_id": 2,
    "item_id": 1,
    "content": "要約結果",
    # "updated_at": record_datetime,
}

for i in range(1, 7):
    values["item_id"] = i
    values["content"] = f"項目{i}の手動要約のメモ"
    InsertValue(mymodel, values)  # DBへ値を挿入
