import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from pytz import timezone
from github_utils import get_github_repo, upload_github_issue

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

access_token = os.environ['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']
repository_name = "ci-cd-test"

seoul_timezone = timezone('Asia/Seoul')
today = datetime.now(seoul_timezone)
today_date = today.strftime("%Y년 %m월 %d일")
issue_title = f"YES24 IT 신간 도서 알림({today_date})"

repo = get_github_repo(access_token, repository_name)
upload_github_issue(repo, issue_title, data)
