import pytest
import requests
from src.api import HeadHunterAPI
from typing import List, Dict, Any

def test_connect_success(monkeypatch):
    """Тест успешного подключения к API."""
    class MockResponse:
        def __init__(self):
            self.status_code = 200
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: MockResponse())
    api = HeadHunterAPI()
    api._connect()  # Не должно выбросить исключение

def test_connect_failure(monkeypatch):
    """Тест неудачного подключения к API."""
    class MockResponse:
        def __init__(self):
            self.status_code = 404
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: MockResponse())
    api = HeadHunterAPI()
    with pytest.raises(Exception, match="Ошибка подключения: HTTP 404"):
        api._connect()

def test_get_vacancies_success(monkeypatch):
    """Тест успешного получения вакансий."""
    class MockResponse:
        def __init__(self):
            self.status_code = 200
        def json(self):
            return {"items": [{"name": "Job", "alternate_url": "https://hh.ru", "salary": None, "description": "Desc", "id": "1"}]}
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: MockResponse())
    api = HeadHunterAPI()
    vacancies = api.get_vacancies("test")
    assert len(vacancies) == 1
    assert vacancies[0]["title"] == "Job"

def test_get_vacancies_failure(monkeypatch, capsys):
    """Тест неудачного получения вакансий."""
    # Создаём два разных ответа: один для _connect, другой для get_vacancies
    def mock_get(*args, **kwargs):
        # Для _connect (без параметров, только базовый URL)
        if args[0] == "https://api.hh.ru/vacancies" and not kwargs.get("params"):
            class ConnectResponse:
                def __init__(self):
                    self.status_code = 200
                def json(self):  # Добавляем метод json, чтобы избежать ошибок
                    return {}
            return ConnectResponse()
        # Для get_vacancies (с параметрами)
        else:
            class FailResponse:
                def __init__(self):
                    self.status_code = 500
            return FailResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    api = HeadHunterAPI()
    # Проверяем, что метод возвращает пустой список вместо выброса исключения
    vacancies = api.get_vacancies("test")
    assert vacancies == [], "Ожидался пустой список при ошибке API"
    # Проверяем, что отладочное сообщение было выведено
    captured = capsys.readouterr()
    assert "Ошибка API: HTTP 500" in captured.out, "Ожидалось сообщение об ошибке API"