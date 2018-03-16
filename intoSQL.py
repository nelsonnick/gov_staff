#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import requests
from selenium import webdriver
import re
import urllib.parse
import pymysql

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


def department_get(dwzd):
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


def person_info(dwbh, bzlx, dwzd):
    rt = requests.get(
        "http://" + Dict[dwzd] + "jnbb.gov.cn/smzgs/PersonList.aspx?unitId=" + dwbh + "&BZLX=" + bzlx, timeout=60)
    key = rt.text
    # 定位到具体人员
    if len(re.findall(r'<td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td>', key)) == 0:
        if len(re.findall(r'<td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td>', key)) == 0:
            persons = re.findall(r'<td>.+?</td><td>.+?</td><td>.+?</td>', key)
            for person in persons:
                information = re.findall(r'<td>.+?</td>', person)
                dwmc = information[0][4:len(information[0]) - 5]
                ssbm = ""
                ryxm = information[1][4:len(information[1]) - 5]
                ryxb = information[2][4:len(information[2]) - 5]
                bzqk = bzlx
                db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
                cursor = db.cursor()
                sql = "INSERT INTO person(dwzd, dwbh, dwmc, ssbm, ryxm, ryxb, bzlx, bzqk) \
                                  VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                      (dwzd, dwbh, dwmc, ssbm, ryxm, ryxb, bzlx, bzqk)
                try:
                    cursor.execute(sql)
                    db.commit()
                except:
                    db.rollback()
                db.close()
        else:
            persons = re.findall(r'<td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td>', key)
            for person in persons:
                information = re.findall(r'<td>.+?</td>', person)
                dwmc = information[0][4:len(information[0]) - 5]
                ssbm = ""
                ryxm = information[1][4:len(information[1]) - 5]
                ryxb = information[2][4:len(information[2]) - 5]
                bzqk = information[3][4:len(information[3]) - 5]
                db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
                cursor = db.cursor()
                sql = "INSERT INTO person(dwzd, dwbh, dwmc, ssbm, ryxm, ryxb, bzlx, bzqk) \
                      VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                      (dwzd, dwbh, dwmc, ssbm, ryxm, ryxb, bzlx, bzqk)
                try:
                    cursor.execute(sql)
                    db.commit()
                except:
                    db.rollback()
                db.close()
    else:
        persons = re.findall(r'<td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td>', key)
        for person in persons:
            information = re.findall(r'<td>.+?</td>', person)
            dwmc = information[0][4:len(information[0]) - 5]
            ssbm = information[1][4:len(information[1]) - 5]
            if ssbm == "&nbsp;":
                ssbm = ""
            ryxm = information[2][4:len(information[2]) - 5]
            ryxb = information[3][4:len(information[3]) - 5]
            bzqk = information[4][4:len(information[4]) - 5]
            db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
            cursor = db.cursor()
            sql = "INSERT INTO person(dwzd, dwbh, dwmc, ssbm, ryxm, ryxb, bzlx, bzqk) \
                   VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )" % \
                  (dwzd, dwbh, dwmc, ssbm, ryxm, ryxb, bzlx, bzqk)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()


def down():
    for location in Dict:
        department_get(location)


down()
