#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import requests
import json
import pymysql
import os


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
                        or line.split('-')[1] == '事业单位\n' or line.split('-')[1] == '党委系统\n'or line.split('-')[1] == '人大系统\n' or line.split('-')[1] == '政府系统\n' or line.split('-')[1] == '政协系统\n' \
                        or line.split('-')[1] == '民主党派系统\n' or line.split('-')[1] == '群众团体体统\n' or line.split('-')[1] == '法院系统\n' or line.split('-')[1] == '检察院系统\n' \
                        or line.split('-')[1] == '经济实体系统\n' or line.split('-')[1] == '其他系统\n' or line.split('-')[1] == '街、镇\n' or line.split('-')[1] == '街道\n' \
                        or line.split('-')[1] == '镇政府\n' or line.split('-')[1] == '群众团体体统\n':
                        for index in range(line.count('\t')):
                            after.write('\t')
                        after.write(line.split('-')[1].replace('系统\n', '\n').replace('体统\n', '\n').replace('镇政府\n', '镇\n').replace('街道\n', '街道办事处\n'))
                    else:
                        after.write(line)
            line = before.readline()
        after.close()
        before.close()
    else:
        before.close()
        os.rename("d:\\" + filename + "-before.txt", "d:\\" + filename + ".txt")


# 获取编号
# 参数：前置字符串、序号字符串
def get_id(front_str, id_str):
    if len(str(id_str)) == 1:
        return front_str + "00" + str(id_str)
    elif len(str(id_str)) == 2:
        return front_str + "0" + str(id_str)
    elif len(str(id_str)) == 3:
        return front_str + str(id_str)
    else:
        return front_str + "000"


def get_name(name_str):
    if name_str == '党委' or name_str == '人大' or name_str == '政府' or name_str == '政协' \
            or name_str == '民主党派' or name_str == '群众团体' or name_str == '法院' or name_str == '检察院' \
            or name_str == '经济实体' or name_str == '其他' or name_str == '街道办事处' or name_str == '乡' \
            or name_str == '镇' or name_str == '行政机关' or name_str == '直属事业单位' or name_str == '下设机构' \
            or name_str == '事业单位' or name_str == '党委系统' or name_str == '人大系统' or name_str == '政府系统' \
            or name_str == '政协系统' or name_str == '民主党派系统' or name_str == '群众团体体统' or name_str == '法院系统' \
            or name_str == '检察院系统' or name_str == '经济实体系统' or name_str == '其他系统' or name_str == '街、镇' \
            or name_str == '街道' or name_str == '镇政府' or name_str == '群众团体体统':
        return False
    else:
        return True


# 根据JSON数据解析生成单位结构文件
# 参数：单位列表
# 济宁市需要用到这个，手动修改结构字符串
def down_structure_by_json(dict_list):
    # file = open("d:\\" + filename + "-before.txt", "a", encoding='UTF-8')
    for dwzd in dict_list:
        file = open("d:\\" + dwzd + "-before.txt", "a", encoding='UTF-8')
        url = dict_list[dwzd] + "index.php/Home/Index/get_list.html"
        req = requests.get(url, timeout=1000)
        if req.encoding == 'ISO-8859-1':
            encodings = requests.utils.get_encodings_from_content(req.text)
            if encodings:
                encoding = encodings[0]
            else:
                encoding = req.apparent_encoding
        encode_content = req.content.decode(encoding, 'replace').encode('utf-8', 'replace')
        t = str(encode_content.decode('utf-8')).replace('id', "'code'").replace('pId', "'cid'").replace('name', "'name'").replace("'", '"')
        for j in json.loads(t):
            db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
            cursor = db.cursor()
            p = str(j['cid']) + j['name']
            sql = "INSERT INTO json(code, cid, name) VALUES ('%s', '%s', '%s')" % (j['code'], j['cid'], j['name'])
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
            db.close()
        db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
        cursor = db.cursor()
        cursor.execute("SELECT id, jid, name FROM json WHERE cid =0")
        result = cursor.fetchone()
        print(result)
        cursor.execute("SELECT id, jid, name FROM json WHERE jid =" + result[0])
        file.write('\t1-' + dwzd + '\n')
        for a in cursor.fetchall():
            cursor_a = db.cursor()
            cursor_a.execute("SELECT id, jid, name FROM json WHERE jid =" + a[0])
            file.write('\t\t' + a[0] + '-' + a[2] + '\n')
            for b in cursor_a.fetchall():
                cursor_b = db.cursor()
                cursor_b.execute("SELECT id, jid, name FROM json WHERE jid =" + b[0])
                file.write('\t\t\t' + b[0] + '-' + b[2] + '\n')
                for c in cursor_b.fetchall():
                    cursor_c = db.cursor()
                    cursor_c.execute("SELECT id, jid, name FROM json WHERE jid =" + c[0])
                    file.write('\t\t\t\t' + c[0] + '-' + c[2] + '\n')
                    for d in cursor_c.fetchall():
                        cursor_d = db.cursor()
                        cursor_d.execute("SELECT id, jid, name FROM json WHERE jid =" + d[0])
                        file.write('\t\t\t\t\t' + d[0] + '-' + d[2] + '\n')
                        for e in cursor_d.fetchall():
                            cursor_e = db.cursor()
                            cursor_e.execute("SELECT id, jid, name FROM json WHERE jid =" + e[0])
                            file.write('\t\t\t\t\t\t' + e[0] + '-' + e[2] + '\n')
                            for f in cursor_e.fetchall():
                                cursor_f = db.cursor()
                                cursor_f.execute("SELECT id, jid, name FROM json WHERE jid =" + f[0])
                                file.write('\t\t\t\t\t\t\t' + f[0] + '-' + f[2] + '\n')
                                for g in cursor_f.fetchall():
                                    cursor_g = db.cursor()
                                    cursor_g.execute("SELECT id, jid, name FROM json WHERE jid =" + g[0])
                                    file.write('\t\t\t\t\t\t\t\t' + g[0] + '-' + g[2] + '\n')
                                    for h in cursor_g.fetchall():
                                        cursor_h = db.cursor()
                                        cursor_h.execute("SELECT id, jid, name FROM json WHERE jid =" + h[0])
                                        file.write('\t\t\t\t\t\t\t\t\t' + h[0] + '-' + h[2] + '\n')
                                        for i in cursor_h.fetchall():
                                            file.write('\t\t\t\t\t\t\t\t\t\t' + i[0] + '-' + i[2] + '\n')
        db.close()
        # db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
        # cursors = db.cursor()
        # try:
        #     cursors.execute("DELETE FROM json")
        #     db.commit()
        # except:
        #     db.rollback()
        # db.close()
        file.close()
        print(dwzd + '：已下载完成！')
        change_text(dwzd)


# 导出测试
def aaaa():
    file = open("d:\\济宁-before.txt", "a", encoding='UTF-8')
    db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
    cursor = db.cursor()
    cursor.execute("SELECT id, jid, name FROM json WHERE jid =0")
    result = cursor.fetchone()
    cursor.execute("SELECT id, jid, name FROM json WHERE jid =" + str(result[0]))
    file.write('\t1-市直\n')
    for a in cursor.fetchall():
        cursor_a = db.cursor()
        cursor_a.execute("SELECT id, jid, name FROM json WHERE jid =" + str(a[0]))

        num = get_id("037008000", a[0]) if get_name(a[2]) else ""

        file.write('\t\t' + get_id("037008000", a[0]) + '-' + a[2] + '\n')
        for b in cursor_a.fetchall():
            cursor_b = db.cursor()
            cursor_b.execute("SELECT id, jid, name FROM json WHERE jid =" + str(b[0]))
            file.write('\t\t\t' + get_id("037008000", b[0]) + '-' + b[2] + '\n')
            for c in cursor_b.fetchall():
                cursor_c = db.cursor()
                cursor_c.execute("SELECT id, jid, name FROM json WHERE jid =" + str(c[0]))
                file.write('\t\t\t\t' + get_id("037008000", c[0]) + '-' + c[2] + '\n')
                for d in cursor_c.fetchall():
                    cursor_d = db.cursor()
                    cursor_d.execute("SELECT id, jid, name FROM json WHERE jid =" + str(d[0]))
                    file.write('\t\t\t\t\t' + get_id("037008000", d[0]) + '-' + d[2] + '\n')
                    for e in cursor_d.fetchall():
                        cursor_e = db.cursor()
                        cursor_e.execute("SELECT id, jid, name FROM json WHERE jid =" + str(e[0]))
                        file.write('\t\t\t\t\t\t' + get_id("037008000", e[0]) + '-' + e[2] + '\n')
                        for f in cursor_e.fetchall():
                            cursor_f = db.cursor()
                            cursor_f.execute("SELECT id, jid, name FROM json WHERE jid =" + str(f[0]))
                            file.write('\t\t\t\t\t\t\t' + get_id("037008000", f[0]) + '-' + f[2] + '\n')
                            for g in cursor_f.fetchall():
                                cursor_g = db.cursor()
                                cursor_g.execute("SELECT id, jid, name FROM json WHERE jid =" + str(g[0]))
                                file.write('\t\t\t\t\t\t\t\t' + get_id("037008000", g[0]) + '-' + g[2] + '\n')
                                for h in cursor_g.fetchall():
                                    cursor_h = db.cursor()
                                    cursor_h.execute("SELECT id, jid, name FROM json WHERE jid =" + str(h[0]))
                                    file.write('\t\t\t\t\t\t\t\t\t' + get_id("037008000", h[0]) + '-' + h[2] + '\n')
                                    for i in cursor_h.fetchall():
                                        file.write('\t\t\t\t\t\t\t\t\t\t' + get_id("037008000", i[0]) + '-' + i[2] + '\n')
    db.close()
    # db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
    # cursors = db.cursor()
    # try:
    #     cursors.execute("DELETE FROM json")
    #     db.commit()
    # except:
    #     db.rollback()
    # db.close()
    file.close()
    print('已下载完成！')
    change_text("济宁")


