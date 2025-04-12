import pytest
from collections import defaultdict
from main import parse_log_file, generate_report 
import os


LOG_CONTENT = """\
2024-04-12 12:00:00,123 INFO myapp.views: GET /home
2024-04-12 12:00:01,456 ERROR myapp.views: POST /submit
2024-04-12 12:00:02,789 WARNING myapp.views: GET /home
2024-04-12 12:00:03,000 DEBUG myapp.views: GET /home
2024-04-12 12:00:04,000 WARNING myapp.views: POST /submit
"""

def test_parse_log_file(tmp_path):
    file_path = tmp_path / "test.log"
    file_path.write_text(LOG_CONTENT, encoding='utf-8')

    result = parse_log_file(str(file_path))

    assert isinstance(result, defaultdict)
    assert result["/home"]["INFO"] == 1
    assert result["/home"]["WARNING"] == 1
    assert result["/home"]["DEBUG"] == 1
    assert result["/submit"]["ERROR"] == 1
    assert result["/submit"]["WARNING"] == 1

def test_generate_report(tmp_path, capsys):
    file_path = tmp_path / "test.log"
    file_path.write_text(LOG_CONTENT, encoding='utf-8')

    generate_report([str(file_path)])
    captured = capsys.readouterr()

    assert "Total requests: 5" in captured.out
    assert "/home" in captured.out
    assert "/submit" in captured.out
    assert "INFO" in captured.out
    assert "ERROR" in captured.out
    assert "CRITICAL" in captured.out


def test_generate_report_file_not_exist(capsys):
    fake_file = "non_existent.log"
    generate_report([fake_file])
    captured = capsys.readouterr()
    assert f"Файл {fake_file} не существует." in captured.out
