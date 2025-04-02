from config import Config
import logging
from aiogram import Dispatcher, Bot, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from filters import AskStats
from kb import gen_kb_set_volume
from db import get_active_volumes, check_user, create_user


CFG = Config()


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
        await message.answer('Зарегал тебя, давай приступим к работе. Твоя роль junior')


@dp.message(Command(commands=['show']))
async def set_volume_user(message: Message):
    volumes = await get_active_volumes(CFG.get_dsn())
    await message.answer(text='Выбирай бродяга',
                         reply_markup=gen_kb_set_volume(volumes)
                         )


########################### CallBacks ###########################

@dp.callback_query(AskStats())
async def show_volume_stats(callback: CallbackQuery, volume: int):
    print(callback.data)
    await callback.message.answer(text=str(volume))



if __name__ == '__main__':
    print(CFG.get_dsn())
    dp.run_polling(bot)