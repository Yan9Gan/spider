# -*- coding: utf-8 -*-
import json
import scrapy
from . import get_brand_url as gbu
from scrapy.http import Request
from urllib.parse import urlencode


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['www.jd.com']
    base_url = 'https://search.jd.com/Search?'
    headers = {
        'cookie': 'shshshfpa=953e8d25-60e0-b22f-1257-709613744249-1544175519; xtest=3849.cf6b6759; qrsc=3; shshshfpb=jfZWHxwyMOLD5NpNK7jXlHQ%3D%3D; ipLoc-djd=1-72-2799-0; __jdu=1544175519090151046347; __jda=122270672.1544175519090151046347.1544175519.1551165380.1551944537.43; __jdc=122270672; __jdv=122270672|baidu|-|organic|not set|1551944537310; rkv=V0900; PCSYCityID=1601; shshshfp=b15df21deacbca2bfb7e6de035566044; 3AB9D23F7A4B3C9B=M7E73QMR2UZZGHIVSA6TXFUUOV7Y3AONXSZD5YN3PRW73FICPNSUKGIEZ2CHU4Y3ZBKPKA4P7G6XAJCFNMSQ5V2VNQ; __jdb=122270672.13.1544175519090151046347|43.1551944537; shshshsID=5143ee6f5f64437f4646046892fcc608_13_1551945155670',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    }

    params = {
        'keyword': '',
        'enc': 'utf-8',
        'qrst': 1,
        'rt': 1,
        'stop': 1,
        'vt': 2,
        'suggest': '1.def.0.V19;',
        'stock': 1,
        'uc': 0
    }

    def __init__(self, keyword, *args, **kwargs):
        super(JdSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword
        self.params['keyword'] = self.keyword
        self.json_path = 'brand_url.json'

        start_url = self.base_url + urlencode(self.params)

        gbu.GetBrandUrl(start_url, self.json_path)

        with open(self.json_path, 'r', encoding='utf-8') as f:
            json_data = f.read()
        self.brand_dict = json.loads(json_data)

        self.brand_name = self.brand_url = ''

    def start_requests(self):
        self.brand_name = list(self.brand_dict.keys()).pop(0)
        self.brand_url = list(self.brand_dict.values()).pop(0)
        yield Request(self.brand_url, callback=self.get_page)

    def get_page(self):
        pass

    def parse(self, response):
        pass


