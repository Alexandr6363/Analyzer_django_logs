import re

dict_result = {}

def extract_url(text):
    # Исправленное регулярное выражение
    url_pattern = r'/[a-zA-Z0-9$-_@.&+!*(),;:%#]+(?:/[a-zA-Z0-9-_.?=&+!*(),;:%#~+]+)*/'
    
    # Находим все совпадения
    urls = re.findall(url_pattern, text)
    
    return urls[0]

def count_log_levels(text):
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


def process_large_log_file(file_path):
    current_block = ""
    
    with open(file_path, 'r') as file:
        for line in file:
            if "django.request" in line:
                if current_block:
                    yield current_block.strip()
                current_block = line
            else:
                current_block += line
        
        # Возвращаем последний блок
        if current_block:
            yield current_block.strip()



file_path1 = "logs/app1.log"
file_path2 = "logs/app2.log"
file_path3 = "logs/app3.log"


def main(file_path):
    for i, block in enumerate(process_large_log_file(file_path)):
        current_url = extract_url(block)
        count_result_in_block = count_log_levels(block)
        if current_url in dict_result:
            dict1 = dict_result[current_url]
            dict2 = count_result_in_block
            dict_result[current_url] = {k: dict1.get(k, 0) + dict2.get(k, 0) for k in set(dict1) | set(dict2)}
        else:
            dict_result[current_url] = count_result_in_block



main(file_path1)
main(file_path2)
main(file_path3)

print(dict_result)


