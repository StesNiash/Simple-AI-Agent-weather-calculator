# Модуль общих утилит, в основном для работы с данными.
import os

def load_env_variables():
    # Load environment variables from .env file if it exists
    if os.path.exists(".env"):
        with open(".env", "r") as env_file:
            for line in env_file:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

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