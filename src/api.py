from abc import ABC, abstractmethod
import requests
from typing import List, Dict, Any


class APIClient(ABC):
    """Абстрактный класс для работы с API вакансий."""

    @abstractmethod
    def _connect(self) -> None:
        """Подключается к API и проверяет статус."""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """Получает вакансии по ключевому слову."""
        pass


class HeadHunterAPI(APIClient):
    """Класс для интеграции с API hh.ru."""

    def __init__(self):
        self._base_url: str = "https://api.hh.ru/vacancies"

    def _connect(self) -> None:
        """
        Проверяет подключение к API по базовому URL.

        Raises:
            Exception: Если статус-код не 200.
        """
        response = requests.get(self._base_url)
        if response.status_code != 200:
            raise Exception(f"Ошибка подключения: HTTP {response.status_code}")

    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Получает вакансии с hh.ru по ключевому слову.

        Args:
            keyword: Ключевое слово для поиска.

        Returns:
            List[Dict[str, Any]]: Список вакансий с извлеченными полями.
        """
        self._connect()
        params = {"text": keyword, "per_page": 100}
        try:
            response = requests.get(self._base_url, params=params)
            print(f"API response status: {response.status_code}")  # Отладочный вывод
            if response.status_code == 200:
                items = response.json().get("items", [])
                print(f"API returned {len(items)} items")  # Отладочный вывод
                return [
                    {
                        "title": item.get("name", "Неизвестная вакансия"),
                        "url": item.get("alternate_url", ""),
                        "salary": self._parse_salary(item.get("salary", None)),
                        "description": item.get("snippet", {}).get("responsibility", "") or item.get("snippet", {}).get(
                            "requirement", ""),
                        "id": item.get("id")
                    }
                    for item in items
                ]
            raise Exception(f"Ошибка API: HTTP {response.status_code}")
        except Exception as e:
            print(f"Ошибка при запросе к API: {e}")  # Отладочный вывод
            return []

    def _parse_salary(self, salary_data: Dict[str, Any] | None) -> str:
        """Извлекает зарплату из данных API."""
        if not salary_data or (salary_data.get("from") is None and salary_data.get("to") is None):
            return "Зарплата не указана"
        currency = salary_data.get("currency", "RUR")
        salary_from = salary_data.get("from")
        salary_to = salary_data.get("to")
        if salary_from and salary_to:
            return f"{int(salary_from)}-{int(salary_to)} {currency}"
        elif salary_from:
            return f"от {int(salary_from)} {currency}"
        elif salary_to:
            return f"до {int(salary_to)} {currency}"
        return "Зарплата не указана"