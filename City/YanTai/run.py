#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import City.YanTai as Object

# var zNodes = []
FileName = '烟台'
DownURL = {
    '烟台': 'http://smz.yantai.gov.cn/'
}
URL = {
    '市直': 'http://smz.yantai.gov.cn/',
    '开发区': 'http://smz.yantai.gov.cn/',
    '高新区': 'http://smz.yantai.gov.cn/',
    '保税港区': 'http://smz.yantai.gov.cn/',
    '昆嵛山保护区': 'http://smz.yantai.gov.cn/',
    '芝罘区': 'http://smz.yantai.gov.cn/',
    '福山区': 'http://smz.yantai.gov.cn/',
    '莱山区': 'http://smz.yantai.gov.cn/',
    '牟平区': 'http://smz.yantai.gov.cn/',
    '莱州区': 'http://smz.yantai.gov.cn/',
    '龙口区': 'http://smz.yantai.gov.cn/',
    '莱阳市': 'http://smz.yantai.gov.cn/',
    '蓬莱市': 'http://smz.yantai.gov.cn/',
    '招远市': 'http://smz.yantai.gov.cn/',
    '栖霞市': 'http://smz.yantai.gov.cn/',
    '海阳市': 'http://smz.yantai.gov.cn/',
    '长岛县': 'http://smz.yantai.gov.cn/'
}
# Object.down_structure(DownURL, FileName)
Object.down_detail(URL, FileName)
# Object.down_error()
