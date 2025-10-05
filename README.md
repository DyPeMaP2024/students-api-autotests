# Students API — автотесты

Тестовый фреймворк для http://93.77.188.34/apidocs (ручки `/student`).

## Стек

- Python 3.10+
- pytest
- requests
- allure-pytest

## Установка

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Запуск

```bash
pytest
```

Результаты для Allure складываются в `allure-results/`.

Отчёт (нужен Allure CLI):

```bash
allure serve allure-results
```

## Структура

- `api/students_client.py` — обёртка над HTTP
- `tests/` — сценарии GET/POST/PUT/DELETE
- `BUGS.md` — найденные дефекты API

## Автор

ДЗ по тестированию API (Петрович-ТЕХ).
