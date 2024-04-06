from sqlalchemy import ForeignKey, Integer, String, Date, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from datetime import datetime, date
import enum


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
