from config import CHAT_ID, USER_ID, TG_BOT_TOKEN
from telebot import TeleBot
from connect_db import session_maker
from models.message import Table_id
from sqlalchemy import select
from threading import Timer


bot = TeleBot(TG_BOT_TOKEN)

def check_last_message_id():
    with session_maker() as session:
        last_id = session.execute(select(Table_id.last_message_id)).scalar()
        new_message = bot.send_message(CHAT_ID, "__,,,^._.^,,,__")
        new_id = new_message.message_id - 1 
        bot.delete_message(CHAT_ID, new_message.message_id)
        
        if last_id != new_id:
            return {False, new_id}
        else:
            return {True}
        

def check_new_message():
    Timer(5, check_new_message).start()
    check_last_message_id()



    # global text_id 
    # bot.send_message(message.chat.id, "asdsadsadsadsadsa")
    # new_message = bot.copy_message(message.chat.id, message.chat.id, 1)
    # new_id = new_message.message_id -1 
    # bot.delete_message(message.chat.id, new_message.message_id)
    
    # if text_id == new_id:
    #     bot.send_message(message.chat.id, "copy")
    # else:
    #     bot.edit_message_text(text="win", chat_id=message.chat.id, message_id=new_id)
    #     text_id = new_id
    #     print(text_id)
    
