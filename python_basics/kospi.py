import requests
from bs4 import BeautifulSoup

# 개발자도구 단축키: F12

response = requests.get('https://finance.naver.com/sise/').text
# requests = 브라우저 요청 방식을 코드로 할 수 있게끔
# .text = html 파일을 text로 변환
soup = BeautifulSoup(response, 'html.parser')
# parsing = 원하는 코드만 가져올 수 있게끔 
kospi = soup.select_one('#KOSPI_now').text
# Copy Selector 이용
print(kospi)

response1 = requests.get('https://finance.naver.com/marketindex/').text
soup1 = BeautifulSoup(response1, 'html.parser')
usd = soup1.select_one('#exchangeList > li.on > a.head.usd > div > span.value').text
print(usd)