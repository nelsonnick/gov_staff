#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import City.RiZhao as Object

# var zNodes = []
FileName = '日照'
DownURL = {
    '日照': 'http://www.rzbb.gov.cn/smzxxnew/'
}
URL = {
    '市直': 'http://www.rzbb.gov.cn/smzxxnew/',
    '东港区': 'http://www.rzbb.gov.cn/smzxxnew/',
    '岚山区': 'http://www.rzbb.gov.cn/smzxxnew/',
    '莒县': 'http://www.rzbb.gov.cn/smzxxnew/',
    '五莲县': 'http://www.rzbb.gov.cn/smzxxnew/'
}
# Object.down_structure(DownURL, FileName)
Object.down_detail(URL, FileName)
# Object.down_error()
