import argparse
import os
from log_analizer.reports import get_report

def main() -> None:
    """
    Основная функция программы, запускающая весь процесс анализа логов
    
    Создает парсер аргументов, проверяет существование файлов и вызывает соответствующий
    генератор отчета на основе переданных параметров
    """
    
    # Создаем парсер аргументов командной строки
    parser = argparse.ArgumentParser(description="Анализатор логов Django")
    
    # Добавляем обязательные позиционные аргументы
    parser.add_argument(
        'log_files', 
        metavar='log_files', 
        type=str, 
        nargs='+', 
        help="Пути к лог-файлам"
    )
    
    # Добавляем обязательный именованный аргумент
    parser.add_argument(
        '--report', 
        type=str, 
        required=True, 
        help="Тип отчета (например, handlers)"
    )
    
    # Парсим аргументы командной строки
    args = parser.parse_args()
    
    # Проверяем существование всех переданных файлов
    for path in args.log_files:
        if not os.path.exists(path):
            print(f"Файл {path} не существует.")
            return
    
    # Получаем функцию генерации отчета по его типу
    report_func = get_report(args.report)
    
    # Проверяем, существует ли функция для генерации такого отчета
    if not report_func:
        print(f"Неизвестный тип отчета: {args.report}")
        return
    
    # Вызываем функцию генерации отчета с переданными файлами
    report_func(args.log_files)

if __name__ == "__main__":
    """
    Точка входа в программу
    Запускает основную функцию при запуске скрипта напрямую
    """
    main()