from aiogram import F
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


__all__ = [
    'AskStats', 'AddNewVolume', 'DelVolume',
    'NextPageVolumes', 'PrevPageVolumes', 'CancelPageVolumes',
    'AddNotificationVolume', 'CancelNotificationVolumes',
    'AddStartTimeNotification', 'AddEndTimeNotification',
    'AddTzNotification', 'AddThresholdNotification',
    'DelNotification', 'SetUserTz'
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
            # print(e)
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
            # print(e)
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
            # print(e)
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
            # print(e)
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
            # print(e)
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
            # print(e)
            return False


class AddNotificationVolume(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, num = callback.data.split('_')
            if suf == 'setvol' and num.isdigit():
                return {'setvol': int(num)}
            else:
                return False
        except (ValueError, IndexError) as e:
            # print(e)
            return False


class CancelNotificationVolumes(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, command = callback.data.split('_')
            if suf == 'setvol' and command == 'cancel':
                return True
            else:
                return False
        except (ValueError, IndexError) as e:
            # print(e)
            return False


class AddStartTimeNotification(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, vol, start_time = callback.data.split('_')
            if suf == 'starttime':
                return {'vol': int(vol), 'start_time': start_time}
            else:
                return False
        except (ValueError, IndexError) as e:
            # print(e)
            return False


class AddEndTimeNotification(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, vol, end_time = callback.data.split('_')
            if suf == 'endtime':
                return {'vol': int(vol), 'end_time': end_time}
            else:
                return False
        except (ValueError, IndexError) as e:
            return False


class AddTzNotification(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, vol, tz = callback.data.split('_')
            if suf == 'tz':
                return {'vol': int(vol), 'tz': int(tz)}
            else:
                return False
        except (ValueError, IndexError) as e:
            return False


class AddThresholdNotification(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, vol, th = callback.data.split('_')
            if suf == 'threshold':
                return {'vol': int(vol), 'threshold': int(th)}
            else:
                return False
        except (ValueError, IndexError):
            return False


class DelNotification(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, vol = callback.data.split('_')
            if suf == 'delnot':
                return {'vol': int(vol)}
            else:
                return False
        except (ValueError, IndexError):
            return False


class SetUserTz(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        try:
            suf, tz = callback.data.split('_')
            if suf == 'usertz' and tz.isdigit():
                return {'usertz': int(tz)}
            else:
                return False
        except (ValueError, IndexError):
            return False
