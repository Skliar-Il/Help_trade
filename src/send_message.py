from sqlalchemy import select 
from connect_db import session_maker
from models.users import Table_Users
from config import CHAT_ID, TG_BOT_TOKEN
from telebot import TeleBot

bot = TeleBot(TG_BOT_TOKEN)


def send_message(message_id):
    with session_maker() as session:
        
        users_id = session.query(Table_Users.tg_id).where(Table_Users.subscribe == True).all()
        
        for i in users_id:
            bot.copy_message(i[0], CHAT_ID, message_id)
        
        



