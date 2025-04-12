import pytest
from ..reports.handlers import generate_handler_report

LOG = """\
2024-04-12 12:00:00,123 INFO django.request: GET /api/
2024-04-12 12:00:01,456 DEBUG django.request: GET /api/
2024-04-12 12:00:02,789 ERROR django.request: POST /login/
"""

def test_generate_handler_report(capsys, tmp_path):
    log_file = tmp_path / "log.log"
    log_file.write_text(LOG, encoding='utf-8')

    generate_handler_report([str(log_file)])
    output = capsys.readouterr().out

    assert "Total requests: 3" in output
    assert "/api/" in output
    assert "/login/" in output