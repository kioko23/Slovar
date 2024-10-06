import psycopg2
import telebot
TOKEN = '7977665644:AAE4lENEdOG0jI0GEK2yGMtaJDjV1aP5mCU'

conn = psycopg2.connect(
        host="127.0.0.1",
        database="my_slovar",
        user="postgres",
        password="tashkent88",
        port=5432
    )
cursor = conn.cursor()

dict = {}

import re
def kirilica(text):
    if re.match(r'^[A-Za-z]', text):
        return False
    elif re.match(r'^[А-Яа-я]', text):
        return True


def PerevodSlova():
    while True:
        world = input("Введите слово на английском (или 'exit' для выхода): ")
        if world.lower() == 'exit':
            break
        if kirilica(world):
            print("ВВедите слово на английском")
            continue


        if world in dict:
            print("слово уже есть в словаре")
        slovo = input("Введите перевод на русском: ")
        if not kirilica(slovo):
            print("Введите слово на русском")
            continue
        dict[world] = slovo
        print(f"Слово '{world}' добавлено с переводом '{slovo}'")


def Vivod():
    print("\nВаш словарь:")
    for key, value in dict.items():
        print(f"{key}: {value}")
    return 1



for key, value in dict.items():
    cursor.execute("INSERT INTO slovar (english_word, russian_word) VALUES (%s, %s)", (key, value))
    conn.commit()


cursor.execute("SELECT * FROM slovar;")
records = cursor.fetchall()

for record in records:
    print(record)
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    while True:
        vivod = input("если хотите добавить слово, напишите 1, если хотите вывести словарь напишите 2")
        if int(vivod) == 1:
            PerevodSlova()
        elif int(vivod) == 2:
            print(Vivod())
        else:
            break
    """Обработчик команды /start."""
    bot.send_message(message.chat.id, "Привет! Я ваш новый Telegram-бот.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """Обработчик для всех текстовых сообщений, который отвечает тем же текстом."""
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)