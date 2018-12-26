#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import URL
import pymysql
import requests
import json
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


# 保存到数据库
# 参数：url字符串
def save_sql(url_str):
    url = url_str + "index.php/Home/Index/get_list.html"
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
        sql = "INSERT INTO json(code, cid, name) VALUES ('%s', '%s', '%s')" % (j['code'], j['cid'], j['name'])
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        db.close()


# 更新jid字段
def update_jid():
    db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
    a_cursor = db.cursor()
    a_cursor.execute("SELECT id,jid,code,cid,name FROM json WHERE cid =0")
    for a in a_cursor.fetchall():
        a_update = db.cursor()
        a_update.execute("UPDATE json SET jid = '0' WHERE cid ='0'")
        db.commit()
        a_select = db.cursor()
        a_select.execute("SELECT id,jid,code,cid,name FROM json WHERE cid =" + a[2])
        for b in a_select.fetchall():
            b_update = db.cursor()
            b_update.execute("UPDATE json SET jid = '" + str(a[0]) + "' WHERE code ='" + b[2] + "'")
            db.commit()
            b_select = db.cursor()
            b_select.execute("SELECT id,jid,code,cid,name FROM json WHERE cid =" + b[2])
            for c in b_select.fetchall():
                c_update = db.cursor()
                c_update.execute("UPDATE json SET jid = '" + str(b[0]) + "' WHERE code ='" + c[2] + "'")
                db.commit()
                c_select = db.cursor()
                c_select.execute("SELECT id,jid,code,cid,name FROM json WHERE cid =" + c[2])
                for d in c_select.fetchall():
                    d_update = db.cursor()
                    d_update.execute("UPDATE json SET jid = '" + str(c[0]) + "' WHERE code ='" + d[2] + "'")
                    db.commit()
                    d_select = db.cursor()
                    d_select.execute("SELECT id,jid,code,cid,name FROM json WHERE cid =" + d[2])
                    for e in d_select.fetchall():
                        e_update = db.cursor()
                        e_update.execute("UPDATE json SET jid = '" + str(d[0]) + "' WHERE code ='" + e[2] + "'")
                        db.commit()
                        e_select = db.cursor()
                        e_select.execute("SELECT id,jid,code,cid,name FROM json WHERE cid =" + e[2])
                        for f in e_select.fetchall():
                            f_update = db.cursor()
                            f_update.execute("UPDATE json SET jid = '" + str(e[0]) + "' WHERE code ='" + f[2] + "'")
                            db.commit()
                            f_select = db.cursor()
                            f_select.execute("SELECT id,jid,code,cid,name FROM json WHERE cid =" + f[2])
                            for g in f_select.fetchall():
                                g_update = db.cursor()
                                g_update.execute("UPDATE json SET jid = '" + str(f[0]) + "' WHERE code ='" + g[2] + "'")
                                db.commit()
                                g_select = db.cursor()
                                g_select.execute("SELECT id,jid,code,cid,name FROM json WHERE cid =" + g[2])
                                for h in g_select.fetchall():
                                    h_update = db.cursor()
                                    h_update.execute("UPDATE json SET jid = '" + str(g[0]) + "' WHERE code ='" + h[2] + "'")
                                    db.commit()
                                    h_select = db.cursor()
                                    h_select.execute("SELECT id,jid,code,cid,name FROM json WHERE cid =" + h[2])
                                    for i in h_select.fetchall():
                                        i_update = db.cursor()
                                        i_update.execute("UPDATE json SET jid = '" + str(h[0]) + "' WHERE code ='" + i[2] + "'")
                                        db.commit()
    db.close()


# 更新序号
def update_num():
    db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
    cursor = db.cursor()
    cursor.execute("SELECT id,name FROM json")
    n = 0
    for row in cursor.fetchall():
        if row[1] == '党委' or row[1] == '人大' or row[1] == '政府' or row[1] == '政协' \
            or row[1] == '民主党派' or row[1] == '群众团体' or row[1] == '法院' or row[1] == '检察院' \
            or row[1] == '经济实体' or row[1] == '其他' or row[1] == '街道办事处' or row[1] == '乡' \
            or row[1] == '镇' or row[1] == '行政机关' or row[1] == '直属事业单位' or row[1] == '下设机构' \
            or row[1] == '事业单位' or row[1] == '党委系统' or row[1] == '人大系统' or row[1] == '政府系统' \
            or row[1] == '政协系统' or row[1] == '民主党派系统' or row[1] == '群众团体体统' or row[1] == '法院系统' \
            or row[1] == '检察院系统' or row[1] == '经济实体系统' or row[1] == '其他系统' or row[1] == '街、镇' \
            or row[1] == '街道' or row[1] == '镇政府' or row[1] == '群众团体体统':
            num = 0
        else:
            num = n
            n = n + 1
        up = db.cursor()
        try:
            up.execute("UPDATE json SET num = %s WHERE id = %s" % (num, row[0]))
            db.commit()
        except:
            db.rollback()
    db.close()


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


# 更新单位编号
def update_dwbh(front_str):
    db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
    cursor = db.cursor()
    cursor.execute("SELECT id,jid,code,cid,name,num FROM json")
    for row in cursor.fetchall():
        if row[5] != 0:
            up = db.cursor()
            up.execute("SELECT id,jid,code,cid,name,num,dwbh FROM json WHERE id = %s" % (row[1]))
            result = up.fetchone()
            # 有上级部门
            if result[5] != 0:
                this_dwbh = get_id(result[6], row[5])
                print(this_dwbh)
            # 无上级部门
            else:
                this_dwbh = get_id(front_str, row[5])
                print(this_dwbh)
        else:
            pass


# 导出文本
def export(dwzd):
    file = open("d:\\" + dwzd + "-before.txt", "a", encoding='UTF-8')
    db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
    cursor = db.cursor()
    cursor.execute("SELECT id, jid, name FROM json WHERE cid =0")
    result = cursor.fetchone()
    cursor.execute("SELECT id, jid, name FROM json WHERE jid  = %s" % (result[0]))
    file.write('\t1-' + dwzd + '\n')
    for a in cursor.fetchall():
        cursor_a = db.cursor()
        cursor_a.execute("SELECT id, jid, name FROM json WHERE jid = %s" % (a[0]))
        file.write('\t\t%s-%s\n' % (a[0], a[2]))
        for b in cursor_a.fetchall():
            cursor_b = db.cursor()
            cursor_b.execute("SELECT id, jid, name FROM json WHERE jid = %s" % (b[0]))
            file.write('\t\t\t%s-%s\n' % (b[0], b[2]))
            for c in cursor_b.fetchall():
                cursor_c = db.cursor()
                cursor_c.execute("SELECT id, jid, name FROM json WHERE jid = %s" % (c[0]))
                file.write('\t\t\t\t%s-%s\n' % (c[0], c[2]))
                for d in cursor_c.fetchall():
                    cursor_d = db.cursor()
                    cursor_d.execute("SELECT id, jid, name FROM json WHERE jid = %s" % (d[0]))
                    file.write('\t\t\t\t\t%s-%s\n' % (d[0], d[2]))
                    for e in cursor_d.fetchall():
                        cursor_e = db.cursor()
                        cursor_e.execute("SELECT id, jid, name FROM json WHERE jid = %s" % (e[0]))
                        file.write('\t\t\t\t\t\t%s-%s\n' % (e[0], e[2]))
                        for f in cursor_e.fetchall():
                            cursor_f = db.cursor()
                            cursor_f.execute("SELECT id, jid, name FROM json WHERE jid = %s" % (f[0]))
                            file.write('\t\t\t\t\t\t\t%s-%s\n' % (f[0], f[2]))
                            for g in cursor_f.fetchall():
                                cursor_g = db.cursor()
                                cursor_g.execute("SELECT id, jid, name FROM json WHERE jid = %s" % (g[0]))
                                file.write('\t\t\t\t\t\t\t\t%s-%s\n' % (g[0], g[2]))
                                for h in cursor_g.fetchall():
                                    cursor_h = db.cursor()
                                    cursor_h.execute("SELECT id, jid, name FROM json WHERE jid = %s" % (h[0]))
                                    file.write('\t\t\t\t\t\t\t\t\t%s-%s\n' % (h[0], h[2]))
                                    for i in cursor_h.fetchall():
                                        file.write('\t\t\t\t\t\t\t\t\t\t%s-%s\n' % (i[0], i[2]))
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


update_dwbh('037008000')
