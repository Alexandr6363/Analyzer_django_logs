from collections import defaultdict
from typing import List
from log_analizer.parser.parser import parse_file


LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

def generate_handler_report(log_files: List[str]) -> None:
    """
    Функция для генерации отчета по обработчикам
    
    Параметры:
    log_files (List[str]): список путей к лог-файлам
    
    Возвращает:
    None (выводит отчет в консоль)
    """
    
    # Инициализируем счетчики
    total_count_requests = 0  # Общее количество запросов
    total_requests = defaultdict(int)  # Счетчик общего количества по уровням
    all_handlers = defaultdict(lambda: defaultdict(int))  # Словарь для хранения данных по всем обработчикам

    # Проходим по каждому лог-файлу
    for log_file in log_files:
        count_request, file_data = parse_file(log_file)  
        total_count_requests += count_request
        
        # Проходим по каждому обработчику и его уровням
        for handler, levels in file_data.items():
            for level, count in levels.items():
                # Обновляем счетчики
                all_handlers[handler][level] += count
                total_requests[level] += count

    # Сортируем обработчики по имени
    sorted_handlers = sorted(all_handlers.keys())

    # Выводим общий заголовок
    print(f"Total requests: {total_count_requests}\n")
    
    # Выводим шапку таблицы
    print("HANDLER".ljust(24) + "\t".join(LOG_LEVELS))

    # Выводим данные по каждому обработчику
    for handler in sorted_handlers:
        print(handler.ljust(24), end="")  # Выводим название обработчика
        for level in LOG_LEVELS:
            # Выводим количество для каждого уровня
            print(f"{all_handlers[handler].get(level, 0):<8}", end="")
        print()  # Переходим на новую строку

    # Выводим итоговую строку
    print("".ljust(24), end="")
    for level in LOG_LEVELS:
        print(f"{total_requests[level]:<8}", end="")
    print("")