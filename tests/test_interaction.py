import pytest
from src.interaction import user_interaction
from src.api import HeadHunterAPI
from src.vacancy import Vacancy
from unittest.mock import patch

def test_user_interaction_exit():
    """Тест выхода из интерфейса."""
    with patch("builtins.input", side_effect=["8"]):
        user_interaction()

def test_user_interaction_search(monkeypatch):
    """Тест поиска вакансий."""
    class MockResponse:
        def __init__(self):
            self.status_code = 200
        def json(self):
            return {
                "items": [
                    {"name": "Job1", "alternate_url": "https://hh.ru", "salary": {"from": 100000, "to": 150000, "currency": "RUR"}, "description": "Desc", "id": "1"}
                ]
            }
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: MockResponse())
    with patch("builtins.input", side_effect=["1", "Python", "8"]):
        user_interaction()

def test_user_interaction_invalid_choice():
    """Тест обработки неверного выбора."""
    with patch("builtins.input", side_effect=["9", "8"]):
        with patch("builtins.print") as mocked_print:
            user_interaction()
            mocked_print.assert_any_call("Введите число от 1 до 8.")

def test_user_interaction_add_vacancy():
    """Тест добавления вакансии."""
    with patch("builtins.input", side_effect=["5", "Test Job", "https://hh.ru", "100000 RUR", "Description", "8"]):
        with patch("src.file_worker.JSONSaver.add_vacancy") as mocked_add:
            user_interaction()
            mocked_add.assert_called()

def test_user_interaction_filter_description(monkeypatch):
    """Тест фильтрации по описанию."""
    class MockResponse:
        def __init__(self):
            self.status_code = 200
        def json(self):
            return {
                "items": [
                    {"name": "Job1", "alternate_url": "https://hh.ru", "salary": None, "description": "Python", "id": "1"}
                ]
            }
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: MockResponse())
    with patch("builtins.input", side_effect=["1", "Python", "2", "Python", "8"]):
        user_interaction()

def test_user_interaction_top_vacancies(monkeypatch):
    """Тест вывода топ вакансий."""
    class MockResponse:
        def __init__(self):
            self.status_code = 200
        def json(self):
            return {
                "items": [
                    {"name": "Job1", "alternate_url": "https://hh.ru", "salary": {"from": 100000, "to": 150000, "currency": "RUR"}, "description": "Desc", "id": "1"}
                ]
            }
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: MockResponse())
    with patch("builtins.input", side_effect=["1", "Python", "3", "1", "8"]):
        user_interaction()

def test_user_interaction_salary_filter(monkeypatch):
    """Тест фильтрации по зарплате."""
    class MockResponse:
        def __init__(self):
            self.status_code = 200
        def json(self):
            return {
                "items": [
                    {"name": "Job1", "alternate_url": "https://hh.ru", "salary": {"from": 100000, "to": 150000, "currency": "RUR"}, "description": "Desc", "id": "1"}
                ]
            }
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: MockResponse())
    with patch("builtins.input", side_effect=["1", "Python", "4", "100000-150000", "8"]):
        user_interaction()