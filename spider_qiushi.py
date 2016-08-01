# -*- coding: utf-8 -*-

import time
import codecs

import requests
from bs4 import BeautifulSoup
import redis

import settings


def spider_content_search(content, out_file):
    # 添加时间信息
    with codecs.open(out_file, 'a', 'utf-8') as f:
        now = time.strftime('%Y-%m-%d---%H-%M-%S',
                            time.localtime(time.time()))
        f.write('\n#######')
        f.write(now)
        f.write('#######\n')

    # 输出糗事详情
    for item in content:
        if item.string is not None:
            try:
                with codecs.open(out_file, 'a', 'utf-8') as f:
                    line = '\n' + '. '
                    line += item.string.strip() + '\n'
                    f.write(line)
            except IOError, e:
                print '无法找到输出文件'
                print e
        else:
            line = '\n' + '. '
            for tag in item.contents:
                if hasattr(tag, 'contents'):
                    pass
                else:
                    line += tag.strip()
                    line += '\n'
                    with codecs.open(out_file, 'a', 'utf-8') as f:
                        f.write(line)
                        line = ''


def spider_search(url):
    print url
    out_name = url.split('|')[1]
    url = url.split('|')[0]

    r = requests.get(url)
    if r.status_code == 200:
        pass
    else:
        print '访问页面错误: ' + r.status_code
        return
    source = BeautifulSoup(r.content, 'html.parser')

    # 保存源网页
    with codecs.open(out_name+'.html', 'w', 'utf-8') as f:
        f.write(source.prettify())

    content = source.find_all('a', target='_blank')
    links = source.find_all('a')

    for item in links:
        if 'title' in item.attrs and 'href' in item.attrs:
            name = item['title']
            link = url + item['href'] + '/articles/' + '|' + name
            global red
            red.lpush(settings.DBname, link)

    spider_content_search(content, out_name+'.baike')


if __name__ == '__main__':
    source_url = 'http://www.qiushibaike.com'

    red = redis.Redis(host='localhost', port='6379', db=1)
    while red.rpop(DBname) is not None:
        pass
    red.lpush(DBname, source_url+'|index')

    count = 0
    while True:
        url = red.rpop(settings.DBname)
        if url and count < settings.MAX_NUM:
            spider_search(url)
            count += 1
        else:
            break

    print '搜寻完毕'
