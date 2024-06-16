from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional
from aiogram.filters.callback_data import CallbackData


class PaymentCallbackFactory(CallbackData, prefix="pay"):
    choice: str
    value_gen: Optional[str] = None
    value_price: Optional[str] = None


# кноппки оценки
def get_kb_rate():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="1⭐", callback_data='1'
    )
    builder.button(
        text="2⭐", callback_data='2'
    )
    builder.button(
        text="3⭐", callback_data='3'
    )
    builder.button(
        text="4⭐", callback_data='4'
    )
    builder.button(
        text="5⭐", callback_data='5'
    )
    # Выравниваем кнопки по 5 в ряд
    builder.adjust(5)
    return builder.as_markup()


# Создаем объекты инлайн-кнопок
skip_btn = InlineKeyboardButton(
    text='Пропустить',
    callback_data='skip'
)

continue_btn = InlineKeyboardButton(
    text='Продолжить',
    callback_data='skip'
)

seller_btn = InlineKeyboardButton(
    text='Продающий',
    callback_data='seller'
)

engaging_btn = InlineKeyboardButton(
    text='Вовлекающий',
    callback_data='engaging'
)

say_btn = InlineKeyboardButton(
    text='Мне есть что сказать',
    callback_data='say'
)

offer_btn = InlineKeyboardButton(
    text='Нет, предложи',
    callback_data='offer'
)

agree_btn = InlineKeyboardButton(
    text='Согласен',
    callback_data='agree'
)

disagree_btn = InlineKeyboardButton(
    text='Не согласен',
    callback_data='disagree'
)
