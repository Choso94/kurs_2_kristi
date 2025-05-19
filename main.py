import json


def load_vacancies(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)  # Parse JSON into a Python list
    except Exception as e:
        print(f"Ошибка при чтении {file_path}: {e}")
        return []


def main():
    print("Добро пожаловать в поиск вакансий на hh.ru!")
    use_local = input("Использовать локальный vacancies.json? (да/нет, y/n): ").lower()

    if use_local in ['да', 'y']:
        vacancies = load_vacancies('vacancies.json')
        print(f"Обработка вакансий: {vacancies[:2]}")  # Print first two for debugging
        # Add your vacancy processing logic here
    else:
        print("Загрузка вакансий с hh.ru не реализована в этом примере.")


if __name__ == "__main__":
    main()