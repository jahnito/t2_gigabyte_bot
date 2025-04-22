import asyncio
from config import Config
import logging
from datetime import timedelta
from aiogram import Dispatcher, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ParseMode
import tabulate
from filters import AskStats, AddNewVolume, DelVolume, NextPageVolumes
from filters import PrevPageVolumes, CancelPageVolumes
from filters import AddNotificationVolume, CancelNotificationVolumes
from filters import AddStartTimeNotification, AddEndTimeNotification
from filters import AddTzNotification, AddThresholdNotification
from filters import DelNotification, SetUserTz
from kb import gen_kb_show_volume, gen_kb_add_volume, gen_kb_del_volume
from kb import gen_kb_notifi_volume, gen_kb_notifi_time, gen_kb_notifi_tz
from kb import gen_kb_notifi_threshold, gen_kb_del_notifi, gen_kb_user_tz
from db import get_active_volumes, check_user, create_user, get_data_in_delta
from db import get_user_role, add_new_volume_db, del_volume_db, check_database
from db import create_admin, get_users, add_new_notification, add_notifier_tz
from db import check_vol_notifier, add_notifier_starttime, add_notifier_endtime
from db import add_notifier_threshold, get_notifier_lots, del_notifier_lots
from db import update_user_tz, get_user_tz
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
    if await check_user(DSN, message):
        await message.answer('Ну ну, харэ стартули жать...')
    elif len(await get_users(DSN, message)) == 0:
        await create_admin(DSN, message)
        await message.answer(text='Ты первый одел тапочки, теперь ты админ бота')
    else:
        await create_user(DSN, message)
        await message.answer(text='Зарегал тебя, выбери свою временную '
                                  'зону и приступим к работе\.'
                                  ' Твоя текущая роль **малец** 👶',
                             reply_markup=gen_kb_user_tz(),
                             parse_mode=ParseMode.MARKDOWN_V2)


@dp.message(Command(commands=['show']))
async def show_volume_user(message: Message):
    if await check_user(DSN, message):
        volumes = await get_active_volumes(CFG.get_dsn())
        await message.answer(text='Выбирай бродяга',
                         reply_markup=gen_kb_show_volume(volumes)
                         )
    else:
        await message.answer(text='Вы не зарегестрированы, запустите команду /start')


@dp.message(Command(commands=['add']))
async def add_volume_user(message: Message):
    if await check_user(DSN, message):
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
    else:
        await message.answer(text='Вы не зарегестрированы, запустите команду /start')


@dp.message(Command(commands=['del', 'remove']))
async def del_volume_user(message: Message):
    if await check_user(DSN, message):
        role = await get_user_role(DSN, message)
        if role == 'junior':
            await message.answer(text='Недостаточно прав, ваша роль малец')
        elif len(await get_active_volumes(DSN)) == 0:
            await message.answer(text='А нечего удалять, вот так...')
        else:
            volumes = await get_active_volumes(CFG.get_dsn())
            await message.answer(
                text=f'Доступные для удаления объемы {", ".join(map(str, volumes))}\n'
                    'нажатие кнопки удалит объем из мониторинга',
                reply_markup=gen_kb_del_volume(volumes)
                                )
    else:
        await message.answer(text='Вы не зарегестрированы, запустите команду /start')


@dp.message(Command(commands=['setnotification']))
async def set_notification_user(message: Message):
    if await check_user(DSN, message):
        role = await get_user_role(DSN, message)
        if role == 'junior':
            await message.answer(text='Недостаточно прав, ваша роль малец')
        elif len(await get_active_volumes(DSN)) == 0:
            await message.answer(
                text='А нечего поставить на уведомление, воть')
        else:
            volumes = await get_active_volumes(CFG.get_dsn())
            await message.answer(
                text=f'Доступные для уведомления объемы {", ".join(map(str, volumes))}\n'
                      'нажатие кнопки запустит мастер создания нотификации по объему',
                reply_markup=gen_kb_notifi_volume(volumes)
                                )
    else:
        await message.answer(
            text='Вы не зарегестрированы, запустите команду /start\n'
                 'хотя у меня есть стойкое ощущение, что это не поможет'
            )


@dp.message(Command(commands=['delnotification']))
async def set_notification_user(message: Message):
    if await check_user(DSN, message):
        role = await get_user_role(DSN, message)
        if role == 'junior':
            await message.answer(text='Недостаточно прав, ваша роль малец')
        else:
            volumes = await get_notifier_lots(CFG.get_dsn(), message)
            await message.answer(
                text=f'Доступные для удаления объемы {", ".join(map(lambda x: str(x[0]), volumes))}\n'
                      'нажатие кнопки  удалит уведомление по объему',
                reply_markup=gen_kb_del_notifi(volumes)
                                 )
    else:
        await message.answer(
            text='Вы не зарегестрированы, запустите команду /start\n'
                 'хотя у меня есть стойкое ощущение, что это не поможет'
            )


########################### CallBacks ###########################

@dp.callback_query(SetUserTz())
async def set_user_tz(callback: CallbackQuery, usertz: int):
    await update_user_tz(DSN, callback, usertz)
    await callback.message.edit_text(text=f'Твоя временная зона +{usertz}')


@dp.callback_query(AskStats())
async def show_volume_stats(callback: CallbackQuery, volume: int):
    tz = timedelta(minutes=300)
    periods = (10, 60)
    head = [f'{i} минут' for i in periods]
    res = []
    res.append(['Лоты'] + [await get_data_in_delta(DSN, 'lots', timedelta(minutes=i), tz, volume) for i in periods])
    res.append(['Ракеты'] + [await get_data_in_delta(DSN, 'rockets', timedelta(minutes=i), tz, volume) for i in periods])
    res.append(['Аномалии'] + [await get_data_in_delta(DSN, 'anomaly', timedelta(minutes=i), tz, volume) for i in periods])
    res.append(['Продано'] + [await get_data_in_delta(DSN, 'sold', timedelta(minutes=i), tz, volume) for i in periods])
    last_row = ['Продано (%)']
    for i in range(1, len(periods) + 1):
        last_row.append(round(calculate_coefficient(res[0][i],
                                              res[1][i],
                                              res[2][i],
                                              res[3][i]) * 100, 2))
    res.append(last_row)
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


@dp.callback_query(AddNotificationVolume())
async def add_notification_volume(callback: CallbackQuery, setvol: int):
    if await check_vol_notifier(DSN, callback, setvol):
        await callback.message.edit_text(
            text=f'Объем {setvol} уже добавлен')
    else:
        await add_new_notification(DSN, callback, setvol)
        await callback.message.edit_text(
            text=f'⬇️ В какой час начинать уведомлять по объему {setvol} 🕐\n',
            reply_markup=gen_kb_notifi_time('starttime', setvol)
        )


@dp.callback_query(AddStartTimeNotification())
async def add_notification_starttime(callback: CallbackQuery, vol: int, start_time: str):
    await add_notifier_starttime(DSN, callback, vol, start_time)
    await callback.message.edit_text(
        text=f'⬆️ В какой час заканчивать уведомлять по объему {vol} 🕥\n',
        reply_markup=gen_kb_notifi_time('endtime', vol)
    )


# @dp.callback_query(AddEndTimeNotification())
# async def add_notification_endtime(callback: CallbackQuery, vol: int, end_time: str):
#     await add_notifier_endtime(DSN, callback, vol, end_time)
#     await callback.message.edit_text(
#         text=f'🇷🇺 Выбери свою таймзону\n',
#         reply_markup=gen_kb_notifi_tz(vol)
#     )


@dp.callback_query(AddEndTimeNotification())
async def add_notification_tz(callback: CallbackQuery, vol: int, end_time: str):
    tz = await get_user_tz(DSN, callback)
    await add_notifier_endtime(DSN, callback, vol, end_time)
    await add_notifier_tz(DSN, callback, vol, tz)
    await callback.message.edit_text(
        text=f'На каком уровне тригерим для объема {vol}\n',
        reply_markup=gen_kb_notifi_threshold(vol)
    )


@dp.callback_query(AddThresholdNotification())
async def add_notification_threshold(callback: CallbackQuery, vol: int, threshold: str):
    await add_notifier_threshold(DSN, callback, vol, threshold)
    await callback.message.edit_text(
        text=f'Добавили уведомление для объема {vol}\n'
    )


@dp.callback_query(DelNotification())
async def del_notification(callback: CallbackQuery, vol: int):
    await del_notifier_lots(DSN, callback, vol)
    await callback.message.edit_text(
        text=f'Удалено уведомление для объема {vol}\n'
    )


@dp.callback_query(CancelNotificationVolumes())
async def cancel_notification_volume(callback: CallbackQuery):
    await callback.message.delete()


@dp.callback_query()
async def test(callback: CallbackQuery):
    print(callback.data)


if __name__ == '__main__':
    asyncio.run(check_database(DSN))
    dp.run_polling(bot)
