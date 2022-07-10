import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_cmd_message(message: types.Message):
    await message.reply("Привет! Введите название города!")


@dp.message_handler()
async def get_weather(message: types.Message):
        
    сode_to_smile = {
        "Clear": "Ясно \U00002600", 
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614", 
        "Drizzle": "Моросящий Дождь \U00002614", 
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
  
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()   

        city = data['name']
        cur_weather = data['main']['temp']

        weather_description = data["weather"][0]["main"]
        if weather_description in сode_to_smile:
            wd = сode_to_smile[weather_description]
        
        else:
            wd = "Посмотри в окно, не могу понять что там не так!"
        
        
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(
            data['sys']['sunrise'])
        
        
        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода в городе: {city}\nТемпература:{cur_weather}C° {wd} \n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind}\n"
              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
              f"***Хорошего дня!***"
              )


    except:     
        await message.reply('\U00002620 Проверьте названия введеного города! \U00002620')



if __name__ == "__main__":
    try:
        executor.start_polling(dp)
    except Exception:
        os._exit(0)