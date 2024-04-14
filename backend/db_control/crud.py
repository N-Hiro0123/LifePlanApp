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


def read_chatpostsgpt(mymodel, values):
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
        print("ChatPostsGPTからの読み込みに失敗しました", e)
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


def get_item_id(mymodel, item_name):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    # itme_nameに対応するitem_idを受け取る
    query = session.query(mymodel).filter(mymodel.item_name == item_name)

    try:
        items_obj = query.first()  # 無ければNoneが変える
        if items_obj is not None:
            item_id = items_obj.item_id  # idフィールドにitem_idが存在すると仮定
        else:
            item_id = None  # 見つからなかった場合はNoneを返す

    except sqlalchemy.exc.IntegrityError as e:
        print("itemsからの読み込みに失敗しました", e)
        session.rollback()
        return "error"

    finally:
        # セッションを閉じる
        session.close()

    return item_id


def insert_chatsummaris(mymodel, values):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    # values = {
    #     "parent_user_id": values_all.get("parent_user_id"),
    #     "child_user_id": values_all.get("child_user_id"),
    #     "item_id": item_id,
    #     "content": content,
    # }

    # datetime文字列をdatetimeオブジェクトへ変換
    parent_user_id = values.get("parent_user_id")
    child_user_id = values.get("child_user_id")
    item_id = values.get("item_id")
    content = values.get("content")

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


def read_roadmaps(mymodel, parent_user_id):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    # itme_nameに対応するitem_idを受け取る
    query = session.query(mymodel).filter(mymodel.parent_user_id == parent_user_id)

    try:
        # query結果をpdにする場合はread_sqlでよいみたい
        df = pd.read_sql(query.statement, session.bind)

    except sqlalchemy.exc.IntegrityError:
        print("roadmaps読み込みに失敗しました")
        session.rollback()
        return "error"

    finally:
        # セッションを閉じる
        session.close()

    return df


def read_items(mymodel):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(mymodel)  # すべて読み込む

    try:
        # query結果をpdにする場合はread_sqlでよいみたい
        df = pd.read_sql(query.statement, session.bind)

    except sqlalchemy.exc.IntegrityError:
        print("items読み込みに失敗しました")
        session.rollback()
        return "error"

    finally:
        # セッションを閉じる
        session.close()

    return df


def get_select_roadmap(mymodel, parent_user_id, item_id):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    # itme_nameに対応するitem_idを受け取る
    query = session.query(mymodel).filter(mymodel.parent_user_id == parent_user_id, mymodel.item_id == item_id)

    try:
        # query結果をpdにする場合はread_sqlでよいみたい
        df = pd.read_sql(query.statement, session.bind)

    except sqlalchemy.exc.IntegrityError as e:
        print("itemsからの読み込みに失敗しました", e)
        session.rollback()
        return "error"

    finally:
        # セッションを閉じる
        session.close()

    return df


def get_select_chatsummaries(mymodel, parent_user_id, child_user_id, item_id):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    # itme_nameに対応するitem_idを受け取る
    query = session.query(mymodel).filter(
        mymodel.parent_user_id == parent_user_id,
        mymodel.child_user_id == child_user_id,
        mymodel.item_id == item_id,
    )

    try:
        # query結果をpdにする場合はread_sqlでよいみたい
        df = pd.read_sql(query.statement, session.bind)

    except sqlalchemy.exc.IntegrityError as e:
        print("ChatSummariesからの読み込みに失敗しました", e)
        session.rollback()
        return "error"

    finally:
        # セッションを閉じる
        session.close()

    return df


def get_select_manualsummaries(mymodel, parent_user_id, item_id):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    # itme_nameに対応するitem_idを受け取る
    query = session.query(mymodel).filter(mymodel.parent_user_id == parent_user_id, mymodel.item_id == item_id)

    try:
        # query結果をpdにする場合はread_sqlでよいみたい
        df = pd.read_sql(query.statement, session.bind)

    except sqlalchemy.exc.IntegrityError as e:
        print("ManualSummariesからの読み込みに失敗しました", e)
        session.rollback()
        return "error"

    finally:
        # セッションを閉じる
        session.close()

    return df


def update_roadmap(mymodel, values):
    # values = {
    #     "parent_user_id": values.get("parent_user_id"),
    #     "item_id": item_id,
    #     "item_input_num": item_input_num,
    #     "item_updated_at": item_updated_at,
    # }

    parent_user_id = values.get("parent_user_id")
    item_id = values.get("item_id")
    item_input_num = values.get("item_input_num")
    item_state = values.get("item_state")
    item_updated_at = values.get("item_updated_at")

    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    # 更新する
    query = (
        session.query(mymodel)
        .filter(mymodel.parent_user_id == parent_user_id, mymodel.item_id == item_id)
        .update(
            {mymodel.item_input_num: item_input_num, mymodel.item_state: item_state, mymodel.item_updated_at: item_updated_at},
        )
    )

    try:
        # トランザクションをコミット
        session.commit()

    except sqlalchemy.exc.IntegrityError as e:
        print("ManualSummariesからの読み込みに失敗しました", e)
        session.rollback()
        return "error"

    finally:
        # セッションを閉じる
        session.close()

    return "put"


def get_chatsummaries_info(mymodel, parent_user_id, item_id):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    # itme_nameに対応するitem_idを受け取る
    query = session.query(mymodel).filter(mymodel.parent_user_id == parent_user_id, mymodel.item_id == item_id)

    try:
        # query結果をpdにする場合はread_sqlでよいみたい
        df = pd.read_sql(query.statement, session.bind)

    except sqlalchemy.exc.IntegrityError as e:
        print("ChatSummariesからの読み込みに失敗しました", e)
        session.rollback()
        return "error"

    finally:
        # セッションを閉じる
        session.close()

    return df


def insert_chatpostgpt(mymodel, values):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    # values = {
    #     "parent_user_id": values_all.get("parent_user_id"),
    #     "child_user_id": values_all.get("child_user_id"),
    #     "content": content,
    # }

    query = insert(mymodel).values(values)

    try:
        # トランザクションを開始
        with session.begin():
            # データの挿入
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("ChatPostsGPTへの挿入に失敗しました")
        session.rollback()
        return "error"

    finally:
        # セッションを閉じる
        session.close()

    return "inserted"
