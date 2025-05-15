from abc import ABC, abstractmethod
from typing import List, Dict, Any
import json
import os


class AbstractFileWorker(ABC):
    """Абстрактный класс для работы с файлами."""

    @abstractmethod
    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """Добавляет вакансию в файл."""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Получает вакансии по критериям."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """Удаляет вакансию из файла."""
        pass


class JSONSaver(AbstractFileWorker):
    """Класс для работы с JSON-файлами."""

    def __init__(self, filename: str = "vacancies.json"):
        """Инициализирует имя файла."""
        self.__filename = filename

    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """Добавляет вакансию, избегая дубликатов."""
        vacancies = self._read_vacancies()
        # Проверяем, что vacancies - это список
        if not isinstance(vacancies, list):
            vacancies = []
        # Проверяем, нет ли вакансии с таким же URL
        if not any(
            isinstance(v, dict) and v.get("url") == vacancy["url"]
            for v in vacancies
        ):
            vacancies.append(vacancy)
            self._write_vacancies(vacancies)

    def get_vacancies(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Получает вакансии по критериям."""
        vacancies = self._read_vacancies()
        if not isinstance(vacancies, list):
            return []
        filtered = []
        for vacancy in vacancies:
            if not isinstance(vacancy, dict):
                continue
            matches = True
            for key, value in criteria.items():
                if key not in vacancy or vacancy[key] != value:
                    matches = False
                    break
            if matches:
                filtered.append(vacancy)
        return filtered

    def delete_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """Удаляет вакансию по URL."""
        vacancies = self._read_vacancies()
        if not isinstance(vacancies, list):
            return
        vacancies = [
            v for v in vacancies
            if not isinstance(v, dict) or v.get("url") != vacancy["url"]
        ]
        self._write_vacancies(vacancies)

    def _read_vacancies(self) -> List[Dict[str, Any]]:
        """Читает вакансии из файла."""
        if not os.path.exists(self.__filename):
            return []
        try:
            with open(self.__filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, TypeError):
            return []

    def _write_vacancies(self, vacancies: List[Dict[str, Any]]) -> None:
        """Записывает вакансии в файл."""
        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=2)