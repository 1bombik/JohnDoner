from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """
    Таблица с пользователями, которые использовали бота. Добавляются после команды /start
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)

    hours = relationship("Hour", back_populates="user")


class Hour(Base):
    """
    Таблица с данными о сменах сотрудников.
    """
    __tablename__ = 'hours'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    working_hours = Column(Float)

    user = relationship("User", back_populates="hours")
