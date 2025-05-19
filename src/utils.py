from typing import List
from src.vacancy import Vacancy


def filter_vacancies(
    vacancies: List[Vacancy], filter_words: List[str]
) -> List[Vacancy]:
    """Фильтрует вакансии по ключевым словам в описании."""
    if not filter_words:
        return vacancies
    return [
        v
        for v in vacancies
        if any(word.lower() in v.description.lower() for word in filter_words)
    ]


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Сортирует вакансии по зарплате (по убыванию)."""
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], n: int) -> List[Vacancy]:
    """Возвращает топ-N вакансий."""
    return vacancies[:n]


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """Выводит вакансии в консоль."""
    if not vacancies:
        print("Вакансии не найдены.")
        return
    for i, vacancy in enumerate(vacancies, 1):
        print(f"Вакансия {i}:")
        print(f"Название: {vacancy.title}")
        print(f"URL: {vacancy.url}")
        print(f"Зарплата: {vacancy.salary}")
        print(f"Описание: {vacancy.description}")
        print("-" * 40)
