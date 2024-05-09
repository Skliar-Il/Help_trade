from telebot import *

from config import TG_BOT_TOKEN
from connect_db import get_async_session
from models.users import Table_Users

import time
import asyncio




bot = TeleBot(TG_BOT_TOKEN)


@bot.message_handler(commands=["start"])    
def start(message, session = get_async_session()):
    session.add(Table_Users(tg_id = message.chat.id, tg_teg = message.fom_user.username))
    session.commit()
    
    bot.send_message(message.chat.id, "win!")
    







while True:
    try:
        asyncio.run(bot.polling(non_stop=True, interval=1, timeout=0))
    except:
        time.sleep(2)