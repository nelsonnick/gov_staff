def down_department2(dwbh, dwzd):
    rt = requests.get(Dict[dwzd] + "UnitDetails.aspx?unitId=" + dwbh, timeout=60)
    key = rt.text
    # 去掉全部的空格
    keys = re.compile(r' ').sub('', key)
    # 定位到单位名称
    patternA_1 = re.compile(r'<spanid="lblUnitName"><b><fontsize="3">.+?</font></b></span>')
    if re.search(patternA_1, keys) is None:
        dwmc = ''
    else:
        nameA_2 = re.search(re.compile(r'3">.+?</'), re.search(patternA_1, keys).group(0)).group(0)
        dwmc = nameA_2[3:len(nameA_2) - 2]
    if dwmc == '':
        print('编号：' + dwbh + '-->不存在！')
        return
    # 定位到其它名称
    patternB_1 = re.compile(r'11pt"colspan=\'3\'>.+?<spanclass="STYLE2">领导职数</span>')
    if re.search(patternB_1, keys) is None:
        qtmc = ""
    else:
        nameB_2 = re.search(re.compile(r'3\'>.+?</td>'), re.search(patternB_1, keys).group(0)).group(0)
        qtmc = nameB_2[3:len(nameB_2) - 5].strip()
    # 定位到领导职数
    patternC_1 = re.compile(r'<spanclass="STYLE2">\d*</span>')
    if re.search(patternC_1, keys) is None:
        ldzs = ""
    else:
        nameC_1 = re.search(patternC_1, keys).group(0)
        ldzs = nameC_1[20:len(nameC_1) - 7]
    # 定位到级别
    patternD_1 = re.compile(r'<spanid="lblUnitGuiGe"><b><fontsize="3">.+?</font></b></span>')
    if re.search(patternD_1, keys) is None:
        jb = ""
    else:
        nameD_1 = re.search(patternD_1, keys).group(0)
        # 获取级别
        patternD_2 = re.compile(r'3">.+?</')
        nameD_2 = re.search(patternD_2, nameD_1).group(0)
        jb = nameD_2[3:len(nameD_2) - 2]
    # 定位到内设机构
    patternI_1 = re.compile(r'<spanid="lblNeiSheJG"style="line-height:180%;">.+?</span>')
    if re.search(patternI_1, keys) is None:
        nsjg = ""
    else:
        nameI_1 = re.search(patternI_1, keys).group(0)
        # 获取内设机构
        patternI_2 = re.compile(r';">.+?</')
        nameI_2 = re.search(patternI_2, nameI_1).group(0)
        nsjg = nameI_2[3:len(nameI_2) - 2]
    # 定位到编制数
    xz_bzs = ""
    xz_sjs = ""
    sy_bzs = ""
    sy_sjs = ""
    gq_bzs = ""
    gq_sjs = ""
    nameE = re.findall(r'<tdwidth="18%">.+?</a></td>', keys)
    for name in nameE:
        if name.find("行政编制数") != -1:
            nameF = re.search(re.compile(r'Black">.+?</font></td><t'), name).group(0)
            if nameF[7:len(nameF) - 14] == "&nbsp;":
                xz_bzs = "0"
            else:
                xz_bzs = nameF[7:len(nameF) - 14]
            nameG = re.search(re.compile(r"'>.+?</a></td>"), name).group(0)
            if nameG[2:len(nameG) - 9] == "&nbsp;":
                xz_sjs = "0"
            else:
                xz_sjs = nameG[2:len(nameG) - 9]
        elif name.find("事业编制数") != -1:
            nameF = re.search(re.compile(r'Black">.+?</font></td><t'), name).group(0)
            if nameF[7:len(nameF) - 14] == "&nbsp;":
                sy_bzs = "0"
            else:
                sy_bzs = nameF[7:len(nameF) - 14]
            nameG = re.search(re.compile(r"'>.+?</a></td>"), name).group(0)
            if nameG[2:len(nameG) - 9] == "&nbsp;":
                sy_sjs = "0"
            else:
                sy_sjs = nameG[2:len(nameG) - 9]
        elif name.find("工勤编制数") != -1:
            nameF = re.search(re.compile(r'Black">.+?</font></td><t'), name).group(0)
            if nameF[7:len(nameF) - 14] == "&nbsp;":
                gq_bzs = "0"
            else:
                gq_bzs = nameF[7:len(nameF) - 14]
            nameG = re.search(re.compile(r"'>.+?</a></td>"), name).group(0)
            if nameG[2:len(nameG) - 9] == "&nbsp;":
                gq_sjs = "0"
            else:
                gq_sjs = nameG[2:len(nameG) - 9]
        else:
            pass
        # 定位到编制类型
        patternH = re.compile(r"BZLX=.+?'style='")
        nameH = re.search(patternH, name).group(0)
        bzlx = nameH[5:len(nameH) - 8]
        down_person(dwmc, dwbh, bzlx, dwzd)
    # 定位到编制数
    nameJJ = re.findall(r'<tdwidth="18%">.+?</a>名\)</td>', keys)
    for name in nameJJ:
        if name.find("行政编制数") != -1:
            nameF = re.search(re.compile(r'Black">.+?</font></td><t'), name).group(0)
            if nameF[7:len(nameF) - 14] == "&nbsp;":
                xz_bzs = "0"
            else:
                xz_bzs = nameF[7:len(nameF) - 14]
            print(name)
            nameG = re.search(re.compile(r"'>.+?</a>名\)</td>"), name).group(0)

            if nameG[2:len(nameG) - 9] == "&nbsp;":
                xz_sjs = "0"
            else:
                xz_sjs = nameG[2:len(nameG) - 9]
        elif name.find("事业编制数") != -1:
            nameF = re.search(re.compile(r'Black">.+?</font></td><t'), name).group(0)
            if nameF[7:len(nameF) - 14] == "&nbsp;":
                sy_bzs = "0"
            else:
                sy_bzs = nameF[7:len(nameF) - 14]
            nameG = re.search(re.compile(r"'>.+?</a>名\)</td>"), name).group(0)
            if nameG[2:len(nameG) - 9] == "&nbsp;":
                sy_sjs = "0"
            else:
                sy_sjs = nameG[2:len(nameG) - 9]
        elif name.find("工勤编制数") != -1:
            nameF = re.search(re.compile(r'Black">.+?</font></td><t'), name).group(0)
            if nameF[7:len(nameF) - 14] == "&nbsp;":
                gq_bzs = "0"
            else:
                gq_bzs = nameF[7:len(nameF) - 14]
            nameG = re.search(re.compile(r"'>.+?</a>名\)</td>"), name).group(0)
            if nameG[2:len(nameG) - 9] == "&nbsp;":
                gq_sjs = "0"
            else:
                gq_sjs = nameG[2:len(nameG) - 9]
        else:
            pass
        # 定位到编制类型
        patternO = re.compile(r"BZLX=.+?'style='")
        nameO = re.search(patternO, name).group(0)
        bzlx = nameO[5:len(nameO) - 8]
        down_person(dwmc, dwbh, bzlx, dwzd)
    db = pymysql.connect("localhost", "root", "root", "bz", charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO department(dwzd, dwbh, dwmc, qtmc, ldzs, jb, nsjg, xz_plan_num, xz_real_num, sy_plan_num, sy_real_num, gq_plan_num, gq_real_num) \
              VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
          (dwzd, dwbh, dwmc, qtmc, ldzs, jb, nsjg, xz_bzs, xz_sjs, sy_bzs, sy_sjs, gq_bzs, gq_sjs)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print(xz_sjs)
        db.rollback()
    db.close()
    # print(dwzd + ':' + dwbh + '-' + dwmc + '下载完成！')

