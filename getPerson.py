#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import requests
from selenium import webdriver
import re
import urllib.parse
import pymysql

# 槐荫区：单位、姓名、性别
# 市中区：单位、部门、姓名、性别
# 历下区：单位、姓名、性别、占用编制情况
# 历城区：单位、姓名、性别
# 天桥区：单位、姓名、性别
# 章丘区：单位、姓名、性别
# 市直：单位、姓名、性别、占用编制情况

Dict = {
    '槐荫': 'hy.',
    '历下': 'lx.',
    '历城': 'lc.',
    '商河': 'sh.',
    '天桥': 'tq.',
    '市中': 'sz.',
    '市直': '',
    '平阴': 'py.',
    '济阳': 'jy.',
    '章丘': 'zq.',
    '长清': 'cq.'
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


def person_info(dwbh, bzlx, dwzd):
    rt = requests.get(
        "http://" + Dict[dwzd] + "jnbb.gov.cn/smzgs/PersonList.aspx?unitId=" + dwbh + "&BZLX=" + bzlx, timeout=60)
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
    elif len(cols) == 4:
        persons = re.findall(r'<td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td>', key)
        for person in persons:
            information = re.findall(r'<td>.+?</td>', person)
            save_person(get_person_info(cols, information), dwzd, dwbh, bzlx)
    elif len(cols) == 5:
        persons = re.findall(r'<td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td>', key)
        for person in persons:
            information = re.findall(r'<td>.+?</td>', person)
            save_person(get_person_info(cols, information), dwzd, dwbh, bzlx)
    else:
        print('出现六列表格，无法识别')


def get_department(dwzd):
    browser = webdriver.Chrome()
    browser.get("http://" + Dict[dwzd] + "jnbb.gov.cn/smzgs/TreeViewPage.aspx")
    t = browser.page_source
    browser.close()
    department_string = re.compile(r"ipt:f\(.+?\);\" title=").findall(t)
    file = open("C:\\" + dwzd + ".txt", "a", encoding='utf-8')
    for d in department_string:
        code = d.split('\'')[1]
        name = urllib.parse.unquote(d.split('\'')[3])
        department_info(code, dwzd)
        file.write(code + "\t" + name + "\n")
    file.close()


def department_info(dwbh, dwzd):
    rt = requests.get("http://" + Dict[dwzd] + "jnbb.gov.cn/smzgs/UnitDetails.aspx?unitId=" + dwbh, timeout=60)
    key = rt.text
    # 去掉全部的空格
    keys = re.compile(r' ').sub('', key)
    # 定位到单位名称
    patternA_1 = re.compile(r'<spanid="lblUnitName"><b><fontsize="3">.+?</font></b></span>')
    nameA_1 = re.search(patternA_1, keys).group(0)
    # 获取单位名称
    patternA_2 = re.compile(r'3">.+?</')
    nameA_2 = re.search(patternA_2, nameA_1).group(0)
    dwmc = nameA_2[3:len(nameA_2) - 2]
    # 定位到其它名称
    patternB_1 = re.compile(r'11pt"colspan=\'3\'>[\s\S]*<spanclass="STYLE2">领导职数</span>')
    if re.search(patternB_1, keys) is None:
        qtmc = ""
    else:
        nameB_1 = re.search(patternB_1, keys).group(0)
        # 获取其它名称
        patternB_2 = re.compile(r'3\'>[\s\S]*</td>')
        nameB_2 = re.search(patternB_2, nameB_1).group(0)
        qtmc = nameB_2[3:len(nameB_2) - 5].strip()
    # 定位到领导职数
    patternC_1 = re.compile(r'<spanclass="STYLE2">\d*</span>')
    if re.search(patternC_1, keys) is None:
        ldzs = ""
    else:
        nameC_1 = re.search(patternC_1, keys).group(0)
        ldzs = nameC_1[20:len(nameC_1) - 7]
    # 定位到级别
    patternD_1 = re.compile(r'<spanid="lblUnitGuiGe"><b><fontsize="3">.+?</font></b></span>')
    if re.search(patternD_1, keys) is None:
        jb = ""
    else:
        nameD_1 = re.search(patternD_1, keys).group(0)
        # 获取级别
        patternD_2 = re.compile(r'3">.+?</')
        nameD_2 = re.search(patternD_2, nameD_1).group(0)
        jb = nameD_2[3:len(nameD_2) - 2]
    # 定位到内设机构
    patternI_1 = re.compile(r'<spanid="lblNeiSheJG"style="line-height:180%;">.+?</span>')
    if re.search(patternI_1, keys) is None:
        nsjg = ""
    else:
        nameI_1 = re.search(patternI_1, keys).group(0)
        # 获取内设机构
        patternI_2 = re.compile(r';">.+?</')
        nameI_2 = re.search(patternI_2, nameI_1).group(0)
        nsjg = nameI_2[3:len(nameI_2) - 2]
    # 定位到编制数
    xz_bzs = ""
    xz_sjs = ""
    sy_bzs = ""
    sy_sjs = ""
    gq_bzs = ""
    gq_sjs = ""
    nameE = re.findall(r'<tdwidth="18%">.+?</a></td>', keys)
    for name in nameE:
        if name.find("行政编制数") != -1:
            nameF = re.search(re.compile(r'Black">.+?</font></td><t'), name).group(0)
            if nameF[7:len(nameF) - 14] == "&nbsp;":
                xz_bzs = "0"
            else:
                xz_bzs = nameF[7:len(nameF) - 14]
            nameG = re.search(re.compile(r"'>.+?</a></td>"), name).group(0)
            if nameG[2:len(nameG) - 9] == "&nbsp;":
                xz_sjs = "0"
            else:
                xz_sjs = nameG[2:len(nameG) - 9]
        elif name.find("事业编制数") != -1:
            nameF = re.search(re.compile(r'Black">.+?</font></td><t'), name).group(0)
            if nameF[7:len(nameF) - 14] == "&nbsp;":
                sy_bzs = "0"
            else:
                sy_bzs = nameF[7:len(nameF) - 14]
            nameG = re.search(re.compile(r"'>.+?</a></td>"), name).group(0)
            if nameG[2:len(nameG) - 9] == "&nbsp;":
                sy_sjs = "0"
            else:
                sy_sjs = nameG[2:len(nameG) - 9]
        elif name.find("工勤编制数") != -1:
            nameF = re.search(re.compile(r'Black">.+?</font></td><t'), name).group(0)
            if nameF[7:len(nameF) - 14] == "&nbsp;":
                gq_bzs = "0"
            else:
                gq_bzs = nameF[7:len(nameF) - 14]
            nameG = re.search(re.compile(r"'>.+?</a></td>"), name).group(0)
            if nameG[2:len(nameG) - 9] == "&nbsp;":
                gq_sjs = "0"
            else:
                gq_sjs = nameG[2:len(nameG) - 9]
        else:
            pass
        # 定位到编制类型
        patternH = re.compile(r"BZLX=.+?'style='")
        nameH = re.search(patternH, name).group(0)
        bzlx = nameH[5:len(nameH) - 8]
        person_info(dwbh, bzlx, dwzd)
    # 定位到编制数
    nameJJ = re.findall(r'<tdwidth="18%">.+?</a>名\)</td>', keys)
    for name in nameJJ:
        if name.find("行政编制数") != -1:
            nameF = re.search(re.compile(r'Black">.+?</font></td><t'), name).group(0)
            if nameF[7:len(nameF) - 14] == "&nbsp;":
                xz_bzs = "0"
            else:
                xz_bzs = nameF[7:len(nameF) - 14]
            nameG = re.search(re.compile(r"'>.+?</a>名\)</td>"), name).group(0)
            if nameG[2:len(nameG) - 9] == "&nbsp;":
                xz_sjs = "0"
            else:
                xz_sjs = nameG[2:len(nameG) - 9]
        elif name.find("事业编制数") != -1:
            nameF = re.search(re.compile(r'Black">.+?</font></td><t'), name).group(0)
            if nameF[7:len(nameF) - 14] == "&nbsp;":
                sy_bzs = "0"
            else:
                sy_bzs = nameF[7:len(nameF) - 14]
            nameG = re.search(re.compile(r"'>.+?</a>名\)</td>"), name).group(0)
            if nameG[2:len(nameG) - 9] == "&nbsp;":
                sy_sjs = "0"
            else:
                sy_sjs = nameG[2:len(nameG) - 9]
        elif name.find("工勤编制数") != -1:
            nameF = re.search(re.compile(r'Black">.+?</font></td><t'), name).group(0)
            if nameF[7:len(nameF) - 14] == "&nbsp;":
                gq_bzs = "0"
            else:
                gq_bzs = nameF[7:len(nameF) - 14]
            nameG = re.search(re.compile(r"'>.+?</a>名\)</td>"), name).group(0)
            if nameG[2:len(nameG) - 9] == "&nbsp;":
                gq_sjs = "0"
            else:
                gq_sjs = nameG[2:len(nameG) - 9]
        else:
            pass
        # 定位到编制类型
        patternO = re.compile(r"BZLX=.+?'style='")
        nameO = re.search(patternO, name).group(0)
        bzlx = nameO[5:len(nameO) - 8]
        person_info(dwbh, bzlx, dwzd)
    db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO department(dwzd, dwbh, dwmc, qtmc, ldzs, jb, nsjg, xz_bzs, xz_sjs, sy_bzs, sy_sjs, gq_bzs, gq_sjs) \
          VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
          (dwzd, dwbh, dwmc, qtmc, ldzs, jb, nsjg, xz_bzs, xz_sjs, sy_bzs, sy_sjs, gq_bzs, gq_sjs)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()
    print(dwzd + ":" + dwbh + "下载完成！")


def down():
    for location in Dict:
        get_department(location)


down()
