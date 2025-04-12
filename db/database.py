import aiopg
from aiogram.types import Message, CallbackQuery
from datetime import timedelta

import asyncio

__all__ = [
            "get_active_volumes", "check_user", "create_user", "create_admin",
            "get_data_in_delta", "get_user_role", "add_new_volume_db",
            "del_volume_db", "check_database", "get_users",
            "add_new_notification", "check_vol_notifier", "add_notifier_tz",
            "add_notifier_starttime", "add_notifier_endtime",
            "add_notifier_threshold", "get_notifier_lots", "del_notifier_lots"
           ]


async def check_database(dsn: str, dbconf: str = 'setup/db_pg.sql'):
    with open(dbconf) as dump:
        query = dump.read()
    pool = await aiopg.create_pool(dsn)
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
            await conn.close()
    except Exception as e:
        print(e)
        return None


async def get_active_volumes(dsn: str) -> tuple:
    '''
    Возвращает кортеж с торгуемыми объемами, которые находятся в мониторинге
    '''
    query = 'SELECT volume FROM volumes ORDER BY volume ASC'
    pool = await aiopg.create_pool(dsn)
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                ret = await cursor.fetchall()
            await conn.close()
        return tuple(i[0] for i in ret)
    except Exception as e:
        print(e)
        return None


async def check_user(dsn: str, m: Message) -> bool:
    '''
    Функция проверяет существование пользователя в БД
    '''
    query = f'SELECT count(*) FROM users WHERE tg_id = {m.from_user.id};'
    pool = await aiopg.create_pool(dsn)
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                ret = await cursor.fetchone()
            await conn.close()
        if ret[0]:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return None


async def get_users(dsn: str, m: Message) -> tuple:
    query = 'SELECT * FROM users'
    pool = await aiopg.create_pool(dsn)
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                ret = await cursor.fetchall()
            await conn.close()
            return ret
    except Exception as e:
        print(e)
        return None


async def get_user_role(dsn: str, m: Message) -> str:
    '''
    Функция возвращает роль пользователя в строке
    '''
    query = f'SELECT role FROM users WHERE tg_id = {m.from_user.id}'
    pool = await aiopg.create_pool(dsn)
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                ret = await cursor.fetchone()
            await conn.close()
        return ret[0].strip()
    except Exception as e:
        print(e)
        return None


async def create_user(dsn: str, m: Message):
    query = 'INSERT INTO "users" ("tg_id", "create_user", "update_user", "status", "role", "username", "firstname", "lastname")'\
            f'VALUES ({m.from_user.id}, now(), now(), {1}, \'junior\', \'{m.from_user.username}\', \'{m.from_user.first_name}\', \'{m.from_user.last_name}\');'
    pool = await aiopg.create_pool(dsn)
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
            await conn.close()
    except Exception as e:
        print(e)
        return None


async def create_admin(dsn: str, m: Message):
    query = 'INSERT INTO "users" ("tg_id", "create_user", "update_user", "status", "role", "username", "firstname", "lastname")'\
            f'VALUES ({m.from_user.id}, now(), now(), {1}, \'senior\', \'{m.from_user.username}\', \'{m.from_user.first_name}\', \'{m.from_user.last_name}\');'
    pool = await aiopg.create_pool(dsn)
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
            await conn.close()
    except Exception as e:
        print(e)
        return None


async def get_data_in_delta(dsn: str, data: str, delta: timedelta,
                            tz: timedelta, volume: int):
    delta = delta.total_seconds() // 60
    # tz = tz.total_seconds() // 60

    query = f'SELECT sum(cnt) FROM {data} WHERE dtime >= (now() - interval \''\
            f' {delta} minutes\')'\
            f' and volume = {volume}'

    pool = await aiopg.create_pool(dsn)
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                ret = await cursor.fetchall()
            await conn.close()
        return ret[0][0]
    except Exception as e:
        print(e)
        return None


async def add_new_volume_db(dsn: str, addvol: int):
    query = f'INSERT INTO volumes (volume) VALUES ({addvol})'
    pool = await aiopg.create_pool(dsn)
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
            await conn.close()
        return True
    except Exception as e:
        print(e)
        return None


async def del_volume_db(dsn: str, delvol: int):
    query = f'DELETE FROM volumes WHERE volume = {delvol}'
    pool = await aiopg.create_pool(dsn)
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
            await conn.close()
        return True
    except Exception as e:
        print(e)
        return None


async def add_new_notification(dsn: str, message: Message, vol: int):
    query = f'INSERT INTO notifier (tg_id, volume) VALUES '\
            f'({message.from_user.id}, {vol})'
    pool = await aiopg.create_pool(dsn)
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
            await conn.close()
        return True
    except Exception as e:
        print(e)
        return None


async def check_vol_notifier(dsn: str, m: Message | CallbackQuery, vol: int) -> int:
    '''
    Функция проверяет наличие существующего
    волюма в нотификации для пользователя
    '''
    query = f'SELECT volume FROM notifier '\
            f'WHERE tg_id = {m.from_user.id} and volume = {vol}'
    pool = await aiopg.create_pool(dsn)
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                ret = await cursor.fetchone()
            await conn.close()
        if ret[0]:
            return True
        else:
            return False
    except Exception as e:
        # print(e)
        return None


async def add_notifier_starttime(dsn: str,
                                 m: Message | CallbackQuery,
                                 vol: int,
                                 start_time: str
                                 ) -> int:
    '''
    Функция вносит время старта нотификации для волюма
    '''
    query = f'UPDATE notifier SET '\
            f'start_time = \'{start_time}:00:00\' '\
            f'WHERE tg_id = {m.from_user.id} and volume = {vol}'
    pool = await aiopg.create_pool(dsn)
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
            await conn.close()
    except Exception as e:
        return None


async def add_notifier_endtime(dsn: str,
                               m: Message | CallbackQuery,
                               vol: int,
                               end_time: str
                               ) -> int:
    '''
    Функция вносит время старта нотификации для волюма
    '''
    query = f'UPDATE notifier SET '\
            f'end_time = \'{end_time}:00:00\' '\
            f'WHERE tg_id = {m.from_user.id} and volume = {vol}'
    pool = await aiopg.create_pool(dsn)
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
            await conn.close()
    except Exception as e:
        return None


async def add_notifier_tz(dsn: str,
                          m: Message | CallbackQuery,
                          vol: int,
                          tz: int
                          ) -> int:
    '''
    Функция вносит таймзхону пользователя в нотификации для волюма
    '''
    query = f'UPDATE notifier SET '\
            f'tz = {tz} '\
            f'WHERE tg_id = {m.from_user.id} and volume = {vol}'
    pool = await aiopg.create_pool(dsn)
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
            await conn.close()
    except Exception:
        return None


async def add_notifier_threshold(dsn: str,
                          m: Message | CallbackQuery,
                          vol: int,
                          threshold: int
                          ) -> int:
    '''
    Функция вносит пороговое значение, после которого начинает высылать уведомления
    '''
    query = f'UPDATE notifier SET '\
            f'threshold = {threshold} '\
            f'WHERE tg_id = {m.from_user.id} and volume = {vol}'
    pool = await aiopg.create_pool(dsn)
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
            await conn.close()
    except Exception:
        return None


async def get_notifier_lots(dsn: str, m: Message | CallbackQuery):
    '''
    SELECT * FROM notifier WHERE tg_id = 133073976;
    '''
    query = f'SELECT volume, start_time, end_time, threshold FROM notifier WHERE tg_id = {m.from_user.id} ORDER BY volume'
    pool = await aiopg.create_pool(dsn)
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                ret = await cursor.fetchall()
            await conn.close()
            return ret
    except Exception:
        return None


async def del_notifier_lots(dsn: str, m: Message | CallbackQuery, vol: int):
    '''
    Удаление нотификации для объема
    '''
    query = f'DELETE FROM notifier WHERE tg_id = {m.from_user.id} and volume = {vol}'
    pool = await aiopg.create_pool(dsn)
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
            await conn.close()
    except Exception:
        return None
