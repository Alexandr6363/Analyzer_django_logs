import re


def file_to_block(file_path: str):
    """
    Функция для чтения файла и разделения его на блоки по метке django.request
    
    Параметры:
    file_path (str): путь к файлу
    
    Возвращает:
    генератор блоков текста
    """
    current_block = ""
    
    with open(file_path, 'r') as file:
        for line in file:
            if "django.request" in line:
                # Если нашли новую метку django.request
                if current_block:
                    # Если есть текущий блок, возвращаем его
                    yield current_block.strip()
                current_block = line
            else:
                # Добавляем строку к текущему блоку
                current_block += line
        
        # Возвращаем последний блок
        if current_block:
            yield current_block.strip()


def extract_url(text: str) -> str:
    """
    Функция для извлечения URL из текста
    
    Параметры:
    text (str): текст для поиска URL
    
    Возвращает:
    str: найденный URL
    """
    # Регулярное выражение для поиска URL
    url_pattern = r'/[a-zA-Z0-9$-_@.&+!*(),;:%#]+(?:/[a-zA-Z0-9-_.?=&+!*(),;:%#~+]+)*/'
    
    # Находим все совпадения
    urls = re.findall(url_pattern, text)
    
    return urls[0]


def count_log_levels(text: str) -> dict:
    """
    Функция для подсчета уровней логирования в тексте
    
    Параметры:
    text (str): текст для анализа
    
    Возвращает:
    dict: словарь с количеством каждого уровня логирования
    """
    # Создаем словарь для хранения результатов
    result = {
        "DEBUG": 0,
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
        "CRITICAL": 0
    }
    
    # Разбиваем текст на слова
    words = text.split()
    
    # Проходим по каждому слову
    for word in words:
        # Убираем знаки препинания с начала и конца слова
        clean_word = word.strip(".,:;!?()[]{}\"'-")
        
        # Проверяем, есть ли слово в нашем списке уровней логирования
        if clean_word in result:
            # Увеличиваем счетчик для найденного уровня
            result[clean_word] += 1
    
    return result


def parse_file(file_path:str) -> dict:
    """
    Основная функция для парсинга файла
    
    Параметры:
    file_path (str): путь к файлу
    
    Возвращает:
    dict: словарь с результатами анализа
    """
    
    # Инициализируем переменные
    dict_result = {}  # Словарь для хранения результатов
    count_request = 0  # Счетчик запросов
    
    # Проходим по всем блокам файла
    for i, block in enumerate(file_to_block(file_path)):
        # Увеличиваем счетчик запросов
        count_request += 1
        
        # Извлекаем URL из текущего блока
        current_url = extract_url(block)
        
        # Подсчитываем уровни логирования в текущем блоке
        count_result_in_block = count_log_levels(block)
        
        # Проверяем, есть ли такой URL в результатах
        if current_url in dict_result:
            # Если есть, получаем текущие счетчики для этого URL
            dict1 = dict_result[current_url]
            dict2 = count_result_in_block
            
            # Суммируем счетчики для одинаковых ключей
            dict_result[current_url] = {
                k: dict1.get(k, 0) + dict2.get(k, 0) 
                for k in set(dict1) | set(dict2)
            }
        else:
            # Если URL встречается впервые, добавляем его в результаты
            dict_result[current_url] = count_result_in_block
    
    # Возвращаем кортеж с количеством запросов и результатами
    return (count_request, dict_result)



