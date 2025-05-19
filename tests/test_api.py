import pytest
import requests
from unittest.mock import patch
from src.api import HeadHunterAPI


@pytest.fixture
def hh_api():
    return HeadHunterAPI()


@patch("requests.get")
def test_get_vacancies_success(mock_get, hh_api):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "items": [
            {"name": "Python Developer", "alternate_url": "https://hh.ru/vacancy/123"}
        ]
    }
    vacancies = hh_api.get_vacancies("Python")
    assert len(vacancies) == 1
    assert vacancies[0]["name"] == "Python Developer"


@patch("requests.get")
def test_get_vacancies_empty(mock_get, hh_api):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"items": []}
    vacancies = hh_api.get_vacancies("Python")
    assert vacancies == []


@patch("requests.get")
def test_get_vacancies_connection_error(mock_get, hh_api):
    mock_get.side_effect = requests.ConnectionError("No internet")
    with pytest.raises(Exception, match="Ошибка подключения"):
        hh_api.get_vacancies("Python")


@patch("requests.get")
def test_get_vacancies_http_error(mock_get, hh_api):
    mock_get.side_effect = requests.HTTPError(
        response=type("Response", (), {"status_code": 404})()
    )
    with pytest.raises(Exception, match="Ошибка API: HTTP 404"):
        hh_api.get_vacancies("Python")
