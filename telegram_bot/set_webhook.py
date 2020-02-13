from decouple import config
import requests

token = config("TELEGRAM_BOT_TOKEN")
app_url = f'https://api.telegram.org/bot{token}'

set_webhook_url = f'{app_url}/setWebhook?url=https://countrygamza.pythonanywhere.com/{token}'

response = requests.get(set_webhook_url)
print(response)