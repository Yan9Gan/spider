from lxml.html import etree


text = """
<div>
<ul>
<li class="item-0"><a href="link1.templates">first item</a></li>
<li class="item-1"><a href="link2.templates">second item</a></li>
<li class="item-inactive"><a href="link3.templates">third item</a></li>
<li class="item-1"><a href="link4.templates">fourth item</a></li>
<li class="item-0"><a href="link5.templates">fifth item</a>
"""
html = etree.HTML(text)
result = etree.tostring(html)
print(result.decode('utf-8'))








