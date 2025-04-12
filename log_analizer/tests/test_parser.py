import pytest
from ..parser.parser import parse_file

LOG = """\
2025-03-27 12:38:43,000 INFO django.request: GET /api/v1/users/ 200 OK [192.168.1.98]
2025-03-27 12:44:49,000 INFO django.request: GET /admin/dashboard/ 200 OK [192.168.1.77]
2025-03-27 12:47:46,000 WARNING django.security: IntegrityError: duplicate key value violates unique constraint
2025-03-27 12:19:42,000 ERROR django.request: Internal Server Error: /api/v1/products/ [192.168.1.99] - SuspiciousOperation: Invalid HTTP_HOST header
2025-03-27 12:28:34,000 WARNING django.security: OSError: No space left on device
2025-03-27 12:40:30,000 CRITICAL django.core.management: ConnectionError: Failed to connect to payment gateway
2025-03-27 12:22:27,000 INFO django.request: GET /api/v1/support/ 204 OK [192.168.1.26]
2025-03-27 12:45:09,000 DEBUG django.db.backends: (0.48) SELECT * FROM 'shipping' WHERE id = 17;
"""

def test_parse_file(tmp_path):
    file_path = tmp_path / "sample.log"
    file_path.write_text(LOG, encoding='utf-8')

    count, result = parse_file(str(file_path))

    assert result["/api/v1/users/"]["INFO"] == 1
    assert result["/admin/dashboard/"]["INFO"] == 1
    assert result["/api/v1/support/"]["INFO"] == 1
    assert result["/api/v1/products/"]["ERROR"] == 1
    assert count == 4