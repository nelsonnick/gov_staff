#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import requests
import re
from bs4 import BeautifulSoup
from person import get_person
from person import save_person
from person import get_person_err
from person import person_text
from department import get_department_err
from department import department_text
from department import save_department
from department import get_department
from department import down_department_dwbh_json

Dict = {
    '烟台': 'http://smz.yantai.gov.cn/'
        }


def down():
    for dwzd in Dict:
        down_department_dwbh_json(dwzd, Dict[dwzd])
        # file = open("c:\\" + dwzd + ".txt", "r",encoding='UTF-8')
        # line = file.readline()
        # while line:
        #     dwbh = line.split('\t')[0]
        #     dwmc = line.split('\t')[1]
        #     down_department(dwzd, dwbh, dwmc)
        #     line = file.readline()
        # file.close()
