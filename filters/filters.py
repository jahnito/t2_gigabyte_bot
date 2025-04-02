from aiogram import F
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


__all__ = ['AskStats']


class AskStats(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, num = callback.data.split('_')
            if suf == 'volume' and num.isdigit:
                return {'volume': int(num)}
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False
