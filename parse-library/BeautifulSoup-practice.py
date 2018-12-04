from bs4 import BeautifulSoup


html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters;and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/titllie" class="sister" id="link3">Titllie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

soup = BeautifulSoup(html, 'lxml')  # lxml为解析器
# print(soup.prettify())  # 按标准的缩进格式输出
# print(soup.title.string)
# print(soup.head)
# print(soup.p)

# print(soup.title.name)
# print(soup.p.attrs)
# print(soup.p.attrs['name'])
# print(soup.p['name'])

# print(soup.p.contents)

# print(soup.p.children)
# for i, child in enumerate(soup.p.children):
#     print(i, child)


html2 = """
<div class="panel">
<div class="panel-heading">
<h4>Hello</h4> 
</div> 
<div class="panel-body">
<ul class="list" id="list-1"> 
<li class="element">Foo</li> 
<li class="element">Bar</li> 
<li class="element">]ay</li>
</ul> 
<ul class="list list-small" id="list-2"> 
<li class="element">Foo</li> 
<li class="element">Bar</li> 
</ul> 
</div> 
</div> 
"""

soup2 = BeautifulSoup(html2, 'lxml')
# print(soup2.select('.panel .panel-heading'))
# print(soup2.select('ul li'))
# print(soup2.select('#list-2 .element'))
# print(type(soup2.select('ul')[0]))
# for ul in soup2.select('ul'):
    # print(ul.select('li'))
    # print(ul['id'])
    # print(ul.attrs['id'])
# for li in soup2.select('li'):
#     print('Get Text: ', li.get_text())
#     print('String: ', li.string)
