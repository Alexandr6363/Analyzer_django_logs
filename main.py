import argparse
import os
from log_analizer.reports import get_report

def main() -> None:
    parser = argparse.ArgumentParser(description="Анализатор логов Django")
    parser.add_argument('log_files', metavar='log_files', type=str, nargs='+', help="Пути к лог-файлам")
    parser.add_argument('--report', type=str, required=True, help="Тип отчета (например, handlers)")

    args = parser.parse_args()

    # Проверка на существование файлов
    for path in args.log_files:
        if not os.path.exists(path):
            print(f"Файл {path} не существует.")
            return

    # Получение отчета
    report_func = get_report(args.report)
    if not report_func:
        print(f"Неизвестный тип отчета: {args.report}")
        return

    report_func(args.log_files)

if __name__ == "__main__":
    main()