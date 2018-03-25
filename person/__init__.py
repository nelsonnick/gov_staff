#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import pymysql


class Person:
    # 单位驻地、单位编号、单位名称、所属部门、人员姓名、人员性别、编制类型、占用编制情况
    def __init__(self, dwzd, dwbh, dwmc, ssbm, ryxm, ryxb, bzlx, bzqk):
        self.dwzd = dwzd
        self.dwbh = dwbh
        self.dwmc = dwmc
        self.ssbm = ssbm
        self.ryxm = ryxm
        self.ryxb = ryxb
        self.bzlx = bzlx
        self.bzqk = bzqk


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


def save_person(person):
    db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO person(dwzd, dwbh, dwmc, ssbm, ryxm, ryxb, bzlx, bzqk) \
                                      VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
          (person.dwzd, person.dwbh, person.dwmc, person.ssbm, person.ryxm, person.ryxb, person.bzlx, person.zybzqk)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print(person.dwzd + ':' + person.dwbh + '-' + person.ryxm + '-' + person.bzlx + '--->保存错误！')
        db.rollback()
    db.close()
