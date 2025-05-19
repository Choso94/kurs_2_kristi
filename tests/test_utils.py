import pytest
from src.utils import (
    filter_vacancies,
    sort_vacancies,
    get_top_vacancies,
    print_vacancies,
)
from src.vacancy import Vacancy


@pytest.fixture
def vacancies():
    return [
        Vacancy(
            "Python Developer",
            "https://hh.ru/vacancy/1",
            "100000-150000 RUR",
            "Python experience",
        ),
        Vacancy(
            "Java Developer",
            "https://hh.ru/vacancy/2",
            "80000-120000 RUR",
            "Java experience",
        ),
        Vacancy("No Salary", "https://hh.ru/vacancy/3", "Не указана", "No description"),
    ]


def test_filter_vacancies(vacancies):
    filtered = filter_vacancies(vacancies, ["python"])
    assert len(filtered) == 1
    assert filtered[0].title == "Python Developer"


def test_filter_vacancies_empty(vacancies):
    filtered = filter_vacancies(vacancies, [])
    assert len(filtered) == 3


def test_sort_vacancies(vacancies):
    sorted_vacs = sort_vacancies(vacancies)
    assert sorted_vacs[0].title == "Python Developer"
    assert sorted_vacs[1].title == "Java Developer"
    assert sorted_vacs[2].title == "No Salary"


def test_get_top_vacancies(vacancies):
    top = get_top_vacancies(vacancies, 2)
    assert len(top) == 2
    assert top[0].title == "Python Developer"
    assert top[1].title == "Java Developer"


def test_print_vacancies(capsys, vacancies):
    print_vacancies(vacancies[:1])
    captured = capsys.readouterr()
    assert "Вакансия 1:" in captured.out
    assert "Python Developer" in captured.out


def test_print_vacancies_empty(capsys):
    print_vacancies([])
    captured = capsys.readouterr()
    assert "Вакансии не найдены." in captured.out
