import json
import os
import urllib.request
import urllib.parse
import urllib.error


def get_weather(location):
    '''
    Получает текущую погоду для указанного местоположения через WorldWeatherOnline API.

    :param location: Название города, почтовый индекс, IP или координаты (широта,долгота)
    :return: Словарь с ключами success, error (при неудаче), либо данными о погоде
    '''
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return {
            "success": False,
            "error": "WEATHER_API_KEY не установлен. Добавьте его в .env файл."
        }

    base_url = "https://api.worldweatheronline.com/premium/v1/weather.ashx"
    params = {
        "key": api_key,
        "q": location,
        "format": "json",
        "num_of_days": "1",
        "lang": "ru",
        "tp": "24",
    }

    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())

        # WWO при неверном ключе может вернуть 200 с ошибкой в теле
        if "data" not in data or "error" in data.get("data", {}):
            error_msg = data.get("data", {}).get("error", [{}])[0].get("msg", "Неизвестная ошибка API")
            return {"success": False, "error": error_msg}

        current = data["data"]["current_condition"][0]
        request_query = data["data"]["request"][0]["query"]

        temp_c = current["temp_C"]
        feels_like = current["FeelsLikeC"]
        humidity = current["humidity"]
        description = current["weatherDesc"][0]["value"]
        wind_speed = current["windspeedKmph"]
        wind_dir = current["winddir16Point"]
        pressure = current["pressure"]
        cloudcover = current["cloudcover"]

        return {
            "success": True,
            "location": request_query,
            "temperature_c": temp_c,
            "feels_like_c": feels_like,
            "humidity": humidity,
            "description": description,
            "wind_speed_kmh": wind_speed,
            "wind_direction": wind_dir,
            "pressure_mb": pressure,
            "cloud_cover_percent": cloudcover,
        }

    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"HTTP ошибка {e.code}: {e.reason}"}
    except urllib.error.URLError as e:
        return {"success": False, "error": f"Ошибка соединения: {e.reason}"}
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return {"success": False, "error": f"Ошибка обработки ответа API: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Неизвестная ошибка: {e}"}


def format_weather_report(data):
    '''
    Форматирует результат get_weather() в человекочитаемую строку.
    '''
    if not data.get("success"):
        return f"[Ошибка] {data.get('error', 'Неизвестная ошибка')}"

    return (
        f"Погода в {data['location']}: {data['temperature_c']}°C, {data['description']}. "
        f"Ощущается как {data['feels_like_c']}°C. "
        f"Влажность: {data['humidity']}%. "
        f"Ветер: {data['wind_speed_kmh']} км/ч, {data['wind_direction']}. "
        f"Давление: {data['pressure_mb']} гПа. "
        f"Облачность: {data['cloud_cover_percent']}%."
    )

if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv(".env")

    if not os.getenv("WEATHER_API_KEY"):
        print("WEATHER_API_KEY не найден в .env. Добавьте строку: WEATHER_API_KEY=ваш_ключ")
    else:
        print("=== Тест 1: London ===")
        result = get_weather("London")
        print(format_weather_report(result))
        print()

        print("=== Тест 2: Москва ===")
        result = get_weather("Moscow")
        print(format_weather_report(result))
        print()

        print("=== Тест 3: Пустой запрос (проверка ошибки) ===")
        result = get_weather("")
        print(format_weather_report(result))
        print()

        print("=== Тест 4: Сырые данные (raw JSON) ===")
        result = get_weather("Tokyo")
        if result.get("success"):
            import pprint
            pprint.pprint(result)
        else:
            print(format_weather_report(result))
