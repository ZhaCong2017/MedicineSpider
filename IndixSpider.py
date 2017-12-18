#/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import xlwt
import sys

def getHTMLText(url):
    kv = {'user-agent':'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=kv)
        r.raise_for_status()
        r.encoding = 'gb2312'
        return r.text
    except:
        return "Wrong"

def getdata(text):
    p = u"addItem\(\"(.*)\",\""
    indix = re.compile(p).findall(text)
    # print indix

    p = u"\",\"(.*)\""
    name = re.compile(p).findall(text)
    # for i in name:
    #     print i.encode('utf-8')

    with open('indix.txt','w') as f:
        for i in range(len(indix)):
            s = str(indix[i].encode('utf-8')) + ',' + str(name[i].encode('utf-8')).replace(' ', '') + '\n'
            f.write(s)

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    url = 'http://www.bjrbj.gov.cn/LDJAPP/search/testtree.html'
    text = getHTMLText(url)
    # print text
    getdata(text)