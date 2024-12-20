from datetime import datetime
from aiogram.types import Message, CallbackQuery
from keyboard import open_workday, close_workday

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Hour
from private_data import admins

engine = create_engine('postgresql://dima:d1ma@localhost:5432/johndoner')
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

async def start_handler(message: Message):
    """
    Обработчик команды /start.
    """
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    if not user:
        user = User(
            telegram_id = message.from_user.id,
            username = message.from_user.username
        )
        session.add(user)
        session.commit()

    await message.answer(f"Привет, {message.from_user.first_name}!\n"
                         f" Чтобы начать смену нажми кнопку «Открыть смену»",
                         reply_markup=open_workday())


async def process_open_button(query: CallbackQuery):
    """
    Обработчик кнопки «Открыть смену».
    """
    data = query.data

    if data == 'open':
        open_time = datetime.now()
        user = session.query(User).filter_by(telegram_id=query.from_user.id).first()
        hour = Hour(
            user = user,
            date = datetime.now().date(),
            start_time = open_time.time()
        )
        session.add(hour)
        session.commit()

        await query.message.edit_text(f"Смена открыта! Продуктивного дня!\n"
                                      f"Не забудь нажать «Закрыть смену» в конце дня :)",
                                      reply_markup=close_workday())


async def process_close_button(query: CallbackQuery):
    """
    Обработчик кнопки «Закрыть смену».
    """
    data = query.data

    if data == 'close':
        close_time = datetime.now()

        user = session.query(User).filter_by(telegram_id=query.from_user.id).first()
        last_hour = session.query(Hour).filter_by(user=user, end_time=None).order_by(Hour.id.desc()).first()
        open_time = last_hour.start_time
        open_datetime = datetime.combine(close_time.date(), open_time)

        working_time = close_time - open_datetime
        working_time = working_time.total_seconds()
        if working_time > 21600:  # если рабочее время больше 6 часов,
            working_time -= 1800  # отнять 30 минут обеда
        elif working_time > 14400:  # если рабочее время больше 4 часов, т.е. 4-6,
            working_time -= 900  # отнять 15 минут обеда
        hours, remainder = divmod(working_time, 3600)
        minutes, _ = divmod(remainder, 60)

        last_hour.end_time = close_time.time()
        last_hour.working_hours = working_time / 3600
        session.commit()

        await query.message.edit_text(
            f"Отличная работа, {query.from_user.first_name}!\n"
            f"{last_hour.date.day()}.{last_hour.date.month()}.{last_hour.date.year()}"
            f" ты работал {int(hours)} часов {int(minutes)} минут.",
            reply_markup=None)

        await query.message.answer(
            f"Чтобы начать новую смену нажми Открыть смену",
            reply_markup=open_workday())

        for admin in admins: # пересылка сообщений всем админам
            await query.message.forward(chat_id=admin)
