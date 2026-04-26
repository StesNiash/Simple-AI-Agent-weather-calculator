# This is the main entry point for the LLM chat application. It initializes the chat interface and handles user input.
import os

from api_call import call_llm
from utils import check_for_api_key, check_for_base_url, load_env_variables

class LLM_Chat:
    def __init__(self):
        self.chat_history = []

    def send_message(self, message):
        self.chat_history.append({"role": "user", "content": message})
        response = call_llm(self.chat_history)
        if response:
            print(f"LLM: {response}")
            self.chat_history.append({"role": "assistant", "content": response})
        else:
            print("Не удалось получить ответ от LLM.")

def get_api_key_from_user():
    print("Вы хотите ввести API-ключ для LLM? (y/n)")
    choice = input().strip().lower()
    if choice != 'n':
        api_key = input("Введите ваш API-ключ для LLM: ").strip()
        os.environ["LLM_API_KEY"] = api_key
        with open(".env", "a") as env_file:
            env_file.write(f"LLM_API_KEY={api_key}\n")
        print("API-ключ сохранен.")
        return True
    else:
        print("API-ключ не был сохранен. Пожалуйста, убедитесь, что переменная окружения LLM_API_KEY установлена.")
        return False

def get_base_url_from_user():
    print("Вы хотите ввести базовый URL для LLM? (y/n)")
    choice = input().strip().lower()
    if choice != 'n':
        base_url = input("Введите базовый URL для LLM (оставьте пустым для использования openrouter.ai): ").strip()
        if not base_url:
            base_url = "https://openrouter.ai/api/v1"
        os.environ["LLM_BASE_URL"] = base_url
        # save in .env file for future use        
        with open(".env", "a") as env_file:
            env_file.write(f"LLM_BASE_URL={base_url}\n")
        print("Базовый URL сохранен.")
        return True
    else:
        print("Базовый URL не был сохранен. Пожалуйста, убедитесь, что переменная окружения LLM_BASE_URL установлена.")
        return False

def initialize_chat():
    # Ensure the API key and base URL are loaded before starting the chat
    load_env_variables()
    if not check_for_api_key():
        print("Переменная окружения LLM_API_KEY не установлена.")
        if not get_api_key_from_user():
            return False
    if not check_for_base_url():
        print("Пременная окружения LLM_BASE_URL не установлена.")
        if not get_base_url_from_user():
            return False
    return True

def new_chat():
    print("Начинаем новый чат... Напишите 'exit' чтобы закончить. Используйте 'new' чтобы начать новый чат.")
    return LLM_Chat()

if __name__ == "__main__":
    print("Инициализация чата...")
    if not initialize_chat():
        print("Инициализация чата не удалась.")
        exit(1)
    chat = new_chat()
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Exiting chat. Goodbye!")
            break
        elif user_input.lower() == "new":
            chat = new_chat()
        else:
            chat.send_message(user_input)