import json
import random

# Фильмы по настроениям на двух языках
MOVIES = {
    'cry': {
        'rus': ["1+1", "Зеленая книга", "Хатико", "Форрест Гамп", "Побег из Шоушенка", "Список Шиндлера"],
        'eng': ["The Intouchables", "Green Book", "Hachiko", "Forrest Gump", "The Shawshank Redemption", "Schindler's List"]
    },
    'laugh': {
        'rus': ["Одни дома", "Иван Васильевич", "Бриллиантовая рука", "Мальчишник в Вегасе", "Операция Ы", "Джентельмены удачи"],
        'eng': ["Home Alone", "Ivan Vasilievich", "The Diamond Arm", "The Hangover", "Operation Y", "The Gentlemen of Fortune"]
    },
    'nostalgic': {
        'rus': ["Назад в будущее", "Титаник", "Гарри Поттер", "Король Лев", "Властелин колец", "Матрица"],
        'eng': ["Back to the Future", "Titanic", "Harry Potter", "The Lion King", "The Lord of the Rings", "The Matrix"]
    },
    'happy': {
        'rus': ["Отпуск по обмену", "В погоне за счастьем", "Амели", "Крупная рыба", "Поллианна", "Марли и я"],
        'eng': ["The Holiday", "The Pursuit of Happyness", "Amélie", "Big Fish", "Pollyanna", "Marley & Me"]
    }
}

# Словари с текстами кнопок
BUTTON_TEXTS = {
    "rus": {
        "cry": "Поплакать",
        "laugh": "Посмеяться",
        "nostalgic": "Поностальгировать",
        "happy": "Порадоваться",
        "another": "Еще фильм",
        "main_menu": "Главное меню",
        "language": "Язык",
        "russian": "Русский",
        "english": "English"
    },
    "eng": {
        "cry": "Cry",
        "laugh": "Laugh",
        "nostalgic": "Feel nostalgic",
        "happy": "Feel happy",
        "another": "Another movie",
        "main_menu": "Main Menu",
        "language": "Language",
        "russian": "Russian",
        "english": "English"
    }
}

def prepare_basic_text(scen):
    try:
        with open('basic.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get(scen, data["welcome"])
    except Exception as ex:
        print(f"Ошибка при загрузке basic.json: {ex}")
        return {"text": "welcome", "replies": {"Главное меню": "welcome"}}

def prepare_lang_text(scen, lang="rus", film=None):
    temp = prepare_basic_text(scen)
    
    try:
        with open(f'{lang}.json', 'r', encoding='utf-8') as f:
            lang_data = json.load(f)
        
        # Получаем текст для сценария
        text_key = temp["text"]
        if text_key in lang_data:
            final_text = lang_data[text_key]
            # Заменяем плейсхолдер {film} если передан фильм
            if film and "{film}" in final_text:
                final_text = final_text.replace("{film}", film)
        else:
            final_text = f"Текст для '{text_key}' не найден"
        
        # Создаем кнопки
        replies = {}
        button_texts = BUTTON_TEXTS.get(lang, BUTTON_TEXTS["rus"])
        
        for rep_key, callback_data in temp["replies"].items():
            button_text = button_texts.get(rep_key, rep_key)
            replies[button_text] = callback_data
        
        return {
            "text": final_text,
            "replies": replies
        }
        
    except Exception as ex:
        print(f'Ошибка в prepare_lang_text: {ex}')
        return temp

def get_random_movie(mood, lang="rus", previous_film=None):
    """Возвращает случайный фильм для настроения и языка, исключая предыдущий"""
    films_dict = MOVIES.get(mood, {})
    films = films_dict.get(lang, ["Movie not found"])
    
    # Если есть предыдущий фильм, исключаем его из выбора
    if previous_film and previous_film in films and len(films) > 1:
        films = [movie for movie in films if movie != previous_film]
    
    # Если все фильмы уже показаны, начинаем сначала
    if not films:
        films = films_dict.get(lang, ["Movie not found"])
    
    return random.choice(films)