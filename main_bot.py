import logging
from asyncio import sleep
import os

from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook


import kurs_dollaruz
from api_hh import get_id, get_vacancy

API_TOKEN = os.getenv("api_bot")

logging.basicConfig(level=logging.INFO)
WEBHOOK_HOST = 'https://botaiogrampy.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{API_TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv("PORT"))

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer('reaksiya to command')


@dp.message_handler(text='kurs')
async def kurs(message: types.Message):
    a = kurs_dollaruz.get_malumot()
    await message.answer(a, parse_mode=types.ParseMode.HTML)


@dp.message_handler()
async def echo(message: types.Message):
    msg = message.text
    if message.from_user.id != 711910507:
        await bot.send_message(711910507, msg, disable_web_page_preview=True,
                                               parse_mode=types.ParseMode.HTML)
    if msg.startswith('vacant'):
        """ vacant dan keyin bir nechta sozlar keladi, ularni alohida ajratib olamiz"""
        
        

        id_ = []  # vacanciya id larini toplaymiz
        if len(msg) > 7:
            msg = str(msg[7:])  # vacantdan keyingi sozlarni hammasi
            msg = msg.split()  # vacandan keyingi sozlarni alohida qilib massivga aylantiramiz
            for i in msg:
                print(i)
                id_1 = get_id(i)  # id larni yigamiz
                for index in id_1:
                    print(index)
                    id_.append(index)

        if id_[0] != 0:
            print(str(id_))
            for ii in id_:
                await sleep(2)                
                try:
                    text = get_vacancy(ii)
                    if message.from_user.id == 711910507:
                        await bot.send_message(-1001442434898, text, disable_web_page_preview=True,
                                               parse_mode=types.ParseMode.HTML)
                    else:
                        await message.answer(text, parse_mode='HTML', disable_web_page_preview=True)
                except Exception:
                    await bot.send_message(711910507, Exception, disable_web_page_preview=True,
                                               parse_mode=types.ParseMode.HTML)

            await message.answer('Hozircha bori shular ekan')
        else:
            await message.answer(message.text + '  buguncha vacansiya yo''q ekan' + str(message.chat.id))
    else:
        await message.answer(message.text + ' ' + str(message.chat.id))


async def on_startup(dp):
    logging.warning(
        'Starting connection. ')

    try:
        await bot.set_webhook(WEBHOOK_URL)
    except Exception:
        print('XAto boldi bu ish bolmadi')
    await bot.send_message(711910507, "Men ishga tushdim")


async def on_shutdown(dp):
    logging.warning('Bye! Shutting down webhook connection')
    await bot.send_message(711910507, "Men o'chyapman")
    # await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT, )
