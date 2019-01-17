#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import City.QingDao as Object

FileName = '青岛'
DownURL = {
    '青岛': 'http://120.221.95.1:1888/'
}
URL = {
    '市直': 'http://120.221.95.1:1888/',
    '市南区': 'http://120.221.95.1:1888/',
    '市北区': 'http://120.221.95.1:1888/',
    '李沧区': 'http://120.221.95.1:1888/',
    '崂山区': 'http://120.221.95.1:1888/',
    '城阳区': 'http://120.221.95.1:1888/',
    '西海岸新区、黄岛区': 'http://120.221.95.1:1888/',
    '即墨区': 'http://120.221.95.1:1888/',
    '胶州市': 'http://120.221.95.1:1888/',
    '平度市': 'http://120.221.95.1:1888/',
    '莱西市': 'http://120.221.95.1:1888/'
}
# Object.down_structure(DownURL, FileName)
Object.down_detail(URL, FileName)
# Object.down_error()
