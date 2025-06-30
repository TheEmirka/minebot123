import telebot
import json
import random
import time
from datetime import datetime, timedelta
import os

BOT_TOKEN = "8138804925:AAFQdS-7N_7LiM4S6cCIpAMJn98EaE4TV0I"
bot = telebot.TeleBot(BOT_TOKEN)

DATA_FILE = "players_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_player_data(user_id):
    data = load_data()
    if str(user_id) not in data:
        data[str(user_id)] = {
            "name": "Player",
            "dollars": 0,
            "vip": False,
            "iron": 0,
            "bronze": 0,
            "silver": 0,
            "gold": 0,
            "mine": "Нет",
            "bronze_mine": False,
            "silver_mine": False,
            "gold_mine": False,
            "last_dig": 0,
            "last_bonus": 0,
            "last_vip_dig": 0,
            "last_vip_bonus": 0,
            "last_mine_dig": 0,
            "gift_cases": 0,
            "bronze_cases": 0,
            "silver_cases": 0,
            "gold_cases": 0
        }
        save_data(data)
    return data[str(user_id)]

def update_player_data(user_id, player_data):
    data = load_data()
    player_data['dollars'] = round(player_data['dollars'], 2)
    data[str(user_id)] = player_data
    save_data(data)

def format_number(num):
    if isinstance(num, float):
        if num == int(num):
            return str(int(num))
        else:
            return str(round(num, 2))
    return str(num)

@bot.message_handler(func=lambda message: message.text.lower() == 'помощь')
def help_command(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("🤖 Команды", callback_data="help_commands")
    btn2 = telebot.types.InlineKeyboardButton("👑 Вип", callback_data="help_vip")
    btn3 = telebot.types.InlineKeyboardButton("💰 Бонус", callback_data="help_bonus")
    markup.add(btn1)
    markup.add(btn2, btn3)
    
    bot.send_message(message.chat.id, "*Здравствуй! Я помощник Роб! Зайди в нужный раздел и я тебе отвечу на твои вопросы!*", 
                     parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "help_commands")
def help_commands_callback(call):
    text = """*Если ты хочешь просмотреть что делает каждая команда - я сделал список, посмотри ниже*

*ЗАРАБОТОК*
Копать - выкопать железо
Трейд - обменник всего карьера
Обменять `(колво)` - обменять железо на доллары
Купить вип - купить вип привилегию
Казино `(ставка)` - сыграть в казино
Дать `(сколько)` - передача денег

*ПРОФИЛЬ*
Профиль - просмотреть профиль
Ник `[новое имя]` - поменять имя

*КЕЙСЫ*
Кейсы - вся информация о кейсах
Купить бронзовый кейс `(количество)` - купить бронз кейс
Купить серебрянный кейс `(количество)` - купить сильвер кейс
Купить золотой кейс `(количество)` - купить голд кейс
Открыть бронзовый/серебрянный/золотой кейс - открыть кейсы соответственно

*ЧАСТНЫЕ ШАХТЫ*
Частные шахты - вся информация о частных шахтах
Купить бронзовую/серебрянную/золотую шахту - купить частную шахту
Копать в шахте - копать в частной шахте

**КРАФТ**
Крафты - вся информация о крафтах
Скрафтить подарочный кейс - скрафтить подарочный кейс
Скрафтить бронзовый кейс - скрафтить бронзовый кейс
Скрафтить серебрянный кейс - скрафтить серебрянный кейс
Скрафтить золотой кейс - скрафтить золотой кейс"""
    
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("🤖 Команды", callback_data="help_commands")
    btn2 = telebot.types.InlineKeyboardButton("👑 Вип", callback_data="help_vip")
    btn3 = telebot.types.InlineKeyboardButton("💰 Бонус", callback_data="help_bonus")
    markup.add(btn1)
    markup.add(btn2, btn3)
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "help_vip")
def help_vip_callback(call):
    text = """*VIP статус:*

*❓ Приобрести можно в трейде*

*Преимущества:*

*Вип шахта:*
Вип копать - копать в вип шахте

*Вип бонус:*
Вип бонус - получить вип бонус

❗ Кулдаун команды "Копать" уменьшается в 2 раза до 1 минуты 30 секунд.

**На этом всё!**"""
    
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("🤖 Команды", callback_data="help_commands")
    btn2 = telebot.types.InlineKeyboardButton("👑 Вип", callback_data="help_vip")
    btn3 = telebot.types.InlineKeyboardButton("💰 Бонус", callback_data="help_bonus")
    markup.add(btn1)
    markup.add(btn2, btn3)
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "help_bonus")
def help_bonus_callback(call):
    text = """*Ты можешь получить подарочный кейс абсолютно бесплатно!*

Твоя задача просто написать команду "Бонус", тогда ты получишь бесплатный подарочный кейс!
*Удачи!*"""
    
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("🤖 Команды", callback_data="help_commands")
    btn2 = telebot.types.InlineKeyboardButton("👑 Вип", callback_data="help_vip")
    btn3 = telebot.types.InlineKeyboardButton("💰 Бонус", callback_data="help_bonus")
    markup.add(btn1)
    markup.add(btn2, btn3)
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.lower() == 'топ')
def top_command(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("💲 Доллары", callback_data="top_dollars")
    btn2 = telebot.types.InlineKeyboardButton("⚙️ Железо", callback_data="top_iron")
    btn3 = telebot.types.InlineKeyboardButton("🥉 Бронза", callback_data="top_bronze")
    btn4 = telebot.types.InlineKeyboardButton("🥈 Серебро", callback_data="top_silver")
    btn5 = telebot.types.InlineKeyboardButton("🪙 Золото", callback_data="top_gold")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    
    bot.send_message(message.chat.id, "*🏆 Топ игроков!*\n*Выберите категорию для просмотра рейтинга:*", 
                     parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "top_dollars")
def top_dollars_callback(call):
    data = load_data()
    players = [(player_data['name'], player_data['dollars']) for player_data in data.values()]
    players.sort(key=lambda x: x[1], reverse=True)
    
    text = "*💲 Топ игроков по долларам:*\n\n"
    for i, (name, amount) in enumerate(players[:10], 1):
        text += f"`{i}.` *{name}* - `{format_number(amount)}` 💲\n"
    
    if not players:
        text += "*Пока никого нет в рейтинге!*"
    
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("💲 Доллары", callback_data="top_dollars")
    btn2 = telebot.types.InlineKeyboardButton("⚙️ Железо", callback_data="top_iron")
    btn3 = telebot.types.InlineKeyboardButton("🥉 Бронза", callback_data="top_bronze")
    btn4 = telebot.types.InlineKeyboardButton("🥈 Серебро", callback_data="top_silver")
    btn5 = telebot.types.InlineKeyboardButton("🪙 Золото", callback_data="top_gold")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "top_iron")
def top_iron_callback(call):
    data = load_data()
    players = [(player_data['name'], player_data['iron']) for player_data in data.values()]
    players.sort(key=lambda x: x[1], reverse=True)
    
    text = "*⚙️ Топ игроков по железу:*\n\n"
    for i, (name, amount) in enumerate(players[:10], 1):
        text += f"`{i}.` *{name}* - `{format_number(amount)}` ⚙️\n"
    
    if not players:
        text += "*Пока никого нет в рейтинге!*"
    
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("💲 Доллары", callback_data="top_dollars")
    btn2 = telebot.types.InlineKeyboardButton("⚙️ Железо", callback_data="top_iron")
    btn3 = telebot.types.InlineKeyboardButton("🥉 Бронза", callback_data="top_bronze")
    btn4 = telebot.types.InlineKeyboardButton("🥈 Серебро", callback_data="top_silver")
    btn5 = telebot.types.InlineKeyboardButton("🪙 Золото", callback_data="top_gold")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "top_bronze")
def top_bronze_callback(call):
    data = load_data()
    players = [(player_data['name'], player_data['bronze']) for player_data in data.values()]
    players.sort(key=lambda x: x[1], reverse=True)
    
    text = "*🥉 Топ игроков по бронзе:*\n\n"
    for i, (name, amount) in enumerate(players[:10], 1):
        text += f"`{i}.` *{name}* - `{format_number(amount)}` 🥉\n"
    
    if not players:
        text += "*Пока никого нет в рейтинге!*"
    
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("💲 Доллары", callback_data="top_dollars")
    btn2 = telebot.types.InlineKeyboardButton("⚙️ Железо", callback_data="top_iron")
    btn3 = telebot.types.InlineKeyboardButton("🥉 Бронза", callback_data="top_bronze")
    btn4 = telebot.types.InlineKeyboardButton("🥈 Серебро", callback_data="top_silver")
    btn5 = telebot.types.InlineKeyboardButton("🪙 Золото", callback_data="top_gold")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "top_silver")
def top_silver_callback(call):
    data = load_data()
    players = [(player_data['name'], player_data['silver']) for player_data in data.values()]
    players.sort(key=lambda x: x[1], reverse=True)
    
    text = "*🥈 Топ игроков по серебру:*\n\n"
    for i, (name, amount) in enumerate(players[:10], 1):
        text += f"`{i}.` *{name}* - `{format_number(amount)}` 🥈\n"
    
    if not players:
        text += "*Пока никого нет в рейтинге!*"
    
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("💲 Доллары", callback_data="top_dollars")
    btn2 = telebot.types.InlineKeyboardButton("⚙️ Железо", callback_data="top_iron")
    btn3 = telebot.types.InlineKeyboardButton("🥉 Бронза", callback_data="top_bronze")
    btn4 = telebot.types.InlineKeyboardButton("🥈 Серебро", callback_data="top_silver")
    btn5 = telebot.types.InlineKeyboardButton("🪙 Золото", callback_data="top_gold")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "top_gold")
def top_gold_callback(call):
    data = load_data()
    players = [(player_data['name'], player_data['gold']) for player_data in data.values()]
    players.sort(key=lambda x: x[1], reverse=True)
    
    text = "*🪙 Топ игроков по золоту:*\n\n"
    for i, (name, amount) in enumerate(players[:10], 1):
        text += f"`{i}.` *{name}* - `{format_number(amount)}` 🪙\n"
    
    if not players:
        text += "*Пока никого нет в рейтинге!*"
    
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("💲 Доллары", callback_data="top_dollars")
    btn2 = telebot.types.InlineKeyboardButton("⚙️ Железо", callback_data="top_iron")
    btn3 = telebot.types.InlineKeyboardButton("🥉 Бронза", callback_data="top_bronze")
    btn4 = telebot.types.InlineKeyboardButton("🥈 Серебро", callback_data="top_silver")
    btn5 = telebot.types.InlineKeyboardButton("🪙 Золото", callback_data="top_gold")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.lower() == 'профиль')
def profile_command(message):
    player = get_player_data(message.from_user.id)
    
    # Определяем привилегию
    if message.from_user.id == 7143373003:
        privilege = "👮🏿‍♂️ Админ"
    elif player["vip"]:
        privilege = "👑 Вип"
    else:
        privilege = "👤 Игрок"
    
    text = f"""📛 *Имя:* `{player['name']}`
💲 *Доллары:* `{format_number(player['dollars'])}`
👑 *Привилегия:* {privilege}

⚙️ *Железо:* `{format_number(player['iron'])}`
🥉 *Бронза:* `{format_number(player['bronze'])}`
🥈 *Серебро:* `{format_number(player['silver'])}`
🥇 *Золото:* `{format_number(player['gold'])}`

🏗 *Бронзовая шахта:* {'✔️' if player.get('bronze_mine', False) else '❌'}
🏗 *Серебрянная шахта:* {'✔️' if player.get('silver_mine', False) else '❌'}
🏗 *Золотая шахта:* {'✔️' if player.get('gold_mine', False) else '❌'}

*❓ Чтобы изменить имя, введите: ник [новое имя]*"""
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower().startswith('ник'))
def change_name_command(message):
    try:
        parts = message.text.split(' ', 2)
        if len(parts) < 3:
            bot.send_message(message.chat.id, "*Использование: ник [новое имя]*", parse_mode='Markdown')
            return
            
        new_name = parts[2]
        if len(new_name) > 30:
            bot.send_message(message.chat.id, "*Действует ограничение в* `30` *букв!*", parse_mode='Markdown')
            return
        
        player = get_player_data(message.from_user.id)
        player['name'] = new_name
        update_player_data(message.from_user.id, player)
        
        bot.send_message(message.chat.id, f"*Вы сменили имя, теперь вас зовут {new_name}!*", parse_mode='Markdown')
    except Exception:
        bot.send_message(message.chat.id, "*Использование: ник [новое имя]*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower() == 'копать')
def dig_command(message):
    player = get_player_data(message.from_user.id)
    current_time = time.time()
    
    cooldown = 90 if player['vip'] else 180
    
    if current_time - player['last_dig'] < cooldown:
        remaining_time = cooldown - (current_time - player['last_dig'])
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        bot.send_message(message.chat.id, f"*Вы устали, отдохните, можете идти копать через* `{minutes}` *минут* `{seconds}` *секунд*", parse_mode='Markdown')
        return
    
    iron_found = random.randint(5, 20)
    player['iron'] += iron_found
    player['last_dig'] = current_time
    update_player_data(message.from_user.id, player)
    
    bot.send_message(message.chat.id, f"*Вы зашли на территорию шахты, и выкопали* `{iron_found}` *железа!*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower().startswith('обменять'))
def exchange_command(message):
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.send_message(message.chat.id, "*Использование: Обменять железо/бронзу/серебро/золото (количество)*", parse_mode='Markdown')
            return
            
        resource = parts[1].lower()
        amount = int(parts[2])
        
        if amount <= 0:
            bot.send_message(message.chat.id, "*Количество должно быть больше 0!*", parse_mode='Markdown')
            return
        
        player = get_player_data(message.from_user.id)
        
        if resource in ['железо', 'железа']:
            if player['iron'] >= amount:
                player['iron'] -= amount
                earned = round(amount * 0.2, 2)
                player['dollars'] += earned
                update_player_data(message.from_user.id, player)
                bot.send_message(message.chat.id, f"**Вы успешно обменяли** `{amount}` **железа на** `{format_number(earned)}` **долларов**", parse_mode='Markdown')
            else:
                bot.send_message(message.chat.id, "*У вас недостаточно железа!*", parse_mode='Markdown')
        
        elif resource in ['бронзу', 'бронзы']:
            if player['bronze'] >= amount:
                player['bronze'] -= amount
                earned = round(amount * 0.5, 2)
                player['dollars'] += earned
                update_player_data(message.from_user.id, player)
                bot.send_message(message.chat.id, f"**Вы успешно обменяли** `{amount}` **бронзы на** `{format_number(earned)}` **долларов**", parse_mode='Markdown')
            else:
                bot.send_message(message.chat.id, "*У вас недостаточно бронзы!*", parse_mode='Markdown')
        
        elif resource in ['серебро', 'серебра']:
            if player['silver'] >= amount:
                player['silver'] -= amount
                earned = round(amount * 1, 2)
                player['dollars'] += earned
                update_player_data(message.from_user.id, player)
                bot.send_message(message.chat.id, f"**Вы успешно обменяли** `{amount}` **серебра на** `{format_number(earned)}` **долларов**", parse_mode='Markdown')
            else:
                bot.send_message(message.chat.id, "*У вас недостаточно серебра!*", parse_mode='Markdown')
        
        elif resource in ['золото', 'золота']:
            if player['gold'] >= amount:
                player['gold'] -= amount
                earned = round(amount * 3, 2)
                player['dollars'] += earned
                update_player_data(message.from_user.id, player)
                bot.send_message(message.chat.id, f"**Вы успешно обменяли** `{amount}` **золота на** `{format_number(earned)}` **долларов**", parse_mode='Markdown')
            else:
                bot.send_message(message.chat.id, "*У вас недостаточно золота!*", parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "*Неизвестный ресурс! Доступные: железо, бронзу, серебро, золото*", parse_mode='Markdown')
        
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "*Использование: Обменять железо/бронзу/серебро/золото (количество)*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower() == 'бонус')
def bonus_command(message):
    player = get_player_data(message.from_user.id)
    current_time = time.time()
    
    if current_time - player['last_bonus'] < 86400:
        remaining_time = 86400 - (current_time - player['last_bonus'])
        hours = int(remaining_time // 3600)
        minutes = int((remaining_time % 3600) // 60)
        bot.send_message(message.chat.id, f"*Я не богач, подожди* `{hours}` *часов* `{minutes}` *минут*", parse_mode='Markdown')
        return
    
    player['gift_cases'] += 1
    player['last_bonus'] = current_time
    update_player_data(message.from_user.id, player)
    
    bot.send_message(message.chat.id, "😄 *Вы получили* `1` *подарочный кейс!*\n*Чтобы открыть подарочный кейс, нужно написать: Открыть подарочный кейс*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower() == 'открыть подарочный кейс')
def open_gift_case(message):
    player = get_player_data(message.from_user.id)
    
    if player['gift_cases'] <= 0:
        bot.send_message(message.chat.id, "*У вас нет подарочных кейсов!*", parse_mode='Markdown')
        return
    
    player['gift_cases'] -= 1
    reward = random.randint(1, 12)
    player['dollars'] += reward
    update_player_data(message.from_user.id, player)
    
    bot.send_message(message.chat.id, f"*Вы открыли подарочный кейс и получили* `{reward}` *долларов!*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower() == 'кейсы')
def cases_command(message):
    player = get_player_data(message.from_user.id)
    
    text = f"""*📦 Кейсы!*

❗️*Нельзя открыть больше* `1` *кейса за раз!*

*1. Подарочный кейс, можно скрафтить или получить в бонусе, у вас в наличии:* `{player['gift_cases']}`

*2. Бронзовый кейс, стоимость:* `50`$*, у вас в наличии:* `{player['bronze_cases']}`

*3. Серебрянный кейс, стоимость:* `100`$*, у вас в наличии:* `{player['silver_cases']}`

*4. Золотой кейс, стоимость:* `300`$*, у вас в наличии:* `{player['gold_cases']}`

*Купить бронзовый кейс - Купить бронзовый кейс (колво)*
*Купить серебрянный кейс - Купить серебрянный кейс (колво)*
*Купить золотой кейс - Купить золотой кейс (колво)*"""
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower().startswith('купить бронзовый кейс'))
def buy_bronze_case(message):
    try:
        parts = message.text.split()
        amount = int(parts[3]) if len(parts) > 3 else 1
        
        if amount <= 0:
            bot.send_message(message.chat.id, "*Количество должно быть больше 0!*", parse_mode='Markdown')
            return
        
        player = get_player_data(message.from_user.id)
        total_cost = amount * 50
        
        if player['dollars'] < total_cost:
            bot.send_message(message.chat.id, "*У вас недостаточно денег!*", parse_mode='Markdown')
            return
        
        player['dollars'] -= total_cost
        player['bronze_cases'] += amount
        update_player_data(message.from_user.id, player)
        
        bot.send_message(message.chat.id, f"*Вы купили* `{amount}` *бронзовых кейсов за* `{total_cost}` *долларов!*", parse_mode='Markdown')
        
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "*Использование: Купить бронзовый кейс (количество)*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower().startswith('купить серебрянный кейс'))
def buy_silver_case(message):
    try:
        parts = message.text.split()
        amount = int(parts[3]) if len(parts) > 3 else 1
        
        if amount <= 0:
            bot.send_message(message.chat.id, "*Количество должно быть больше 0!*", parse_mode='Markdown')
            return
        
        player = get_player_data(message.from_user.id)
        total_cost = amount * 100
        
        if player['dollars'] < total_cost:
            bot.send_message(message.chat.id, "*У вас недостаточно денег!*", parse_mode='Markdown')
            return
        
        player['dollars'] -= total_cost
        player['silver_cases'] += amount
        update_player_data(message.from_user.id, player)
        
        bot.send_message(message.chat.id, f"*Вы купили* `{amount}` *серебрянных кейсов за* `{total_cost}` *долларов!*", parse_mode='Markdown')
        
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "*Использование: Купить серебрянный кейс (количество)*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower().startswith('купить золотой кейс'))
def buy_gold_case(message):
    try:
        parts = message.text.split()
        amount = int(parts[3]) if len(parts) > 3 else 1
        
        if amount <= 0:
            bot.send_message(message.chat.id, "*Количество должно быть больше 0!*", parse_mode='Markdown')
            return
        
        player = get_player_data(message.from_user.id)
        total_cost = amount * 300
        
        if player['dollars'] < total_cost:
            bot.send_message(message.chat.id, "*У вас недостаточно денег!*", parse_mode='Markdown')
            return
        
        player['dollars'] -= total_cost
        player['gold_cases'] += amount
        update_player_data(message.from_user.id, player)
        
        bot.send_message(message.chat.id, f"*Вы купили* `{amount}` *золотых кейсов за* `{total_cost}` *долларов!*", parse_mode='Markdown')
        
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "*Использование: Купить золотой кейс (количество)*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower() == 'открыть бронзовый кейс')
def open_bronze_case(message):
    player = get_player_data(message.from_user.id)
    
    if player['bronze_cases'] <= 0:
        bot.send_message(message.chat.id, "*У вас нет бронзовых кейсов!*", parse_mode='Markdown')
        return
    
    player['bronze_cases'] -= 1
    reward = random.randint(25, 75)
    player['dollars'] += reward
    update_player_data(message.from_user.id, player)
    
    bot.send_message(message.chat.id, f"*Вы открыли бронзовый кейс и получили* `{reward}` *долларов!*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower() == 'открыть серебрянный кейс')
def open_silver_case(message):
    player = get_player_data(message.from_user.id)
    
    if player['silver_cases'] <= 0:
        bot.send_message(message.chat.id, "*У вас нет серебрянных кейсов!*", parse_mode='Markdown')
        return
    
    player['silver_cases'] -= 1
    reward = random.randint(50, 150)
    player['dollars'] += reward
    update_player_data(message.from_user.id, player)
    
    bot.send_message(message.chat.id, f"*Вы открыли серебрянный кейс и получили* `{reward}` *долларов!*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower() == 'открыть золотой кейс')
def open_gold_case(message):
    player = get_player_data(message.from_user.id)
    
    if player['gold_cases'] <= 0:
        bot.send_message(message.chat.id, "*У вас нет золотых кейсов!*", parse_mode='Markdown')
        return
    
    player['gold_cases'] -= 1
    reward = random.randint(200, 400)
    player['dollars'] += reward
    update_player_data(message.from_user.id, player)
    
    bot.send_message(message.chat.id, f"*Вы открыли золотой кейс и получили* `{reward}` *долларов!*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower() == 'частные шахты')
def private_mines_info(message):
    text = """*⛏️ Частные шахты!*

*1. Бронзовая шахта -* `500`$ *(для покупки: "Купить бронзовую шахту")*

*2. Серебряная шахта -* `850`$ *(для покупки: "Купить серебрянную шахту")*

*3. Золотая шахта -* `1500`$ *(для покупки: "Купить золотую шахту")*"""
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower() == 'купить бронзовую шахту')
def buy_bronze_mine(message):
    player = get_player_data(message.from_user.id)
    
    if player.get('bronze_mine', False):
        bot.send_message(message.chat.id, "*У вас уже имеется бронзовая шахта!*", parse_mode='Markdown')
        return
    
    if player['dollars'] < 500:
        bot.send_message(message.chat.id, "*У вас недостаточно денег!*", parse_mode='Markdown')
        return
    
    player['dollars'] -= 500
    player['bronze_mine'] = True
    update_player_data(message.from_user.id, player)
    
    bot.send_message(message.chat.id, "*Вы купили бронзовую шахту за* `500` *долларов!*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower() == 'купить серебрянную шахту')
def buy_silver_mine(message):
    player = get_player_data(message.from_user.id)
    
    if player.get('silver_mine', False):
        bot.send_message(message.chat.id, "*У вас уже имеется серебрянная шахта!*", parse_mode='Markdown')
        return
    
    if player['dollars'] < 850:
        bot.send_message(message.chat.id, "*У вас недостаточно денег!*", parse_mode='Markdown')
        return
    
    player['dollars'] -= 850
    player['silver_mine'] = True
    update_player_data(message.from_user.id, player)
    
    bot.send_message(message.chat.id, "*Вы купили серебрянную шахту за* `850` *долларов!*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower() == 'купить золотую шахту')
def buy_gold_mine(message):
    player = get_player_data(message.from_user.id)
    
    if player.get('gold_mine', False):
        bot.send_message(message.chat.id, "*У вас уже имеется золотая шахта!*", parse_mode='Markdown')
        return
    
    if player['dollars'] < 1500:
        bot.send_message(message.chat.id, "*У вас недостаточно денег!*", parse_mode='Markdown')
        return
    
    player['dollars'] -= 1500
    player['gold_mine'] = True
    update_player_data(message.from_user.id, player)
    
    bot.send_message(message.chat.id, "*Вы купили золотую шахту за* `1500` *долларов!*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower() == 'копать в шахте')
def dig_in_mine(message):
    player = get_player_data(message.from_user.id)
    current_time = time.time()
    
    if not any([player.get('bronze_mine', False), player.get('silver_mine', False), player.get('gold_mine', False)]):
        bot.send_message(message.chat.id, "*У вас нет частных шахт!*", parse_mode='Markdown')
        return
    
    if current_time - player.get('last_mine_dig', 0) < 120:
        remaining_time = 120 - (current_time - player.get('last_mine_dig', 0))
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        bot.send_message(message.chat.id, f"*Вы устали, отдохните, можете копать в шахте через* `{minutes}` *минут* `{seconds}` *секунд*", parse_mode='Markdown')
        return
    
    results = []
    
    if player.get('bronze_mine', False):
        bronze_found = random.randint(1, 10)
        player['bronze'] += bronze_found
        results.append(f"`{bronze_found}` бронзы 🥉")
    
    if player.get('silver_mine', False):
        silver_found = random.randint(1, 10)
        player['silver'] += silver_found
        results.append(f"`{silver_found}` серебра 🥈")
    
    if player.get('gold_mine', False):
        gold_found = random.randint(1, 10)
        player['gold'] += gold_found
        results.append(f"`{gold_found}` золота 🪙")
    
    player['last_mine_dig'] = current_time
    update_player_data(message.from_user.id, player)
    
    result_text = ", ".join(results)
    bot.send_message(message.chat.id, f"*Вы покопали в своих шахтах и получили:* {result_text}*!*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower() == 'крафты')
def crafts_command(message):
    text = """*🔨 Крафт кейсов!*

*Подарочный кейс* - для крафта нужно `5` долларов и `25` железа *(Чтобы скрафтить, введите: "Скрафтить подарочный кейс")*

*Бронзовый кейс* - для крафта нужно `25` долларов и `50` бронзы *(Чтобы скрафтить, введите: "Скрафтить бронзовый кейс")*

*Серебрянный кейс* - для крафта нужно `50` долларов и `50` серебра *(Чтобы скрафтить, введите: "Скрафтить серебрянный кейс")*

*Золотой кейс* - для крафта нужно `150` долларов и `50` золота *(Чтобы скрафтить, введите: "Скрафтить золотой кейс")*"""
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower() == 'скрафтить подарочный кейс')
def craft_gift_case(message):
    player = get_player_data(message.from_user.id)
    
    if player['dollars'] < 5 or player['iron'] < 25:
        bot.send_message(message.chat.id, "*У вас недостаточно ресурсов! Нужно:* `5` *долларов и* `25` *железа*", parse_mode='Markdown')
        return
    
    player['dollars'] -= 5
    player['iron'] -= 25
    player['gift_cases'] += 1
    update_player_data(message.from_user.id, player)
    
    bot.send_message(message.chat.id, "*Вы скрафтили подарочный кейс!*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower() == 'скрафтить бронзовый кейс')
def craft_bronze_case(message):
    player = get_player_data(message.from_user.id)
    
    if player['dollars'] < 25 or player['bronze'] < 50:
        bot.send_message(message.chat.id, "*У вас недостаточно ресурсов! Нужно:* `25` *долларов и* `50` *бронзы*", parse_mode='Markdown')
        return
    
    player['dollars'] -= 25
    player['bronze'] -= 50
    player['bronze_cases'] += 1
    update_player_data(message.from_user.id, player)
    
    bot.send_message(message.chat.id, "*Вы скрафтили бронзовый кейс!*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower() == 'скрафтить серебрянный кейс')
def craft_silver_case(message):
    player = get_player_data(message.from_user.id)
    
    if player['dollars'] < 50 or player['silver'] < 50:
        bot.send_message(message.chat.id, "*У вас недостаточно ресурсов! Нужно:* `50` *долларов и* `50` *серебра*", parse_mode='Markdown')
        return
    
    player['dollars'] -= 50
    player['silver'] -= 50
    player['silver_cases'] += 1
    update_player_data(message.from_user.id, player)
    
    bot.send_message(message.chat.id, "*Вы скрафтили серебрянный кейс!*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower() == 'скрафтить золотой кейс')
def craft_gold_case(message):
    player = get_player_data(message.from_user.id)
    
    if player['dollars'] < 150 or player['gold'] < 50:
        bot.send_message(message.chat.id, "*У вас недостаточно ресурсов! Нужно:* `150` *долларов и* `50` *золота*", parse_mode='Markdown')
        return
    
    player['dollars'] -= 150
    player['gold'] -= 50
    player['gold_cases'] += 1
    update_player_data(message.from_user.id, player)
    
    bot.send_message(message.chat.id, "*Вы скрафтили золотой кейс!*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower().startswith('дать') and message.reply_to_message)
def give_money(message):
    try:
        amount = float(message.text.split()[1])
        
        if amount <= 0:
            bot.send_message(message.chat.id, "*Сумма должна быть больше 0!*", parse_mode='Markdown')
            return
        
        sender_id = message.from_user.id
        receiver_id = message.reply_to_message.from_user.id
        
        if sender_id == receiver_id:
            bot.send_message(message.chat.id, "*Нельзя передавать деньги самому себе!*", parse_mode='Markdown')
            return
        
        sender = get_player_data(sender_id)
        receiver = get_player_data(receiver_id)
        
        if sender['dollars'] < amount:
            bot.send_message(message.chat.id, "*У вас недостаточно денег!*", parse_mode='Markdown')
            return
        
        sender['dollars'] -= amount
        receiver['dollars'] += amount
        
        update_player_data(sender_id, sender)
        update_player_data(receiver_id, receiver)
        
        bot.send_message(message.chat.id, f"*Вы передали* `{format_number(amount)}` *долларов игроку* {receiver['name']}*!*", parse_mode='Markdown')
        
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "*Использование: Дать (сумма) в ответ на сообщение*", parse_mode='Markdown')



@bot.message_handler(func=lambda message: message.text.lower() == 'купить вип')
def buy_vip(message):
    player = get_player_data(message.from_user.id)
    
    if player['vip']:
        bot.send_message(message.chat.id, "*У вас уже есть VIP статус!*", parse_mode='Markdown')
        return
    
    if player['dollars'] < 1000:
        bot.send_message(message.chat.id, "*У вас недостаточно денег! Стоимость VIP:* `1000` *долларов*", parse_mode='Markdown')
        return
    
    player['dollars'] -= 1000
    player['vip'] = True
    update_player_data(message.from_user.id, player)
    
    bot.send_message(message.chat.id, "*Поздравляем! Вы купили VIP статус за* `1000` *долларов!*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower() == 'вип копать')
def vip_dig(message):
    player = get_player_data(message.from_user.id)
    
    if not player['vip']:
        bot.send_message(message.chat.id, "*У вас нет VIP статуса!*", parse_mode='Markdown')
        return
    
    current_time = time.time()
    
    if current_time - player.get('last_vip_dig', 0) < 90:
        remaining_time = 90 - (current_time - player.get('last_vip_dig', 0))
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        bot.send_message(message.chat.id, f"*Вы устали, отдохните, можете копать в VIP шахте через* `{minutes}` *минут* `{seconds}` *секунд*", parse_mode='Markdown')
        return
    
    dollars_found = random.randint(3, 12)
    player['dollars'] += dollars_found
    player['last_vip_dig'] = current_time
    update_player_data(message.from_user.id, player)
    
    bot.send_message(message.chat.id, f"*Вы зашли на территорию вип шахты, и выкопали* `{dollars_found}` *долларов!*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower() == 'вип бонус')
def vip_bonus(message):
    player = get_player_data(message.from_user.id)
    
    if not player['vip']:
        bot.send_message(message.chat.id, "*У вас нет VIP статуса!*", parse_mode='Markdown')
        return
    
    current_time = time.time()
    
    if current_time - player.get('last_vip_bonus', 0) < 86400:
        remaining_time = 86400 - (current_time - player.get('last_vip_bonus', 0))
        hours = int(remaining_time // 3600)
        minutes = int((remaining_time % 3600) // 60)
        bot.send_message(message.chat.id, f"*Я не богач, подожди* `{hours}` *часов* `{minutes}` *минут*", parse_mode='Markdown')
        return
    
    bonus = random.randint(10, 30)
    player['dollars'] += bonus
    player['last_vip_bonus'] = current_time
    update_player_data(message.from_user.id, player)
    
    bot.send_message(message.chat.id, f"😄 *Вы получили VIP бонус:* `{bonus}` *долларов!*", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text.lower() == 'трейд')
def trade_command(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("⚒️ Обмен ресурсов", callback_data="trade_resources")
    btn2 = telebot.types.InlineKeyboardButton("👑 Привилегии", callback_data="trade_privileges")
    btn3 = telebot.types.InlineKeyboardButton("📦 Кейсы", callback_data="trade_cases")
    markup.add(btn1)
    markup.add(btn2, btn3)
    
    bot.send_message(message.chat.id, "*Вы попали в обменник всего карьера!*\n*Зайдите в нужный раздел!*", 
                     parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "trade_resources")
def trade_resources_callback(call):
    text = """*Раздел ресурсов!*

`1` железо ⚙️ - `0.2` доллара $
`5` железа ⚙️ - `1` доллар $
`1` бронза 🥉 - `0.5` долларов $
`2` бронзы 🥉 - `1` долларов $
`1` серебро 🥈 - `1` доллар $
`1` золото 🥇 - `3` доллара $

*Для того чтобы совершить обмен - напишите: Обменять железо/бронзу/серебро/золото (сумма)*"""
    
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("⚒️ Обмен ресурсов", callback_data="trade_resources")
    btn2 = telebot.types.InlineKeyboardButton("👑 Привилегии", callback_data="trade_privileges")
    btn3 = telebot.types.InlineKeyboardButton("📦 Кейсы", callback_data="trade_cases")
    markup.add(btn1)
    markup.add(btn2, btn3)
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "trade_privileges")
def trade_privileges_callback(call):
    text = """*Раздел привилегии!* 👑

*1. Привилегия VIP*
*Стоимость - `1000`$*
*Возможности -> Помощь -> VIP*

*2. Привилегия Админ*
*Стоимость - Бесценна
*Выдаётся только администраторам проекта.*
*Возможности - доступны админ команды.*"""
    
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("⚒️ Обмен ресурсов", callback_data="trade_resources")
    btn2 = telebot.types.InlineKeyboardButton("👑 Привилегии", callback_data="trade_privileges")
    btn3 = telebot.types.InlineKeyboardButton("📦 Кейсы", callback_data="trade_cases")
    markup.add(btn1)
    markup.add(btn2, btn3)
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "trade_cases")
def trade_cases_callback(call):
    player = get_player_data(call.from_user.id)
    
    text = f"""*Кейсы!*

❗️*Нельзя открыть больше* `1` *кейса за раз!*

*1. Подарочный кейс, можно скрафтить или получить в бонусе, у вас в наличии:* `{player['gift_cases']}`

*2. Бронзовый кейс, стоимость:* `50`$*, у вас в наличии:* `{player['bronze_cases']}`

*3. Серебрянный кейс, стоимость:* `100`$*, у вас в наличии:* `{player['silver_cases']}`

*4. Золотой кейс, стоимость:* `300`$*, у вас в наличии:* `{player['gold_cases']}`

*Купить бронзовый кейс - Купить бронзовый кейс (колво)*
*Купить серебрянный кейс - Купить серебрянный кейс (колво)*
*Купить золотой кейс - Купить золотой кейс (колво)*"""
    
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("⚒️ Обмен ресурсов", callback_data="trade_resources")
    btn2 = telebot.types.InlineKeyboardButton("👑 Привилегии", callback_data="trade_privileges")
    btn3 = telebot.types.InlineKeyboardButton("📦 Кейсы", callback_data="trade_cases")
    markup.add(btn1)
    markup.add(btn2, btn3)
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.lower().startswith('казино'))
def casino_command(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.send_message(message.chat.id, "*Использование: казино (ставка)*", parse_mode='Markdown')
            return
            
        bet = round(float(parts[1]), 2)
        
        if bet < 5:
            bot.send_message(message.chat.id, "*Минимальная ставка:* `5` *долларов!*", parse_mode='Markdown')
            return
            
        player = get_player_data(message.from_user.id)
        
        if player['dollars'] < bet:
            bot.send_message(message.chat.id, "*У вас недостаточно денег!*", parse_mode='Markdown')
            return
        
        multipliers = [
            (0, 10), (0.2, 30), (0.5, 30), (1.0, 50),
            (1.2, 30), (1.5, 25), (2.0, 15), (5.0, 5)
        ]
        
        choices = []
        for mult, chance in multipliers:
            choices.extend([mult] * chance)
        
        multiplier = random.choice(choices)
        winnings = round(bet * multiplier, 2)
        
        player['dollars'] -= bet
        player['dollars'] += winnings
        player['dollars'] = round(player['dollars'], 2)
        update_player_data(message.from_user.id, player)
        
        result = "выиграли" if multiplier >= 1.0 else "проиграли"
        
        text = f"""👤 *Игрок:* `{player['name']}`
🗝 *Ставка:* `{format_number(bet)}`
*🍬 Множитель:* `{format_number(multiplier)}`
💎 *Вы {result}!*
*⚡ Вы получили:* `{format_number(winnings)}` *долларов!*"""
        
        bot.send_message(message.chat.id, text, parse_mode='Markdown')
        
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "*Использование: казино (ставка)*", parse_mode='Markdown')

if __name__ == "__main__":
    bot.polling(none_stop=True)