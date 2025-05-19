import pytest
from src.file_worker import JSONSaver


@pytest.fixture
def json_saver(tmp_path):
    filename = tmp_path / "test_vacancies.json"
    return JSONSaver(filename=str(filename))


def test_add_vacancy(json_saver):
    vacancy = {
        "title": "Python Developer",
        "url": "http://hh.ru/vacancy/1",
        "salary": "100000-150000 RUR",
        "description": "Требуется Python",
    }
    json_saver.add_vacancy(vacancy)
    vacancies = json_saver.get_vacancies({})
    assert len(vacancies) == 1
    assert vacancies[0]["title"] == "Python Developer"


def test_add_vacancy_no_duplicates(json_saver):
    vacancy = {
        "title": "Python Developer",
        "url": "http://hh.ru/vacancy/1",
        "salary": "100000-150000 RUR",
        "description": "Требуется Python",
    }
    json_saver.add_vacancy(vacancy)
    json_saver.add_vacancy(vacancy)
    vacancies = json_saver.get_vacancies({})
    assert len(vacancies) == 1


def test_delete_vacancy(json_saver):
    vacancy = {
        "title": "Python Developer",
        "url": "http://hh.ru/vacancy/1",
        "salary": "100000-150000 RUR",
        "description": "Требуется Python",
    }
    json_saver.add_vacancy(vacancy)
    json_saver.delete_vacancy(vacancy)
    vacancies = json_saver.get_vacancies({})
    assert len(vacancies) == 0
