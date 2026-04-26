# Утилиты для работы с памятью и историей сообщений.

import tiktoken

def crop_history(history, max_tokens=3000):
    """
    Обрезает историю сообщений, чтобы она не превышала заданное количество токенов.
    
    :param history: Список словарей с историей сообщений (каждое сообщение должно иметь ключи "role" и "content").
    :param max_tokens: Максимальное количество токенов для истории (по умолчанию 3000).
    :return: Обрезанная история сообщений.
    """
    # Инициализируем переменные
    total_tokens = 0
    cropped_history = []
    
    # Проходим по истории в обратном порядке, начиная с последнего сообщения
    for message in reversed(history):
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        tokens = encoding.encode(message["content"])
        message_tokens_count = len(tokens)
        
        # Если добавление этого сообщения не превышает лимит, добавляем его в обрезанную историю
        if total_tokens + message_tokens_count <= max_tokens:
            cropped_history.append(message)
            total_tokens += message_tokens_count
        else:
            break
    
    # Возвращаем обрезанную историю в правильном порядке
    return list(reversed(cropped_history))
