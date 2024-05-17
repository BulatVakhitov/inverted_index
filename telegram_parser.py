import json
import os

from datetime import datetime

from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, bytes):
            return list(o)
        return json.JSONEncoder.default(self, o)


class Telegram_Parser:

    def __init__(self, api_id, api_hash, phone):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone

    def client_start(self):
        try:
            client = TelegramClient(session=self.phone, api_id=self.api_id, api_hash=self.api_hash, system_version="4.16.30-vxCUSTOM")
            if not client.is_connected():
                client.start(phone=self.phone)

            self.client = client
        except Exception:
            raise Exception("Неправильно введен токен")

    def parse_channel(self, url, path_to_json="channel_messages.json", offset_id=0, 
                      limit=100, total_count_limit=50):
        try:
            channel = self.client.get_entity(url)

            all_messages = []

            while True:
                history = self.client(GetHistoryRequest(
                    peer=channel,
                    offset_id=offset_id,
                    offset_date=None,
                    add_offset=0,
                    limit=limit,
                    max_id=0,
                    min_id=0,
                    hash=0
                ))
                if not history.messages:
                    break
                messages = history.messages
                for message in messages:
                    all_messages.append(message.to_dict())
                offset_id = messages[len(messages) - 1].id
                total_messages = len(all_messages)
                if total_count_limit == 0:
                    break
                total_count_limit -= 1

            with open(path_to_json, "w", encoding="UTF-8") as outfile:
                json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)
        except Exception:
            raise Exception("Указан неверный url")

    def client_disconnect(self):
        self.client.disconnect()