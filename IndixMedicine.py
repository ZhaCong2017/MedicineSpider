#/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import xlwt
import sys

num = 0

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = 'gb2312'
        return r.text
    except:
        return "Wrong"

def getdata(text, head, worksheet):
    global num
    soup = BeautifulSoup(text, 'html.parser')
    data = soup.findAll('tr', attrs={'bgcolor':'#FFFFFF'})

    for i in range(2, len(data)):
        # print head
        now = str(data[i]).replace(" ", "").encode('utf-8')
        # print now
        p = u"<tdalign=\"center\"bgcolor=\"E4E8EF\"height=\"28\">(.*)?</td>"
        result = re.compile(p).findall(now)
        worksheet.write(num, 0, label = str(head))
        worksheet.write(num, 2, label=str(result[1]))

        p = u"\"target=\"_blank\">(.*)?</a>"
        result = re.compile(p).findall(now)
        worksheet.write(num, 1, label=str(result[0]).encode('utf-8'))
        # print result[0].encode('utf-8')

        p = u"<tdbgcolor=\"E4E8EF\"height=\"28\">(.*)?</td>"
        result = re.compile(p).findall(now)
        worksheet.write(num, 3, label=str(result[0]))
        worksheet.write(num, 4, label=str(result[1]))
        num += 1


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('IndixMedicine')
    name = []
    indix = []
    with open('indix.txt', 'r') as f:
        while True:
            tmp = f.readline()
            if not tmp:
                break;
            a, b = tmp.split(',')
            indix.append(a)
            name.append(b[:-1].encode('utf-8'))

    url = 'http://www.bjrbj.gov.cn/LDJAPP/search/mframe_2005.jsp?&hn='
    i = 0
    while i < len(indix):
        if i != len(indix) - 1 and indix[i] in indix[i + 1]:
            i += 1
            continue;

        if indix[i][0] == 'X':
            head = u'西药\\'
        else:
            head = u'中药\\'
        for j in range(i + 1):
            if indix[j] in indix[i] and (len(indix[i]) == len(indix[j]) or indix[i][len(indix[j])] == '.'):
                head += name[j] + '\\'

        text = getHTMLText(url + indix[i].encode('utf-8'))
        if text == 'Wrong':
            continue;

        soup = BeautifulSoup(text, 'html.parser')
        n = soup.findAll('b')
        p = u"<font color=\"red\">(.*?)</font>"
        total = re.compile(p).findall(str(n))
        print i, total
        if len(total) == 0:
            i += 1
            continue;
        k = int(total[0])
        total = int(total[1])
        key = 0
        start = num
        for j in range(total):
            text = getHTMLText(url + indix[i].encode('utf-8') + '&sno=' + str(key))
            if text == 'Wrong':
                j -= 1
                continue
            key += 20
            getdata(text, head[:-1], worksheet)
        end = num
        if k != end - start:
            print "Wrong", end - start
        i += 1

    workbook.save('IndixMedicine.xls')