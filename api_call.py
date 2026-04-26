# Модуль, ответственный за выполнение API-запросов к внешним сервисам (LLM).

import openai
from utils import get_api_key, get_base_url, get_system_prompt

def get_client():
    base_url = get_base_url()
    api_key = get_api_key()
    if api_key and base_url:
        client = openai.OpenAI(api_key=api_key, base_url=base_url)
        return client
    print("Не удалось создать клиента LLM. Убедитесь, что переменные окружения LLM_API_KEY и LLM_BASE_URL установлены.")
    return None

def crop_history(history, max_tokens=3000):
    """
    Обрезает историю сообщений, чтобы она не превышала заданное количество токенов.
    
    :param history: Список словарей с историей сообщений (каждое сообщение должно иметь ключи "role" и "content").
    :param max_tokens: Максимальное количество токенов для истории (по умолчанию 3000).
    :return: Обрезанная история сообщений.
    """
    # 1 токен в среднем соответствует примерно 4 символам, но для простоты будем считать 1 токен = 1 слову
    total_tokens = 0
    cropped_history = []
    
    # Проходим по истории в обратном порядке, начиная с последнего сообщения
    for message in reversed(history):
        # Подсчитываем количество токенов в текущем сообщении (1 токен = 1 слово)
        message_tokens = len(message["content"].split())
        
        # Если добавление этого сообщения не превышает лимит, добавляем его в обрезанную историю
        if total_tokens + message_tokens <= max_tokens:
            cropped_history.append(message)
            total_tokens += message_tokens
        else:
            break
    
    # Возвращаем обрезанную историю в правильном порядке
    return list(reversed(cropped_history))

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