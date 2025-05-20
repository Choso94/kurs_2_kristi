Job Search
Проект для поиска и управления вакансиями с платформы hh.ru с использованием API.
Функциональность

API: Интеграция с hh.ru через HeadHunterAPI.
Вакансии: Класс Vacancy с атрибутами title, url, salary, description, поддержкой сравнения по зарплате и валидацией.
Файлы: Сохранение вакансий в JSON (JSONSaver) без дубликатов.
Интерфейс: Консольное взаимодействие для поиска, фильтрации и вывода топ-N вакансий, с поддержкой локального vacancies.json.
Тесты: Покрытие >70% для всех модулей.

Установка

Склонируйте репозиторий:git clone <repository_url>


Установите зависимости:poetry install


Запустите тесты:poetry run pytest --cov=src --cov-report=term


Проверьте стиль кода:poetry run flake8 src tests main.py


Запустите программу:poetry run python main.py



Использование
poetry run python main.py


Выберите использование локального vacancies.json или поиск через API.
Для API введите поисковый запрос (например, "Python").
Выберите действие: топ-N вакансий, фильтрация по словам, выход.

Структура проекта

src/api.py: Классы для работы с API (AbstractAPI, HeadHunterAPI).
src/vacancy.py: Класс Vacancy.
src/file_worker.py: Классы для работы с файлами (AbstractFileWorker, JSONSaver).
src/utils.py: Вспомогательные функции.
src/interaction.py: Интерфейс пользователя.
tests/: Тесты для всех модулей.
main.py: Точка входа.
README.md: Описание.
pyproject.toml, poetry.lock: Зависимости.
vacancies.json: Пример данных (игнорируется Git).

Тестирование

Покрытие: >70% (проверяйте через pytest --cov=src --cov-report=html).
Flake8: Соответствие PEP 8 (максимальная длина строки 79 символов).

