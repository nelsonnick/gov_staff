#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import requests
import re
import os
code = "037001004500"
place = "hy"


def down(code, place):
    if not os.path.exists("C:\\爬虫\\" + code + ".txt"):
        file = open("C:\\爬虫\\" + code + ".txt", "w", encoding='utf-8')
        rt = requests.get("http://" + place + ".jnbb.gov.cn/smzgs/UnitDetails.aspx?unitId=" + code)
        key = rt.text
        # 去掉全部的空格
        keys = re.compile(r' ').sub('', key)
        # 定位到单位名称
        patternA_1 = re.compile(r'<spanid="lblUnitName"><b><fontsize="3">.+?</font></b></span>')
        nameA_1 = re.search(patternA_1, keys).group(0)
        # 获取单位名称
        patternA_2 = re.compile(r'3">.+?</')
        nameA_2 = re.search(patternA_2, nameA_1).group(0)
        dwmc = nameA_2[3:len(nameA_2)-2]
        file.write("单位名称" + "\t" + dwmc)
        file.write("\r\n")
        # 定位到其它名称
        patternB_1 = re.compile(r'11pt"colspan=\'3\'>[\s\S]*<spanclass="STYLE2">领导职数</span>')
        if re.search(patternB_1, keys) != "None":
            nameB_1 = re.search(patternB_1, keys).group(0)
            # 获取其它名称
            patternB_2 = re.compile(r'3\'>[\s\S]*</td>')
            nameB_2 = re.search(patternB_2, nameB_1).group(0)
            qtmc = nameB_2[3:len(nameB_2)-5].strip()
        else:
            qtmc = ""
        file.write("其它名称" + "\t" + qtmc)
        file.write("\r\n")
        # 定位到领导职数
        patternC_1 = re.compile(r'<spanclass="STYLE2">\d*</span>')
        if re.search(patternC_1, keys) != "None":
            nameC_1 = re.search(patternC_1, keys).group(0)
            ldzs = nameC_1[20:len(nameC_1)-7]
        else:
            ldzs = ""
        file.write("领导职数" + "\t" + ldzs)
        file.write("\r\n")
        # 定位到级别
        patternD_1 = re.compile(r'<spanid="lblUnitGuiGe"><b><fontsize="3">.+?</font></b></span>')
        if re.search(patternD_1, keys) != "None":
            nameD_1 = re.search(patternD_1, keys).group(0)
            # 获取级别
            patternD_2 = re.compile(r'3">.+?</')
            nameD_2 = re.search(patternD_2, nameD_1).group(0)
            jb = nameD_2[3:len(nameD_2)-2]
        else:
            jb = ""
        file.write("级别" + "\t" + jb)
        file.write("\r\n")
        # 定位到内设机构
        patternI_1 = re.compile(r'<spanid="lblNeiSheJG"style="line-height:180%;">.+?</span>')
        if re.search(patternI_1, keys) == "None":
            nameI_1 = re.search(patternI_1, keys).group(0)
            # 获取内设机构
            patternI_2 = re.compile(r';">.+?</')
            nameI_2 = re.search(patternI_2, nameI_1).group(0)
            nsjg = nameI_2[3:len(nameI_2) - 2]
        else:
            nsjg = ""
        file.write("内设机构" + "\t" + nsjg)
        file.write("\r\n")
        # 定位到编制数
        nameE = re.findall(r'<tdwidth="18%">.+?</a></td>', keys)
        for name in nameE:
            # 定位到编制数
            patternF = re.compile(r'Black">.+?</font></td><t')
            nameF = re.search(patternF, name).group(0)
            bzs = nameF[7:len(nameF)-14]
            # 定位到实际数
            patternG = re.compile(r"'>.+?</a></td>")
            nameG = re.search(patternG, name).group(0)
            sjs = nameG[2:len(nameG) - 9]
            # 定位到编制类型
            patternH = re.compile(r"BZLX=.+?'style='")
            nameH = re.search(patternH, name).group(0)
            bzlx = nameH[5:len(nameH) - 8]
            file.write("编制类型" + "\t" + bzlx + "\t" +bzs +"/"+sjs)
            file.write("\r\n")
            detail(code, bzlx, place)
        file.close()
        print(code + ".txt下载完成！")
    else:
        print(code + ".txt存在，跳过")

def detail(code, bzlx, place):
    if not os.path.exists("C:\\爬虫\\" + code + "_" + bzlx + ".txt"):
        file = open("C:\\爬虫\\" + code + "_" + bzlx + ".txt", "w", encoding='utf-8')
        rt = requests.get("http://" + place + ".jnbb.gov.cn/smzgs/PersonList.aspx?unitId=" + code + "&BZLX=" + bzlx)
        key = rt.text
        # 定位到具体人员
        if len(re.findall(r'<td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td>', key)) == 0:
            persons = re.findall(r'<td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td>', key)
        else:
            persons = re.findall(r'<td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td><td>.+?</td>', key)
        for person in persons:
            information = re.findall(r'<td>.+?</td>', person)
            for info in information:
                file.write(info[4:len(info) - 5] + "\t")
            file.write("\r\n")
        file.close()
    else:
        print(code + "_" + bzlx + ".txt存在，跳过")
# down(code, place)
f = open("槐荫.txt")
line = f.readline()
while line:
    down(line.replace("\n", ""), place)
    line = f.readline()
f.close()
