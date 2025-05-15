import pytest
from unittest.mock import patch
from src.interaction import user_interaction


@patch("builtins.input", side_effect=["Python", "3", "2", "django", "3"])
@patch("src.api.HeadHunterAPI.get_vacancies")
def test_user_interaction(mock_get_vacancies, mock_input, capsys):
    mock_get_vacancies.return_value = [
        {
            "name": "Python Developer",
            "alternate_url": "http://hh.ru/vacancy/1",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "snippet": {"requirement": "Django experience"}
        }
    ]
    user_interaction()
    captured = capsys.readouterr()
    assert "Python Developer" in captured.out
    assert "Django" in captured.out