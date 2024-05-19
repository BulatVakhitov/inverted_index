from telegram_parser import Telegram_Parser

API_ID = 11111111
API_HASH = '11111111111111111111111111111'
PHONE = '11111111111111'

telegram_channels_names = [
    'meduzalive',
    'spbuniversity',
    'naukamsu',
    'grandexam_ege',
    'lyandpy',
    'minobrnaukiofficial',
    'bbcrussian'
]

parser = Telegram_Parser(api_id=API_ID, api_hash=API_HASH, phone=PHONE)
parser.client_start()

for name in telegram_channels_names:
    url = 't.me/' + name
    parser.parse_channel(url=url, path_to_json=f"data/{name}.json", limit=500, total_count_limit=200)

parser.client_disconnect()
