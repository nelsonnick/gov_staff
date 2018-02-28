#!/usr/bin/env python3
# encoding:UTF-8
import os


# 获取领导职数
def get_ldzs(code, location):
    number = 0
    if os.path.exists("C:\\爬虫\\" + location + "\\" + code + ".txt"):
        file = open("C:\\爬虫\\" + location + "\\" + code + ".txt", "r", encoding='utf-8')
        line = file.readline()
        while line:
            if line.find("领导职数") != -1:
                if line.replace("\n", "").split("\t")[1] == "":
                    number = 0
                else:
                    number = int(line.replace("\n", "").split("\t")[1])
                break
            line = file.readline()
        file.close()
    return number


# 获取编制数
def get_bzs(code, location, types):
    number = 0
    if os.path.exists("C:\\爬虫\\" + location + "\\" + code + ".txt"):
        file = open("C:\\爬虫\\" + location + "\\" + code + ".txt", "r", encoding='utf-8')
        line = file.readline()
        while line:
            if line.find("\t" + types + "\t") != -1:
                if line.replace("\n", "").split("\t")[2].split("/")[0] == "":
                    number = 0
                else:
                    number = int(line.replace("\n", "").split("\t")[2].split("/")[0])
                break
            line = file.readline()
        file.close()
    return number


# 获取实际数
def get_sjs(code, location, types):
    number = 0
    if os.path.exists("C:\\爬虫\\" + location + "\\" + code + ".txt"):
        file = open("C:\\爬虫\\" + location + "\\" + code + ".txt", "r", encoding='utf-8')
        line = file.readline()
        while line:
            if line.find("\t" + types + "\t") != -1:
                if line.replace("\n", "").split("\t")[2].split("/")[1] == "":
                    number = 0
                else:
                    number = int(line.replace("\n", "").split("\t")[2].split("/")[1])
                break
            line = file.readline()
        file.close()
    return number


Dict = {'槐荫': 'hy.',
        '历下': 'lx.',
        '历城': 'lc.',
        '商河': 'sh.',
        '天桥': 'tq.',
        '市中': 'sz.',
        '市直': '',
        '平阴': 'py.',
        '济阳': 'jy.',
        '章丘': 'zq.',
        '长清': 'cq.'}


# 获取领导职数-总数
def get_ldzs_total():
    number = 0
    for location in Dict:
        file = open(location + ".txt")
        line = file.readline().replace("\n", "")
        while line:
            number = number + int(get_ldzs(line, location))
            line = file.readline().replace("\n", "")
        file.close()
    return number


# 获取编制总数 types:行政编制/工勤编制/事业编制
def get_bzs_total(types):
    number = 0
    for location in Dict:
        file = open(location + ".txt")
        line = file.readline().replace("\n", "")
        while line:
            number = number + int(get_bzs(line, location, types))
            line = file.readline().replace("\n", "")
        file.close()
    return number


# 获取实际总数 types:行政编制/工勤编制/事业编制
def get_sjs_total(types):
    number = 0
    for location in Dict:
        file = open(location + ".txt")
        line = file.readline().replace("\n", "")
        while line:
            number = number + int(get_sjs(line, location, types))
            line = file.readline().replace("\n", "")
        file.close()
    return number


# 获取编制情况（1空编2超编0满编）
def get_info(code, location, types):
    bzs = get_bzs(code, location, types)
    sjs = get_sjs(code, location, types)
    if bzs > sjs:
        return 1
    elif bzs < sjs:
        return 2
    else:
        return 0


print("领导职数-总数:" + str(get_ldzs_total()))
