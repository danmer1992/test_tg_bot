import requests
import telebot
from telebot import types
from TOKEN import API_KEY

def request_weather(city):
    API_KEY_WEATHER = "Your-api_key"
    towns = {"Казань": "Kazan", "Магадан": "Magadan", "Дубай": "Dubai","Анталия": "Antalya", "Сиде": "Side"}
    responce = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={towns[city]}&appid={API_KEY_WEATHER}&lang=RU",params={"units": "metric"})
    return responce

bot = telebot.TeleBot(API_KEY)
@bot.message_handler(commands=['start'])
def Hello(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard= True)
    keyboard.add(types.KeyboardButton("Узнать погоду"))
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}", reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def request_of_weather(message):
    if message.text == "Узнать погоду":
        inline_keyboard = types.InlineKeyboardMarkup()
        inline_keyboard.add(types.InlineKeyboardButton("Дубай",callback_data="Dubai"))
        inline_keyboard.add(types.InlineKeyboardButton("Казань",callback_data="Kazan"))
        inline_keyboard.add(types.InlineKeyboardButton("Магадан", callback_data="Magadan"))
        inline_keyboard.add(types.InlineKeyboardButton("Анталия", callback_data="Antalya"))
        inline_keyboard.add(types.InlineKeyboardButton("Сиде", callback_data="Side"))
        bot.send_message(message.chat.id, "Выберите город ",reply_markup=inline_keyboard)
@bot.callback_query_handler(func=lambda call: True)
def Answer(call):
    if call.message:
        if call.data == "Dubai":
            bot.send_message(call.message.chat.id,f"Температура в городе: {int(request_weather('Дубай').json()['main']['temp'])}\nСостояние: {request_weather('Дубай').json()['weather'][0]['description']}")
        elif call.data == "Kazan":
            bot.send_message(call.message.chat.id,f"Температура в городе: {int(request_weather('Казань').json()['main']['temp'])}\nСостояние: {request_weather('Казань').json()['weather'][0]['description']}")
        elif call.data == "Magadan":
            bot.send_message(call.message.chat.id,f"Температура в городе: {int(request_weather('Магадан').json()['main']['temp'])}\nСостояние: {request_weather('Магадан').json()['weather'][0]['description']}")
        elif call.data == "Antalya":
            bot.send_message(call.message.chat.id,f"Температура в городе: {int(request_weather('Анталия').json()['main']['temp'])}\nСостояние: {request_weather('Анталия').json()['weather'][0]['description']}")
        elif call.data == "Side":
            bot.send_message(call.message.chat.id,f"Температура в городе: {int(request_weather('Сиде').json()['main']['temp'])}\nСостояние: {request_weather('Сиде').json()['weather'][0]['description']}")
        bot.answer_callback_query(call.id)
bot.polling(none_stop=False)
