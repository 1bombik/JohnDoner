from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def open_workday():
    """
    Клавиатура открытия смены. Содержит кнопку открытия смены, от которой считается рабочее время.
    """
    buttons = [
        [
            InlineKeyboardButton(text='Открыть смену', callback_data='open')
        ]
    ]
    open_workday_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return open_workday_keyboard


def close_workday():
    """
    Клавиатура закрытия смены. Содержит кнопку закрытия смены. После нажатия высчитывается длительность смены.
    """
    buttons = [
        [
            InlineKeyboardButton(text='Закрыть смену', callback_data='close')
        ]
    ]
    close_workday_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return close_workday_keyboard
