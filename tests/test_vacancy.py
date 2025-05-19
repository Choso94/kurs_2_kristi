import pytest
from src.vacancy import Vacancy


def test_vacancy_init_valid():
    vacancy = Vacancy(
        title="Python Developer",
        url="https://hh.ru/vacancy/1",
        salary="100000-150000 RUR",
        description="Требуется Python",
    )
    assert vacancy.title == "Python Developer"
    assert vacancy.url == "https://hh.ru/vacancy/1"
    assert vacancy.salary == "100000-150000 RUR"
    assert vacancy.description == "Требуется Python"


def test_vacancy_init_invalid_title():
    with pytest.raises(ValueError, match="Название должно быть непустой строкой"):
        Vacancy(
            title="",
            url="https://hh.ru/vacancy/1",
            salary="100000-150000 RUR",
            description="Тест",
        )


def test_vacancy_salary_not_specified():
    vacancy = Vacancy(
        title="Developer", url="https://hh.ru/vacancy/1", salary="", description="Тест"
    )
    assert vacancy.salary == "Не указана"


def test_vacancy_comparison():
    vacancy1 = Vacancy(
        title="Dev1",
        url="https://hh.ru/vacancy/1",
        salary="100000-150000 RUR",
        description="Тест1",
    )
    vacancy2 = Vacancy(
        title="Dev2",
        url="https://hh.ru/vacancy/2",
        salary="80000-120000 RUR",
        description="Тест2",
    )
    assert vacancy1 > vacancy2


def test_cast_to_object_list():
    data = [
        {
            "name": "Python Developer",
            "alternate_url": "https://hh.ru/vacancy/1",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "snippet": {"requirement": "Python experience"},
        },
        {
            "title": "Java Developer",
            "url": "https://hh.ru/vacancy/2",
            "salary": "80000-120000 RUR",
            "description": "Java experience",
        },
    ]
    vacancies = Vacancy.cast_to_object_list(data)
    assert len(vacancies) == 2
    assert vacancies[0].title == "Python Developer"
    assert vacancies[1].title == "Java Developer"
