import json
import os
from src.api import HeadHunterAPI
from src.vacancy import Vacancy
from src.file_worker import JSONSaver
from src.utils import (
    filter_vacancies,
    sort_vacancies,
    get_top_vacancies,
    print_vacancies,
)


def user_interaction() -> None:
    """Функция для взаимодействия с пользователем через консоль."""
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()

    print("Добро пожаловать в поиск вакансий на hh.ru!")
    while True:
        use_local = (
            input("Использовать локальный vacancies.json? (да/нет, y/n): ")
            .strip()
            .lower()
        )
        if use_local in ("y", "yes", "да"):
            use_local = True
            break
        elif use_local in ("n", "no", "нет"):
            use_local = False
            break
        print("Ошибка: введите 'да', 'нет', 'y' или 'n'.")

    if use_local:
        if not os.path.exists("vacancies.json"):
            print("Ошибка: файл vacancies.json не найден.")
            print(
                "Попробуйте запустить программу с API для создания файла или добавьте vacancies.json вручную."
            )
            return
        try:
            with open("vacancies.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            # Проверяем, является ли data списком или словарем с 'items'
            vacancies_data = data.get("items", data) if isinstance(data, dict) else data
            if not isinstance(vacancies_data, list):
                print("Ошибка: некорректный формат данных в vacancies.json.")
                return
            vacancies = Vacancy.cast_to_object_list(vacancies_data)
            if not vacancies:
                print("В файле vacancies.json нет валидных вакансий.")
                return
        except Exception as e:
            print(f"Ошибка при чтении vacancies.json: {e}")
            return
    else:
        search_query = input("Введите поисковый запрос (например, Python): ").strip()
        if not search_query:
            print("Ошибка: поисковый запрос не может быть пустым.")
            return
        try:
            vacancies_data = hh_api.get_vacancies(search_query)
            vacancies = Vacancy.cast_to_object_list(vacancies_data)
        except Exception as e:
            print(f"Ошибка при получении вакансий: {e}")
            print("Рекомендации:")
            print("- Проверьте подключение к интернету.")
            print(
                "- Используйте локальный файл vacancies.json (выберите 'да' при запуске)."
            )
            print("- Повторите запрос позже.")
            return

    if not vacancies:
        print(f"Вакансии по запросу '{search_query}' не найдены.")
        print("Попробуйте изменить запрос или использовать локальный vacancies.json.")
        return

    # Сохраняем вакансии в файл
    for vacancy in vacancies:
        json_saver.add_vacancy(vacancy.to_dict())

    while True:
        print("\nВыберите действие:")
        print("1. Показать топ-N вакансий по зарплате")
        print("2. Фильтровать вакансии по ключевым словам")
        print("3. Выйти")
        choice = input("Ваш выбор (1-3): ").strip()

        if choice == "1":
            try:
                top_n = int(input("Введите количество вакансий для вывода: "))
                if top_n <= 0:
                    print("Ошибка: количество должно быть положительным.")
                    continue
            except ValueError:
                print("Ошибка: введите целое число.")
                continue
            sorted_vacancies = sort_vacancies(vacancies)
            top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
            print_vacancies(top_vacancies)

        elif choice == "2":
            filter_words = (
                input("Введите ключевые слова для фильтрации (через пробел): ")
                .strip()
                .split()
            )
            filtered_vacancies = filter_vacancies(vacancies, filter_words)
            sorted_vacancies = sort_vacancies(filtered_vacancies)
            print_vacancies(sorted_vacancies)

        elif choice == "3":
            print("До свидания!")
            break

        else:
            print("Ошибка: выберите 1, 2 или 3.")
