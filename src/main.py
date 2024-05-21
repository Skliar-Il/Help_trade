from telebot import *

from config import TG_BOT_TOKEN
from connect_db import get_async_session, async_session_maker
from models.users import Table_Users

import time
import asyncio




bot = TeleBot(TG_BOT_TOKEN)


@bot.message_handler(commands=["start"])    
async def start(message):

    async with async_session_maker() as session:
    
        markup = types.InlineKeyboardMarkup()

        session.add(Table_Users(tg_id = message.chat.id, tg_teg = message.fom_user.username))
        await session.commit()

    markup.add(types.InlineKeyboardButton("Продолжить", callback_data = start))
    bot.send_message(message.chat.id, f"Привет, {message.caht.from_user.name}, я буду тебя оповещать об изменениях на ранке")
    



@bot.callback_query_handler(func=lambda callback: True)
def callback(callback):
    if callback.data == "start":
        pass
    
    





bot.polling(non_stop=True)
