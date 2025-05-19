from typing import List, Dict, Any


class Vacancy:
    """Класс для работы с вакансиями."""

    __slots__ = ("title", "url", "salary", "description")

    def __init__(self, title: str, url: str, salary: str, description: str) -> None:
        """Инициализирует вакансию."""
        self.title = self._validate_string(title, "Название")
        self.url = self._validate_url(url)
        self.salary = salary or "Не указана"
        self.description = description or "Нет описания"

    @staticmethod
    def _validate_string(value: str, field: str) -> str:
        """Проверяет, что строка не пустая."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} должно быть непустой строкой")
        return value

    @staticmethod
    def _validate_url(url: str) -> str:
        """Проверяет, что URL валидный."""
        if not isinstance(url, str) or not url.startswith("http"):
            raise ValueError("URL должен быть валидной строкой, начинающейся с http")
        return url

    def __lt__(self, other: "Vacancy") -> bool:
        """Сравнивает вакансии по зарплате."""
        if not isinstance(other, Vacancy):
            raise TypeError("Сравнение возможно только с объектом Vacancy")
        return self._get_salary_value() < other._get_salary_value()

    def _get_salary_value(self) -> float:
        """Извлекает числовое значение зарплаты для сравнения."""
        if self.salary == "Не указана":
            return 0
        try:
            # Извлекаем первое число из строки вида "100000-150000 RUR" или "от 100000 RUR"
            salary_str = self.salary.split()[0]
            if "-" in salary_str:
                return float(salary_str.split("-")[0])
            return float(salary_str.replace("от ", ""))
        except (ValueError, IndexError):
            return 0

    def to_dict(self) -> Dict[str, str]:
        """Преобразует вакансию в словарь."""
        return {
            "title": self.title,
            "url": self.url,
            "salary": self.salary,
            "description": self.description,
        }

    @staticmethod
    def cast_to_object_list(vacancies: List[Dict[str, Any]]) -> List["Vacancy"]:
        """Преобразует список словарей в список объектов Vacancy."""
        result = []
        print(f"Обработка вакансий: {vacancies[:2]}")  # Отладка
        for item in vacancies:
            try:
                title = item.get("name") or item.get("title", "Неизвестная вакансия")
                url = item.get("alternate_url") or item.get("url", "")
                salary_data = item.get("salary")
                salary = "Не указана"
                if salary_data:
                    currency = salary_data.get("currency", "RUR")
                    from_salary = salary_data.get("from")
                    to_salary = salary_data.get("to")
                    if from_salary and to_salary:
                        salary = f"{from_salary}-{to_salary} {currency}"
                    elif from_salary:
                        salary = f"от {from_salary} {currency}"
                    elif to_salary:
                        salary = f"до {to_salary} {currency}"
                description = item.get("snippet", {}).get("requirement") or item.get(
                    "description", "Нет описания"
                )
                print(f"Создание вакансии: title={title}, url={url}")  # Отладка
                vacancy = Vacancy(title, url, salary, description)
                result.append(vacancy)
            except (ValueError, TypeError) as e:
                print(
                    f"Пропущена вакансия: {item.get('name', item.get('title', 'Неизвестно'))} - {e}"
                )
                continue
        return result
