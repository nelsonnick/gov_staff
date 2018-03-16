#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from selenium import webdriver
import re
import urllib.parse

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


def get(department_name):
    browser = webdriver.Chrome()
    browser.get("http://" + Dict[department_name] + "jnbb.gov.cn/smzgs/TreeViewPage.aspx")
    t = browser.page_source
    browser.close()
    department_string = re.compile(r"ipt:f\(.+?\);\" title=").findall(t)
    file = open("C:\\" + department_name + ".txt", "a", encoding='utf-8')
    for d in department_string:
        code = d.split('\'')[1]
        name = urllib.parse.unquote(d.split('\'')[3])
        file.write(code + "\t" + name + "\n")
    file.close()
    print(department_name + "已保存")


def get_all():
    for location in Dict:
        get(location)
    print("全部下载完成")


get_all()
