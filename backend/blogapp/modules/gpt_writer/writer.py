import logging
from pathlib import Path

import langdetect
import openai
from fastapi import HTTPException
from openai.openai_object import OpenAIObject
import yaml

from ...core.config import BACKEND_DIR_PATH

log = logging.getLogger("blogapp")


class Writer:
    """Класс работы с ChatGPT"""

    settings: dict

    @classmethod
    def init_writer(cls, host: str, api_key: str):
        """
        Инициализация Writer. Подготавливает библиотеку openai и получает настройки из .yml
        :param host: сервер API. Если пустой, то будет использован стандартный ендпоинт OpenAI.
        :param api_key: API ключ.
        """

        # Конфигурация Host и API ключа в openai
        if not (host == "" or host == "https://api.openai.com/v1"):
            openai.api_base = host
        openai.api_key = api_key

        # Загрузка настроек для промптов
        settings_path = Path(
            BACKEND_DIR_PATH, "blogapp", "modules", "gpt_writer", "chatgpt_settings.yml"
        )
        with open(settings_path, "r", encoding="utf-8") as file:
            cls.settings = yaml.safe_load(file)

    @classmethod
    def prepare_article_generation_prompt(
        cls, title: str, tags: list | None, key_phrases: list | None
    ) -> str:
        prompt = cls.settings["prompt"].format(
            title=title,
            tags=(tags if tags else "[ai generated]"),
            key_phrases=(key_phrases if key_phrases else "[Ai generated text]"),
        )
        # имя функции в log
        log.debug(f"Создан промт {prompt} в функции prepare_article_generation_prompt")
        return prompt

    @classmethod
    async def generate_article_content(cls, prompt: str = "") -> OpenAIObject:
        """
        Генерирует текст статьи через ChatGPT
        :param prompt: промт для генерации
        :return: OpenAIObject - chat completion object
        :raises HTTPException: при любой возможной ошибке
        """

        try:
            response: OpenAIObject = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )
        except Exception as e:
            log.error(str(e))
            raise HTTPException(status_code=500, detail=str(e))

        return response

    @classmethod
    def check_article(cls, article_text) -> list:
        """Проверяет текст статьи на наличие ошибок и возвращает список обнаруженных ошибок."""
        error_list = []

        # Содержит ли более 50 слов
        if len(article_text.split()) < 50:
            error_list.append("Статья должна содержать более 50 слов")

        # Написана ли на русском языке
        if langdetect.detect(article_text) != "ru":
            error_list.append("Статья должна быть написана на русском языке")

        return error_list
