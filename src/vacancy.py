from typing import Optional, List, Dict, Any


class Vacancy:
    """Класс для работы с вакансиями."""
    __slots__ = ("_title", "_url", "_salary", "_description")

    def __init__(
        self,
        title: str,
        url: str,
        salary: Optional[Dict[str, Any]] = None,
        description: Optional[str] = None
    ):
        """Инициализирует вакансию с валидацией данных."""
        self._title = self._validate_title(title)
        self._url = self._validate_url(url)
        self._salary = self._validate_salary(salary)
        self._description = self._validate_description(description)

    @staticmethod
    def _validate_title(title: str) -> str:
        """Проверяет, что название не пустое."""
        if not title or not isinstance(title, str):
            raise ValueError("Название вакансии должно быть непустой строкой")
        return title

    @staticmethod
    def _validate_url(url: str) -> str:
        """Проверяет, что URL не пустой."""
        if not url or not isinstance(url, str):
            raise ValueError("URL вакансии должен быть непустой строкой")
        return url

    @staticmethod
    def _validate_salary(salary: Optional[Dict[str, Any]]) -> str:
        """Валидирует зарплату, возвращает строку или 'Не указана'."""
        if not salary:
            return "Не указана"
        salary_from = salary.get("from")
        salary_to = salary.get("to")
        currency = salary.get("currency", "RUR")
        if salary_from and salary_to:
            return f"{salary_from}-{salary_to} {currency}"
        elif salary_from:
            return f"от {salary_from} {currency}"
        elif salary_to:
            return f"до {salary_to} {currency}"
        return "Не указана"

    @staticmethod
    def _validate_description(description: Optional[str]) -> str:
        """Проверяет описание, возвращает пустую строку, если None."""
        return description if isinstance(description, str) else ""

    @property
    def title(self) -> str:
        """Возвращает название вакансии."""
        return self._title

    @property
    def url(self) -> str:
        """Возвращает URL вакансии."""
        return self._url

    @property
    def salary(self) -> str:
        """Возвращает зарплату в текстовом формате."""
        return self._salary

    @property
    def description(self) -> str:
        """Возвращает описание вакансии."""
        return self._description

    def get_salary_value(self) -> int:
        """Возвращает числовое значение зарплаты для сравнения."""
        if self._salary == "Не указана":
            return 0
        try:
            if "от" in self._salary:
                return int(self._salary.split()[1])
            elif "до" in self._salary:
                return int(self._salary.split()[1])
            else:
                salary_range = self._salary.split("-")
                return int(salary_range[1].split()[0])
        except (ValueError, IndexError):
            return 0

    def __lt__(self, other: "Vacancy") -> bool:
        """Сравнивает вакансии по зарплате (<)."""
        return self.get_salary_value() < other.get_salary_value()

    def __le__(self, other: "Vacancy") -> bool:
        """Сравнивает вакансии по зарплате (<=)."""
        return self.get_salary_value() <= other.get_salary_value()

    def __eq__(self, other: "Vacancy") -> bool:
        """Сравнивает вакансии по зарплате (==)."""
        return self.get_salary_value() == other.get_salary_value()

    def __ne__(self, other: "Vacancy") -> bool:
        """Сравнивает вакансии по зарплате (!=)."""
        return self.get_salary_value() != other.get_salary_value()

    def __gt__(self, other: "Vacancy") -> bool:
        """Сравнивает вакансии по зарплате (>)."""
        return self.get_salary_value() > other.get_salary_value()

    def __ge__(self, other: "Vacancy") -> bool:
        """Сравнивает вакансии по зарплате (>=)."""
        return self.get_salary_value() >= other.get_salary_value()

    def to_dict(self) -> Dict[str, Any]:
        """Преобразует вакансию в словарь."""
        return {
            "title": self._title,
            "url": self._url,
            "salary": self._salary,
            "description": self._description
        }

    @classmethod
    def cast_to_object_list(cls, vacancies: List[Dict[str, Any]]) -> List["Vacancy"]:
        """Преобразует список словарей в список объектов Vacancy."""
        return [
            cls(
                title=v.get("name", ""),
                url=v.get("alternate_url", ""),
                salary=v.get("salary"),
                description=v.get("snippet", {}).get("requirement", "")
            )
            for v in vacancies
        ]