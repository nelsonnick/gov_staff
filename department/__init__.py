#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import urllib.parse
from selenium import webdriver
import re
import pymysql


class Department:
    # 单位驻地、单位编号、单位名称、其他名称、领导职数、级别、内设机构、行政编制数、行政实际数、事业编制数、事业实际数、工勤编制数、工勤实际数
    def __init__(self, dwzd, dwbh, dwmc, qtmc, ldzs, jb, nsjg, xz_plan_num, xz_real_num, sy_plan_num, sy_real_num,
                 gq_plan_num, gq_real_num):
        self.dwzd = dwzd
        self.dwbh = dwbh
        self.dwmc = dwmc
        self.qtmc = qtmc
        self.ldzs = ldzs
        self.jb = jb
        self.nsjg = nsjg
        self.xz_plan_num = xz_plan_num
        self.xz_real_num = xz_real_num
        self.sy_plan_num = sy_plan_num
        self.sy_real_num = sy_real_num
        self.gq_plan_num = gq_plan_num
        self.gq_real_num = gq_real_num


def down_department_code(dwzd, url):
    browser = webdriver.Chrome()
    browser.get(url + "TreeViewPage.aspx")
    t = browser.page_source
    browser.close()
    department_string = re.compile(r'ipt:f\(.+?\);\"').findall(t)
    file = open("C:\\" + dwzd + ".txt", "a", encoding='utf-8')
    for d in department_string:
        code = d.split('\'')[1]
        name = urllib.parse.unquote(d.split('\'')[3])
        file.write(code + "\t" + name + "\n")
    file.close()


def save_department(department):
    db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO department(dwzd, dwbh, dwmc, qtmc, ldzs, jb, nsjg, xz_plan_num, xz_real_num, sy_plan_num, sy_real_num, gq_plan_num, gq_real_num) \
              VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
          (department.dwzd, department.dwbh, department.dwmc, department.qtmc, department.ldzs, department.jb,
           department.nsjg, department.xz_plan_num, department.xz_real_num, department.sy_plan_num,
           department.sy_real_num, department.gq_plan_num,
           department.gq_real_num)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print(department.dwzd + ':' + department.dwbh + '-' + department.dwmc + '-' + '--->保存错误！')
        db.rollback()
    db.close()
