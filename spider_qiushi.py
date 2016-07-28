# -*- coding: utf-8 -*-

import time
import codecs
import requests
from bs4 import BeautifulSoup

url = 'http://www.qiushibaike.com'
r = requests.get(url)
c = BeautifulSoup(r.content, 'html.parser')
content = c.find_all('div', class_='content')

# 保存源网页
with codecs.open('./qiushi.html', 'w', 'utf-8') as f:
    f.write(c.prettify())

# 添加时间信息
with codecs.open('./qiushi.baike', 'a', 'utf-8') as f:
    now = time.strftime('%Y-%m-%d---%H-%M-%S', 
                        time.localtime(time.time()))
    f.write('\n#######')
    f.write(now)
    f.write('#######\n')

# 输出糗事详情
count = 1
for item in content:
    if item.string is not None:
        try:
            with codecs.open('./qiushi.baike', 'a', 'utf-8') as f:
                line = '\n' + str(count) + '. '
                line += item.string.strip() + '\n'
                f.write(line)
                count += 1
        except IOError, e:
            print '无法找到qiushi.baike文件'
            print e
    else:
        line = '\n' + str(count) + '. '
        for tag in item.contents:
            if hasattr(tag, 'contents'):
                pass
            else:
                line += tag.strip()
                line += '\n'
        with codecs.open('./qiushi.baike', 'a', 'utf-8') as f:
            f.write(line)
            count += 1
