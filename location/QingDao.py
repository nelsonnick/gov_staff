#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import requests
import re
from bs4 import BeautifulSoup
from person import get_person
from person import save_person
from person import get_person_err
from person import person_text
from department import get_department_err
from department import department_text
from department import save_department
from department import get_department
from department import down_department_dwbh

Dict = {
    '青岛': 'http://120.221.95.1:1888/',
}


def down_person(dwzd, dwbh, dwmc, bzlx):
    url = Dict[dwzd] + "PersonList.aspx?unitId=" + dwbh + "&BZLX=" + bzlx
    try:
        rt = requests.get(url, timeout=1000)
    except:
        get_person_err(dwzd, dwbh, dwmc, bzlx, url)
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
            save_person(get_person(cols, information, dwzd, dwbh, bzlx))
        person_text(dwzd + ':' + dwbh + '-' + dwmc + '-' + bzlx + '--->下载完成！')
    elif len(cols) == 4:
        persons = re.findall(r'<td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td>', key)
        for person in persons:
            information = re.findall(r'<td>.+?</td>', person)
            save_person(get_person(cols, information, dwzd, dwbh, bzlx))
        person_text(dwzd + ':' + dwbh + '-' + dwmc + '-' + bzlx + '--->下载完成！')
    elif len(cols) == 5:
        persons = re.findall(r'<td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td>', key)
        for person in persons:
            information = re.findall(r'<td>.+?</td>', person)
            save_person(get_person(cols, information, dwzd, dwbh, bzlx))
        person_text(dwzd + ':' + dwbh + '-' + dwmc + '-' + bzlx + '--->下载完成！')
    elif len(cols) == 0:
        person_text(dwzd + ':' + dwbh + '-' + dwmc + '-' + bzlx + '--->无人员信息！')
    else:
        person_text(dwzd + ':' + dwbh + '-' + dwmc + '-' + bzlx + '--->无法识别！')


def down_department(dwzd, dwbh, dwmc):
    xz_plan_num = xz_real_num = sy_plan_num = sy_real_num = gq_plan_num = gq_real_num = '0'
    url = Dict[dwzd] + "UnitDetails.aspx?unitId=" + dwbh
    try:
        rt = requests.get(url, timeout=1000)
    except:
        get_department_err(dwzd, dwbh, dwmc, url)
        return
    soup = BeautifulSoup(rt.text, "html.parser").div.table.find_all('tr')[2].td.table
    if soup.find_all('tr')[0].find_all('td')[1].span.b.font.string is not None:
        dwmc = soup.find_all('tr')[0].find_all('td')[1].span.b.font.string.strip()
    else:
        dwmc = ''
    if dwmc == '':
        department_text('编号：' + dwbh + '-->不存在！')
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
    if soup.find_all(id="lblNeiSheJG")[0].string is not None:
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
        down_person(dwzd, dwbh, dwmc, bzlx)
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
        down_person(dwzd, dwbh, dwmc, bzlx)
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
        down_person(dwzd, dwbh, dwmc, bzlx)
    else:
        sy_real_num = ''

    save_department(
        get_department(dwzd, dwbh, dwmc, qtmc, ldzs, jb, nsjg, xz_plan_num, xz_real_num, sy_plan_num, sy_real_num,
                   gq_plan_num, gq_real_num))


def down():
    for dwzd in Dict:
        down_department_dwbh(dwzd, Dict[dwzd])
        file = open("c:\\" + dwzd + ".txt", "r", encoding='UTF-8')
        line = file.readline()
        while line:
            dwbh = line.split('\t')[0]
            dwmc = line.split('\t')[1]
            down_department(dwzd, dwbh, dwmc)
            line = file.readline()
        file.close()
