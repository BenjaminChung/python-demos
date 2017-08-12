# -*- coding: utf-8 -*-
import codecs
import cookielib
import csv
import sys
import urllib
import urllib2
import time

from bs4 import BeautifulSoup

reload(sys)

type = sys.getfilesystemencoding()
sys.setdefaultencoding(type)


def req(_no):
    content = ''
    cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    url = "http://www.szsti.gov.cn/services/query/newdefault.aspx"
    firstResponse = opener.open(url)
    index = firstResponse.read()
    soup = BeautifulSoup(index, 'html.parser')
    __EVENTVALIDATION = soup.select("#__EVENTVALIDATION")[0]["value"]
    __VIEWSTATE = soup.select("#__VIEWSTATE")[0]["value"]
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    values = {"txtShenqingdanweimingcheng": _no, "__EVENTVALIDATION": __EVENTVALIDATION, "__VIEWSTATE": __VIEWSTATE}
    data = urllib.urlencode(values)
    request = urllib2.Request(url, data, headers)
    try:
        response = opener.open(request)
        content = response.read()
    except Exception, e:
        print e
        pass
    return content


def fetchContent(_no, count=1, retrytimes=3):
    list = []
    print 'start fetch :' + str(_no) 
    content = req(_no)
    while content == '' and count <= retrytimes:
        time.sleep(2)
        content = req(_no)
        count += 1
    if content == '':
        print 'error,' + str(_no) + ' fetch error'
    else:
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.select('table')[1]
        trs = table.select("td")
        for index in range(len(trs)):
            if index > 0:
                list.append(str(trs[index].getText()).strip().decode("utf-8").encode(type))
    return list


def gen(_nos):
    with open('./result.csv'.encode("utf-8").decode(type), 'wb') as csvfile:
        csvfile.write(codecs.BOM_UTF8)
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        titles = ['受理号', '项目名称', '申报单位', '单位地址', '联系人', '指南领域', '业务小类', '业务中类', '审核状态']
        for index in range(len(titles)):
            titles[index] = titles[index].decode("utf-8").encode(type)
        spamwriter.writerow(titles)
        for _no in _nos:
            list = fetchContent(_no)
            if len(list) > 0:
                spamwriter.writerow(list)



if __name__ == "__main__":
    paras = []
    start = input("please input the start number:")
    end = input("please input the end number:")
    for i in range(start, end + 1, 1):
        paras.append(i)
    startTime = time.time()
    gen(paras)
    endTime = time.time()
    print 'finished,cost time:' + str(endTime - startTime) + "seconds"
