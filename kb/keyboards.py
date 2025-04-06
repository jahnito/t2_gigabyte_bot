from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

__all__ = ['gen_kb_show_volume', 'gen_kb_add_volume', 'gen_kb_del_volume']


def gen_kb_show_volume(volumes: list | tuple):
    if volumes:
        builder = InlineKeyboardBuilder()
        builder.row(*[InlineKeyboardButton(text=str(i), callback_data=f'volume_{i}') for i in volumes], width=4)
        return builder.as_markup()


def gen_kb_add_volume(volumes: list | tuple, page: int, range_vol: int = 50):
    first_button = page*range_vol + 1
    last_button = page*range_vol + range_vol + 1
    builder = InlineKeyboardBuilder()
    builder.add(*[InlineKeyboardButton(text=[f'{i}', f'{i}*'][i in volumes],
                callback_data=[f'addvol_{i}', f'delvol_{i}'][i in volumes])
                for i in range(first_button, last_button)])
    builder.adjust(5)
    reduce = [1, 0][page == 0]
    add = [1, 0][page == 3]
    btn_prev = InlineKeyboardButton(text='<<<', callback_data=f'prevpagevol_{page - reduce}')
    btn_next = InlineKeyboardButton(text='>>>', callback_data=f'nextpagevol_{page + add}')
    btn_cancel = InlineKeyboardButton(text='Отмена', callback_data=f'pagevol_cancel')
    builder.row(btn_prev, btn_cancel, btn_next)
    return builder.as_markup()


def gen_kb_del_volume(volumes: list | tuple):
    builder = InlineKeyboardBuilder()
    builder.row(*[InlineKeyboardButton(text=f'{i}', callback_data=f'delvol_{i}') for i in volumes])
    btn_cancel = InlineKeyboardButton(text='Отмена', callback_data=f'pagevol_cancel')
    builder.row(btn_cancel)
    return builder.as_markup()
