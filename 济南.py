#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import requests
from selenium import webdriver
import re
import urllib.parse
import pymysql
from person import get_person_info
from person import save_person
from bs4 import BeautifulSoup

Dict = {
    '槐荫': 'http://hy.jnbb.gov.cn/smzgs/',
    '历下': 'http://lx.jnbb.gov.cn/smzgs/',
    '历城': 'http://lc.jnbb.gov.cn/smzgs/',
    '商河': 'http://sh.jnbb.gov.cn/smzgs/',
    '天桥': 'http://tq.jnbb.gov.cn/smzgs/',
    '市中': 'http://sz.jnbb.gov.cn/smzgs/',
    '市直': 'http://jnbb.gov.cn/smzgs/',
    '平阴': 'http://py.jnbb.gov.cn/smzgs/',
    '济阳': 'http://jy.jnbb.gov.cn/smzgs/',
    '章丘': 'http://zq.jnbb.gov.cn/smzgs/',
    '长清': 'http://cq.jnbb.gov.cn/smzgs/'
        }


def down_person(dwmc, dwbh, bzlx, dwzd):
    try:
        rt = requests.get(Dict[dwzd] + "PersonList.aspx?unitId=" + dwbh + "&BZLX=" + bzlx, timeout=1000)
    except:
        file = open("C:\\人员列表抓取错误.txt", "a", encoding='utf-8')
        file.write(dwzd + "\t" + dwbh + "\t" + dwmc + "\t" + bzlx + "\t" + Dict[dwzd] + "PersonList.aspx?unitId=" + dwbh + "&BZLX=" + bzlx + "\n")
        file.close()
        print(dwzd + ':' + dwbh + '-' + '--->抓取失败！')
        return
    key = rt.text
    titles = re.findall(r'<th.+?</th>', key)
    cols = []
    for title in titles:
        cols.append(re.findall(r'[\u4e00-\u9fa5]{2,}', title))
    if len(cols) == 3:
        persons = re.findall(r'<td>.+?</td><td>.+?</td><td>.+?</td>', key)
        for person in persons:
            information = re.findall(r'<td>.+?</td>', person)
            save_person(get_person_info(cols, information, dwzd, dwbh, bzlx))
        print(dwzd + ':' + dwbh + '-' + dwmc + '-' + bzlx + '--->下载完成！')
    elif len(cols) == 4:
        persons = re.findall(r'<td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td>', key)
        for person in persons:
            information = re.findall(r'<td>.+?</td>', person)
            save_person(get_person_info(cols, information, dwzd, dwbh, bzlx))
        print(dwzd + ':' + dwbh + '-' + dwmc + '-' + bzlx + '--->下载完成！')
    elif len(cols) == 5:
        persons = re.findall(r'<td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td>', key)
        for person in persons:
            information = re.findall(r'<td>.+?</td>', person)
            save_person(get_person_info(cols, information, dwzd, dwbh, bzlx))
        print(dwzd + ':' + dwbh + '-' + dwmc + '-' + bzlx + '--->下载完成！')
    elif len(cols) == 0:
        print(dwzd + ':' + dwbh + '-' + dwmc + '-' + bzlx + '--->无人员信息！')
    else:
        print(dwzd + ':' + dwbh + '-' + dwmc + '-' + bzlx + '--->无法识别！')


def get_department(dwzd):
    browser = webdriver.Chrome()
    browser.get(Dict[dwzd] + "TreeViewPage.aspx")
    t = browser.page_source
    browser.close()
    department_string = re.compile(r'ipt:f\(.+?\);\"').findall(t)
    file = open("C:\\" + dwzd + ".txt", "a", encoding='utf-8')
    for d in department_string:
        code = d.split('\'')[1]
        name = urllib.parse.unquote(d.split('\'')[3])
        down_department(code, dwzd)
        file.write(code + "\t" + name + "\n")
    file.close()


def down_department(dwbh, dwzd):
    xz_plan_num = xz_real_num = sy_plan_num = sy_real_num = gq_plan_num = gq_real_num = '0'
    rt = requests.get(Dict[dwzd] + "UnitDetails.aspx?unitId=" + dwbh, timeout=1000)
    # print(Dict[dwzd] + "UnitDetails.aspx?unitId=" + dwbh)
    soup = BeautifulSoup(rt.text, "html.parser").div.table.find_all('tr')[2].td.table
    if soup.find_all('tr')[0].find_all('td')[1].span.b.font.string is not None:
        dwmc = soup.find_all('tr')[0].find_all('td')[1].span.b.font.string.strip()
    else:
        dwmc = ''
    if dwmc == '':
        print('编号：' + dwbh + '-->不存在！')
        return
    if soup.find_all('tr')[1].find_all('td')[1].string is not None:
        qtmc = soup.find_all('tr')[1].find_all('td')[1].string.strip()
    else:
        qtmc = ''
    if soup.find_all('tr')[2].find_all('td')[1].span.string is not None:
        ldzs = soup.find_all('tr')[2].find_all('td')[1].span.string.strip()
    else:
        ldzs = ''
    if soup.find_all('tr')[2].find_all('td')[3].span.b.font.string is not None:
        jb = soup.find_all('tr')[2].find_all('td')[3].span.b.font.string.strip()
    else:
        jb = ''
    if soup.find_all(id="lblNeiSheJG")[0].string is not None:
        nsjg = soup.find_all(id="lblNeiSheJG")[0].string.strip()
    else:
        nsjg = ''
    if soup.find_all('tr')[4].td.div.table is not None:
        number = soup.find_all('tr')[4].td.div.table.find_all('tr')
        for num in number:
            if num.find_all('td')[0].string.strip().find("行政编制数") != -1:
                if num.find_all('td')[1].font.string.strip() == "&nbsp;":
                    xz_plan_num = "0"
                else:
                    xz_plan_num = num.find_all('td')[1].font.string.strip()
                if num.find_all('td')[3].a.string.strip() == "&nbsp;":
                    xz_real_num = "0"
                else:
                    xz_real_num = num.find_all('td')[3].a.string.strip()
            elif num.find_all('td')[0].string.strip().find("事业编制数") != -1:
                if num.find_all('td')[1].font.string.strip() == "&nbsp;":
                    sy_plan_num = "0"
                else:
                    sy_plan_num = num.find_all('td')[1].font.string.strip()
                if num.find_all('td')[3].a.string.strip() == "&nbsp;":
                    sy_real_num = "0"
                else:
                    sy_real_num = num.find_all('td')[3].a.string.strip()
            elif num.find_all('td')[0].string.strip().find("工勤编制数") != -1:
                if num.find_all('td')[1].font.string.strip() == "&nbsp;":
                    gq_plan_num = "0"
                else:
                    gq_plan_num = num.find_all('td')[1].font.string.strip()
                if num.find_all('td')[3].a.string.strip() == "&nbsp;":
                    gq_real_num = "0"
                else:
                    gq_real_num = num.find_all('td')[3].a.string.strip()
            else:
                pass
            lx = re.search(re.compile(r'BZLX=.+?$'), num.find_all('td')[3].a['href']).group(0)
            bzlx = lx[5:len(lx)]
            down_person(dwmc, dwbh, bzlx, dwzd)
    else:
        print(dwzd + ':' + dwbh + '-' + dwmc + '-' + '--->无编制人员！')




def down():
    for location in Dict:
        get_department(location)


down()

