from googletrans import Translator
import requests
import telebot
from telebot import types
from TOKEN import API_KEY, API_KEY_WEATHER

def translate(city):
    translator = Translator()
    result = translator.translate(city, dest='en')
    return result.text

bot = telebot.TeleBot(API_KEY)
@bot.message_handler(commands=['start'])
def Hello(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard= True)
    keyboard.add(types.KeyboardButton("Узнать погоду"))
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}", reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def request_of_weather(message):
    if message.text == "Узнать погоду":
        msg = bot.send_message(message.chat.id, "Введите город, в котором хотите узнать погоду")
        bot.register_next_step_handler(msg, answer)

@bot.message_handler(content_types=['text'])
def answer(message):
    town = message.text.strip().capitalize()
    result_weather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={translate(town)}&appid={API_KEY_WEATHER}&lang=RU&units=metric")
    if result_weather.status_code == 200:
        bot.reply_to(message,f"Температура: {int(result_weather.json()['main']['temp'])}\nСостояние: {result_weather.json()['weather'][0]['description']}")
        win = bot.send_message(message.chat.id, f"{message.from_user.id}")
        bot.register_next_step_handler(win, answer)
    else:
        lose = bot.send_message(message.chat.id,f"Такого города не существует {message.from_user.first_name},\nлибо вы неправильно написали название города.")
        bot.register_next_step_handler(lose, answer)

bot.polling(none_stop=True)
