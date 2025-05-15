from abc import ABC, abstractmethod
from typing import List, Dict, Any
import requests


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API сервисов с вакансиями."""

    @abstractmethod
    def _connect(self) -> None:
        """Подключается к API, проверяет доступность."""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """Получает вакансии по ключевому слову."""
        pass


class HeadHunterAPI(AbstractAPI):
    """Класс для работы с API HeadHunter."""

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100}

    def _connect(self) -> None:
        """Проверяет доступность API hh.ru."""
        response = requests.get(self.__url, headers=self.__headers)
        if response.status_code != 200:
            raise ConnectionError(
                f"Ошибка подключения к API hh.ru: {response.status_code}"
            )

    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """Получает вакансии с hh.ru по ключевому слову."""
        self._connect()
        self.__params["text"] = keyword
        self.__params["page"] = 0
        vacancies = []
        while self.__params["page"] < 20:  # Ограничение до 2000 вакансий
            response = requests.get(
                self.__url, headers=self.__headers, params=self.__params
            )
            if response.status_code != 200:
                raise ValueError(
                    f"Ошибка получения вакансий: {response.status_code}"
                )
            data = response.json()
            vacancies.extend(data.get("items", []))
            self.__params["page"] += 1
            if self.__params["page"] >= data.get("pages", 1):
                break
        return vacancies