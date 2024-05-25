from sqlalchemy import select

from main import bot 
from connect_db import session_maker
from models.users import Table_Users
from config import CHAT_ID

def send_message(message_id):
    with session_maker() as session:
        
        users_id = session.query(Table_Users.tg_id).all()
        
        for i in users_id:
            bot.copy_message(i[0], CHAT_ID, message_id)
        
        



