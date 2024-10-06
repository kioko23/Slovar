import telebot
import threading
import re
import psycopg2
conn = psycopg2.connect(
        host="127.0.0.1",
        database="my_slovar",
        user="postgres",
        password="tashkent88",
        port=5432
    )

cursor = conn.cursor()

# Замените 'YOUR_BOT_TOKEN' на ваш токен, полученный от BotFather
TOKEN = '7977665644:AAE4lENEdOG0jI0GEK2yGMtaJDjV1aP5mCU'
bot = telebot.TeleBot(TOKEN)

# Глобальный словарь для хранения переводов
slovar = {}
def kirilica(text):
    if re.match(r'^[А-Яа-я]', text):
        return True
    else:
        return False
def latinica(text):
    if re.match(r'^[A-Za-z]', text):
        return True
    else:
        return False

def PerevodSlova(chat_id):
    """Функция для добавления слова и его перевода в словарь."""
    bot.send_message(chat_id, "Введите слово для перевода (английское слово):")
    bot.register_next_step_handler_by_chat_id(chat_id, get_word)

def get_word(message):
    """Получение слова от пользователя и регистрация следующего шага для ввода перевода."""
    word = message.text
    chat_id = message.chat.id
    if latinica(word):  # Если слово не на кириллице, запрашиваем перевод
        bot.send_message(chat_id, f"Введите перевод для слова '{word}':")
        bot.register_next_step_handler_by_chat_id(chat_id, get_translation, word)
    else:  # Если введено слово на кириллице, запрашиваем повторный ввод
        bot.send_message(chat_id, "Введите слово на английском:")
        bot.register_next_step_handler_by_chat_id(chat_id, get_word)  # Правильная регистрация повторного шага

def get_translation(message, word):
    """Получение перевода и добавление его в словарь."""
    translation = message.text
    chat_id = message.chat.id
    if kirilica(translation):  # Проверка, что перевод на русском
        cursor.execute("INSERT INTO slovar (english_word, russian_word) VALUES (%s, %s)", (word, translation))
        conn.commit()

        bot.send_message(chat_id, f"Слово '{word}' добавлено с переводом '{translation}'.")
        bot.send_message(chat_id, "Операция завершена. Спасибо!")
    else:  # Если перевод не на кириллице, запрашиваем корректный перевод
        bot.send_message(chat_id, f"Слово '{translation}' не на русском. Пожалуйста, введите перевод на русском языке:")
        bot.register_next_step_handler_by_chat_id(chat_id, get_translation, word)

def Vivod(chat_id):
    """Функция для вывода словаря пользователю."""
    cursor.execute("SELECT * FROM slovar;")
    records = cursor.fetchall()
    if records:
        for record in records:
            # Преобразуем каждую запись в строку для отправки
            record_str = ", ".join(map(str, record))  # Преобразуем кортеж в строку
            bot.send_message(chat_id, record_str)

    else:
        bot.send_message(chat_id, "Ваш словарь пуст.")



def start_logic(chat_id):
    """Запуск опроса пользователя для выбора действий."""
    # bot.send_message(chat_id, "Если хотите добавить слово, напишите 1. Если хотите вывести словарь, напишите 2. Для завершения напишите что-то другое.")
    bot.register_next_step_handler_by_chat_id(chat_id, process_choice)

def process_choice(message):
    """Обработка выбора пользователя."""
    choice = message.text
    chat_id = message.chat.id

    if choice == '1':
        PerevodSlova(chat_id)
    elif choice == '2':
        Vivod(chat_id)
    else:
        bot.send_message(chat_id, "Завершение работы.")
        return  # Выход из функции завершает цикл

    # # После выполнения действия предлагаем снова выбрать
    # bot.send_message(chat_id, "Выберите следующее действие. Напишите 1 для добавления слова или 2 для вывода словаря. Напишите что-то другое для выхода.")
    # bot.register_next_step_handler_by_chat_id(chat_id, process_choice)


@bot.message_handler(commands=['start'])
def start_handler(message):
    """Запуск логики через команду /start."""
    chat_id = message.chat.id
    bot.send_message(chat_id, "Запускаю режим ввода. Напишите 1 для добавления слова или 2 для вывода словаря.")
    start_logic(chat_id)  # Запуск первой итерации логики

if __name__ == '__main__':
    print("Бот готов к работе...")
    bot.polling(none_stop=True)





