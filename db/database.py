import aiopg
from aiogram.types import Message, CallbackQuery


__all__ = ["get_active_volumes", "check_user", "create_user"]


async def get_active_volumes(dsn):
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


async def check_user(dsn, m: Message):
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


async def create_user(dsn, m: Message):
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


