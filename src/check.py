from config import CHAT_ID, USER_ID, TG_BOT_TOKEN
from telebot import TeleBot
from connect_db import session_maker
from models.message import Table_id
from sqlalchemy import select, update
from threading import Timer
from send_message import send_message

bot = TeleBot(TG_BOT_TOKEN)

def check_last_message_id():
    with session_maker() as session:
        last_id = session.execute(select(Table_id.last_message_id)).scalar()
        
    
        try:
            message = bot.copy_message(CHAT_ID, CHAT_ID, 1+last_id)
            last_id = last_id + 2
            session.execute(update(Table_id).values({"last_message_id": last_id}).where(Table_id.id == 1))
            session.commit()
            
            send_message(message.message_id)
            
        except:
            pass
        
        finally:
            session.close()
            return 0
            
        
        

def check_new_message():
    Timer(5, check_new_message).start()
    check_last_message_id()

        



    
