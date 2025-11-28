import telebot
from config import BOT_TOKEN
from telebot import types
from viewer import prepare_lang_text, get_random_movie

bot = telebot.TeleBot(BOT_TOKEN)

# Храним выбор языка, последнее настроение и последний фильм пользователей
user_languages = {}
user_moods = {}
user_last_films = {}

def get_user_language(user_id):
    return user_languages.get(user_id, "rus")

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    show_language_selection(message.chat.id, user_id)

def show_language_selection(chat_id, user_id):
    """Показывает выбор языка"""
    lang = get_user_language(user_id)
    scene_data = prepare_lang_text("language", lang)
    
    markup = types.InlineKeyboardMarkup()
    for button_text, callback_data in scene_data["replies"].items():
        markup.add(types.InlineKeyboardButton(button_text, callback_data=callback_data))
    
    bot.send_message(chat_id, scene_data["text"], reply_markup=markup)

def show_main_menu(chat_id, user_id, notification_text=None):
    """Показывает главное меню на выбранном языке"""
    lang = get_user_language(user_id)
    scene_data = prepare_lang_text("welcome", lang)
    
    markup = types.InlineKeyboardMarkup()
    for button_text, callback_data in scene_data["replies"].items():
        markup.add(types.InlineKeyboardButton(button_text, callback_data=callback_data))
    
    if notification_text:
        bot.send_message(chat_id, notification_text)
    
    bot.send_message(chat_id, scene_data["text"], reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id
    
    # Обработка выбора языка
    if call.data == "switch_rus":
        user_languages[user_id] = "rus"
        show_main_menu(call.message.chat.id, user_id, "Язык изменен на Русский")
        return
    
    elif call.data == "switch_eng":
        user_languages[user_id] = "eng"
        show_main_menu(call.message.chat.id, user_id, "Language changed to English")
        return
    
    lang = get_user_language(user_id)
    
    # Обработка выбора настроения
    if call.data in ["cry", "laugh", "nostalgic", "happy"]:
        mood = call.data
        user_moods[user_id] = mood
        previous_film = user_last_films.get(user_id)
        film = get_random_movie(mood, lang, previous_film)
        user_last_films[user_id] = film
        scene_data = prepare_lang_text(mood, lang, film)
        
        markup = types.InlineKeyboardMarkup()
        for button_text, callback_data in scene_data["replies"].items():
            markup.add(types.InlineKeyboardButton(button_text, callback_data=callback_data))
        
        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=scene_data["text"],
                reply_markup=markup
            )
        except Exception as e:
            bot.send_message(call.message.chat.id, scene_data["text"], reply_markup=markup)
    
    # Обработка "еще фильм" для каждого настроения
    elif call.data in ["another_cry", "another_laugh", "another_nostalgic", "another_happy"]:
        mood = call.data.replace("another_", "")
        user_moods[user_id] = mood
        previous_film = user_last_films.get(user_id)
        film = get_random_movie(mood, lang, previous_film)
        user_last_films[user_id] = film
        scene_data = prepare_lang_text(mood, lang, film)
        
        markup = types.InlineKeyboardMarkup()
        for button_text, callback_data in scene_data["replies"].items():
            markup.add(types.InlineKeyboardButton(button_text, callback_data=callback_data))
        
        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=scene_data["text"],
                reply_markup=markup
            )
        except Exception as e:
            bot.send_message(call.message.chat.id, scene_data["text"], reply_markup=markup)
    
    # Меню выбора языка
    elif call.data == "language":
        show_language_selection(call.message.chat.id, user_id)
    
    # Главное меню
    elif call.data == "welcome":
        show_main_menu(call.message.chat.id, user_id)

@bot.message_handler(commands=['help'])
def help_command(message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    
    scene_data = prepare_lang_text("help", lang)
    
    markup = types.InlineKeyboardMarkup()
    for button_text, callback_data in scene_data["replies"].items():
        markup.add(types.InlineKeyboardButton(button_text, callback_data=callback_data))
    
    bot.send_message(message.chat.id, text=scene_data["text"], reply_markup=markup)

@bot.message_handler(commands=['about'])
def about(message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    
    scene_data = prepare_lang_text("about", lang)
    
    markup = types.InlineKeyboardMarkup()
    for button_text, callback_data in scene_data["replies"].items():
        markup.add(types.InlineKeyboardButton(button_text, callback_data=callback_data))
    
    bot.send_message(message.chat.id, text=scene_data["text"], reply_markup=markup)

@bot.message_handler(commands=['lang'])
def change_language(message):
    """Команда для смены языка"""
    user_id = message.from_user.id
    show_language_selection(message.chat.id, user_id)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    """Обработка текстовых сообщений"""
    user_id = message.from_user.id
    show_main_menu(message.chat.id, user_id)

if __name__ == "__main__":
    print("Movie bot started...")
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(f"Bot error: {e}")