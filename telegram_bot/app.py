from flask import Flask
from flask import request
from flask import render_template
from decouple import config
import requests
import random
app = Flask(__name__)

token = config('TELEGRAM_BOT_TOKEN')
app_url = f'https://api.telegram.org/bot{token}'

naver_client_id = config('NAVER_CLIENT_ID')
naver_client_secret = config('NAVER_CLIENT_SECRET')

# chat_id = config('CHAT_ID') ---> papago때 안 하니 일단 지워준다.
# CHAT_ID=902084106 ===> 원래는 .env에 있어야 함
# 실전에서는 token을 github에 올리면 api 털리니 .env 파일에 숨겨준다.

## @app.route로 써주면 로컬호스트주소/name으로 들어갔을 때 화면에 나오게 해준다.
# @app.route('/write')  # /로 들어왔을 때 쓸 함수

# def write():
#     return render_template('write.html')

# @app.route('/send')
# def send():
#     message = request.args.get('message')
#     message_url = f"{app_url}/sendMessage?chat_id={chat_id}&text={message}"
#     requests.get(message_url)
#     return '메세지 전송 완료!'

@app.route(f'/{token}', methods=["POST"])
def telegram():
    # # 1. request print 해보기
    # from_telegram = request.get_json()
    
    # chat_id = from_telegram.get('message').get('from').get('id')
    # text = from_telegram.get('message').get('text')
    # requests.get(f'{app_url}/sendMessage?chat_id={chat_id}&text={text}')

    # 2. '/로또'라고 치면 로또 번호 6자리 나오도록 해보기
    from_telegram = request.get_json()
    
    chat_id = from_telegram.get('message').get('from').get('id')
    text = from_telegram.get('message').get('text')

    if from_telegram.get('message').get('photo') is not None:
        # 클로바 코드 여기에 작성
        # 1. 우선 파일의 아이디 값을 가져온다.
        file_id = from_telegram.get('message').get('photo')[-1].get('file_id')
        # 2. 가져온 파일 아이디로 실제 파일을 가져온다.
        file_res = requests.get(f'{app_url}/getFile?file_id={file_id}')
        # 3. file path를 뽑아내서 저장
        file_path = file_res.json().get('result').get('file_path')
        # 4. 최종적으로 해당 파일의 경로를 찾아서 저장
        file_url = f'https://api.telegram.org/file/bot{token}/{file_path}'
        print(file_url)
        # 5. 사진(파일)이 있는 주소로 요청을 보내서 가져온다.
        real_file_res = requests.get(file_url, stream=True)

        headers = {
            'X-Naver-Client-Id': naver_client_id,
            'X-Naver-Client-Secret': naver_client_secret
        }
        clova_res = requests.post(
            'https://openapi.naver.com/v1/vision/celebrity',
            headers = headers,
            files = {
                'image': real_file_res.raw.read()
            }
        )
        
        # 6. 닮은 유명인의 수가 있을 경우
        if clova_res.json().get('info').get('faceCount'):
            celebrity = clova_res.json().get('faces')[0].get('celebrity')
            reply = f"{celebrity.get('value')} - {celebrity.get('confidence')*100}%"
        else:
            reply="인식된 사람이 없습니다."
    else:
        # text가 왔을 때 실행
        if "로또" in text:   # or if text == '/로또'
            reply = random.sample(range(1,40), 6)
            requests.get(f'{app_url}/sendMessage?chat_id={chat_id}&text={reply}')
        if text[0:4] == '/번역 ':  # '/번역 번역할문장'
            headers = {
                'X-Naver-Client-Id': naver_client_id,
                'X-Naver-Client-Secret': naver_client_secret,
            }
            data = {
                'source': 'en',  # 번역할 언어
                'target': 'ko',
                'text': text[4:]
            }
            papago_url = 'https://openapi.naver.com/v1/papago/n2mt'
            papago_res = requests.post(papago_url, data=data, headers=headers)
            # naver developer에서 API 기본정보 발췌
            papago_res = papago_res.json()
            reply = papago_res.get("message").get("result").get("translatedText")
        
        else:
            reply = text

    print(from_telegram)    
    requests.get(f'{app_url}/sendMessage?chat_id={chat_id}&text={reply}')

    return '', 200


if __name__ == '__main__':
    app.run(debug=True)  # debug=True 하면 서버를 껐다 켤 필요 없다. 알아서 재실행됨.
