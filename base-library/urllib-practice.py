import urllib.request

# response = urllib.request.urlopen('https://www.python.org')
# print(response.read().decode('utf-8'))
# print(type(response))
# print(response.status)
# print(response.getheaders())


import urllib.parse

# data = bytes(urllib.parse.urlencode({'world': 'hello'}), encoding='utf8')
# response = urllib.request.urlopen('http://httpbin.org/post', data=data)
# print(response.read().decode('utf-8'))


# response = urllib.request.urlopen('http://httpbin.org/get', timeout=0.1)
# print(response.read())


import socket
import urllib.error

# try:
#     response = urllib.request.urlopen('http://httpbin.org/get', timeout=0.1)
# except urllib.error.URLError as e:
#     if isinstance(e.reason, socket.timeout):
#         print('TIME OUT')


# request = urllib.request.Request('https://python.org')
# response = urllib.request.urlopen(request)
# print(response.read().decode('utf-8'))


from urllib import request, parse

# url = 'http://httpbin.org/post'
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
#     'Host': 'httpbin.org',
# }
# dict = {
#     'name': 'Germey'
# }
# data = bytes(parse.urlencode(dict), encoding='utf-8')
# req = request.Request(url=url, data=data, headers=headers, method='POST')
# response = request.urlopen(req)
# print(response.read().decode('utf-8'))


from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener
from urllib.error import URLError

# username = 'username'
# password = 'password'
# url = 'http://localhost:5000'
#
# p = HTTPPasswordMgrWithDefaultRealm()
# p.add_password(None, url, username, password)
# auth_handler = HTTPBasicAuthHandler(p)
# opener = build_opener(auth_handler)
#
# try:
#     result = opener.open(url)
#     html = result.read().decode('utf-8')
#     print(html)
# except URLError as e:
#     print(e.reason)


from urllib.request import ProxyHandler

# proxy_handler = ProxyHandler({
#     'http': 'http://127.0.0.1:9743',
#     'https': 'https://127.0.0.1:9743',
# })
# opener = build_opener(proxy_handler)
# try:
#     result = opener.open('https://www.baidu.com')
#     html = result.read().decode('utf-8')
#     print(html)
# except URLError as e:
#     print(e.reason)


import http.cookiejar, urllib.request

# cookie = http.cookiejar.CookieJar()
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# response = opener.open('http://www.baidu.com')
# for item in cookie:
#     print('='.join([item.name, item.value]))


from urllib import request, error

# try:
#     response = request.urlopen('https://cuiqingcai.com/index.html')
# except error.URLError as e:
#     print(e.reason)


# try:
#     response = request.urlopen('https://cuiqingcai.com/index.html')
# except error.HTTPError as e:
#     print(e.reason, e.code, e.headers, sep='\n')


# try:
#     response = request.urlopen('https://cuiqingcai.com/index.html')
# except error.HTTPError as e:
#     print(e.reason, e.code, e.headers, sep='\n')
# except error.URLError as e:
#     print(e.reason)
# else:
#     print('Request Successfully')


# try:
#     response = urllib.request.urlopen('https://www.baidu.com', timeout=0.01)
# except urllib.error.URLError as e:
#     print(type(e.reason))
#     if isinstance(e.reason, socket.timeout):
#         print('TIME OUT')


from urllib.parse import urlparse

# result = urlparse('http://www.baidu.com/index.html;user?id=5#comment')
# print(type(result), result, sep='\n')


# result = urlparse('http://www.baidu.com/index.html;user?id=5#comment', allow_fragments=False)
# print(type(result), result, sep='\n')


from urllib.parse import urlunparse

# data = ['http', 'www.baidu.com', 'index.html', 'user', 'a=6', 'comment']
# print(urlunparse(data))


from urllib.parse import urlsplit

# result = urlsplit('http://www.baidu.com/index.html;user?id=5#comment')
# print(result)


from urllib.parse import urlunsplit

# data = ['http', 'www.baidu.com', 'index.html', 'a=6', 'comment']
# print(urlunsplit(data))


from urllib.parse import urljoin

print(urljoin('http://www.baidu.com', 'FAQ.html'))
print(urljoin('http://www.baidu.com', 'https://cuiqingcai.com/FAQ.html'))
print(urljoin('http://www.baidu.com/about.html', 'https://cuiqingcai.com/FAQ.html'))
print(urljoin('http://www.baidu.com/about.html', 'https://cuiqingcai.com/FAQ.html?question=2'))
print(urljoin(' http://www.baidu.com?wd=abc', 'https://cuiqingcai.com/index.php'))
print(urljoin('http://www.baidu.com', '?category=2#comment'))
print(urljoin('www.baidu.com', '?category=2#comment'))
print(urljoin('www.baidu.com#conent', '?category=2'))
