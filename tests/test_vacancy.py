import pytest
from src.vacancy import Vacancy
from typing import List, Dict, Any

def test_vacancy_creation():
    """Тест создания вакансии."""
    v = Vacancy("Test Job", "https://hh.ru", "100000-150000 RUR", "Test desc")
    assert v.title == "Test Job"
    assert v.salary == "100000-150000 RUR"
    assert v.description == "Test desc"

def test_vacancy_comparison():
    """Тест сравнения вакансий по зарплате."""
    v1 = Vacancy("Job1", "https://hh.ru", "100000-150000 RUR", "Desc")
    v2 = Vacancy("Job2", "https://hh.ru", "80000-120000 RUR", "Desc")
    assert v1 > v2
    assert v2 < v1
    assert v1 == v1

def test_vacancy_validation():
    """Тест валидации данных вакансии."""
    v = Vacancy("", "", "", "")
    assert v.salary == "Зарплата не указана"
    assert v.title == "Неизвестная вакансия"
    assert v.url == ""
    assert v.description == ""

def test_vacancy_salary_parsing():
    """Тест парсинга зарплаты."""
    v = Vacancy("Job", "https://hh.ru", "100000-200000 RUR", "Desc")
    min_salary, max_salary = v._get_salary_value()
    assert min_salary == 100000
    assert max_salary == 200000
    v_single = Vacancy("Job", "https://hh.ru", "150000 RUR", "Desc")
    min_single, max_single = v_single._get_salary_value()
    assert min_single == 150000
    assert max_single == 150000
    v_invalid = Vacancy("Job", "https://hh.ru", "", "Desc")
    min_invalid, max_invalid = v_invalid._get_salary_value()
    assert min_invalid == 0.0
    assert max_invalid == 0.0

def test_cast_to_object_list():
    """Тест преобразования списка словарей в список объектов."""
    data = [{"title": "Job1", "url": "https://hh.ru", "salary": "100000 RUR", "description": "Desc", "id": 1}]
    vacancies = Vacancy.cast_to_object_list(data)
    assert len(vacancies) == 1
    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].title == "Job1"