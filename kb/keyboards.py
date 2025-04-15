from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

__all__ = ['gen_kb_show_volume', 'gen_kb_add_volume', 'gen_kb_del_volume',
           'gen_kb_notifi_volume', 'gen_kb_notifi_time', 'gen_kb_notifi_tz',
           'gen_kb_notifi_threshold', 'gen_kb_del_notifi', 'gen_kb_user_tz'
           ]


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


def gen_kb_notifi_volume(volumes: list | tuple):
    builder = InlineKeyboardBuilder()
    builder.row(*[InlineKeyboardButton(text=f'{i}', callback_data=f'setvol_{i}') for i in volumes])
    btn_cancel = InlineKeyboardButton(text='Отмена', callback_data=f'setvol_cancel')
    builder.row(btn_cancel)
    return builder.as_markup()


def gen_kb_notifi_time(suffix: str, vol: int):
    builder = InlineKeyboardBuilder()
    builder.row(*[InlineKeyboardButton(text=f'{i}', callback_data=f'{suffix}_{vol}_{i:02}') for i in range(25)])
    builder.adjust(5)
    return builder.as_markup()


def gen_kb_notifi_tz(vol: int):
    tzones = {
        'KALT +2': 2, 'MSK +3': 3, 'SAMT +4': 4,
        'YEKT +5': 5, 'OMST +6': 6, 'KRAT +7': 7,
        'IRKT +8': 8, 'YAKT +9': 9, 'VLAT +10': 10,
        'MAGT +11': 11, 'PETT +12': 12
              }
    builder = InlineKeyboardBuilder()
    builder.row(*[InlineKeyboardButton(text=f'{k}', callback_data=f'tz_{vol}_{v}') for k, v in tzones.items()])
    builder.adjust(3)
    return builder.as_markup()


def gen_kb_notifi_threshold(vol: int):
    builder = InlineKeyboardBuilder()
    builder.row(*[InlineKeyboardButton(text=f'{i}%', callback_data=f'threshold_{vol}_{i}') for i in range(40, 125, 5)])
    builder.adjust(6)
    return builder.as_markup()


def gen_kb_del_notifi(volumes: list):
    builder = InlineKeyboardBuilder()
    builder.row(*[InlineKeyboardButton(text=f'Объем {i[0]} с {i[1]} до {i[2]} порог {i[3]}%', callback_data=f'delnot_{i[0]}') for i in volumes])
    builder.adjust(1)
    return builder.as_markup()


def gen_kb_user_tz():
    tzones = {
        '⛵️ Калининград +2': 2, '🐉 Москва +3': 3, '🦌 Самара +4': 4,
        '🧸 Екатеринбург +5': 5, '🌺 Омск +6': 6, '🦁 Красноярск +7': 7,
        '🐈‍⬛ Иркутск +8': 8, '🏇 Якутия +9': 9, '🐅 Владивосток +10': 10,
        '🦌 Магадан +11': 11, '🌋 Камчатка +12': 12
              }
    builder = InlineKeyboardBuilder()
    builder.row(*[InlineKeyboardButton(text=f'{k}', callback_data=f'usertz_{v}') for k, v in tzones.items()])
    builder.adjust(2)
    return builder.as_markup()