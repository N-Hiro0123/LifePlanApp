from sqlalchemy import ForeignKey, Integer, String, Date, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from datetime import datetime, date


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_name: Mapped[str] = mapped_column(String(50), unique=True)
    name: Mapped[str] = mapped_column(String(50))
    birthdate: Mapped[date] = mapped_column(Date)
    address: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    parent_child_class: Mapped[str] = mapped_column(String(50), nullable=False)
    family_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), nullable=True)


class Children(Base):
    __tablename__ = "children"
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), primary_key=True)
    father_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), nullable=True)
    mather_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), nullable=True)
    relationship: Mapped[str] = mapped_column(String(50))


class Parents(Base):
    __tablename__ = "parents"
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), primary_key=True)
    parent_child_class: Mapped[str] = mapped_column(String(50))


class Roadmaps(Base):
    __tablename__ = "roadmaps"
    roadmap_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parent_user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'))
    item_id: Mapped[int] = mapped_column(Integer, ForeignKey('items.item_id'))
    item_input_num: Mapped[int] = mapped_column(Integer, nullable=True)
    item_state: Mapped[str] = mapped_column(String(50))
    item_updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Items(Base):
    __tablename__ = "items"
    item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    itme_name: Mapped[str] = mapped_column(String(50))


class PromtCategories(Base):
    __tablename__ = "promtcategories"
    prompt_category_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    prompt_usage: Mapped[str] = mapped_column(String(50))


class GptPrompts(Base):
    __tablename__ = "gptprompts"
    prompt_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(Integer, ForeignKey('items.item_id'), nullable=True)
    prompt_category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('promtcategories.prompt_category_id'), nullable=True
    )
    content: Mapped[str] = mapped_column(String)


class ChatRawDatas(Base):
    __tablename__ = "chatrawdatas"
    chat_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parent_user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'))
    child_user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'))
    content: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ChatPosts(Base):
    __tablename__ = "chatposts"
    post_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parent_user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'))
    child_user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'))
    recording_start_datetime: Mapped[date] = mapped_column(DateTime)
    recording_end_datetime: Mapped[date] = mapped_column(DateTime)


class ChatSummaries(Base):
    __tablename__ = "chatsummaries"
    chat_summary_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parent_user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'))
    child_user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'))
    item_id: Mapped[int] = mapped_column(Integer, ForeignKey('items.item_id'), nullable=True)
    content: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ManualSummaries(Base):
    __tablename__ = "manualsummaries"
    manual_summary_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parent_user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'))
    item_id: Mapped[int] = mapped_column(Integer, ForeignKey('items.item_id'), nullable=True)
    content: Mapped[str] = mapped_column(String)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
