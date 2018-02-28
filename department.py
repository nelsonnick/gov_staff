#!/usr/bin/env python3
# encoding:UTF-8

import requests

url = "http://hy.jnbb.gov.cn/smzgs/UnitDetails.aspx?unitId=037001004515"
re = requests.post(url)
print(re.content.decode('UTF-8'))
