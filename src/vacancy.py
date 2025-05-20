from typing import Any, Tuple, List, Dict


class Vacancy:
    """Класс для представления вакансии."""
    __slots__ = ("title", "url", "salary", "description", "id")

    def __init__(self, title: str, url: str, salary: str, description: str, id: int = None):
        """
        Инициализирует объект вакансии.

        Args:
            title: Название вакансии.
            url: Ссылка на вакансию.
            salary: Зарплата (строка, например "100000-150000 RUR").
            description: Описание вакансии.
            id: Уникальный идентификатор (опционально).
        """
        self.title = self._validate_string(title, "Неизвестная вакансия")
        self.url = self._validate_string(url, "")
        self.salary = self._validate_salary(salary)
        self.description = self._validate_string(description, "")
        self.id = id if id is not None else id

    def __lt__(self, other: "Vacancy") -> bool:
        """
        Сравнивает вакансии по зарплате (<).

        Args:
            other: Другая вакансия.

        Returns:
            bool: True, если текущая зарплата меньше.
        """
        return self._get_salary_value()[0] < other._get_salary_value()[0]

    def __gt__(self, other: "Vacancy") -> bool:
        """
        Сравнивает вакансии по зарплате (>).

        Args:
            other: Другая вакансия.

        Returns:
            bool: True, если текущая зарплата больше.
        """
        return self._get_salary_value()[0] > other._get_salary_value()[0]

    def __eq__(self, other: "Vacancy") -> bool:
        """
        Сравнивает вакансии по зарплате (==).

        Args:
            other: Другая вакансия.

        Returns:
            bool: True, если зарплаты равны.
        """
        return self._get_salary_value()[0] == other._get_salary_value()[0]

    def _validate_string(self, value: str, default: str) -> str:
        """Валидирует строковые поля."""
        return value.strip() if value and isinstance(value, str) else default

    def _validate_salary(self, salary: str) -> str:
        """Валидирует поле зарплаты."""
        if not salary or not isinstance(salary, str) or salary.strip() == "":
            return "Зарплата не указана"
        return salary.strip()

    def _get_salary_value(self) -> Tuple[float, float]:
        """Извлекает минимальную и максимальную зарплату для сравнения."""
        if "не указана" in self.salary.lower():
            return 0.0, 0.0
        try:
            salary_clean = self.salary.replace(" RUR", "").replace(",", "")
            if "-" in salary_clean:
                start, end = map(float, salary_clean.split("-"))
                return start, end
            num = float(salary_clean.replace("от ", "").replace("до ", ""))
            return num, num
        except (ValueError, TypeError):
            return 0.0, 0.0

    def to_dict(self) -> dict:
        """Преобразует вакансию в словарь."""
        return {
            "title": self.title,
            "url": self.url,
            "salary": self.salary,
            "description": self.description,
            "id": self.id
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Vacancy":
        """Создает объект Vacancy из словаря."""
        return cls(
            data.get("title", ""),
            data.get("url", ""),
            data.get("salary", ""),
            data.get("description", ""),
            data.get("id")
        )

    @classmethod
    def cast_to_object_list(cls, data: List[Dict[str, Any]]) -> List["Vacancy"]:
        """Преобразует список словарей в список объектов Vacancy."""
        return [cls.from_dict(item) for item in data]