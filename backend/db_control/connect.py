# uname() error回避
import platform

print(platform.uname())
# 意図は理解しきれていないが入れておく


from sqlalchemy import create_engine
import sqlalchemy

import os

main_path = os.path.dirname(os.path.abspath(__file__))  # 絶対パスを取得
path = os.chdir(main_path)  # main_pathをカレントディレクトリにする
print(path)
engine = create_engine("sqlite:///LifePlan.db", echo=True)  # SQLiteにパスを入れる
