import asyncio
from aiogram import Bot
from config import Config


CFG = Config()
notifier = Bot(token=CFG.token)


async def send_message(tg_id, message):
    await notifier.send_message(tg_id, message)


async def main():
    c = 0
    while True:
        if c >= 1:
            break
        await send_message(133073976, 'hello petrushka, testiruem notifikator')
        await send_message(159421991, 'hello petrushka, testiruem notifikator')
        await send_message(277271712, 'hello petrushka, testiruem notifikator')
        c += 1


if __name__ == '__main__':
    asyncio.run(main())
