#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import requests
import re
from selenium import webdriver
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
    '市直': 'http://jnbb.gov.cn/smzgs/',
    '市中': 'http://sz.jnbb.gov.cn/smzgs/',
    '历下': 'http://lx.jnbb.gov.cn/smzgs/',
    '槐荫': 'http://hy.jnbb.gov.cn/smzgs/',
    '天桥': 'http://tq.jnbb.gov.cn/smzgs/',
    '历城': 'http://lc.jnbb.gov.cn/smzgs/',
    '长清': 'http://cq.jnbb.gov.cn/smzgs/',
    '章丘': 'http://zq.jnbb.gov.cn/smzgs/',
    '济阳': 'http://jy.jnbb.gov.cn/smzgs/',
    '商河': 'http://sh.jnbb.gov.cn/smzgs/',
    '平阴': 'http://py.jnbb.gov.cn/smzgs/'
        }


# 下载人员信息
# 参数：单位驻地、单位编号、单位名称、编制类型
def down_person(dwzd, dwbh, dwmc, bzlx):
    url = Dict[dwzd] + "PersonList.aspx?unitId=" + dwbh + "&BZLX=" + bzlx
    try:
        rt = requests.get(url, timeout=1000)
    except:
        get_person_err(dwzd, dwbh, dwmc, bzlx, url)
        return
    key = rt.text
    titles = re.findall(r'<th.+?</th>', key)
    # 不同的地区，展示的信息有区别：3列、4列、5列
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


# 下载单位信息
# 参数：单位驻地、单位编号、单位名称
def down_department(dwzd, dwbh, dwmc):
    xz_plan_num = xz_real_num = xz_lone_num = sy_plan_num = sy_real_num = sy_lone_num = gq_plan_num = gq_real_num = gq_lone_num = '0'
    url = Dict[dwzd] + "UnitDetails.aspx?unitId=" + dwbh
    time = BeautifulSoup(requests.get(Dict[dwzd]).text, "html.parser").find_all(id="SPAN1")[0].get_text()[9:]
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
        # 有一行的情况
    if soup.find_all(id="lblMainDuty")[0].string is not None:
        zyzz = soup.find_all(id="lblMainDuty")[0].string.strip()
    else:
        # 获取单位的主要职责：大部分主要职责似乎是延迟加载，正常的方式抓取不到，需要借助浏览器
        browser = webdriver.Chrome()
        browser.get(url)
        rt = browser.page_source
        browser.close()
        zyzz = BeautifulSoup(rt, "html.parser").find_all(id="lblMainDuty")[0].get_text()
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
                    xz_lone_num = "0"
                else:
                    if len(num.find_all('td')[3].find_all('a')) == 1:
                        xz_real_num = num.find_all('td')[3].find_all('a')[0].string.strip()
                        xz_lone_num = "0"
                    else:
                        xz_real_num = num.find_all('td')[3].find_all('a')[0].string.strip()
                        xz_lone_num = num.find_all('td')[3].find_all('a')[1].string.strip()
            elif num.find_all('td')[0].string.strip().find("事业编制数") != -1:
                if num.find_all('td')[1].font.string.strip() == "&nbsp;":
                    sy_plan_num = "0"
                else:
                    sy_plan_num = num.find_all('td')[1].font.string.strip()
                if num.find_all('td')[3].a.string.strip() == "&nbsp;":
                    sy_real_num = "0"
                    sy_lone_num = "0"
                else:
                    if len(num.find_all('td')[3].find_all('a')) == 1:
                        sy_real_num = num.find_all('td')[3].find_all('a')[0].string.strip()
                        sy_lone_num = "0"
                    else:
                        sy_real_num = num.find_all('td')[3].find_all('a')[0].string.strip()
                        sy_lone_num = num.find_all('td')[3].find_all('a')[1].string.strip()
            elif num.find_all('td')[0].string.strip().find("工勤编制数") != -1:
                if num.find_all('td')[1].font.string.strip() == "&nbsp;":
                    gq_plan_num = "0"
                else:
                    gq_plan_num = num.find_all('td')[1].font.string.strip()
                if num.find_all('td')[3].a.string.strip() == "&nbsp;":
                    gq_real_num = "0"
                    gq_lone_num = "0"
                else:
                    if len(num.find_all('td')[3].find_all('a')) == 1:
                        gq_real_num = num.find_all('td')[3].find_all('a')[0].string.strip()
                        gq_lone_num = "0"
                    else:
                        gq_real_num = num.find_all('td')[3].find_all('a')[0].string.strip()
                        gq_lone_num = num.find_all('td')[3].find_all('a')[1].string.strip()
            else:
                pass
            lx = re.search(re.compile(r'BZLX=.+?$'), num.find_all('td')[3].a['href']).group(0)
            bzlx = lx[5:len(lx)]
            down_person(dwzd, dwbh, dwmc, bzlx)
        save_department(
            get_department(dwzd, dwbh, dwmc, qtmc, ldzs, jb, nsjg, zyzz, xz_plan_num, xz_real_num, xz_lone_num,
                           sy_plan_num, sy_real_num, sy_lone_num, gq_plan_num, gq_real_num, gq_lone_num, url, time))
    else:
        department_text(dwzd + ':' + dwbh + '-' + dwmc + '-' + '--->无编制人员！')


# 全部下载
def down_all():
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


# 按地区下载
# 参数：单位驻地
def down_one(dwzd):
    down_department_dwbh(dwzd, Dict[dwzd])
    file = open("c:\\" + dwzd + ".txt", "r", encoding='UTF-8')
    line = file.readline()
    while line:
        dwbh = line.split('\t')[0]
        dwmc = line.split('\t')[1]
        down_department(dwzd, dwbh, dwmc)
        line = file.readline()
    file.close()


# 按地区下载单位结构
# 参数：单位驻地
# 返回值：结构字符串
def down_structure_one(dwzd):
    browser = webdriver.Chrome()
    browser.get(Dict[dwzd] + "TreeViewPage.aspx")
    rt = browser.page_source
    browser.close()
    soup = BeautifulSoup(rt, "html.parser").body.form.table.tbody.tr.td.div
    del soup['id']
    del soup['style']
    del soup['class']
    # 清洗html标签
    for s in soup.find_all('div'):
        del s['id']
        del s['style']
        del s['class']
    for s in soup.find_all('img'):
        s.extract()
    for s in soup.find_all('a'):
        del s['id']
        del s['style']
        del s['class']
        del s['title']
        try:
            s['href'] = re.search(r'ipt:f\(.+?\);\"', str(s)).group().split('\'')[1] + '-'
        except:
            del s['href']
    for s in soup.find_all('table'):
        del s['cellpadding']
        del s['cellspacing']
        del s['style']
        del s['class']
    for s in soup.find_all('td'):
        del s['id']
        del s['class']
        del s['style']
    # 正则替换标签
    t = re.sub(r'\s', '', str(soup))
    t = re.sub(r'<a></a>', '', t)
    t = re.sub(r'<div>', '', t)
    t = re.sub(r'</div>', '', t)
    t = re.sub(r'<td></td>', '\t', t)
    t = re.sub(r'<td><a', '\t', t)
    t = re.sub(r'</a></td>', '\n', t)
    t = re.sub(r'<tr>', '', t)
    t = re.sub(r'</tr>', '', t)
    t = re.sub(r'<table>', '', t)
    t = re.sub(r'</table>', '', t)
    t = re.sub(r'<tbody>', '', t)
    t = re.sub(r'</tbody>', '', t)
    t = re.sub(r'href=\"', '', t)
    t = re.sub(r'\"\>', '', t)
    t = re.sub(r'\>', '', t)
    return t


# 下载单位结构
# 参数：单位驻地
def down_structure_all():
    file = open("d:\\济南.txt", "a", encoding='UTF-8')
    for dwzd in Dict:
        file.write(down_structure_one(dwzd))
        print(dwzd + '：已下载完成！')
    file.close()


city = district = category = type = dwbh = dwmc = ''
num = 0
for line in open("d:\\济南.txt", "r", encoding='UTF-8'):
    if line == '\t济南市\n':
        city = '济南市'
        continue
    if line == '\t\t市直\n':
        district = '市直'
        continue
    if line == '\t\t市中区\n':
        district = '市中区'
        continue
    if line == '\t\t历下区\n':
        district = '历下区'
        continue
    if line == '\t\t槐荫区\n':
        district = '槐荫区'
        continue
    if line == '\t\t天桥区\n':
        district = '天桥区'
        continue
    if line == '\t\t历城区\n':
        district = '历城区'
        continue
    if line == '\t\t长清区\n':
        district = '长清区'
        continue
    if line == '\t\t章丘区\n':
        district = '章丘区'
        continue
    if line == '\t\t济阳县\n':
        district = '济阳县'
        continue
    if line == '\t\t商河县\n':
        district = '商河县'
        continue
    if line == '\t\t平阴县\n':
        district = '平阴县'
        continue
    if line == '\t\t\t党委\n':
        category = '党委'
        continue
    if line == '\t\t\t人大\n':
        category = '人大'
        continue
    if line == '\t\t\t政府\n':
        category = '政府'
        continue
    if line == '\t\t\t政协\n':
        category = '政协'
        continue
    if line == '\t\t\t民主党派\n':
        category = '民主党派'
        continue
    if line == '\t\t\t群众团体\n':
        category = '群众团体'
        continue
    if line == '\t\t\t法院\n':
        category = '法院'
        continue
    if line == '\t\t\t检察院\n':
        category = '检察院'
        continue
    if line == '\t\t\t经济实体\n':
        category = '经济实体'
        continue
    if line == '\t\t\t街道办事处\n':
        category = '街道办事处'
        continue
    if line == '\t\t\t乡\n':
        category = '乡'
        continue
    if line == '\t\t\t镇\n':
        category = '镇'
        continue
    if line == '\t\t\t\t行政机关\n':
        type = '行政机关'
        continue
    if line == '\t\t\t\t直属事业单位\n':
        type = '事业单位'
        continue
    if line == '\t\t\t\t\t\t下设机构\n':
        type = '行政机关'
        continue
    if line == '\t\t\t\t\t\t事业单位\n':
        type = '事业单位'
        continue
    if line.count('\t') > num:
        num = line.count('\t')
    else:
        num = 0

    co = line.replace('\t', '').replace('\n', '')
    dwbh = co.split("-")[0]
    dwmc = co.split("-")[1]
    print(city + '-' + district + '-' + category + '-' + type + '-' + dwbh + '-' + dwmc)
