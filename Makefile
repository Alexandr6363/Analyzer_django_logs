# Общие настройки
PYTHON := python3
VENV := venv
ACTIVATE := $(VENV)/bin/activate
PIP := $(VENV)/bin/pip
PROJECT_DIR := log_analizer

# Цели
.PHONY: help init clean test lint format run docs

# Вывод справки
help:
	@echo "init - создать виртуальное окружение и установить зависимости"
	@echo "test - запустить тесты"
	@echo "run - запустить основной скрипт"

# Инициализация проекта
init: $(VENV) requirements.txt
	@echo "Создаем виртуальное окружение..."
	$(PYTHON) -m venv $(VENV)
	@echo "Устанавливаем зависимости..."
	. $(ACTIVATE) && $(PIP) install -r requirements.txt

# Создание виртуального окружения
$(VENV):
	$(PYTHON) -m venv $(VENV)

# Запуск основного скрипта
run:
	. $(ACTIVATE) && python3 main.py logs/app1.log logs/app2.log logs/app3.log --report handlers

# Запуск тестов
test:
	. $(ACTIVATE) && pytest $(PROJECT_DIR)/tests



