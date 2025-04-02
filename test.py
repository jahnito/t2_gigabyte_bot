import asyncio
from config import Config
from db import *


CFG = Config()


async def main(dsn):
    a = await get_active_volumes(dsn)
    print(a)



if __name__ == '__main__':
    # print(CFG.get_dsn())
    asyncio.run(main(CFG.get_dsn()))
