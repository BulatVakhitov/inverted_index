from telegram_parser import Telegram_Parser

API_ID = 1111111111
API_HASH = '1111111111111111111111111'
PHONE = '111111111'

telegram_channels_urls = [
    't.me/meduzalive',
    't.me/spbuniversity',
    't.me/naukamsu'
]

parser = Telegram_Parser(api_id=API_ID, api_hash=API_HASH, phone=PHONE)
parser.client_start()

for url in telegram_channels_urls:
    name = url.split('/')[-1]
    parser.parse_channel(url=url, path_to_json=f"data/{name}.json")

parser.client_disconnect()
