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
        t = str(encode_content.decode('utf-8')).replace('id', "'id'").replace('pId', "'pid'").replace('name', "'name'").replace("'", '"')
        for j in json.loads(t):
            db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
            cursor = db.cursor()
            sql = "INSERT INTO json(id, pid, name) VALUES ('%s', '%s', '%s')" % (j['id'], j['pid'], j['name'])
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
            db.close()
        db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
        cursor = db.cursor()
        cursor.execute("SELECT id,pid,name FROM json WHERE pid =0")
        result = cursor.fetchone()
        cursor.execute("SELECT id,pid,name FROM json WHERE pid =" + result[0])
        file.write('\t1-' + dwzd + '\n')
        for a in cursor.fetchall():
            cursor_a = db.cursor()
            cursor_a.execute("SELECT id,pid,name FROM json WHERE pid =" + a[0])
            file.write('\t\t' + a[0] + '-' + a[2] + '\n')
            for b in cursor_a.fetchall():
                cursor_b = db.cursor()
                cursor_b.execute("SELECT id,pid,name FROM json WHERE pid =" + b[0])
                file.write('\t\t\t' + b[0] + '-' + b[2] + '\n')
                for c in cursor_b.fetchall():
                    cursor_c = db.cursor()
                    cursor_c.execute("SELECT id,pid,name FROM json WHERE pid =" + c[0])
                    file.write('\t\t\t\t' + c[0] + '-' + c[2] + '\n')
                    for d in cursor_c.fetchall():
                        cursor_d = db.cursor()
                        cursor_d.execute("SELECT id,pid,name FROM json WHERE pid =" + d[0])
                        file.write('\t\t\t\t\t' + d[0] + '-' + d[2] + '\n')
                        for e in cursor_d.fetchall():
                            cursor_e = db.cursor()
                            cursor_e.execute("SELECT id,pid,name FROM json WHERE pid =" + e[0])
                            file.write('\t\t\t\t\t\t' + e[0] + '-' + e[2] + '\n')
                            for f in cursor_e.fetchall():
                                cursor_f = db.cursor()
                                cursor_f.execute("SELECT id,pid,name FROM json WHERE pid =" + f[0])
                                file.write('\t\t\t\t\t\t\t' + f[0] + '-' + f[2] + '\n')
                                for g in cursor_f.fetchall():
                                    file.write('\t\t\t\t\t\t\t' + g[0] + '-' + g[2] + '\n')
        db.close()
        db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
        cursors = db.cursor()
        try:
            cursors.execute("DELETE FROM json WHERE 1=1")
            db.commit()
        except:
            db.rollback()
        db.close()
        file.close()
        print(dwzd + '：已下载完成！')
    change_text(dwzd)
