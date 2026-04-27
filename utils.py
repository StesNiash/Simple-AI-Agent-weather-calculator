# Модуль общих утилит, в основном для работы с данными.
import os
import dotenv

def load_env_variables():
    # Load environment variables from .env file if it exists
    if os.path.exists(".env"):
        dotenv.load_dotenv(".env")

def get_base_url():
    base_url = os.getenv("LLM_BASE_URL")
    if base_url:
        return base_url
    else:
        print("Базовый URL для LLM не найден. Пожалуйста, установите переменную окружения LLM_BASE_URL.")
        return None

def check_for_base_url():
    base_url = os.getenv("LLM_BASE_URL")
    if base_url:
        return True
    else:
        return False

def get_api_key():
    api_key = os.getenv("LLM_API_KEY")
    if api_key:
        return api_key
    else:
        print("API-ключ для LLM не найден. Пожалуйста, установите переменную окружения LLM_API_KEY.")
        return None

def check_for_api_key():
    api_key = os.getenv("LLM_API_KEY")
    if api_key:
        return True
    else:
        return False

def get_system_prompt():
    """
    Возвращает системный промпт для LLM, который задает контекст и инструкции для модели.
    
    :return: Строка с системным промптом.
    """
    return '''
Ты - помощник, который помогает пользователю с задачами.
У тебя в распоряжении есть инструменты для получения текущей погоды и калькулятор для выполнения математических операций.
Ты должен использовать эти инструменты, когда это необходимо, чтобы помочь пользователю.
'''
def get_weather_api_key():
    weather_api_key = os.getenv("WEATHER_API_KEY")
    if weather_api_key:
        return weather_api_key
    else:
        print("API-ключ для погоды (WEATHER_API_KEY) не найден. Установите его в .env файле.")
        return None

def check_for_weather_api_key():
    weather_api_key = os.getenv("WEATHER_API_KEY")
    if weather_api_key:
        return True
    else:
        return False
