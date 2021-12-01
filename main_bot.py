


import logging
from asyncio import sleep

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.executor import start_webhook
from bs4 import BeautifulSoup

import kurs_dollaruz
from api_hh import get_id, get_vacancy

API_TOKEN = '1186351704:AAHirEt4saAqr7pjC5xDyWY3ZxKrEMqkpmA'

logging.basicConfig(level=logging.INFO)
WEBHOOK_HOST = 'https://botaiogrampy.herokuapp.com/'
WEBHOOK_PATH = f'/webhook/{API_TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 3001


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer('reaksiya to command')


@dp.message_handler(text='kurs')
async def kurs(message: types.Message):
    a = kurs_dollaruz.get_malumot()
    # await message.answer(a)
    # await bot.send_photo(-1001442434898, photo='https://hhcdn.ru/employer-logo-original/909971.jpeg', caption='Bu huddi testga oxshaydi lekin asli bu juda katta tes')
    await bot.send_message(-1001442434898, a, parse_mode=types.ParseMode.HTML)

@dp.message_handler()
async def echo(message: types.Message):
    msg = message.text
    if msg.startswith('vacant'):
        """ vacant dan keyin bir nechta sozlar keladi, ularni alohida ajratib olamiz"""

        id_ = [] # vacanciya id larini toplaymiz
        if len(msg) > 7:
            msg = str(msg[7:]) #vacantdan keyingi sozlarni hammasi
            msg = msg.split() # vacandan keyingi sozlarni alohida qilib massivga aylantiramiz
            for i in  msg:
                id_1 = get_id(i) # id larni yigamiz
                for index in id_1:
                    id_.append(index)
        # id_ = get_id()
        if id_[0] != 0:
            for ii in id_:
                photo, text = get_vacancy(ii)
                # if photo != ' ':
                #     if len(text) > 1024:
                #         try:
                #             print(text)
                #             await message.answer_photo(photo=photo, caption=text[:1024], parse_mode='HTML')
                #             await message.answer(text[1024:], parse_mode='HTML')
                #         except Exception:
                #             continue
                # else:
                try:
                    await message.answer(text, parse_mode='HTML', disable_web_page_preview=True)
                    if message.from_user.id == 711910507:
                        await bot.send_message(-1001442434898, text, disable_web_page_preview=True, parse_mode=types.ParseMode.HTML)
                except Exception:
                    continue
                await sleep(2)
            await message.answer('Hozircha bori shular ekan')
        else:
            await message.answer(message.text + '  buguncha vacansiya yoq ekan' + str(message.chat.id))
    else:
        await message.answer(message.text + ' ' + str(message.chat.id))


async def on_startup(dp):
    logging.warning(
        'Starting connection. ')
    await bot.set_webhook(WEBHOOK_URL,drop_pending_updates=True)


async def on_shutdown(dp):
    logging.warning('Bye! Shutting down webhook connection')


def main():
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )


if __name__ == '__main__':
    main()


