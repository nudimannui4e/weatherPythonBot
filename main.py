import requests
from pprint import pprint
from config import open_weather_token
import datetime


def get_weather(city, open_weather_token):

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
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        # pprint(data)
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

        print(f"Погода в городе: {city}\nСтрана: {country}\n"
              f"Температура: {cur_weather}°C {wd}\n"
              f"Макс: {temp_max}°C\nМин: {temp_min}°C\nВетер: {wind}м/с\n"
              f"Влажность: {humidity}%\nДавление {pressure} мм рт.ст\n"
              f"Рассвет: {sunrise}\nЗакат: {sunset}\n"
              f"Продолжительность дня: {length_of_day}")
    except Exception as ex:
        print(ex)
        print("Проверьте название города.")


def main():
    city = input("Введите город: ")
    get_weather(city, open_weather_token)


if __name__ == "__main__":
    main()
