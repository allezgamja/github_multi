import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.naver.com').text
soup = BeautifulSoup(response, 'html.parser')

tags  = soup.select('#PM_ID_ct > div.header > div.section_navbar > div.area_hotkeyword.PM_CL_realtimeKeyword_base > div.ah_roll.PM_CL_realtimeKeyword_rolling_base > div > ul > li .ah_k')

#부모태그 li에서 .ah_k (class 이름)

for tag in tags:
    print(tag.text)


with open('naver_rank.txt', 'w') as f:
    f.write('네이버 검색어 순위 \n')
    for tag in enumerate(tags):     # enumerate: 인덱스 번호까지 반환
        f.write(f'{i+1}, {tag.text} \n')


