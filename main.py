from config import Config
import logging
from datetime import timedelta, timezone
from aiogram import Dispatcher, Bot, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ParseMode
import tabulate
from filters import AskStats, AddNewVolume, DelVolume, NextPageVolumes
from filters import PrevPageVolumes, CancelPageVolumes
from kb import gen_kb_show_volume, gen_kb_add_volume, gen_kb_del_volume
from db import get_active_volumes, check_user, create_user, get_data_in_delta
from db import get_user_role, add_new_volume_db, del_volume_db
from functions import calculate_coefficient


CFG = Config()
DSN = CFG.get_dsn()
MAX_VOLUMES = 3


logging.basicConfig(level=logging.INFO)
bot = Bot(token=CFG.token)
dp = Dispatcher()

########################### Commands ###########################

@dp.message(Command(commands=['start']))
async def welcome(message: Message):
    if await check_user(CFG.get_dsn(), message):
        await message.answer('Ну ну, харэ стартули жать...')
    else:
        await create_user(CFG.get_dsn(), message)
        await message.answer(text='Зарегал тебя, давай приступим к работе\.'
                                  ' Твоя текущая роль **малец**',
                             parse_mode=ParseMode.MARKDOWN_V2)


@dp.message(Command(commands=['show']))
async def show_volume_user(message: Message):
    volumes = await get_active_volumes(CFG.get_dsn())
    await message.answer(text='Выбирай бродяга',
                         reply_markup=gen_kb_show_volume(volumes)
                         )


@dp.message(Command(commands=['add']))
async def add_volume_user(message: Message):
    role = await get_user_role(DSN, message)
    if role == 'junior':
        await message.answer(text='Недостаточно прав, ваша роль малец')
    elif len(await get_active_volumes(DSN)) >= MAX_VOLUMES:
        await message.answer(text='Достигнуто максимальное количество '
                                  'поставленных на мониторинг объемов: '
                                  f'{MAX_VOLUMES}')
    else:
        volumes = await get_active_volumes(CFG.get_dsn())
        await message.answer(
            text=f'Уже мониторим {", ".join(map(str, volumes))}\n'
                 f'можно добавить еще {MAX_VOLUMES - len(volumes)}, всего доступно {MAX_VOLUMES}\n\n'
                 'звездочкой (*) помечены те, что в мониторинге, '
                 'нажатие кнопки со звездочкой (*) приведет к удалению объема',
            reply_markup=gen_kb_add_volume(volumes, 0)
                            )


@dp.message(Command(commands=['del', 'remove']))
async def del_volume_user(message: Message):
    role = await get_user_role(DSN, message)
    if role == 'junior':
        await message.answer(text='Недостаточно прав, ваша роль малец')
    elif len(await get_active_volumes(DSN)) == 0:
        await message.answer(text='А нечего удалять, вот так...')
    else:
        volumes = await get_active_volumes(CFG.get_dsn())
        await message.answer(
            text=f'Достпные для удаления объемы {", ".join(map(str, volumes))}\n'
                 'нажатие кнопки удалит объем из мониторинга',
            reply_markup=gen_kb_del_volume(volumes)
                            )


########################### CallBacks ###########################

@dp.callback_query(AskStats())
async def show_volume_stats(callback: CallbackQuery, volume: int):
    # print(callback.model_dump_json(indent=4))
    tz = timedelta(minutes=300)
    head = ['10 минут', '1 час', '1 день']
    res = []
    res.append(['Лоты'] + [await get_data_in_delta(DSN, 'lots', timedelta(minutes=i), tz, volume) for i in (10, 60, 1440)])
    res.append(['Ракеты'] + [await get_data_in_delta(DSN, 'rockets', timedelta(minutes=i), tz, volume) for i in (10, 60, 1440)])
    res.append(['Аномалии'] + [await get_data_in_delta(DSN, 'anomaly', timedelta(minutes=i), tz, volume) for i in (10, 60, 1440)])
    res.append(['Продано'] + [await get_data_in_delta(DSN, 'sold', timedelta(minutes=i), tz, volume) for i in (10, 60, 1440)])
    l10, l60, l1440 = res[0][1], res[0][2], res[0][3]
    r10, r60, r1440 = res[1][1], res[1][2], res[1][3]
    a10, a60, a1440 = res[2][1], res[2][2], res[2][3]
    s10, s60, s1440 = res[3][1], res[3][2], res[3][3]
    k10 = calculate_coefficient(l10, r10, a10, s10)
    k60 = calculate_coefficient(l60, r60, a60, s60)
    k1440 = calculate_coefficient(l1440, r1440, a1440, s1440)
    res.append(['Процент проданых', f'{round(k10*100, 3)}%', f'{round(k60*100, 3)}%', f'{round(k1440*100, 3)}%'])
    text_msg = tabulate.tabulate(res, headers=head, )
    await callback.message.edit_text(text=f'Объем: {volume}\n```\n{text_msg}\n```', parse_mode=ParseMode.MARKDOWN_V2)


@dp.callback_query(AddNewVolume())
async def add_volume(callback: CallbackQuery, addvol: int):
    volumes = await get_active_volumes(DSN)
    if addvol in volumes:
        await callback.message.edit_text(
            text='Ктото опередил тебя бродяга!')
    elif len(volumes) == MAX_VOLUMES:
        await callback.message.edit_text(
            text='Уперлись в ограничения по количеству объемов')
    else:
        await add_new_volume_db(DSN, addvol)
        await callback.message.edit_text(
            text=f'В мониторинг добавлен объем {addvol}')


@dp.callback_query(DelVolume())
async def del_volume(callback: CallbackQuery, delvol: int):
    await del_volume_db(DSN, delvol)
    await callback.message.edit_text(
        text=f'Из мониторинга удален объем {delvol}')


@dp.callback_query(NextPageVolumes())
async def change_to_next_page(callback: CallbackQuery, nextpagevol: int):
    volumes = await get_active_volumes(CFG.get_dsn())
    await callback.message.edit_text(
        text=f'Уже мониторим {", ".join(map(str, volumes))}\n'
                f'можно добавить еще {MAX_VOLUMES - len(volumes)}, всего доступно {MAX_VOLUMES}\n\n'
                'звездочкой (*) помечены те, что в мониторинге, '
                'нажатие кнопки со звездочкой (*) приведет к удалению объема',
        reply_markup=gen_kb_add_volume(volumes, nextpagevol)
                        )

@dp.callback_query(PrevPageVolumes())
async def change_to_prev_page(callback: CallbackQuery, prevpagevol: int):
    volumes = await get_active_volumes(CFG.get_dsn())
    await callback.message.edit_text(
        text=f'Уже мониторим {", ".join(map(str, volumes))}\n'
                f'можно добавить еще {MAX_VOLUMES - len(volumes)}, всего доступно {MAX_VOLUMES}\n\n'
                'звездочкой (*) помечены те, что в мониторинге, '
                'нажатие кнопки со звездочкой (*) приведет к удалению объема',
        reply_markup=gen_kb_add_volume(volumes, prevpagevol)
                        )


@dp.callback_query(CancelPageVolumes())
async def cancel_volume_pages(callback: CallbackQuery):
    await callback.message.delete()


@dp.callback_query()
async def test(callback: CallbackQuery):
    print(callback.data)


if __name__ == '__main__':
    dp.run_polling(bot)
