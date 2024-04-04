import asyncio
import logging
import time

import schedule
from src import main


def run():
    asyncio.run(main())


schedule.every().day.at("16:04").do(run)
if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
