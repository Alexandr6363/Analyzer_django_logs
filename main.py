import argparse
import os
import re
from collections import defaultdict
from typing import List


# Функция для чтения одного файла
def parse_log_file(file_path: str) -> defaultdict:
    request_counts = defaultdict(lambda: defaultdict(int))  # [handler][level]
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.search(r'(?P<timestamp>\S+ \S+),\d+\s+(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)\s+(?P<component>[\w\.]+):\s+(?P<method>\S+)\s+(?P<handler>/[^\s]+)', line)

            if match:
                level = match.group('level')
                handler = match.group('handler')
                request_counts[handler][level] += 1
    return request_counts


# Функция для генерации отчета
def generate_report(log_files: List[str]) -> None:
    total_requests = defaultdict(int)  # [handler][level]
    all_handlers = defaultdict(lambda: defaultdict(int))

    # Обработка каждого лог-файла
    for log_file in log_files:
        if not os.path.exists(log_file):
            print(f"Файл {log_file} не существует.")
            return
        file_data = parse_log_file(log_file)
        for handler, levels in file_data.items():
            for level, count in levels.items():
                all_handlers[handler][level] += count
                total_requests[level] += count

    # Сортировка в алфавитном порядке
    sorted_handlers = sorted(all_handlers.keys())

    # Вывод отчета
    print(f"Total requests: {sum(total_requests.values())}\n")
    print("HANDLER", "\t".join(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]))

    for handler in sorted_handlers:
        print(f"{handler:20}", end="")
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            print(f"{all_handlers[handler].get(level, 0):<8}", end="")
        print()

    # Общий итог
    print(f"{'':20}", end="")
    for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        print(f"{total_requests[level]:<8}", end="")
    print()


# Основная точка входа
def main() -> None:
    parser = argparse.ArgumentParser(description="Анализатор логов Django")
    parser.add_argument('log_files', metavar='log_files', type=str, nargs='+', help="Пути к лог-файлам")
    parser.add_argument('--report', type=str, choices=['handlers'], required=True, help="Тип отчета")

    args = parser.parse_args()

    # Проверка правильности аргументов
    if args.report == "handlers":
        generate_report(args.log_files)


if __name__ == "__main__":
    main()
