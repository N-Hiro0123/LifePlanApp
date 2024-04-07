# uname() error回避
import platform

print("platform", platform.uname())
##テスト
##テスト2

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
