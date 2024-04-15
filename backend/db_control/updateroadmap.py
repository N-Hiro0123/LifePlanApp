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

# app.pyを基準に指定すればよさそう
from db_control import crud, mymodels


def update_roadmaps(parent_user_id):

    # 項目をすべて取得する
    items_df = crud.read_items(mymodels.Items)

    # 現在のRoadmap状況を取得する Stateによって更新の仕方を変える
    roadmaps_before_df = crud.read_roadmaps(mymodels.Roadmaps, parent_user_id)

    for index, item in items_df.iterrows():

        df = roadmaps_before_df[roadmaps_before_df["item_id"] == item["item_id"]]

        # completedとなっているものは更新しない
        if (df["item_state"] == "completed").any():
            continue
        else:
            # チャット要約にある情報を取得してくる
            chatsummariesInfo_df = crud.get_chatsummaries_info(mymodels.ChatSummaries, parent_user_id, item["item_id"])
            # チャット要約の数を取得（ダミーデータ除く）
            item_input_num = len(chatsummariesInfo_df) - 1
            # 作成日を逆順でソートして、一つ目の最新の時間を取得
            chatsummariesInfo_df = chatsummariesInfo_df.sort_values(by="created_at", ascending=False)
            item_updated_at = chatsummariesInfo_df["created_at"][0]

            # item_input_num = 0(ダミーデータのみ)の時は更新しない
            if item_input_num == 0:
                continue
            else:
                values = {
                    "parent_user_id": parent_user_id,
                    "item_id": item["item_id"],
                    "item_input_num": item_input_num,
                    "item_state": "entering",
                    "item_updated_at": item_updated_at,
                }
                # Roadmapsを更新
                crud.update_roadmap(mymodels.Roadmaps, values)

    return "updated"
