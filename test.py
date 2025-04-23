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


'''
docker run -d -ti -v /home/jahn/t2_gigabyte_bot/config/config.json:/app/config/config.json --network t2_gigabyte_exchange_default --restart unless-stopped --name t2_gigabyte_bot t2bot:0.1
'''