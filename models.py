from datetime import datetime
from typing import List

from sqlalchemy import DateTime, String, create_engine, func, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
    relationship,
)
from dotenv import load_dotenv
import os

load_dotenv()

USER_DB = os.getenv("USER_DB")
PASSWORD_DB = os.getenv("PASSWORD_DB")
NAME_DB = os.getenv("NAME_DB")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

POSTGRES_DSN = f"postgresql://{USER_DB}:{PASSWORD_DB}@{HOST}:{PORT}/{NAME_DB}"

engine = create_engine(POSTGRES_DSN)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "app_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(70), nullable=False)
    registration_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    advertisements: Mapped[List["Advertisement"]] = relationship(back_populates="owner")


class Advertisement(Base):
    __tablename__ = "app_advertisement"

    id: Mapped[int] = mapped_column(primary_key=True)
    heading: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    date_creation: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    owner_id: Mapped[int] = mapped_column(ForeignKey("app_user.id", ondelete="CASCADE"))
    owner: Mapped["User"] = relationship(back_populates="advertisements")


Base.metadata.create_all(bind=engine)
# Base.metadata.drop_all(bind=engine)
