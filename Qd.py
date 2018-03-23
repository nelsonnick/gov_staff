#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import requests
from selenium import webdriver
import re
import urllib.parse
import pymysql
from bs4 import BeautifulSoup

Dict = {
    '青岛': 'http://120.221.95.1:1888/',
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
        print(dwzd + ':' + dwbh + '-' + person.xm + '-' + bzlx + '--->保存错误！')
        db.rollback()
    db.close()


def down_person(dwmc, dwbh, bzlx, dwzd):
    rt = requests.get(
        Dict[dwzd] + "PersonList.aspx?unitId=" + dwbh + "&BZLX=" + bzlx, timeout=1000)
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
    if soup.find_all('tr')[2].find_all('td')[1].string is not None:
        ldzs = soup.find_all('tr')[2].find_all('td')[1].string.strip()
    else:
        ldzs = ''
    if soup.find_all('tr')[2].find_all('td')[3].span.b.font.string is not None:
        jb = soup.find_all('tr')[2].find_all('td')[3].span.b.font.string.strip()
    else:
        jb = ''
    if soup.find_all(id="lblNeiSheJG"):
        nsjg = soup.find_all(id="lblNeiSheJG")[0].string.strip()
    else:
        nsjg = ''

    if soup.find_all(id="LabelXZ"):
        if soup.find_all(id="LabelXZ")[0].string is not None:
            xz_plan_num = soup.find_all(id="LabelXZ")[0].string.strip()
        else:
            xz_plan_num = ''
    else:
        xz_plan_num = ''
    if soup.find_all(id="RealXZ"):
        xz_real_num = soup.find_all(id="RealXZ")[0].a.string.strip()
        lx = re.search(re.compile(r'BZLX=.+?$'), soup.find_all(id="RealXZ")[0].a['href']).group(0)
        bzlx = lx[5:len(lx)]
        down_person(dwmc, dwbh, bzlx, dwzd)
    else:
        xz_real_num = ''

    if soup.find_all(id="LabelGQ"):
        if soup.find_all(id="LabelGQ")[0].string is not None:
            gq_plan_num = soup.find_all(id="LabelGQ")[0].string.strip()
        else:
            gq_plan_num = ''
    else:
        gq_plan_num = ''
    if soup.find_all(id="RealGQ"):
        gq_real_num = soup.find_all(id="RealGQ")[0].a.string.strip()
        lx = re.search(re.compile(r'BZLX=.+?$'), soup.find_all(id="RealGQ")[0].a['href']).group(0)
        bzlx = lx[5:len(lx)]
        down_person(dwmc, dwbh, bzlx, dwzd)
    else:
        gq_real_num = ''

    if soup.find_all(id="LabelSY"):
        if soup.find_all(id="LabelSY")[0].string is not None:
            sy_plan_num = soup.find_all(id="LabelSY")[0].string.strip()
        else:
            sy_plan_num = ''
    else:
        sy_plan_num = ''

    if soup.find_all(id="RealSY"):
        sy_real_num = soup.find_all(id="RealSY")[0].a.string.strip()
        lx = re.search(re.compile(r'BZLX=.+?$'), soup.find_all(id="RealSY")[0].a['href']).group(0)
        bzlx = lx[5:len(lx)]
        down_person(dwmc, dwbh, bzlx, dwzd)
    else:
        sy_real_num = ''

    db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO department(dwzd, dwbh, dwmc, qtmc, ldzs, jb, nsjg, xz_plan_num, xz_real_num, sy_plan_num, sy_real_num, gq_plan_num, gq_real_num) \
          VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
          (dwzd, dwbh, dwmc, qtmc, ldzs, jb, nsjg, xz_plan_num, xz_real_num, sy_plan_num, sy_real_num, gq_plan_num, gq_real_num)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print(dwzd + ':' + dwbh + '-' + dwmc + '-' + '--->保存错误！')
        db.rollback()
    db.close()


def down():
    for location in Dict:
        get_department(location)


down()
# down_department('037002000266', '青岛')
