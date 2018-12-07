import requests
from pyquery import PyQuery as pq


url = 'https://www.zhihu.com/explore'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
}
html = requests.get(url, headers=headers).text
doc = pq(html)
items = doc('.explore-tab .feed-item').items()
for item in items:
    question = item.find('h2').text()
    author = item.find('.author-link-line').text()
    with open('../images/explore.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join([question, author]))
        f.write('\n' + '=' * 50 + '\n')



