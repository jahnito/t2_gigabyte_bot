import asyncio
from aiogram import Bot
from aiogram.enums import ParseMode
from config import Config
from db import get_data_in_delta, get_notifier_volumes, get_notifier_users
from db import set_notifier_user_status
from datetime import timedelta
import tabulate

CFG = Config()
DSN = CFG.get_dsn()
notifier = Bot(token=CFG.token)


async def check_notifi():
    volumes = await get_notifier_volumes(DSN)
    if volumes:
        for v in volumes:
            data_vol = await calc_coef(v)
            users = await get_notifier_users(DSN, v)
            for user in users:
                # Если у пользователя есть коэф сверяем его с текущим
                # также проверяем статус направлялось ли уведомление (1)
                if user[-1] and data_vol[-1] >= user[-1] and not user[-2]:
                    await set_notifier_user_status(DSN, v, user[0], 1)
                    try:
                        await send_message_now(user, data_vol, v)
                    except Exception:
                        pass
                # Все тоже самое только, тут смотрим если коэф меньше
                elif user[-1] and data_vol[-1] < user[-1] and user[-2]:
                    await set_notifier_user_status(DSN, v, user[0], 0)
                    try:
                        await send_message_lost(user, data_vol, v)
                    except Exception:
                        pass
    else:
        await asyncio.sleep(30)


async def calc_coef(volume):
    tz = timedelta(minutes=300)
    res = []
    res.append(await get_data_in_delta(DSN, 'lots', timedelta(minutes=10), tz, volume))
    res.append(await get_data_in_delta(DSN, 'rockets', timedelta(minutes=10), tz, volume))
    res.append(await get_data_in_delta(DSN, 'anomaly', timedelta(minutes=10), tz, volume) )
    res.append(await get_data_in_delta(DSN, 'sold', timedelta(minutes=10), tz, volume))
    if sum(res[:3]):
        res.append((res[3]/sum(res[:3])) * 100)
    else:
        res.append(res[3] * 100)
    return res


async def send_message_now(user_data, data_vol, volume):
    tg_id = user_data[0]
    data = []
    head = ['10 минут']
    data.append(['Лоты', data_vol[0]])
    data.append(['Ракеты', data_vol[1]])
    data.append(['Аномалии', data_vol[2]])
    data.append(['Продажи', data_vol[3]])
    data.append(['Процент проданых', data_vol[4]])
    message = f'✅ Пора делать ракету дружок на объеме **{volume}**'
    message += '```' + tabulate.tabulate(data, headers=head) + '```'
    await notifier.send_message(tg_id, message, parse_mode=ParseMode.MARKDOWN_V2)


async def send_message_lost(user_data, data_vol, volume):
    tg_id = user_data[0]
    data = []
    head = ['10 минут']
    data.append(['Лоты', data_vol[0]])
    data.append(['Ракеты', data_vol[1]])
    data.append(['Аномалии', data_vol[2]])
    data.append(['Продажи', data_vol[3]])
    data.append(['Процент проданых', data_vol[4]])
    message = f'⛔️ Для объема **{volume}** поезд ушел, жди другой'
    message += '```' + tabulate.tabulate(data, headers=head) + '```'
    await notifier.send_message(tg_id, message, parse_mode=ParseMode.MARKDOWN_V2)


async def main():
    while True:
        await check_notifi()


if __name__ == '__main__':
    asyncio.run(main())
