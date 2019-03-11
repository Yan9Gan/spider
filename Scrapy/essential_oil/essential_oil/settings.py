# -*- coding: utf-8 -*-

# Scrapy settings for essential_oil project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

BOT_NAME = 'essential_oil'

SPIDER_MODULES = ['essential_oil.spiders']
NEWSPIDER_MODULE = 'essential_oil.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'essential_oil (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 100

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0
DOWNLOAD_TIMEOUT = 60
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 100
CONCURRENT_REQUESTS_PER_IP = 100

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'cookie': 'shshshfpa=953e8d25-60e0-b22f-1257-709613744249-1544175519; xtest=3849.cf6b6759; qrsc=3; shshshfpb=jfZWHxwyMOLD5NpNK7jXlHQ%3D%3D; ipLoc-djd=1-72-2799-0; __jdu=1544175519090151046347; __jdv=122270672|baidu|-|organic|not set|1551944537310; PCSYCityID=1601; mt_xid=V2_52007VwMWV1hYVF4bSRFdDWYDFlJcXVVYGk8pVANmU0VSDw9ODx9BGEAAYAdFTg0LVQgDHRlcAW5URlcKCgJcL0oYXA17AhBOXFFDWh5CHVwOYgYiUG1YYlgcTR9ZDWUFG2JdXVRd; __jda=122270672.1544175519090151046347.1544175519.1552016138.1552025710.46; __jdc=122270672; __jdb=122270672.2.1544175519090151046347|46.1552025710; shshshfp=b15df21deacbca2bfb7e6de035566044; shshshsID=fcb0c14d0a8074930faf526158f1bc33_2_1552025713039; rkv=V0900; 3AB9D23F7A4B3C9B=M7E73QMR2UZZGHIVSA6TXFUUOV7Y3AONXSZD5YN3PRW73FICPNSUKGIEZ2CHU4Y3ZBKPKA4P7G6XAJCFNMSQ5V2VNQ',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'essential_oil.middlewares.EssentialOilSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'essential_oil.middlewares.EssentialOilDownloaderMiddleware': 100,
    'essential_oil.middlewares.SeleniumMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'essential_oil.pipelines.ExcelPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

RETRY_ENABLED: True
RETRY_TIMES: 10
