from flask import Flask
from flask import request
from flask import render_template
import random
import requests
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/mulcam')
def mulcam():
    return "This is mulcam!"

@app.route('/greeting/<string:name>')
def greeting(name):
    return f"Hello, {name}"

@app.route("/cube/<int:num>")
def cube(num):
    result = num ** 3
    return str(result)

@app.route("/lunch/<int:people>")
def lunch(people):
    menu = ['짜장면', '짬뽕', '볶음밥', '잡채밥', '제육볶음', '짬뽕밥', '꽝']
    order = random.sample(menu, people)
    return str(order)

@app.route("/html")
def html():
    return '<h1>안녕하세요!!!</h1>'

@app.route('/html_file')
def html_file():
    return render_template('html_file.html')

@app.route('/hi/<string:name>')
def hi(name):
    return render_template('hi.html', your_name=name)

@app.route('/naver')
def naver():
    return render_template('naver.html')


@app.route('/ping')
def ping():
    return render_template('ping.html')

@app.route('/pong')
def pong():
    request.args.get('name')
    messageI= request.args.get('message')
    return render_template('pong.html', name=name, message=message)

@app.route('/vonvon')
def vonvon():
    return rener_template('vonvon.html')

@app.route('/vonvon_result')
def vonvon_result():
    name = request.args.get('nickname')
    features = ['똑똑함','멋짐','웃김','냄새남','운동감각']
    chosen = random.sample(features, 3)
    chosen = ' '.join(map(str, chosen))
    return render_template('vonvon_result.html', name=name)

@app.route('/ascii')
def ascii():
    return render_template('ascii.html')

@app.route('/ascii_result')
def ascii_result():
    # 1. form태그로 날린 데이터(word)를 받는다.
    word = request.args.get('word')
    # 2. word를 가지고 ascii_art API 요청 주소로 요청을 보낸다.
    result = requests.get(f'http://artii.herokuapp.com/make?text={word}').text
    # 3. API 응답 결과를 html 파일에 담아서 보여준다.
    return render_template('ascii_result.html',result= result)

@app.route('/lotto_check')
def lotto_check():
    return render_template('lotto_check.html')

@app.route('/lotto_result')
def lotto_result():
    lotto_round = request.args.get('lotto_round')
    response = requests.get(f'https://dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={lotto_round}')
    # requests는 별개의 라이브러리. 코드를 통해서 어떤 요청을 보낸다.
    lotto = response.json()
    # json 이라는 method를 사용하여 저장해줘야 한다.
    # python의 dictionary와 비슷. key값을 빼와야 한다.
    # drwtNo6 = lotto["drwtNo6"]  ---> 해당 키값이 없을 때 에러
    # drwtNo6 = lotto.get("drwtNo6")  ---> 해당 키값이 없을 때 None 값이 나옴. 이 방법을 더 추천.
    winner = []
    # 1. for문을 활용한다.
    for i in range(1,7):
        winner.append(lotto[f'drwtNo{i}'])
    # 2. List Comprehension을 활용해도 된다.
    # winner = [lotto[f'drwtNo{i}'] for i in range(1,7)]

    
    numbers = request.args.get('numbers')  # 이대로는 string형태로 들어있다.
    numbers = numbers.split() # 리스트 - [;1', '2', '3', '4']
    numbers_int = []
    
    for number in numbers:
        numbers_int.append(int(number))

    matched = len(set(winner) & set(numbers_int))   # 교집합 찾기
    if matched == 6:
        result = '1등입니다!'
    elif matched == 5:
        if lotto["bnusNo"] in numbers_int:
            result = '2등!'
        else:
            result = '3등!'
    elif matched ==4:
        result = '4등!'
    elif matched == 3:
        result = '3등!'
    else:
        result = "꽝..."

    
    return render_template('lotto_result.html',
        lotto_round=lotto_round, winner=winner,
        numbers=numbers, result=result, 
    )

if __name__ == '__main__':
    app.run(debug=True)