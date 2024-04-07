# uname() error回避
import platform

print("platform", platform.uname())


from sqlalchemy import create_engine, insert, delete, update, select
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json
import pandas as pd
from datetime import datetime, date

from db_control.connect import engine
from db_control.mymodels import ChatRawDatas


def chatrawinsert(mymodel, values):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    query = insert(mymodel).values(values)
    try:
        # トランザクションを開始
        with session.begin():
            # データの挿入
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("挿入に失敗しました")
        session.rollback()
        return "error"

    finally:
        # セッションを閉じる
        session.close()

    return "inserted"


def chatpostinsert(mymodel, values):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    # datetime文字列をdatetimeオブジェクトへ変換
    recording_start_time_str = values.get("recording_start_datetime")
    recording_end_time_str = values.get("recording_end_datetime")
    values["recording_start_datetime"] = datetime.strptime(recording_start_time_str, '%Y-%m-%d %H:%M:%S.%f')
    values["recording_end_datetime"] = datetime.strptime(recording_end_time_str, '%Y-%m-%d %H:%M:%S.%f')

    query = insert(mymodel).values(values)

    try:
        # トランザクションを開始
        with session.begin():
            # データの挿入
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("挿入に失敗しました")
        session.rollback()
        return "error"

    finally:
        # セッションを閉じる
        session.close()

    return "inserted"


def read_chatposts(mymodel, values):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    parent_user_id = values.get("parent_user_id")
    child_user_id = values.get("child_user_id")

    # paret_user_id, child_user_idが一致するものを抽出
    query = session.query(mymodel).filter(mymodel.parent_user_id == parent_user_id, mymodel.child_user_id == child_user_id)

    try:
        # query結果をpdにする場合はread_sqlでよいみたい
        df = pd.read_sql(query.statement, session.bind)

    except sqlalchemy.exc.IntegrityError as e:
        print("ChatPostsからの読み込みに失敗しました", e)
        session.rollback()
        return "error"

    finally:
        # セッションを閉じる
        session.close()

    return df


def read_chatrawdatas(mymodel, value):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    parent_user_id = value.get("parent_user_id")
    child_user_id = value.get("child_user_id")
    recording_start_datetime = value.get("recording_start_datetime")  # datetime
    recording_end_datetime = value.get("recording_end_datetime")  # datetime

    # paret_user_id, child_user_idが一致するものを抽出
    query = session.query(mymodel).filter(
        mymodel.parent_user_id == parent_user_id,
        mymodel.child_user_id == child_user_id,
        mymodel.created_at >= recording_start_datetime,
        mymodel.created_at <= recording_end_datetime,
    )

    try:
        # query結果をpdにする場合はread_sqlでよいみたい
        df = pd.read_sql(query.statement, session.bind)

    except sqlalchemy.exc.IntegrityError as e:
        print("ChatPostsからの読み込みに失敗しました", e)
        session.rollback()
        return "error"

    finally:
        # セッションを閉じる
        session.close()

    return df
