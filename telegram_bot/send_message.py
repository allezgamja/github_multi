import requests
# 요청 보낼때 사용하는 모듈은 requests
from decouple import config

# 기본설정
token = config('TELEGRAM_BOT_TOKEN')
app_url = f'https://api.telegram.org/bot{token}'

# 응답내용 저장하기
# update_url = f"{app_url}/getUpdates"
# response = requests.get(update_url)
# response = response.json()

# chat id 찾아서 꺼내기
chat_id = config("CHAT_ID")

# 메세지 보내기
message_url = f"{app_url}/sendMessage?chat_id={chat_id}&text=하잇"
print(requests.get(message_url))
