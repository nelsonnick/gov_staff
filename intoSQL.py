#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import requests
from selenium import webdriver
import re
import urllib.parse
import pymysql
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
    '长清': 'http://cq.jnbb.gov.cn/smzgs/',
    # '青岛': 'http://120.221.95.1:1888/',
        }


class Person:
    def __init__(self, dw, xm, xb, bm, zybzqk):
        self.dw = dw
        self.xm = xm
        self.xb = xb
        self.bm = bm
        self.zybzqk = zybzqk


def get_person_info(cols, info):
    try:
        cols.index(['单位'])
    except ValueError:
        dw_num = ''
    else:
        dw_num = cols.index(['单位'])
    try:
        cols.index(['姓名'])
    except ValueError:
        xm_num = ''
    else:
        xm_num = cols.index(['姓名'])
    try:
        cols.index(['部门'])
    except ValueError:
        bm_num = ''
    else:
        bm_num = cols.index(['部门'])
    try:
        cols.index(['性别'])
    except ValueError:
        xb_num = ''
    else:
        xb_num = cols.index(['性别'])
    try:
        cols.index(['占用编制情况'])
    except ValueError:
        zybzqk_num = ''
    else:
        zybzqk_num = cols.index(['占用编制情况'])
    if dw_num != '':
        dw = info[dw_num][4:len(info[dw_num]) - 5]
    else:
        dw = ''
    if xm_num != '':
        xm = info[xm_num][4:len(info[xm_num]) - 5]
    else:
        xm = ''
    if xb_num != '':
        xb = info[xb_num][4:len(info[xb_num]) - 5]
    else:
        xb = ''
    if bm_num != '':
        bm = info[bm_num][4:len(info[bm_num]) - 5]
    else:
        bm = ''
    if zybzqk_num != '':
        zybzqk = info[zybzqk_num][4:len(info[zybzqk_num]) - 5]
    else:
        zybzqk = ''
    return Person(dw, xm, xb, bm, zybzqk)


def save_person(person, dwzd, dwbh, bzlx):
    db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO person(dwzd, dwbh, dwmc, ssbm, ryxm, ryxb, bzlx, bzqk) \
                                      VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
          (dwzd, dwbh, person.dw, person.bm, person.xm, person.xb, bzlx, person.zybzqk)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()


def down_person(dwmc, dwbh, bzlx, dwzd):
    rt = requests.get(
        Dict[dwzd] + "PersonList.aspx?unitId=" + dwbh + "&BZLX=" + bzlx, timeout=100)
    key = rt.text
    titles = re.findall(r'<th.+?</th>', key)
    cols = []
    for title in titles:
        cols.append(re.findall(r'[\u4e00-\u9fa5]{2,}', title))
    if len(cols) == 3:
        persons = re.findall(r'<td>.+?</td><td>.+?</td><td>.+?</td>', key)
        for person in persons:
            information = re.findall(r'<td>.+?</td>', person)
            save_person(get_person_info(cols, information), dwzd, dwbh, bzlx)
        print(dwzd + ':' + dwbh + '-' + dwmc + '-' + bzlx + '--->下载完成！')
    elif len(cols) == 4:
        persons = re.findall(r'<td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td>', key)
        for person in persons:
            information = re.findall(r'<td>.+?</td>', person)
            save_person(get_person_info(cols, information), dwzd, dwbh, bzlx)
        print(dwzd + ':' + dwbh + '-' + dwmc + '-' + bzlx + '--->下载完成！')
    elif len(cols) == 5:
        persons = re.findall(r'<td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td>', key)
        for person in persons:
            information = re.findall(r'<td>.+?</td>', person)
            save_person(get_person_info(cols, information), dwzd, dwbh, bzlx)
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
    department_string = re.compile(r"ipt:f\(.+?\);\" title=").findall(t)
    file = open("C:\\" + dwzd + ".txt", "a", encoding='utf-8')
    for d in department_string:
        code = d.split('\'')[1]
        name = urllib.parse.unquote(d.split('\'')[3])
        down_department(code, dwzd)
        file.write(code + "\t" + name + "\n")
    file.close()


def down_department(dwbh, dwzd):
    rt = requests.get(Dict[dwzd] + "UnitDetails.aspx?unitId=" + dwbh, timeout=100)
    soup = BeautifulSoup(rt.text, "html.parser").div.table.find_all('tr')[2].td.table
    print(soup)
    dwmc = soup.find_all('tr')[0].find_all('td')[1].span.b.font.string.strip()
    qtmc = soup.find_all('tr')[1].find_all('td')[1].string.strip()
    ldzs = soup.find_all('tr')[2].find_all('td')[1].span.string.strip()
    jb = soup.find_all('tr')[2].find_all('td')[3].span.b.font.string.strip()
    nsjg = soup.find_all('tr')[8].td.span.string.strip()
    number = soup.find_all('tr')[4].td.div.table.find_all('tr')
    xz_plan_num = xz_real_num = sy_plan_num = sy_real_num = gq_plan_num = gq_real_num = '0'
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
    db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO department(dwzd, dwbh, dwmc, qtmc, ldzs, jb, nsjg, xz_plan_num, xz_real_num, sy_plan_num, sy_real_num, gq_plan_num, gq_real_num) \
          VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
          (dwzd, dwbh, dwmc, qtmc, ldzs, jb, nsjg, xz_plan_num, xz_real_num, sy_plan_num, sy_real_num, gq_plan_num, gq_real_num)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()


def down():
    for location in Dict:
        get_department(location)


# down_department('037002000094', '青岛')
# down_department('037001004401414', '槐荫')


down()
