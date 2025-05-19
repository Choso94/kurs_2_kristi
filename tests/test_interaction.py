from unittest.mock import patch
from src.interaction import user_interaction


@patch("builtins.input", side_effect=["y", "3"])
@patch("builtins.print")
@patch("src.interaction.os.path.exists", return_value=True)
@patch(
    "src.interaction.json.load",
    return_value=[
        {
            "title": "Python Developer",
            "url": "https://hh.ru/vacancy/123",
            "salary": "100000-150000 RUR",
            "description": "Python experience",
        }
    ],
)
def test_user_interaction_local(mock_json_load, mock_exists, mock_print, mock_input):
    user_interaction()
    mock_print.assert_any_call("Добро пожаловать в поиск вакансий на hh.ru!")
    mock_print.assert_any_call("До свидания!")


@patch("builtins.input", side_effect=["n", "Python", "3"])
@patch("builtins.print")
@patch(
    "src.interaction.HeadHunterAPI.get_vacancies",
    return_value=[
        {
            "name": "Python Developer",
            "alternate_url": "https://hh.ru/vacancy/123",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "snippet": {"requirement": "Python experience"},
        }
    ],
)
def test_user_interaction_api(mock_get_vacancies, mock_print, mock_input):
    user_interaction()
    mock_print.assert_any_call("Добро пожаловать в поиск вакансий на hh.ru!")
    mock_print.assert_any_call("До свидания!")


@patch("builtins.input", side_effect=["invalid", "y", "3"])
@patch("builtins.print")
@patch("src.interaction.os.path.exists", return_value=True)
@patch("src.interaction.json.load", return_value=[])
def test_user_interaction_invalid_input(
    mock_json_load, mock_exists, mock_print, mock_input
):
    user_interaction()
    mock_print.assert_any_call("Ошибка: введите 'да', 'нет', 'y' или 'n'.")
    mock_print.assert_any_call("В файле vacancies.json нет валидных вакансий.")


@patch("builtins.input", side_effect=["y", "1", "2", "3"])
@patch("builtins.print")
@patch("src.interaction.os.path.exists", return_value=True)
@patch(
    "src.interaction.json.load",
    return_value=[
        {
            "title": "Python Developer",
            "url": "https://hh.ru/vacancy/123",
            "salary": "100000-150000 RUR",
            "description": "Python experience",
        }
    ],
)
def test_user_interaction_top_n(mock_json_load, mock_exists, mock_print, mock_input):
    user_interaction()
    mock_print.assert_any_call("Вакансия 1:")
    mock_print.assert_any_call("До свидания!")
