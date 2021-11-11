import requests
from bs4 import BeautifulSoup
import json
import os

print(os.path.abspath('scraper.py'))
print(os.path.abspath(__file__))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print('\033[92m' + '>> 예스24 - HTML/JavaScript/CSS/jQuery 주간베스트 - 스크래핑 시작' + '\033[0m')

req = requests.get(
    'http://www.yes24.com/24/Category/More/001001003020001?ElemNo=104&ElemSeq=1')
req.encoding = None
html = req.content
soup = BeautifulSoup(html, 'html.parser')
datas = soup.select(
    '#category_layout > ul > li > div > div.goods_info > div.goods_name'
)

data = {}

for title in datas:
    name = title.find_all('a')[0].text
    url = 'https://www.yes24.com'+title.find('a')['href']
    data[name] = url

with open(os.path.join(BASE_DIR, 'bookTitle.json'), 'w+', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent="\t")

print('\033[92m' + '>> 스크래핑 끝' + '\033[0m')
