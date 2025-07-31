import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    def __init__(
        self, daily_limit: int, storage_file: str = "data/rate_limit_data.json"
    ):
        self.daily_limit = daily_limit
        self.storage_file = storage_file
        self.data = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        """Загружает данные о лимитах из файла"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"Ошибка загрузки данных лимитов: {e}")

        return {"users": {}}

    def _save_data(self):
        """Сохраняет данные о лимитах в файл"""
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            logger.error(f"Ошибка сохранения данных лимитов: {e}")

    def _get_user_data(self, user_id: int) -> Dict[str, Any]:
        """Получает данные пользователя, создает если не существует"""
        user_id_str = str(user_id)

        if user_id_str not in self.data["users"]:
            self.data["users"][user_id_str] = {
                "requests_today": 0,
                "last_reset_date": datetime.now().strftime("%Y-%m-%d"),
                "total_requests": 0,
            }
            self._save_data()

        return self.data["users"][user_id_str]

    def _reset_daily_counter_if_needed(self, user_id: int):
        """Сбрасывает счетчик пользователя если прошли сутки"""
        user_data = self._get_user_data(user_id)
        today = datetime.now().strftime("%Y-%m-%d")

        if user_data["last_reset_date"] != today:
            user_data["requests_today"] = 0
            user_data["last_reset_date"] = today
            self._save_data()
            logger.info(f"Счетчик запросов к Gemini сброшен для пользователя {user_id}")

    def can_make_request(self, user_id: int) -> bool:
        """Проверяет, может ли пользователь сделать запрос"""
        self._reset_daily_counter_if_needed(user_id)
        user_data = self._get_user_data(user_id)
        return user_data["requests_today"] < self.daily_limit

    def increment_request_count(self, user_id: int):
        """Увеличивает счетчик запросов пользователя"""
        self._reset_daily_counter_if_needed(user_id)
        user_data = self._get_user_data(user_id)
        user_data["requests_today"] += 1
        user_data["total_requests"] += 1
        self._save_data()

        logger.info(
            f"Пользователь {user_id} использовал запросов к Gemini: {user_data['requests_today']}/{self.daily_limit}"
        )

    def get_remaining_requests(self, user_id: int) -> int:
        """Возвращает количество оставшихся запросов для пользователя"""
        self._reset_daily_counter_if_needed(user_id)
        user_data = self._get_user_data(user_id)
        return max(0, self.daily_limit - user_data["requests_today"])

    def get_reset_time(self) -> datetime:
        """Возвращает время следующего сброса лимита"""
        tomorrow = datetime.now() + timedelta(days=1)
        return tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)

    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Возвращает статистику использования для конкретного пользователя"""
        self.data = self._load_data()
        self._reset_daily_counter_if_needed(user_id)
        user_data = self._get_user_data(user_id)

        return {
            "requests_today": user_data["requests_today"],
            "daily_limit": self.daily_limit,
            "remaining_requests": self.get_remaining_requests(user_id),
            "total_requests": user_data["total_requests"],
            "reset_time": self.get_reset_time(),
        }

    def get_global_stats(self) -> Dict[str, Any]:
        """Возвращает глобальную статистику по всем пользователям"""
        total_users = len(self.data["users"])
        total_requests_all_time = sum(
            user_data["total_requests"] for user_data in self.data["users"].values()
        )

        today = datetime.now().strftime("%Y-%m-%d")
        requests_today_all_users = sum(
            user_data["requests_today"]
            for user_data in self.data["users"].values()
            if user_data["last_reset_date"] == today
        )

        return {
            "total_users": total_users,
            "total_requests_all_time": total_requests_all_time,
            "requests_today_all_users": requests_today_all_users,
            "daily_limit_per_user": self.daily_limit,
        }
