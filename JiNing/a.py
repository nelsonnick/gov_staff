#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import URL
import pymysql
import requests
import json


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


update_num()
