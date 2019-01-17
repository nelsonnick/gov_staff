#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import City.ShengZhi as Object

# var zNodes = []
FileName = '省直'
URL = {
    '省直': 'http://218.56.49.18/'
}
Object.down_structure(URL, FileName)
# Object.down_detail(URL, FileName)
# Object.down_error()
