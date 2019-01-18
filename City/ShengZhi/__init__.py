#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import requests
import re
import json
import os
import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver
from Person import get_person
from Person import save_person
from Person import get_person_err
from Person import person_text
from Department import get_department_err
from Department import department_text
from Department import save_department
from Department import get_department

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': '218.56.49.18',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
}


# 转换文本
def change_text(filename):
    before = open("d:\\" + filename + "-before.txt", "r", encoding='UTF-8')
    line = before.readline()
    if line.find('-') > 0:
        after = open("d:\\" + filename + ".txt", "a", encoding='UTF-8')
        while line:
            if line.count('\t') == 1:
                after.write('\t' + line.split('-')[1])
            elif line.count('\t') == 2:
                after.write('\t\t' + line.split('-')[1])
            else:
                # 可能会出现没有-的情况，比如青岛
                if line.count('-') == 0:
                    after.write(line)
                else:
                    if line.split('-')[1] == '党委\n'or line.split('-')[1] == '人大\n' or line.split('-')[1] == '政府\n' or line.split('-')[1] == '政协\n' \
                        or line.split('-')[1] == '民主党派\n' or line.split('-')[1] == '群众团体\n' or line.split('-')[1] == '法院\n' or line.split('-')[1] == '检察院\n' \
                        or line.split('-')[1] == '经济实体\n' or line.split('-')[1] == '其他\n' or line.split('-')[1] == '街道办事处\n' or line.split('-')[1] == '乡\n' \
                        or line.split('-')[1] == '镇\n' or line.split('-')[1] == '行政机关\n' or line.split('-')[1] == '直属事业单位\n' or line.split('-')[1] == '下设机构\n' \
                        or line.split('-')[1] == '事业单位\n':
                        for index in range(line.count('\t')):
                            after.write('\t')
                        after.write(line.split('-')[1])
                    else:
                        after.write(line)
            line = before.readline()
        after.close()
        before.close()
    else:
        before.close()
        os.rename("d:\\" + filename + "-before.txt", "d:\\" + filename + ".txt")


# 获取更新时间
# 参数：所在城市、单位驻地
def get_time(dict_list, dwzd):
    try:
        response = requests.get(dict_list[dwzd], timeout=1000, headers=headers)
    except ConnectionError as e:
        print(e)
    else:
        try:
            time = BeautifulSoup(response.text, "html.parser").find_all(id="SPAN1")[0].get_text()[9:]
        except IndexError as error:
            print(BeautifulSoup(response.text, "html.parser").find_all(id="SPAN1")[0])
            print(error)
    return time


# 获取网址
# 参数：基础网址、单位编号
def get_department_url(base, dwbh):
    return base + "UnitDetails.aspx?unitId=" + dwbh


# 获取网址
# 参数：基础网址、单位编号、编制类型
def get_person_url(base, dwbh, bzlx):
    return base + "PersonList.aspx?unitId=" + dwbh + "&BZLX=" + bzlx


# 下载人员信息
# 参数：基础网址、单位编号、单位名称、编制类型
def down_person_list(base, szcs, dwzd, dwlb, dwlx, sjdw, dwbh, dwmc, bzlx):
    url = get_person_url(base, dwbh, bzlx)
    try:
        rt = requests.get(url, timeout=1000, headers=headers)
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
            save_person(get_person(szcs, dwzd, dwlb, dwlx, sjdw, cols, information, dwbh, bzlx))
        person_text(dwbh + '-' + dwmc + '-' + bzlx + '--->下载完成！')
    elif len(cols) == 4:
        persons = re.findall(r'<td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td>', key)
        for person in persons:
            information = re.findall(r'<td>.+?</td>', person)
            save_person(get_person(szcs, dwzd, dwlb, dwlx, sjdw, cols, information, dwbh, bzlx))
        person_text(dwbh + '-' + dwmc + '-' + bzlx + '--->下载完成！')
    elif len(cols) == 5:
        persons = re.findall(r'<td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td>', key)
        for person in persons:
            information = re.findall(r'<td>.+?</td>', person)
            save_person(get_person(szcs, dwzd, dwlb, dwlx, sjdw, cols, information, dwbh, bzlx))
        person_text(dwbh + '-' + dwmc + '-' + bzlx + '--->下载完成！')
    elif len(cols) == 0:
        person_text(dwbh + '-' + dwmc + '-' + bzlx + '--->无人员信息！')
    else:
        person_text(dwbh + '-' + dwmc + '-' + bzlx + '--->无法识别！')


# 下载单位信息
# 参数：基础网址、所在城市、单位驻地、单位类别、单位类型、上级部门、单位编号、单位名称、更新日期
def down_department_details(base, szcs, dwzd, dwlb, dwlx, sjdw, dwbh, dwmc, time):
    xz_plan_num = xz_real_num = xz_lone_num = sy_plan_num = sy_real_num = sy_lone_num = gq_plan_num = gq_real_num = gq_lone_num = '0'
    url = get_department_url(base, dwbh)
    try:
        response = requests.get(url, timeout=1000, headers=headers)
    except:
        get_department_err(szcs, dwzd, dwlb, dwlx, sjdw, dwbh, dwmc, base, time)
        return
    response.encoding = 'utf-8'
    try:
        soup = BeautifulSoup(response.text, "html.parser").find('div', style="width: 757; height: 582; background-color: #EFF8FF;").table.find_all('tr')[2].td.table
        # soup = BeautifulSoup(response.text, "html.parser").div.table.find_all('tr')[2].td.table
    except AttributeError:
        get_department_err(szcs, dwzd, dwlb, dwlx, sjdw, dwbh, dwmc, base, time)
        return
    else:
        if soup.find_all('tr')[0].find_all('td')[1].span.string is not None:
            dwmc = soup.find_all('tr')[0].find_all('td')[1].span.string.strip()
        elif soup.find_all('tr')[0].find_all('td')[1].span.b.font.string is not None:
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
        if qtmc == "无":
            qtmc = ''
        if soup.find_all('tr')[2].find_all('td')[1].span.string is not None:
            ldzs = soup.find_all('tr')[2].find_all('td')[1].span.string.strip()
        else:
            ldzs = ''
        if soup.find_all('tr')[2].find_all('td')[3].span.string is None:
            jb = ''
        else:
            try:
                soup.find_all('tr')[2].find_all('td')[3].span.b.font.string
            except AttributeError:
                jb = soup.find_all('tr')[2].find_all('td')[3].span.string.strip()
            else:
                if soup.find_all('tr')[2].find_all('td')[3].span.b.font.string is not None:
                    jb = soup.find_all('tr')[2].find_all('td')[3].span.b.font.string.strip()
                else:
                    jb = ''
        if soup.find_all(id="lblNeiSheJG")[0].string is not None:
            nsjg = soup.find_all(id="lblNeiSheJG")[0].string.strip()
        else:
            nsjg = ''
        if nsjg == "\'":
            nsjg = ''
            # 有一行的情况
        if soup.find_all(id="lblMainDuty")[0].string is not None:
            zyzz = soup.find_all(id="lblMainDuty")[0].string.strip()
        else:
            # 获取单位的主要职责：大部分主要职责似乎是延迟加载，正常的方式抓取不到，需要借助浏览器
            # browser = webdriver.Chrome("c:\\chromedriver.exe")
            # browser.get(url)
            # rt = browser.page_source
            # browser.close()
            # zyzz = BeautifulSoup(rt, "html.parser").find_all(id="lblMainDuty")[0].get_text()
            zyzz = ''
        if zyzz == "\'":
            zyzz = ''
        if soup.find_all('tr')[4].td.div.table is not None:
            number = soup.find_all('tr')[4].td.div.table.find_all('tr')
            for num in number:
                if num.find_all('td')[0].string.strip().find("行政编制数") != -1:
                    if num.find_all('td')[1].font is not None:
                        if num.find_all('td')[1].font.string.strip() == "&nbsp;" or num.find_all('td')[1].font.string.strip() == "":
                            xz_plan_num = "0"
                        else:
                            xz_plan_num = num.find_all('td')[1].font.string.strip()
                    else:
                        if num.find_all('td')[1].string.strip() == "&nbsp;" or num.find_all('td')[1].string.strip() == "":
                            xz_plan_num = "0"
                        else:
                            xz_plan_num = num.find_all('td')[1].string.strip()
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
                    if num.find_all('td')[1].font is not None:
                        if num.find_all('td')[1].font.string.strip() == "&nbsp;" or num.find_all('td')[1].font.string.strip() == "":
                            sy_plan_num = "0"
                        else:
                            sy_plan_num = num.find_all('td')[1].font.string.strip()
                    else:
                        if num.find_all('td')[1].string.strip() == "&nbsp;" or num.find_all('td')[1].string.strip() == "":
                            sy_plan_num = "0"
                        else:
                            sy_plan_num = num.find_all('td')[1].string.strip()
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
                    if num.find_all('td')[1].font is not None:
                        if num.find_all('td')[1].font.string.strip() == "&nbsp;" or num.find_all('td')[1].font.string.strip() == "":
                            gq_plan_num = "0"
                        else:
                            gq_plan_num = num.find_all('td')[1].font.string.strip()
                    else:
                        if num.find_all('td')[1].string.strip() == "&nbsp;" or num.find_all('td')[1].string.strip() == "":
                            gq_plan_num = "0"
                        else:
                            gq_plan_num = num.find_all('td')[1].string.strip()
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
                down_person_list(base, szcs, dwzd, dwlb, dwlx, sjdw, dwbh, dwmc, bzlx)
            save_department(
                get_department(szcs, dwzd, dwlb, dwlx, sjdw, dwbh, dwmc, qtmc, ldzs, jb, nsjg, zyzz, xz_plan_num, xz_real_num,
                     xz_lone_num, sy_plan_num, sy_real_num, sy_lone_num, gq_plan_num, gq_real_num, gq_lone_num, url, time))
        else:
            department_text(dwzd + ':' + dwbh + '-' + dwmc + '-' + '--->无编制人员！')


# 下载单位结构文件---根据json字符串解析
# 参数：单位列表、单位驻地、文件名称
# 烟台、日照、省级
def down_structure(dict_list, dwzd):
    browser = webdriver.Chrome("c:\\chromedriver.exe")
    browser.get(dict_list[dwzd] + "TreeViewPage.aspx")
    rt = browser.page_source
    browser.close()
    soup = BeautifulSoup(rt, "html.parser")
    json_data = re.findall(r'var zNodes =.+?;\n', soup.text)[0].replace(',"icon":"image/Department/1.png"', '').replace(',"icon":"image/Department/2.png"', '').replace(',"icon":"image/Department/3.png"', '')\
        .replace(',"icon":"image/Department/4.png"', '').replace(',"icon":"image/Department/5.png"', '').replace(',"icon":"image/Department/6.png"', '') \
        .replace(',"icon":"image/Department/7.png"', '').replace(',"icon":"image/Department/8.png"', '').replace(',"icon":"image/Department/9.png"', '') \
        .replace(',"icon":"image/Department/10.png"', '').replace(',"icon":"image/Department/11.png"', '').replace(',"icon":"image/Department/12.png"', '') \
        .replace(',"icon":"image/Department/13.png"', '').replace(',"icon":"image/Department/14.png"', '').replace(',"icon":"image/Department/15.png"', '') \
        .replace(',"rn":"0"', '').replace(',"rn":"1"', '').replace(',"rn":"2"', '').replace('var zNodes = ', '')[1:-3]
    dict = json.loads(json_data)
    file = open("d:\\" + dwzd + "-before.txt", "a", encoding='utf-8')
    file.write("\t" + dict['id'] + "-" + dict['name'])
    for a in dict['children']:
        file.write("\n\t\t" + a['id'] + "-" + a['name'])
        if 'children' in a:
            for b in a['children']:
                file.write("\n\t\t\t" + b['id'] + "-" + b['name'])
                if 'children' in b:
                    for c in b['children']:
                        file.write("\n\t\t\t\t" + c['id'] + "-" + c['name'])
                        if 'children' in c:
                            for d in c['children']:
                                file.write("\n\t\t\t\t\t" + d['id'] + "-" + d['name'])
                                if 'children' in d:
                                    for e in d['children']:
                                        file.write("\n\t\t\t\t\t\t" + e['id'] + "-" + e['name'])
                                        if 'children' in e:
                                            for f in e['children']:
                                                file.write("\n\t\t\t\t\t\t\t" + f['id'] + "-" + f['name'])
                                                if 'children' in f:
                                                    for g in f['children']:
                                                        file.write("\n\t\t\t\t\t\t\t\t" + g['id'] + "-" + g['name'])
                                                        if 'children' in g:
                                                            for h in g['children']:
                                                                file.write("\n\t\t\t\t\t\t\t\t\t" + h['id'] + "-" + h['name'])
                                                                if 'children' in h:
                                                                    for i in h['children']:
                                                                        file.write("\n\t\t\t\t\t\t\t\t\t\t" + i['id'] + "-" + i['name'])
                                                                        if 'children' in i:
                                                                            for j in i['children']:
                                                                                file.write("\n\t\t\t\t\t\t\t\t\t\t\t" + j['id'] + "-" + j['name'])
    print(dwzd + '：已下载完成！')
    change_text(dwzd)
    file.close()


# 根据结构字符串下载全部数据
# 生成的结构字符串需要修改，前面要整体缩进一个tab
# 省直机关不能用直接这个，需要在“山东省”下面加一级，省直
# 部分地市需要将“XX市市直”改成“市直”：济南、临沂、枣庄
# 部分地市需要加上最顶级：东营
def down_detail(dict_list, filename):
    szcs = dwzd = dwlb = dwlx = sjdw = dwbh = dwmc = time = ''
    tab = 0
    num = 1
    for line in open("d:\\" + filename + ".txt", "r", encoding='UTF-8'):
        if re.search(r'^\t[^\t].+?$\n', line):
            szcs = line.replace('\t', '').replace('\n', '')
            continue
        if re.search(r'^\t\t[^\t].+?$\n', line):
            dwzd = line.replace('\t', '').replace('\n', '')
            time = get_time(dict_list, dwzd)
            continue
        if re.search(r'^\t\t\t[^\t].+?$\n', line) or re.search(r'^\t\t\t[^\t]$\n', line):
            dwlb = line.replace('\t', '').replace('\n', '')
            continue
        if re.search(r'^\t\t\t经济实体$\n', line):
            dwlx = '事业单位'
            tab = line.count('\t')
            continue
        if re.search(r'^\t\t\t\t行政机关$\n', line):
            dwlx = '行政机关'
            tab = line.count('\t')
            continue
        if re.search(r'^\t\t\t\t直属事业单位$\n', line):
            dwlx = '事业单位'
            tab = line.count('\t')
            continue
        if re.search(r'^\t\t\t\t其他单位$\n', line):
            dwlx = '事业单位'
            tab = line.count('\t')
            continue
        if re.search(r'^\t\t\t\t\t\t下设机构$\n', line):
            dwlx = '行政机关'
            tab = line.count('\t')
            continue
        if re.search(r'^\t\t\t\t\t\t事业单位$\n', line):
            dwlx = '事业单位'
            tab = line.count('\t')
            continue
        if re.search(r'^\t\t\t\t\t\t\t下设机构$\n', line):
            dwlx = '行政机关'
            tab = line.count('\t')
            continue
        if re.search(r'^\t\t\t\t\t\t\t事业单位$\n', line):
            dwlx = '事业单位'
            tab = line.count('\t')
            continue
        if re.search(r'^\t\t\t\t\t\t\t\t下设机构$\n', line):
            dwlx = '行政机关'
            tab = line.count('\t')
            continue
        if re.search(r'^\t\t\t\t\t\t\t\t事业单位$\n', line):
            dwlx = '事业单位'
            tab = line.count('\t')
            continue
        if re.search(r'^\t\t\t街道办事处$\n', line):
            dwlx = '行政机关'
            tab = line.count('\t')
            continue
        if line.count('\t') < tab:
            dwlx = '行政机关'
        if (dwlb == '街道办事处' or dwlb == '乡' or dwlb == '镇') and re.search(r'^\t\t\t\t\t[^\t].+?$\n', line):
            dwlx = '事业单位'
        tab = line.count('\t')
        row = line.replace('\t', '').replace('\n', '')
        dwbh = row.split("-")[0]
        dwmc = row.split("-")[1]
        if len(dwbh) > 6:
            sjdw = dwbh[:-3]
        else:
            sjdw = ''
        down_department_details(dict_list[dwzd], szcs, dwzd, dwlb, dwlx, sjdw, dwbh, dwmc, time)
        num = num + 1


# 下载未正常下载的内容
def down_error():
    db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
    cursor = db.cursor()
    try:
        cursor.execute("SELECT szcs,dwzd,dwlb,dwlx,sjdw,dwbh,dwmc,base,time FROM department_err")
        results = cursor.fetchall()
        for row in results:
            szcs = row[0]
            dwzd = row[1]
            dwlb = row[2]
            dwlx = row[3]
            sjdw = row[4]
            dwbh = row[5]
            dwmc = row[6]
            base = row[7]
            time = row[8]
            down_department_details(base, szcs, dwzd, dwlb, dwlx, sjdw, dwbh, dwmc, time)
    except:
        pass
    db.close()
