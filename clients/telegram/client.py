import logging
from typing import List, Optional, Union

import requests

logger = logging.getLogger(__name__)


def _format_new_product_message(product_data) -> str:
    return f"""
        🚀 <b>Новая анкета предзаписи</b>

👤 <b>Данные:</b>
• ФИО: {product_data.get("full_name") or 'Не указано'}
• Возраст: {product_data.get("age") or 'Не указан'}
• Город: {product_data.get("city") or 'Не указан'}
• Telegram: {product_data.get("telegram") or 'Не указан'}
• Телефон: {product_data.get("phone") or 'Не указан'}
"""


class TelegramBotClient:
    def __init__(self, bot_token: str, chat_ids: Union[str, List[str]] = None):
        self.bot_token = bot_token
        self.base_url = f"https://api.telegram.org/bot{bot_token}"

        if chat_ids is None:
            self.chat_ids = []
        elif isinstance(chat_ids, str):
            self.chat_ids = [chat_ids]
        else:
            self.chat_ids = chat_ids

    def add_chat_id(self, chat_id: str):
        if chat_id not in self.chat_ids:
            self.chat_ids.append(chat_id)

    def add_chat_ids(self, chat_ids: List[str]):
        for chat_id in chat_ids:
            self.add_chat_id(chat_id)

    def remove_chat_id(self, chat_id: str):
        if chat_id in self.chat_ids:
            self.chat_ids.remove(chat_id)

    def set_chat_ids(self, chat_ids: List[str]):
        self.chat_ids = chat_ids

    def send_message(
            self,
            text: str,
            chat_ids: Optional[Union[str, List[str]]] = None,
            parse_mode: str = "HTML",
            disable_web_page_preview: bool = True
    ) -> dict:
        if chat_ids is None:
            target_chat_ids = self.chat_ids
        elif isinstance(chat_ids, str):
            target_chat_ids = [chat_ids]
        else:
            target_chat_ids = chat_ids

        if not target_chat_ids:
            logger.error("Chat IDs not specified")
            return {'success': [], 'failed': []}

        results = {'success': [], 'failed': []}

        for chat_id in target_chat_ids:
            url = f"{self.base_url}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': parse_mode,
                'disable_web_page_preview': disable_web_page_preview
            }

            try:
                response = requests.post(url, json=payload, timeout=10)
                response.raise_for_status()
                results['success'].append(chat_id)
            except requests.exceptions.RequestException:
                results['failed'].append(chat_id)

        return results

    def send_message_with_keyboard(
            self,
            text: str,
            keyboard: list,
            chat_ids: Optional[Union[str, List[str]]] = None,
            parse_mode: str = "HTML"
    ) -> dict:
        if chat_ids is None:
            target_chat_ids = self.chat_ids
        elif isinstance(chat_ids, str):
            target_chat_ids = [chat_ids]
        else:
            target_chat_ids = chat_ids

        if not target_chat_ids:
            logger.error("Chat IDs not specified")
            return {'success': [], 'failed': []}

        results = {'success': [], 'failed': []}

        for chat_id in target_chat_ids:
            url = f"{self.base_url}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': parse_mode,
                'reply_markup': {
                    'keyboard': keyboard,
                    'resize_keyboard': True,
                    'one_time_keyboard': False
                }
            }

            try:
                response = requests.post(url, json=payload, timeout=10)
                response.raise_for_status()
                results['success'].append(chat_id)
            except requests.exceptions.RequestException as e:
                results['failed'].append(chat_id)
                logger.error(f"Failed to send message with keyboard to {chat_id}: {e}")

        return results

    def send_message_with_inline_keyboard(
            self,
            text: str,
            inline_keyboard: List[List[dict]],
            chat_ids: Optional[Union[str, List[str]]] = None,
            parse_mode: str = "HTML",
            disable_web_page_preview: bool = True
    ) -> dict:
        if chat_ids is None:
            target_chat_ids = self.chat_ids
        elif isinstance(chat_ids, str):
            target_chat_ids = [chat_ids]
        else:
            target_chat_ids = chat_ids

        if not target_chat_ids:
            logger.error("Chat IDs not specified")
            return {'success': [], 'failed': []}

        results = {'success': [], 'failed': []}

        for chat_id in target_chat_ids:
            url = f"{self.base_url}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': parse_mode,
                'disable_web_page_preview': disable_web_page_preview,
                'reply_markup': {
                    'inline_keyboard': inline_keyboard
                }
            }

            try:
                response = requests.post(url, json=payload, timeout=10)
                response.raise_for_status()
                results['success'].append(chat_id)
            except requests.exceptions.RequestException:
                results['failed'].append(chat_id)

        return results

    def send_new_product_notification(self, product_data, chat_ids: Optional[Union[str, List[str]]] = None) -> dict:
        inline_keyboard = [
            [
                {
                    'text': '📊 Посмотреть таблицу',
                    'url': 'https://docs.google.com/spreadsheets/d/1_O8jzBH2PaH2xwOy8mTQ451BASVH6ppbbcI-3V_MmzY/edit?usp=drivesdk'
                }
            ]
        ]

        message = _format_new_product_message(product_data)

        return self.send_message_with_inline_keyboard(
            text=message,
            inline_keyboard=inline_keyboard,
            chat_ids=chat_ids
        )

    def get_chat_ids_count(self) -> int:
        return len(self.chat_ids)

    def clear_chat_ids(self):
        self.chat_ids = []
