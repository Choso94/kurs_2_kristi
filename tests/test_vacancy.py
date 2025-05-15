import pytest
from src.vacancy import Vacancy


def test_vacancy_init_valid():
    vacancy = Vacancy(
        title="Python Developer",
        url="http://hh.ru/vacancy/1",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        description="Требуется Python"
    )
    assert vacancy.title == "Python Developer"
    assert vacancy.url == "http://hh.ru/vacancy/1"
    assert vacancy.salary == "100000-150000 RUR"
    assert vacancy.description == "Требуется Python"


def test_vacancy_init_invalid_title():
    with pytest.raises(ValueError, match="Название вакансии"):
        Vacancy(title="", url="http://hh.ru/vacancy/1")


def test_vacancy_salary_not_specified():
    vacancy = Vacancy(
        title="Developer",
        url="http://hh.ru/vacancy/1",
        salary=None
    )
    assert vacancy.salary == "Не указана"


def test_vacancy_comparison():
    vacancy1 = Vacancy(
        title="Dev1",
        url="http://hh.ru/vacancy/1",
        salary={"from": 100000, "to": 150000}
    )
    vacancy2 = Vacancy(
        title="Dev2",
        url="http://hh.ru/vacancy/2",
        salary={"from": 50000, "to": 100000}
    )
    assert vacancy1 > vacancy2
    assert vacancy1 >= vacancy2
    assert vacancy2 < vacancy1
    assert vacancy2 <= vacancy1
    assert vacancy1 != vacancy2