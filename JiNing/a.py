#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import pymysql


# 更新jid字段
def dd():
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
