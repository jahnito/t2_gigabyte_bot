from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

__all__ = ['gen_kb_set_volume']


def gen_kb_set_volume(volumes: list|tuple):
    if volumes:
        builder = InlineKeyboardBuilder()
        builder.row(*[InlineKeyboardButton(text=str(i), callback_data=f'volume_{i}') for i in volumes], width=4)
        # btn_agree = InlineKeyboardButton(text='✅ Принять', callback_data=f'volume_agree')
        # btn_cancel = InlineKeyboardButton(text='⭕️ Отмена', callback_data=f'volume_agree')
        # builder.adjust(5)
        # builder.row(btn_agree, btn_cancel)
        return builder.as_markup()
