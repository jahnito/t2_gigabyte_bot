import aiopg
from aiogram.types import Message, CallbackQuery
from datetime import timedelta, timezone


__all__ = [
            "get_active_volumes", "check_user", "create_user",
            "get_data_in_delta", "get_user_role", "add_new_volume_db",
            "del_volume_db",
           ]


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
    '''
    INSERT INTO "users" ("tg_id", "create_user", "update_user", "status", "role", "username", "firstname", "lastname")
    VALUES ('123456789', now(), now(), '1', 'intern', 'petruha', '', '');
    '''
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


async def get_data_in_delta(dsn: str, data: str, delta: timedelta,
                            tz: timedelta, volume: int):
    delta = delta.total_seconds() // 60
    tz = tz.total_seconds() // 60

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
