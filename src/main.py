from telebot import *

from config import TG_BOT_TOKEN
from connect_db import session_maker
from models.users import Table_Users
from check import check_new_message

import time
import asyncio




bot = TeleBot(TG_BOT_TOKEN)


@bot.message_handler(commands=["start"])    
def start(message):
    bot.send_message(message.chat.id, "win")
        
    
    # bot.send_message(message.chat.id, message.id)
    # bot.send_message(message.chat.id, message.text)
    # bot.send_message(message.chat.id, "---------")
    # time.sleep(5)
    # #bot.edit_message_text("67")
    # bot.send_message(message.chat.id, "---------")
    # bot.send_message(message.chat.id, message.id)
    # bot.send_message(chat_id=message.chat.id, text="---------")
    
    # a = bot.copy_message(message.chat.id, message.chat.id, message.id)
    # bot.send_message(chat_id=message.chat.id, text="---------")
    # bot.send_message(message.chat.id, text=a.message_id)
    
    # with session_maker() as session:
    
    #     markup = types.InlineKeyboardMarkup()

    #     session.add(Table_Users(tg_id = message.chat.id, tg_teg = message.from_user.username))
    #     session.commit()
    #     session.close()

    # markup.add(types.InlineKeyboardButton("Продолжить", callback_data = start))
    # bot.send_message(message.chat.id, f"Привет, {message.from_user.username}, я буду тебя оповещать об изменениях на ранке")
    



@bot.callback_query_handler(func=lambda callback: True)
def callback(callback):
    if callback.data == "start":
        pass
    
    

    


check_new_message()
bot.polling(non_stop=True)




