from typing import List
from src.vacancy import Vacancy


def filter_vacancies(vacancies: List[Vacancy], keyword: str) -> List[Vacancy]:
    """
    Фильтрует вакансии по ключевому слову в описании.

    Args:
        vacancies: Список вакансий.
        keyword: Ключевое слово.

    Returns:
        List[Vacancy]: Отфильтрованный список.
    """
    return [v for v in vacancies if keyword.lower() in v.description.lower()]


def get_top_vacancies(vacancies: List[Vacancy], n: int) -> List[Vacancy]:
    """
    Возвращает топ N вакансий по зарплате.

    Args:
        vacancies: Список вакансий.
        n: Количество вакансий.

    Returns:
        List[Vacancy]: Топ N вакансий.
    """
    return sorted(vacancies, reverse=True)[:n] if n <= len(vacancies) else sorted(vacancies, reverse=True)


def filter_by_salary_range(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """
    Фильтрует вакансии по диапазону зарплат.

    Args:
        vacancies: Список вакансий.
        salary_range: Диапазон зарплат в формате "100000-150000".

    Returns:
        List[Vacancy]: Отфильтрованный список.
    """
    if not salary_range or "-" not in salary_range:
        return vacancies
    try:
        min_salary, max_salary = map(float, salary_range.split("-"))
        return [
            v for v in vacancies
            if v._get_salary_value()[0] >= min_salary and v._get_salary_value()[1] <= max_salary
        ]
    except ValueError:
        return vacancies