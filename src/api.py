from abc import ABC, abstractmethod
from typing import List, Dict, Any
import requests


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API."""

    @abstractmethod
    def get_vacancies(self, search_query: str) -> List[Dict[str, Any]]:
        """Получает список вакансий по поисковому запросу."""
        pass


class HeadHunterAPI(AbstractAPI):
    """Класс для работы с API hh.ru."""

    def get_vacancies(self, search_query: str) -> List[Dict[str, Any]]:
        """Получает вакансии с hh.ru по поисковому запросу."""
        url = "https://api.hh.ru/vacancies"
        params = {"text": search_query, "per_page": 100, "page": 0}
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            print(
                f"Ответ API: {data.get('items', [])[:2]}"
            )  # Отладка: первые 2 вакансии
            vacancies = data.get("items", [])
            if not vacancies:
                print(f"По запросу '{search_query}' вакансии не найдены.")
            return vacancies
        except requests.ConnectionError:
            raise Exception("Ошибка подключения: проверьте интернет-соединение.")
        except requests.Timeout:
            raise Exception("Превышено время ожидания: попробуйте позже.")
        except requests.HTTPError as e:
            msg = (
                f"Ошибка API: HTTP {e.response.status_code}. "
                f"Попробуйте позже или используйте локальный vacancies.json."
            )
            raise Exception(msg)
        except requests.RequestException as e:
            msg = (
                f"Неизвестная ошибка API: {e}. "
                f"Используйте локальный vacancies.json или проверьте запрос."
            )
            raise Exception(msg)
