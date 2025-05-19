import pytest
from unittest.mock import patch
from src.api import HeadHunterAPI


@pytest.fixture
def hh_api():
    return HeadHunterAPI()


@patch("requests.get")
def test_connect_success(mock_get, hh_api):
    mock_get.return_value.status_code = 200
    hh_api._connect()  # Не должно выбросить исключение


@patch("requests.get")
def test_connect_failure(mock_get, hh_api):
    mock_get.return_value.status_code = 404
    with pytest.raises(ConnectionError, match="Ошибка подключения"):
        hh_api._connect()


@patch("requests.get")
def test_get_vacancies(mock_get, hh_api):
    mock_response = {
        "items": [
            {"name": "Python Developer", "alternate_url": "http://hh.ru/vacancy/1"},
            {"name": "Java Developer", "alternate_url": "http://hh.ru/vacancy/2"},
        ],
        "pages": 1,
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response
    vacancies = hh_api.get_vacancies("Python")
    assert len(vacancies) == 2
    assert vacancies[0]["name"] == "Python Developer"
