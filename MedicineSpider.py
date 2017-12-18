#/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import xlwt
import sys

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = 'gb2312'
        return r.text
    except:
        return "Wrong"

def getdata(text, num, n, worksheet):
    soup = BeautifulSoup(text, 'html.parser')
    data = soup.findAll('tr', attrs={'bgcolor':'#FFFFFF'})
    for i in range(2, n + 2):
        now = str(data[i]).replace(" ", "").encode('utf-8')
        # print now
        p = u"<tdalign=\"center\"bgcolor=\"E4E8EF\"height=\"28\">(.*)?</td>"
        result = re.compile(p).findall(now)
        worksheet.write(num  + i - 2, 0, label = str(result[0]))
        worksheet.write(num + i - 2, 2, label=str(result[1]))

        p = u"\"target=\"_blank\">(.*)?</a>"
        result = re.compile(p).findall(now)
        worksheet.write(num + i - 2, 1, label=str(result[0]).encode('utf-8'))
        # print result[0].encode('utf-8')

        p = u"<tdbgcolor=\"E4E8EF\"height=\"28\">(.*)?</td>"
        result = re.compile(p).findall(now)
        worksheet.write(num + i - 2, 3, label=str(result[0]))
        worksheet.write(num + i - 2, 4, label=str(result[1]))

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('Medicine')
    url = 'http://www.bjrbj.gov.cn/LDJAPP/search/mframe_2005.jsp?sno='
    i = 0
    while i <= 2640: #2640
        text = getHTMLText(url + str(i))
        if text == 'Wrong':
            continue;
        getdata(text, i, 20, worksheet)
        # s = '   ' + data + '\n'
        # with open("BTCvalue.txt", "a") as f:
        #     f.write(s)
        i += 20
        if i % 100 == 0:
            print i

    text = 'Wrong'
    while text == 'Wrong':
        text = getHTMLText(url + str(2660))
    getdata(text, 2660, 15, worksheet)

    workbook.save('Medicine.xls')