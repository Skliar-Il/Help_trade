from telebot import TeleBot
from telebot.types import MessageID

from connect_db import session_maker
from config import CHAT_ID, TG_BOT_TOKEN

bot = TeleBot(TG_BOT_TOKEN)


def edit_message(message: MessageID):
    
    print(message)
    
    print("win")

