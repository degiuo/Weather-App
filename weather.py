import os
import sys
import math
from pyowm import OWM
from pyowm.commons.exceptions import NotFoundError, UnauthorizedError
from dotenv import load_dotenv
from googletrans import Translator
import asyncio

async def trans(text, translator):
    try:
        text_translate = await translator.translate(text, dest='ru')
        return text_translate.text
    except Exception as e:
        print(f"Ошибка перевода: {e}")
        return text


async def main():
    load_dotenv('.env')
    translator = Translator()

    api_key = os.getenv('OpenWeatherMapApi')
    if not  api_key:
        print("Ошибка: API ключ OpenWeatherMap не найден в файле .env")
        print("Убедитесь, что переменная OpenWeatherMapApi установлена")
        return
    
    if len(sys.argv) < 2:
        print("Ошибка: не указан город")
        print("Использование: python weather.py <название_города>")
        return
    
    city = sys.argv[1]

    try: 
        owm = OWM(api_key)
        mgr = owm.weather_manager()

        observation = mgr.weather_at_place(city)
        w = observation.weather

        temp_dict = w.temperature('celsius')
        temp = math.trunc(temp_dict['temp'])
        
        translator = Translator()
        status = await trans(w.detailed_status, translator)

        print(f'Город: {city}')
        print(f'Температура(°C): {temp}')
        print(f'Описание погоды: {status}')
    
    except NotFoundError:
        print(f"Ошибка: Город '{city}' не найден")
        print("Проверьте правильность написания названия города на английском или русском языке")
    except UnauthorizedError:
        print("Ошибка: Неверный API ключ OpenWeatherMap")
        print("Проверьте ключ в файле")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        print("Пожалуйста, проверьте соединение и правильность ввода")


if __name__ == "__main__":
    asyncio.run(main())