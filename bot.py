import telebot
from main import graph 
from dotenv import load_dotenv
import os   

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
user_sessions = {}

HELLO = """
Привет! Этот бот - часть резюме для вакансии Python-разработчика в SETTERS.
Данный бот испольует базу знаний из канала Евгения Давыдова https://t.me/hutzp \n
Задавай вопрос, ответ придет на основе всех постов канала
- что главное в жизни? 
- все ли могут быть предпринимателями?
- как найти свое призвание?"""


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, HELLO)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if user_sessions.get(message.from_user.id) == 'find':
        bot.reply_to(message, 'уже идет поиск ответа, подожди немного...')
        return
    user_sessions[message.from_user.id] = 'find'
    bot.reply_to(message, 'начинаю поиск ответа...')
    res = graph.invoke({"question": message.text})
    if res["answer"]:
        bot.reply_to(message, res["answer"])
        user_sessions[message.from_user.id] = 'done'


if __name__ == '__main__':
    bot.infinity_polling()