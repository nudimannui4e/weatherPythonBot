import requests
import datetime
from config import bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши название города:")

@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        country = data["sys"]["country"]
        city = data["name"]
        cur_weather = data["main"]["temp"]
        desc_weather = data["weather"][0]["main"]
        if desc_weather in code_to_smile:
            wd = code_to_smile[desc_weather]
        else:
            wd = "Посмотри в окно, что-то непонятное"
        wind = data["wind"]["speed"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        await message.reply(f"\U000026A1--сводка-погоды--\U000026A1\n"
              f"Погода в городе: {city}\nСтрана: {country}\n"
              f"Температура: {cur_weather}°C {wd}\n"
              f"Макс: {temp_max} °C\nМин:  {temp_min} °C\nВетер: {wind} м/с\n"
              f"Влажность: {humidity}%\nДавление {pressure} мм рт.ст\n"
              f"Рассвет: {sunrise}\nЗакат:   {sunset}\n"
              f"Продолжительность дня: {length_of_day}")
    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")

if __name__ == '__main__':
    executor.start_polling(dp)
