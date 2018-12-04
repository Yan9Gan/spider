from pyquery import PyQuery as pq


html = """
<div id="container"> 
<ul class="list"> 
<li class="item-0">first item</li> 
<li class="item-1"><a href="link2.html">second item</a></li> 
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li> 
<li class="item-1 active"><a href="link4.html">fourth item</a></li> 
<li class="item-0"><a href="link5.html">fifth item</a></li> 
</ul> 
</div> 
"""

# doc = pq(html)
# print(doc('li'))

# doc = pq(url='https://cuiqingcai.com')
# print(doc('title'))


import requests

# doc = pq(requests.get('https://cuiqingcai.com').text)
# print(doc('title'))

doc = pq(html)
# print(doc('#container .list li'))
# print(type(doc('#container .list li')))
items = doc('.list')
print(type(items))
print(items)
# lis = items.find('li')
# print(type(lis))
# print(lis)

# lis = items.children()
# print(type(lis))
# print(lis)

# ------------------------ Page 186 ------------------------




