from aiogram import F
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


__all__ = [
    'AskStats', 'AddNewVolume', 'DelVolume',
    'NextPageVolumes', 'PrevPageVolumes', 'CancelPageVolumes'
           ]


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


class AddNewVolume(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, num = callback.data.split('_')
            if suf == 'addvol' and num.isdigit():
                return {'addvol': int(num)}
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


class DelVolume(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, num = callback.data.split('_')
            if suf == 'delvol' and num.isdigit():
                return {'delvol': int(num)}
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


class NextPageVolumes(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, num = callback.data.split('_')
            if suf == 'nextpagevol' and num.isdigit():
                return {'nextpagevol': int(num)}
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


class PrevPageVolumes(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, num = callback.data.split('_')
            if suf == 'prevpagevol' and num.isdigit():
                return {'prevpagevol': int(num)}
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False


class CancelPageVolumes(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, command = callback.data.split('_')
            if suf == 'pagevol' and command == 'cancel':
                return True
            else:
                return False
        except (ValueError, IndexError) as e:
            print(e)
            return False
