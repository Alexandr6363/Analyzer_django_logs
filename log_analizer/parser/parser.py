import re
from collections import defaultdict


"""
2025-03-28 12:00:48,000 INFO django.request: GET /admin/login/ 204 OK [192.168.1.51]
2025-03-28 12:13:21,000 WARNING django.security: ConnectionError: Failed to connect to payment gateway
2025-03-28 12:05:33,000 INFO django.request: GET /admin/dashboard/ 204 OK [192.168.1.69]
2025-03-28 12:26:26,000 ERROR django.request: Internal Server Error: /api/v1/checkout/ [192.168.1.90] - ConnectionError: Failed to connect to payment gateway
2025-03-28 12:18:25,000 ERROR django.request: Internal Server Error: /admin/dashboard/ [192.168.1.90] - DatabaseError: Deadlock detected
2025-03-28 12:45:52,000 DEBUG django.db.backends: (0.32) SELECT * FROM 'shipping' WHERE id = 51;
2025-03-28 12:13:12,000 INFO django.request: GET /api/v1/payments/ 201 OK [192.168.1.90]
2025-03-28 12:35:15,000 INFO django.request: GET /admin/dashboard/ 201 OK [192.168.1.37]
"""

def parse_log_file(file_path: str) -> defaultdict:
    request_counts = defaultdict(lambda: defaultdict(int))
    pattern = re.compile(
        r'(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL).*?(?P<handler>[/\w\.]+/)'

                         )
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                level = match.group('level')
                handler = match.group('handler')
                request_counts[handler][level] += 1
    return request_counts

