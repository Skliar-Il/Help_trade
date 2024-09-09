from telebot import *
from sqlalchemy import select, insert, update, or_
from sqlalchemy.orm import joinedload

from config import TG_BOT_TOKEN, GROUP_CHAT_ID, CHAT_ID
from databse import async_session_factory
from models.models import *
from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot

import time
import asyncio




bot = AsyncTeleBot(TG_BOT_TOKEN)
user_states = {}
securities = Table_Subscribe.__table__.columns.keys()[7:]
change_settings_types_messages = ["change_settings_type_change_open", "change_settings_type_change_volume"]
types_messages_switch = ["switch_type_change_open", "switch_type_many_lot", "switch_type_change_volume"]


@bot.message_handler(commands=["start"])    
async def start(message):
    
    async with async_session_factory() as session:
        data = await session.execute(select(Table_Users.id).where(Table_Users.tg_id == message.chat.id))
        data = data.scalar()
        
        if data == None:
            user_id = message.chat.id
            await session.execute(insert(Table_Users).values({Table_Users.tg_id: user_id}))
            await session.execute(insert(Table_Subscribe).values({Table_Subscribe.tg_id: user_id, Table_Subscribe.days_subscribe: 30}))
            
            await session.commit()
        await session.close()
        
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Меню", callback_data = "menu"))
    
    await bot.send_message(message.chat.id, f"Привет🖐, {message.from_user.first_name}, я буду оповещать тебя об изменениях на рынке", reply_markup=markup)
    
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "register_change_volume")
async def register_user_state_change_volume(message):
    markup = types.InlineKeyboardMarkup()
    change_volume_settings = message.text
    
    if change_volume_settings == "-":
        markup.add(types.InlineKeyboardButton("«Назад", callback_data="types_message"))
        await bot.send_message(message.chat.id, "Действие отменено", reply_markup=markup)
        return 0 
    
    try:
        change_volume_settings = abs(float(change_volume_settings))

    except:
        markup.add(types.InlineKeyboardButton("Попробовить снова", callback_data="change_settings_type_change_volume"))
        markup.add(types.InlineKeyboardButton("«Назад", callback_data="types_message"))
        await bot.send_message(message.chat.id, "Неверый ввод", reply_markup=markup)
        return 0 
    
    async with async_session_factory() as session:
        await session.execute(update(Table_Subscribe)
                              .values({Table_Subscribe.type_change_volume: change_volume_settings})
                              .where(Table_Subscribe.tg_id == message.chat.id))
        await session.commit()
        
    markup.add(types.InlineKeyboardButton("«Назад", callback_data="types_message"))
    await bot.send_message(message.chat.id, "Настройки успешно обновлены", reply_markup=markup)
    
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "register_change_open")
async def register_user_state_change_open(message):
    markup = types.InlineKeyboardMarkup()
    change_open_settings = message.text
    
    if change_open_settings == "-":
        markup.add(types.InlineKeyboardButton("«Назад", callback_data="types_message"))
        await bot.send_message(message.chat.id, "Действие отменено", reply_markup=markup)
        return 0 
    
    try:
        change_open_settings = abs(float(change_open_settings))

    except:
        markup.add(types.InlineKeyboardButton("Попробовить снова", callback_data="change_settings_type_change_open"))
        markup.add(types.InlineKeyboardButton("«Назад", callback_data="types_message"))
        await bot.send_message(message.chat.id, "Неверый ввод", reply_markup=markup)
        return 0 
    
    async with async_session_factory() as session:
        await session.execute(update(Table_Subscribe)
                              .values({Table_Subscribe.type_change_open: change_open_settings})
                              .where(Table_Subscribe.tg_id == message.chat.id))
        await session.commit()
        
    markup.add(types.InlineKeyboardButton("«Назад", callback_data="types_message"))
    await bot.send_message(message.chat.id, "Настройки успешно обновлены", reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
async def callback_handler(callback):
    if callback.data == "menu":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📎О боте", callback_data="bot_information"))
        markup.add(types.InlineKeyboardButton("👤Профиль", callback_data="profile"))
        markup.add(types.InlineKeyboardButton("⚙️Настройки", callback_data="settings"))
        
        await bot.edit_message_text("Меню:", callback.message.chat.id, callback.message.id, reply_markup=markup)

    if callback.data == "bot_information":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("«Назад", callback_data="menu"))
        
        #Написать описание для бота 
        await bot.edit_message_text("\tЭтот бот отправляет сообщения об изменениях на рынке, есть настройка сообщений которые вы получете. Вы можете выбрать интересующие вас бумаги, а так же выбрать и настроить интересующий вас тип сообщений. \n\nТип сообщений изменения с открытия, отвечает за получение сообщения об изменении с открытия рынка, настройка идет процентно. \nПример: SBER:TQBR Рост с открытия рынка +2 %.\n\nТип сообщения Изменение объема, отвечает  за получения сообщений с резким изменением объема, при настройке вы указываете от какого объема, в миллионах, вы хотите видеть сообщения.\nПример: ROSN:TQBR.  Резкое изменение объема  -   1M. Превышение среднего за день в  14.41 раз. Средний объем за день  53158.9. Цена Закрытия 457.65. Объем 765841. Максимальное изменение цены 5 пунктов. Индикатор SB  811 (0.02)\n\nТип сообщения крупная заявка, отвечает за получения сообщений о крупной заявке на рынке, этот тип сообщения нельзя настроить.\nПример: SBER:TQBR.  Крупная заявка на ПОКУПКУ. Объем  17138 - на сумму 43.016 млн. руб.. Цена  251. Цена лучшей покупки 251.19.", callback.message.chat.id, callback.message.id, reply_markup=markup)
        
    if callback.data == "profile":
        markup = types.InlineKeyboardMarkup()
        
        text = "👤Профиль:\n\nID: {}\nИмя: {}\nПодписка: {}\nДата регистрации: {}\n"
        id = callback.message.chat.id
        name = callback.message.chat.first_name
        subscribe = "✅"
        
        async with async_session_factory() as session:
            data = await session.execute(select(Table_Users)
                                         .where(Table_Users.tg_id == id)
                                         .options(joinedload(Table_Users.detail_subscribe)))
            data = data.scalar()
            await session.close()
            
        date_register = data.date_register + datetime.timedelta(hours=4)
        if data.detail_subscribe.days_subscribe <= 0: 
            subscribe = "❌"
            markup.add(types.InlineKeyboardButton("✅Подписаться", callback_data="subscribe"))
        
        else:
            markup.add(types.InlineKeyboardButton("❌Описаться", callback_data="unsubscribe"))
        
        markup.add(types.InlineKeyboardButton("«Назад", callback_data="menu"))
            
        await bot.edit_message_text(text.format(id, name, subscribe, date_register.strftime("%Y-%m-%d %H:%M")), 
                                    id, callback.message.id, reply_markup=markup)
    
    if callback.data == "subscribe":
        id = callback.message.chat.id
        markup = types.InlineKeyboardMarkup()
        
        async with async_session_factory() as session:
            await session.execute(update(Table_Subscribe).values({Table_Subscribe.days_subscribe: 30})
                            .where(Table_Subscribe.tg_id == id))
            await session.commit()
            
        markup.add(types.InlineKeyboardButton("Обновить", callback_data="profile"))
        await bot.edit_message_text("✅Вы Подписались", id, callback.message.id, reply_markup=markup)
        
    if callback.data == "unsubscribe":
        id = callback.message.chat.id
        markup = types.InlineKeyboardMarkup()
        
        async with async_session_factory() as session:
            await session.execute(update(Table_Subscribe).values({Table_Subscribe.days_subscribe: 0})
                            .where(Table_Subscribe.tg_id == id))
            await session.commit()
            
        markup.add(types.InlineKeyboardButton("Обновить", callback_data="profile"))
        await bot.edit_message_text("❌Вы Отписались", id, callback.message.id, reply_markup=markup)
    
    if callback.data == "settings":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⁉️О настройках", callback_data="settings_information"))
        markup.add(types.InlineKeyboardButton("Типы сообщений", callback_data="types_message"))
        markup.add(types.InlineKeyboardButton("Бумаги", callback_data="securities"))
        markup.add(types.InlineKeyboardButton("«Назад", callback_data="menu"))
        
        await bot.edit_message_text("Настройки:", callback.message.chat.id, callback.message.id, reply_markup=markup)
        
    if callback.data == "types_message":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Иземенение обьема", callback_data="change_volume"))
        markup.add(types.InlineKeyboardButton("Иземенение с открытия рынка", callback_data="change_open"))
        markup.add(types.InlineKeyboardButton("Крупная заявка", callback_data="many_lot"))
        markup.add(types.InlineKeyboardButton("«Назад", callback_data="settings"))
        
        await bot.edit_message_text("Типы сообщений:", callback.message.chat.id, callback.message.id, reply_markup=markup)
        
    if callback.data == "securities":
        markup = types.InlineKeyboardMarkup()
        buttons = []
        
        async with async_session_factory() as session:
            data = await session.execute(select(Table_Subscribe).where(Table_Subscribe.tg_id == callback.message.chat.id))
            data = data.scalars().all()
            for i in securities:
                status = "✅"
                
                if getattr(data[0], i) == False:
                    status = "❌"
                buttons.append(types.InlineKeyboardButton(i+status, callback_data=i))
                
        for i in range(0, len(buttons)-2, 4):
            markup.row(buttons[i], buttons[i+1], buttons[i+2], buttons[i+3])
                
        markup.row(buttons[-1], buttons[-2])
        markup.row(types.InlineKeyboardButton("«Назад", callback_data="settings"))
        
            
        await bot.edit_message_text("📰Бумаги, нажмите на те которые хотите изменить:", callback.message.chat.id, callback.message.id, reply_markup=markup)
    
    if callback.data in securities:
        markup = types.InlineKeyboardMarkup()
        
        async with async_session_factory() as session:
            Table_Subscribe_Column = getattr(Table_Subscribe, callback.data)
            await session.execute(update(Table_Subscribe)
                                  .values({Table_Subscribe_Column: case(
                (Table_Subscribe_Column == True, False),
                else_=True
            )})
                                  .where(Table_Subscribe.tg_id == callback.message.chat.id))
            await session.commit()
            
        if callback.message.text == "Данные обновлены":
            bot.delete_message(callback.message.chat.id, callback.message.id)
            
        markup.add(types.InlineKeyboardButton("Обновить", callback_data="securities"))
        
        await bot.send_message(callback.message.chat.id, "Данные обновлены", reply_markup=markup)
        
    if callback.data == "settings_information":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("«Назад", callback_data="settings"))
        
        #Придумать такст для описания настроек
        await bot.edit_message_text("Тип сообщений изменения с открытия, отвечает за получение сообщения об изменении с открытия рынка, настройка идет процентно. \nПример: SBER:TQBR Рост с открытия рынка +2 %.\n\nТип сообщения Изменение объема, отвечает  за получения сообщений с резким изменением объема, при настройке вы указываете от какого объема, в миллионах, вы хотите видеть сообщения.\nПример: ROSN:TQBR.  Резкое изменение объема  -   1M. Превышение среднего за день в  14.41 раз. Средний объем за день  53158.9. Цена Закрытия 457.65. Объем 765841. Максимальное изменение цены 5 пунктов. Индикатор SB  811 (0.02)\n\nТип сообщения крупная заявка, отвечает за получения сообщений о крупной заявке на рынке, этот тип сообщения нельзя настроить.\nПример: SBER:TQBR.  Крупная заявка на ПОКУПКУ. Объем  17138 - на сумму 43.016 млн. руб.. Цена  251. Цена лучшей покупки 251.19.", callback.message.chat.id, callback.message.id, reply_markup=markup)
        
    if callback.data == "change_volume":
        markup = types.InlineKeyboardMarkup()
        
        async with async_session_factory() as session: 
            data = await session.execute(select(Table_Subscribe.type_change_volume).where(Table_Subscribe.tg_id == callback.message.chat.id))
            data = data.scalar()
            
        if data == -1:
            settings = "Отключено"
            
            markup.add(types.InlineKeyboardButton("Подключить", callback_data="switch_type_change_volume"))
        
        elif data >=0:
            settings = data
            if data == 0: settings = "По умолчанию"
            
            markup.add(types.InlineKeyboardButton("Отключить", callback_data="switch_type_change_volume"))
            markup.add(types.InlineKeyboardButton("Настроить", callback_data="change_settings_type_change_volume"))
            
        markup.add(types.InlineKeyboardButton("Вернуть к настройкам по умолчанию", callback_data="set_default_settings_type_change_volume"))            
        markup.add(types.InlineKeyboardButton("«Назад", callback_data="types_message"))
        
        await bot.edit_message_text(f"Изменение обьема\n\nНастройки: {settings}", callback.message.chat.id, callback.message.id, reply_markup=markup)
        
    if callback.data == "change_open":
        markup = types.InlineKeyboardMarkup()
        
        async with async_session_factory() as session: 
            data = await session.execute(select(Table_Subscribe.type_change_open).where(Table_Subscribe.tg_id == callback.message.chat.id))
            data = data.scalar()
            
        if data == -1:
            settings = "Отключено"
            markup.add(types.InlineKeyboardButton("Подключить", callback_data="switch_type_change_open"))
        
        elif data >=0:
            settings = data
            if data == 0: settings = "По умолчанию"
            
            markup.add(types.InlineKeyboardButton("Отключить", callback_data="switch_type_change_open"))
            markup.add(types.InlineKeyboardButton("Настроить", callback_data="change_settings_type_change_open"))
            
        markup.add(types.InlineKeyboardButton("Вернуть к настройкам по умолчанию", callback_data="set_default_settings_type_change_open"))
        markup.add(types.InlineKeyboardButton("«Назад", callback_data="types_message"))
        
        await bot.edit_message_text(f"Изменение c открытия рынка\n\nНастройки: {settings}", callback.message.chat.id, callback.message.id, reply_markup=markup)
        
    if callback.data == "many_lot":
        markup = types.InlineKeyboardMarkup()
        
        async with async_session_factory() as session: 
            data = await session.execute(select(Table_Subscribe.type_many_lot).where(Table_Subscribe.tg_id == callback.message.chat.id))
            data = data.scalar()
            
        if data == -1:
            markup.add(types.InlineKeyboardButton("Подключить", callback_data="switch_type_many_lot"))
        
        elif data >=0:
            markup.add(types.InlineKeyboardButton("Отключить", callback_data="switch_type_many_lot"))
            
        markup.add(types.InlineKeyboardButton("«Назад", callback_data="types_message"))
        
        await bot.edit_message_text(f"Крупная заявка", callback.message.chat.id, callback.message.id, reply_markup=markup)
    
    if callback.data == "change_settings_type_change_volume":
        user_states[callback.message.chat.id] = "register_change_volume"
        
        await bot.send_message(callback.message.chat.id, "Введите значение, вам будут приходить сообщения только те, где изменения больше или равны по модулю введеного значения\nДля отмены дейсствия введите: -")
        
    if callback.data == "change_settings_type_change_open":
        user_states[callback.message.chat.id] = "register_change_open"
        
        await bot.send_message(callback.message.chat.id, "Введите значение, вам будут приходить сообщения только те, где изменения больше или равны по модулю введеного значения\nДля отмены дейсствия введите: -")
        
    if callback.data == "set_default_settings_type_change_volume":
        async with async_session_factory() as session:
            await session.execute(update(Table_Subscribe).values({Table_Subscribe.type_change_volume: 0}))
            await session.commit()
            
        markup  = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("«Назад", callback_data="types_message"))
        await bot.send_message(callback.message.chat.id, "Настройки успешно обновлены", reply_markup=markup)
        
    if callback.data == "set_default_settings_type_change_open":
        async with async_session_factory() as session:
            await session.execute(update(Table_Subscribe).values({Table_Subscribe.type_change_open: 0}))
            await session.commit()
            
        markup  = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("«Назад", callback_data="types_message"))
        await bot.send_message(callback.message.chat.id, "Настройки успешно обновлены", reply_markup=markup)
        
    if callback.data in types_messages_switch:
        markup = types.InlineKeyboardMarkup()
        column_name = callback.data[7:]
        column = getattr(Table_Subscribe, column_name)
        
        async with async_session_factory() as session:
            await session.execute(update(Table_Subscribe)
                            .values({
                                column: case(
                                    (column == -1, 0),
                                    (column >=0, -1)
                                )
                            })
                            .where(Table_Subscribe.tg_id == callback.message.chat.id))
            await session.commit()
            
            markup.add(types.InlineKeyboardButton("Обновить", callback_data=callback.data[12:]))
            await bot.send_message(callback.message.chat.id, "Данные обновлены", reply_markup=markup)
            
    
            
while True:
    try:
        asyncio.run(bot.polling())
        
    except:
        time.sleep(1)

# asyncio.run(bot.polling())