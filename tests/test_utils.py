import pytest
from src.vacancy import Vacancy
from src.utils import filter_vacancies, get_top_vacancies, filter_by_salary_range
from typing import List

def test_filter_vacancies():
    """Тест фильтрации по описанию."""
    v1 = Vacancy("Job1", "https://hh.ru", "100000 RUR", "Python developer")
    v2 = Vacancy("Job2", "https://hh.ru", "120000 RUR", "Java developer")
    vacancies = [v1, v2]
    filtered = filter_vacancies(vacancies, "python")
    assert len(filtered) == 1
    assert filtered[0].title == "Job1"

def test_get_top_vacancies():
    """Тест получения топ-N вакансий."""
    v1 = Vacancy("Job1", "https://hh.ru", "100000 RUR", "Desc")
    v2 = Vacancy("Job2", "https://hh.ru", "120000 RUR", "Desc")
    vacancies = [v1, v2]
    top = get_top_vacancies(vacancies, 1)
    assert len(top) == 1
    assert top[0].title == "Job2"

def test_filter_by_salary_range():
    """Тест фильтрации по диапазону зарплат."""
    v1 = Vacancy("Job1", "https://hh.ru", "100000-150000 RUR", "Desc")
    v2 = Vacancy("Job2", "https://hh.ru", "200000-250000 RUR", "Desc")
    vacancies = [v1, v2]
    filtered = filter_by_salary_range(vacancies, "100000-200000")
    assert len(filtered) == 1
    assert filtered[0].title == "Job1"