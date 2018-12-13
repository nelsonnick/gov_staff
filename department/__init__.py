#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import urllib.parse
from selenium import webdriver
import re
import pymysql


# Department类
# 参数：所在城市、单位驻地、单位类别、单位类型、上级单位、单位编号、单位名称、其他名称、领导职数、级别、内设机构、主要职责、
# 行政编制数、行政实际数、行政单列数、事业编制数、事业实际数、事业单列数、工勤编制数、工勤实际数、工勤单列数、访问网址、更新日期
class Department:
    def __init__(self, szcs, dwzd, dwlb, dwlx, sjdw, dwbh, dwmc, qtmc, ldzs, jb, nsjg, zyzz, xz_plan_num, xz_real_num,
                 xz_lone_num, sy_plan_num, sy_real_num, sy_lone_num, gq_plan_num, gq_real_num, gq_lone_num, url, time):
        self.szcs = szcs
        self.dwzd = dwzd
        self.dwlb = dwlb
        self.dwlx = dwlx
        self.sjdw = sjdw
        self.dwbh = dwbh
        self.dwmc = dwmc
        self.qtmc = qtmc
        self.ldzs = ldzs
        self.jb = jb
        self.nsjg = nsjg
        self.zyzz = zyzz
        self.xz_plan_num = xz_plan_num
        self.xz_real_num = xz_real_num
        self.xz_lone_num = xz_lone_num
        self.sy_plan_num = sy_plan_num
        self.sy_real_num = sy_real_num
        self.sy_lone_num = sy_lone_num
        self.gq_plan_num = gq_plan_num
        self.gq_real_num = gq_real_num
        self.gq_lone_num = gq_lone_num
        self.url = url
        self.time = time


# 下载单位信息
# 参数：单位驻地、访问网址
def down_department_dwbh(dwzd, url):
    browser = webdriver.Chrome()
    browser.get(url + "TreeViewPage.aspx")
    t = browser.page_source
    browser.close()
    department_string = re.compile(r'ipt:f\(.+?\);\"').findall(t)
    file = open("C:\\" + dwzd + ".txt", "a", encoding='utf-8')
    for d in department_string:
        dwbh = d.split('\'')[1]
        dwmc = urllib.parse.unquote(d.split('\'')[3])
        file.write(dwbh + "\t" + dwmc + "\n")
    file.close()


# 下载单位信息
# 参数：单位驻地、访问网址
def down_department_dwbh_json(dwzd, url):
    browser = webdriver.Chrome()
    browser.get(url + "TreeViewPage.aspx")
    t = browser.page_source
    browser.close()
    department_string = re.compile(r'\"name\":\".+?\",\"id\":\"\d{0,}\"').findall(t)
    file = open("C:\\" + dwzd + ".txt", "a", encoding='utf-8')
    for d in department_string:
        dwbh = d.split('\"')[7]
        dwmc = urllib.parse.unquote(d.split('\"')[3])
        file.write(dwbh + "\t" + dwmc + "\n")
    file.close()


# 根据信息生成单位实例
# 参数：所在城市、单位驻地、单位类别、单位类型、上级单位、单位编号、单位名称、其他名称、领导职数、级别、内设机构、主要职责、
# 行政编制数、行政实际数、行政单列数、事业编制数、事业实际数、事业单列数、工勤编制数、工勤实际数、工勤单列数、访问网址、更新日期
# 返回：单位实例
def get_department(szcs, dwzd, dwlb, dwlx, sjdw, dwbh, dwmc, qtmc, ldzs, jb, nsjg, zyzz, xz_plan_num, xz_real_num,
                 xz_lone_num, sy_plan_num, sy_real_num, sy_lone_num, gq_plan_num, gq_real_num, gq_lone_num, url, time):
    return Department(szcs, dwzd, dwlb, dwlx, sjdw, dwbh, dwmc, qtmc, ldzs, jb, nsjg, zyzz, xz_plan_num, xz_real_num,
                 xz_lone_num, sy_plan_num, sy_real_num, sy_lone_num, gq_plan_num, gq_real_num, gq_lone_num, url, time)


# 保存单位信息到数据库
# 参数：单位实例
def save_department(department):
    db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO department(szcs, dwzd, dwlb, dwlx, sjdw, dwbh, dwmc, qtmc, ldzs, jb, nsjg,zyzz, xz_plan_num, xz_real_num, xz_lone_num," \
          " sy_plan_num, sy_real_num, sy_lone_num, gq_plan_num, gq_real_num, gq_lone_num, url, time) \
              VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
          (department.szcs, department.dwzd, department.dwlb, department.dwlx, department.sjdw, department.dwbh,
           department.dwmc, department.qtmc, department.ldzs, department.jb, department.nsjg, department.zyzz,
           department.xz_plan_num, department.xz_real_num, department.xz_lone_num, department.sy_plan_num,
           department.sy_real_num, department.sy_lone_num, department.gq_plan_num, department.gq_real_num,
           department.gq_lone_num, department.url, department.time)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        department_text(department.dwzd + ':' + department.dwbh + '-' + department.dwmc + '-' + '--->保存错误！')
        db.rollback()
    db.close()


# 保存错误的单位信息到数据库
# 参数：单位编号、单位名称、访问网址
def get_department_err(dwbh, dwmc, url):
    db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO department_err(dwbh, dwmc, url)VALUES ('%s', '%s', '%s')" % (dwbh, dwmc, url)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        department_text(dwbh + '-' + dwmc + '-' + url + '--->打开单位信息错误！')
        db.rollback()
    db.close()


# 输出单位提示信息
# 参数：提示信息
def department_text(info):
    file = open("D:\\单位提示信息.txt", "a", encoding='utf-8')
    file.write(info + "\n")
    file.close()
    print(info)
