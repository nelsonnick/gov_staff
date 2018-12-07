#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import pymysql


# Person类
# 单位驻地、单位编号、单位名称、所属部门、人员姓名、人员性别、编制类型、占用编制情况
class Person:
    def __init__(self, dwzd, dwbh, dwmc, ssbm, ryxm, ryxb, bzlx, bzqk):
        self.dwzd = dwzd
        self.dwbh = dwbh
        self.dwmc = dwmc
        self.ssbm = ssbm
        self.ryxm = ryxm
        self.ryxb = ryxb
        self.bzlx = bzlx
        self.bzqk = bzqk


# 根据信息生成人员实例
# 参数：当前页面所含列信息、详细信息、单位驻地、单位编号、编制类型
# 返回：人员实例
def get_person(cols, info, dwzd, dwbh, bzlx):
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
        dwmc = info[dw_num][4:len(info[dw_num]) - 5]
    else:
        dwmc = ''
    if xm_num != '':
        ryxm = info[xm_num][4:len(info[xm_num]) - 5]
    else:
        ryxm = ''
    if xb_num != '':
        ryxb = info[xb_num][4:len(info[xb_num]) - 5]
    else:
        ryxb = ''
    if bm_num != '':
        ssbm = info[bm_num][4:len(info[bm_num]) - 5]
    else:
        ssbm = ''
    if zybzqk_num != '':
        zybzqk = info[zybzqk_num][4:len(info[zybzqk_num]) - 5]
    else:
        zybzqk = ''
    return Person(dwzd, dwbh, dwmc, ssbm, ryxm, ryxb, bzlx, zybzqk)


# 保存人员信息到数据库
# 参数：人员实例
def save_person(person):
    db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO person(dwzd, dwbh, dwmc, ssbm, ryxm, ryxb, bzlx, bzqk) \
                                      VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
          (person.dwzd, person.dwbh, person.dwmc, person.ssbm, person.ryxm, person.ryxb, person.bzlx, person.bzqk)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        person_text(person.dwzd + ':' + person.dwbh + '-' + person.ryxm + '-' + person.bzlx + '--->保存错误！')
        db.rollback()
    db.close()


# 保存错误的人员信息到数据库
# 参数：单位驻地、单位编号、单位名称、编制类型、访问网址
def get_person_err(dwzd, dwbh, dwmc, bzlx, url):
    db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO person_err(dwzd, dwbh, dwmc, bzlx, url)VALUES ('%s', '%s', '%s', '%s', '%s')" % (dwzd, dwbh, dwmc, bzlx, url)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        person_text(dwzd + ':' + dwbh + '-' + dwmc + '-' + bzlx + '-' + url + '--->打开人员信息错误！')
        db.rollback()
    db.close()


# 输出人员提示信息
# 参数：提示信息
def person_text(info):
    file = open("C:\\人员提示信息.txt", "a", encoding='utf-8')
    file.write(info + "\n")
    file.close()
    print(info)
