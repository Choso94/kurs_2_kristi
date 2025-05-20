import json
import os
import pytest
from src.file_worker import JSONSaver
from typing import List, Dict, Any

@pytest.fixture
def json_saver(tmp_path):
    """Фикстура для создания временного файла."""
    file_path = tmp_path / "test_vacancies.json"
    return JSONSaver(filename=str(file_path))

def test_add_vacancy(json_saver):
    """Тест добавления вакансии."""
    vacancy = {"title": "Test", "url": "https://test.com", "salary": "100000 RUR", "description": "Desc", "id": 1}
    json_saver.add_vacancy(vacancy)
    data = json_saver.get_vacancies({})
    assert len(data) == 1
    assert data[0]["title"] == "Test"

def test_add_duplicate_vacancy(json_saver):
    """Тест добавления дубликата вакансии."""
    vacancy = {"title": "Test", "url": "https://test.com", "salary": "100000 RUR", "description": "Desc", "id": 1}
    json_saver.add_vacancy(vacancy)
    json_saver.add_vacancy(vacancy)
    data = json_saver.get_vacancies({})
    assert len(data) == 1

def test_delete_vacancy(json_saver):
    """Тест удаления вакансии."""
    vacancy = {"title": "Test", "url": "https://test.com", "salary": "100000 RUR", "description": "Desc", "id": 1}
    json_saver.add_vacancy(vacancy)
    json_saver.delete_vacancy(1)
    data = json_saver.get_vacancies({})
    assert len(data) == 0

def test_get_vacancies_with_criteria(json_saver):
    """Тест получения вакансий по критериям."""
    vacancy1 = {"title": "Test Python", "url": "https://test.com", "salary": "100000 RUR", "description": "Python", "id": 1}
    vacancy2 = {"title": "Test Java", "url": "https://test.com", "salary": "200000 RUR", "description": "Java", "id": 2}
    json_saver.add_vacancy(vacancy1)
    json_saver.add_vacancy(vacancy2)
    filtered = json_saver.get_vacancies({"description": "Python"})
    assert len(filtered) == 1
    assert filtered[0]["title"] == "Test Python"