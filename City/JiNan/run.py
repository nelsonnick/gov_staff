#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import City.JiNan as Object

FileName = '济南'
URL = {
    '市直': 'http://jnbb.gov.cn/smzgs/',
    '市中区': 'http://sz.jnbb.gov.cn/smzgs/',
    '历下区': 'http://lx.jnbb.gov.cn/smzgs/',
    '槐荫区': 'http://hy.jnbb.gov.cn/smzgs/',
    '天桥区': 'http://tq.jnbb.gov.cn/smzgs/',
    '历城区': 'http://lc.jnbb.gov.cn/smzgs/',
    '长清区': 'http://cq.jnbb.gov.cn/smzgs/',
    '章丘区': 'http://zq.jnbb.gov.cn/smzgs/',
    '济阳县': 'http://jy.jnbb.gov.cn/smzgs/',
    '商河县': 'http://sh.jnbb.gov.cn/smzgs/',
    '平阴县': 'http://py.jnbb.gov.cn/smzgs/'
}
Object.down_structure(URL, FileName)
# Object.down_detail(URL, FileName)
# Object.down_error()
