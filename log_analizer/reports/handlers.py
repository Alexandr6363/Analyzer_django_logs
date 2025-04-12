from collections import defaultdict
from typing import List
from log_analizer.parser.parser import parse_log_file

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

def generate_handler_report(log_files: List[str]) -> None:
    total_requests = defaultdict(int)
    all_handlers = defaultdict(lambda: defaultdict(int))

    for log_file in log_files:
        file_data = parse_log_file(log_file)
        for handler, levels in file_data.items():
            for level, count in levels.items():
                all_handlers[handler][level] += count
                total_requests[level] += count

    sorted_handlers = sorted(all_handlers.keys())

    print(f"Total requests: {sum(total_requests.values())}\n")
    print("HANDLER".ljust(24) + "\t".join(LOG_LEVELS))

    for handler in sorted_handlers:
        print(handler.ljust(24), end="")
        for level in LOG_LEVELS:
            print(f"{all_handlers[handler].get(level, 0):<8}", end="")
        print()

    print("".ljust(24), end="")
    for level in LOG_LEVELS:
        print(f"{total_requests[level]:<8}", end="")
    print()