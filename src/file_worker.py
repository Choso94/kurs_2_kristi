from abc import ABC, abstractmethod
import json
from typing import List, Dict, Any


class DataManager(ABC):
    """Абстрактный класс для работы с хранилищем данных."""

    @abstractmethod
    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """Добавляет вакансию в хранилище."""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Получает вакансии по критериям."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id: int) -> None:
        """Удаляет вакансию по ID."""
        pass


class JSONSaver(DataManager):
    """Класс для работы с вакансиями в JSON-файле."""

    def __init__(self, filename: str = "vacancies.json"):
        self._filename: str = filename

    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """
        Добавляет вакансию, избегая дубликатов по URL.

        Args:
            vacancy: Словарь с данными вакансии.
        """
        current_data = self._load()
        if not any(v.get("url") == vacancy.get("url") for v in current_data):
            current_data.append(vacancy)
            self._save(current_data)

    def get_vacancies(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Получает вакансии по критериям.

        Args:
            criteria: Словарь с критериями (например, {"description": "Python"}).

        Returns:
            List[Dict[str, Any]]: Отфильтрованный список вакансий.
        """
        data = self._load()
        if not criteria:
            return data
        filtered = [
            v for v in data
            if all(
                str(v.get(key, "")).lower().find(str(value).lower()) != -1
                for key, value in criteria.items()
            )
        ]
        return filtered

    def delete_vacancy(self, vacancy_id: int) -> None:
        """
        Удаляет вакансию по ID.

        Args:
            vacancy_id: ID вакансии для удаления.
        """
        current_data = self._load()
        current_data = [v for v in current_data if v.get("id") != vacancy_id]
        self._save(current_data)

    def _load(self) -> List[Dict[str, Any]]:
        """Загружает данные из файла."""
        try:
            with open(self._filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save(self, data: List[Dict[str, Any]]) -> None:
        """Сохраняет данные в файл."""
        with open(self._filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)