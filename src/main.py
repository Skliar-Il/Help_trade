from telebot import *
from sqlalchemy import select, insert, update

from config import TG_BOT_TOKEN, MESSAGE_PASSWORD
from connect_db import session_maker
from models.users import Table_Users
from check import check_new_message
from telebot.types import Message

import time
import asyncio




bot = TeleBot(TG_BOT_TOKEN)


@bot.message_handler(commands=["start"])    
def start(message):
    
    with session_maker() as session:
        if session.query(Table_Users.id).where(Table_Users.tg_id == message.chat.id).all() == []:
            session.execute(insert(Table_Users).values({"tg_id": message.chat.id, "tg_teg": message.from_user.username}))
            session.commit()
        session.close()
        
        
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Меню", callback_data = "menu"))
    bot.send_message(message.chat.id, f"Привет, {message.from_user.username}, я буду тебя оповещать об изменениях на ранке", reply_markup=markup)
    

@bot.message_handler(commands = ["check_last_message"])
def check_last_message(message):
    bot.register_next_step_handler(bot.send_message(message.chat.id, "Введите пароль"), check_password)

def check_password(message):
    if message.text == MESSAGE_PASSWORD:
        bot.send_message(message.chat.id, message.id)

@bot.callback_query_handler(func=lambda callback: True)
def callback(callback):
    if callback.data == "menu":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Подписка", callback_data="menu_subscribe"))
        bot.send_message(callback.message.chat.id, "Меню:", reply_markup=markup)
        
    
    if callback.data == "menu_subscribe":
        with session_maker() as session:
            status_subscribe = session.query(Table_Users.subscribe).where(Table_Users.tg_id == callback.message.chat.id).scalar()
            session.close()
            
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Меню", callback_data="menu"))
        
        if status_subscribe == False:
            markup.add(types.InlineKeyboardButton("Подписаться ✅", callback_data="subscribe"))
            bot.send_message(callback.message.chat.id, "У вас сейчас нет подписки", reply_markup=markup)
            
        else:
            markup.add(types.InlineKeyboardButton("Отписаться ❌", callback_data="unsubscribe"))
            bot.send_message(callback.message.chat.id, "Вы подписаны", reply_markup=markup)
        
        
    if callback.data == "subscribe": 
        with session_maker() as session:
            session.execute(update(Table_Users).values({"subscribe": True}).where(Table_Users.tg_id == callback.message.chat.id))
            session.commit()
            session.close()
            
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Меню", callback_data="menu"))
        bot.send_message(callback.message.chat.id, "Вы подписаны ✅", reply_markup=markup)
    
    if callback.data == "unsubscribe":
        with session_maker() as session:
            session.execute(update(Table_Users).values({"subscribe": False}).where(Table_Users.tg_id == callback.message.chat.id))
            session.commit()
            session.close()
            
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Меню", callback_data="menu"))
        bot.send_message(callback.message.chat.id, "Вы отписались ❌", reply_markup=markup)
        
    
check_new_message()
#https://api.telegram.org/bot6254570600:AAEJsGiYR2qkNucd3FA3-XUp77_TLfkKOWo/sendMessage?chat_id=1511626416&text=Привет, как дела?
bot.polling(non_stop=True)




