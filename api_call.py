# Модуль, ответственный за выполнение API-запросов к внешним сервисам (LLM).

import openai
from utils import get_api_key, get_base_url, get_system_prompt
from memory_utils import crop_history

def get_client():
    base_url = get_base_url()
    api_key = get_api_key()
    if api_key and base_url:
        client = openai.OpenAI(api_key=api_key, base_url=base_url)
        return client
    print("Не удалось создать клиента LLM. Убедитесь, что переменные окружения LLM_API_KEY и LLM_BASE_URL установлены.")
    return None

def call_llm(history, model="gpt-3.5-turbo"):
    """
    Выполняет API-запрос к LLM с учетом STM.
    
    :param system_prompt: Строка с системным промптом в начале истории.
    :param history: Список словарей с историей сообщений (каждое сообщение должно иметь ключи "role" и "content").
    :param model: Название модели LLM, которую нужно использовать (по умолчанию "gpt-3.5-turbo").
    :return: Ответ от LLM в виде строки.
    """
    try:
        client = get_client()
        if not client:
            return None

        system_prompt_str = get_system_prompt()
        cropped_history = crop_history(history)

        messages = [{"role": "system", "content": system_prompt_str}]
        messages.extend(cropped_history)
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Ошибка при вызове LLM API с историей: {e}")
        return None