from src.api import HeadHunterAPI
from src.file_worker import JSONSaver
from src.vacancy import Vacancy
from src.utils import filter_vacancies, get_top_vacancies, filter_by_salary_range
from typing import List


def user_interaction() -> None:
    """Интерфейс взаимодействия с пользователем через консоль."""
    print("Добро пожаловать в поиск вакансий на hh.ru!")
    saver = JSONSaver()
    # Загружаем сохраненные вакансии
    saved_vacancies_data = saver.get_vacancies({})
    saved_vacancies = Vacancy.cast_to_object_list(saved_vacancies_data)
    vacancies: List[Vacancy] = saved_vacancies.copy()
    next_id = max((v.id for v in saved_vacancies if v.id is not None), default=0) + 1

    while True:
        print("\nВыберите действие:")
        print("1. Поиск вакансий по названию работы")
        print("2. Поиск вакансий по описанию")
        print("3. Топ вакансий по зарплате")
        print("4. Фильтр по диапазону зарплат")
        print("5. Добавить вакансию")
        print("6. Посмотреть сохраненные вакансии")
        print("7. Удалить вакансию")
        print("8. Выйти")

        choice = input("Ваш выбор (1-8): ")

        if choice == "1":
            query = input("Введите название работы (например, Python): ")
            if len(query.strip()) < 2:
                print("Запрос должен содержать минимум 2 символа.")
                continue
            api = HeadHunterAPI()
            try:
                raw_vacancies = api.get_vacancies(query)
                new_vacancies = Vacancy.cast_to_object_list(raw_vacancies)
                # Комбинируем сохранённые и новые вакансии
                vacancies = saved_vacancies + new_vacancies
                # Фильтруем по названию
                filtered_vacancies = [v for v in vacancies if query.lower() in v.title.lower()]
                if filtered_vacancies:
                    print(f"Найдено {len(filtered_vacancies)} вакансий:")
                    for v in filtered_vacancies[:5]:
                        print(f"Название: {v.title} | Зарплата: {v.salary} | URL: {v.url}")
                else:
                    print("Вакансии не найдены.")
            except Exception as e:
                print(f"Ошибка: {e}")
                vacancies = saved_vacancies.copy()  # Возвращаемся к сохранённым вакансиям

        elif choice == "2":
            keyword = input("Введите ключевое слово для описания: ")
            if len(keyword.strip()) < 2:
                print("Ключевое слово должно содержать минимум 2 символа.")
                continue
            if not vacancies:
                print("Сначала выполните поиск вакансий (пункт 1).")
                continue
            filtered = filter_vacancies(vacancies, keyword)
            if filtered:
                print(f"Найдено {len(filtered)} вакансий:")
                for v in filtered[:5]:
                    print(f"Название: {v.title} | Описание: {v.description}")
            else:
                print("Вакансии с таким описанием не найдены.")

        elif choice == "3":
            try:
                n = int(input("Введите количество вакансий для топа: "))
                if n <= 0:
                    print("Введите положительное число.")
                    continue
                if not vacancies:
                    print("Сначала выполните поиск вакансий (пункт 1).")
                    continue
                top = get_top_vacancies(vacancies, n)
                if top:
                    print(f"Топ {len(top)} вакансий по зарплате:")
                    for i, v in enumerate(top, 1):
                        print(f"{i}. Название: {v.title} | Зарплата: {v.salary}")
                else:
                    print("Вакансии не найдены.")
            except ValueError:
                print("Введите число.")

        elif choice == "4":
            salary_range = input("Введите диапазон зарплат (например, 100000-150000): ")
            if not vacancies:
                print("Сначала выполните поиск вакансий (пункт 1).")
                continue
            filtered = filter_by_salary_range(vacancies, salary_range)
            if filtered:
                print(f"Найдено {len(filtered)} вакансий в диапазоне:")
                for v in filtered[:5]:
                    print(f"Название: {v.title} | Зарплата: {v.salary}")
            else:
                print("Вакансии в этом диапазоне не найдены.")

        elif choice == "5":
            title = input("Введите название вакансии: ")
            if len(title.strip()) < 2:
                print("Название должно содержать минимум 2 символа.")
                continue
            url = input("Введите URL (например, https://hh.ru/vacancy/123): ")
            if not url.startswith("http"):
                print("URL должен начинаться с http или https.")
                continue
            salary = input("Введите зарплату (например, 100000-150000 RUR): ")
            description = input("Введите описание: ")
            vacancy = Vacancy(title, url, salary, description, next_id).to_dict()
            saver.add_vacancy(vacancy)
            next_id += 1
            saved_vacancies = Vacancy.cast_to_object_list(saver.get_vacancies({}))
            vacancies = saved_vacancies.copy()
            print("Вакансия добавлена.")

        elif choice == "6":
            data = saver.get_vacancies({})
            if not data:
                print("Сохраненных вакансий нет.")
                continue
            print(f"Найдено {len(data)} сохраненных вакансий:")
            for v in data[:5]:
                print(f"ID: {v['id']} | Название: {v['title']} | Зарплата: {v['salary']}")

        elif choice == "7":
            try:
                vid = int(input("Введите ID вакансии для удаления: "))
                saver.delete_vacancy(vid)
                saved_vacancies = Vacancy.cast_to_object_list(saver.get_vacancies({}))
                vacancies = saved_vacancies.copy()
                print("Вакансия удалена.")
            except ValueError:
                print("Введите число.")

        elif choice == "8":
            print("До свидания!")
            break
        else:
            print("Введите число от 1 до 8.")