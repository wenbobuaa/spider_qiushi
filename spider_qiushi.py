# -*- coding: utf-8 -*-

import codecs
import requests
from bs4 import BeautifulSoup

url = 'http://www.qiushibaike.com'
r = requests.get(url)
c = BeautifulSoup(r.content, 'html.parser')
content = c.find_all('div', class_='content')

#  保存源网页
with codecs.open('./qiushi.html', 'w', 'utf-8') as f:
    f.write(c.prettify())

# 输出糗事详情
count = 1
for item in content:
    if item.string is not None:
        try:
            with codecs.open('./qiushi.baike', 'a', 'utf-8') as f:
                line = str(count) + '. ' + item.string.strip() + '\n'
                f.write(line)
                count += 1
        except IOError, e:
            print '无法找到qiushi.baike文件'
            print e
