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
    '市中区': 'http://sz.jnbb.gov.cn/smzgs/',
    '历下区': 'http://lx.jnbb.gov.cn/smzgs/',
    '槐荫区': 'http://hy.jnbb.gov.cn/smzgs/',
    '天桥区': 'http://tq.jnbb.gov.cn/smzgs/',
    '历城区': 'http://lc.jnbb.gov.cn/smzgs/',
    '长清区': 'http://cq.jnbb.gov.cn/smzgs/',
    '章丘区': 'http://zq.jnbb.gov.cn/smzgs/',
    '济阳区': 'http://jy.jnbb.gov.cn/smzgs/',
    '商河区': 'http://sh.jnbb.gov.cn/smzgs/',
    '平阴区': 'http://py.jnbb.gov.cn/smzgs/'
        }


# 下载人员信息
# 参数：单位驻地、单位编号、单位名称、编制类型
def down_person(dwzd, dwbh, dwmc, bzlx):
    url = Dict[dwzd] + "PersonList.aspx?unitId=" + dwbh + "&BZLX=" + bzlx
    try:
        rt = requests.get(url, timeout=1000)
    except:
        get_person_err(dwbh, dwmc, bzlx, url)
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
            save_person(get_person(cols, information, dwbh, bzlx))
        person_text(dwbh + '-' + dwmc + '-' + bzlx + '--->下载完成！')
    elif len(cols) == 4:
        persons = re.findall(r'<td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td>', key)
        for person in persons:
            information = re.findall(r'<td>.+?</td>', person)
            save_person(get_person(cols, information, dwbh, bzlx))
        person_text(dwbh + '-' + dwmc + '-' + bzlx + '--->下载完成！')
    elif len(cols) == 5:
        persons = re.findall(r'<td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td>', key)
        for person in persons:
            information = re.findall(r'<td>.+?</td>', person)
            save_person(get_person(cols, information, dwbh, bzlx))
        person_text(dwbh + '-' + dwmc + '-' + bzlx + '--->下载完成！')
    elif len(cols) == 0:
        person_text(dwbh + '-' + dwmc + '-' + bzlx + '--->无人员信息！')
    else:
        person_text(dwbh + '-' + dwmc + '-' + bzlx + '--->无法识别！')


# 下载单位信息
# 参数：所在城市、单位驻地、单位类别、单位类型、上级部门、单位编号、单位名称
def down_department(szcs, dwzd, dwlb, dwlx, sjdw, dwbh, dwmc):
    xz_plan_num = xz_real_num = xz_lone_num = sy_plan_num = sy_real_num = sy_lone_num = gq_plan_num = gq_real_num = gq_lone_num = '0'
    url = Dict[dwzd] + "UnitDetails.aspx?unitId=" + dwbh
    time = BeautifulSoup(requests.get(Dict[dwzd]).text, "html.parser").find_all(id="SPAN1")[0].get_text()[9:]
    try:
        rt = requests.get(url, timeout=1000)
    except:
        get_department_err(dwbh, dwmc, url)
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
        # browser = webdriver.Chrome()
        # browser.get(url)
        # rt = browser.page_source
        # browser.close()
        # zyzz = BeautifulSoup(rt, "html.parser").find_all(id="lblMainDuty")[0].get_text()
        zyzz = ''
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
            get_department(szcs, dwzd, dwlb, dwlx, sjdw, dwbh, dwmc, qtmc, ldzs, jb, nsjg, zyzz, xz_plan_num, xz_real_num,
                 xz_lone_num, sy_plan_num, sy_real_num, sy_lone_num, gq_plan_num, gq_real_num, gq_lone_num, url, time))
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
def get_structure_str(dwzd):
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
def down_structure():
    file = open("d:\\济南.txt", "a", encoding='UTF-8')
    for dwzd in Dict:
        file.write(get_structure_str(dwzd))
        print(dwzd + '：已下载完成！')
    file.close()


# 根据结构字符串下载全部数据
# 生成的结构字符串需要修改，主要是济南市市直部门，前面要整体缩进一个tab
# 把“济南市市直”更改成“市直”
def down_by_structure():
    szcs = dwzd = dwlb = dwlx = sjdw = dwbh = dwmc = ''
    tab = 0
    num = 1
    for line in open("d:\\济南.txt", "r", encoding='UTF-8'):
        if re.search(r'^\t[^\t].+?$\n', line):
            szcs = line.replace('\t', '').replace('\n', '')
            continue
        if re.search(r'^\t\t[^\t].+?$\n', line):
            dwzd = line.replace('\t', '').replace('\n', '')
            continue
        if re.search(r'^\t\t\t[^\t].+?$\n', line) or re.search(r'^\t\t\t[^\t]$\n', line):
            dwlb = line.replace('\t', '').replace('\n', '')
            continue
        if re.search(r'^\t\t\t\t行政机关$\n', line):
            dwlx = '行政'
            continue
        if re.search(r'^\t\t\t\t直属事业单位$\n', line):
            dwlx = '事业'
            continue
        if re.search(r'^\t\t\t\t\t\t下设机构$\n', line):
            dwlx = '行政'
            continue
        if re.search(r'^\t\t\t\t\t\t事业单位$\n', line):
            dwlx = '事业'
            continue
        if re.search(r'^\t\t\t街道办事处$\n', line):
            dwlx = '行政'
            continue
        if line.count('\t') < tab:
            dwlx = '行政'
        if (dwlb == '街道办事处' or dwlb == '乡' or dwlb == '镇') and re.search(r'^\t\t\t\t\t[^\t].+?$\n', line):
            dwlx = '事业'
        tab = line.count('\t')
        row = line.replace('\t', '').replace('\n', '')
        dwbh = row.split("-")[0]
        dwmc = row.split("-")[1]
        if len(dwbh) == 18 or len(dwbh) == 15:
            sjdw = dwbh[:-3]
        else:
            sjdw = ''
        down_department(szcs, dwzd, dwlb, dwlx, sjdw, dwbh, dwmc)
        num = num + 1


# down_structure()
down_by_structure()
