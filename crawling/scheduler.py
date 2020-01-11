# -*- coding:utf-8 -*-
import os
import csv
import json
import time
import schedule
from datetime import datetime

import _site
import requests
from bs4 import BeautifulSoup

import pymongo
mongo = pymongo.MongoClient("mongodb://localhost/autobench")["autobench"]

c_rank = 1
day = None
cpu_time = None
gpu_time = None
drive_time = None
ram_time = None

def change_days():
    day = datetime.now().day
    cpu_time = "00:%s" % (day)
    gpu_time = "00:%s" % (day+10)
    drive_time = "00:%s" % (day+20)
    ram_time = "00:%s" % (day+30)

def make_csv_new(name):
    str = []
    tmp = []
    test = ""
    global c_rank

    f = open("tmp/"+name+".csv", 'r', encoding='UTF8')
    lines = f.readlines()
    for line in lines[1:]:
        str.append(line)
    f.close()

    for i in str:
        i = i.replace(",","").strip()
        if "NA" in i:
            i = i[:i.find("NA")]
            if i[i.find('%') - 2] != '(':#두자리 수
                str_rank = repr(c_rank)
                tmp.append(str_rank + "," + i[:i.index('%') - 3] + "," + i[i.index('%') + 2:])
                c_rank+=1
            elif i[i.find('%') - 2] == '(':#한자리 수
                str_rank = repr(c_rank)
                tmp.append(str_rank + "," + i[:i.index('%') - 2] + "," + i[i.index('%') + 2:])
                c_rank+=1
        elif "$" in i:
            i = i[:i.find('$')]
            if i[i.find('%') - 2] != '(':#두자리 수
                str_rank = repr(c_rank)
                tmp.append(str_rank + "," + i[:i.index('%') - 3] + "," + i[i.index('%') + 2:])
                c_rank+=1
            elif i[i.find('%') - 2] == '(':#한자리 수
                str_rank = repr(c_rank)
                tmp.append(str_rank + "," + i[:i.index('%') - 2] + "," + i[i.index('%') + 2:])
                c_rank+=1

    f = open("tmp/"+name+".csv", 'w+', encoding='UTF8')
    for i in tmp:
        f.write(i)
        f.write("\n")

    f.close()

def cpu_crawling():
    id = 1
    for url in _site.cpu:
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'lxml')
        try:
            data = soup.find("ul",{"class": "chartlist"}).get_text().split("*")
        except AttributeError:
            print("[%s] CPU Crawling Fail. Checking HTML Tag" % (datetime.today().strftime("%Y/%m/%d %H:%M:%S")))
        _file = str(id)+"_cpu"
        f = open("tmp/"+_file+".csv", 'w+', encoding='UTF8')
        for i in data:
            f.write(i)
        f.close()
        make_csv_new(_file)
        id += 1
        '''
        1~4_cpu.csv 통합 코드 작성 해야함
        '''
        csvfile = open("tmp/"+_file+".csv", 'r')
        jsonfile = open(_file+'.json', 'w')

        fieldnames = ("rank","model_name","score")
        reader = csv.DictReader(csvfile, fieldnames)
        out = json.dumps( [ row for row in reader ] )
        jsonfile.write(out)
    # mongo["cpu"]
    
def gpu_crawling():
    # mongo["gpu"]
    pass
def drive_crawling():
    # mongo["diskdrive"]
    pass
def ram_crawling():
    # mongo["ram"]
    pass

schedule.every().day.at("00:00").do(change_days)
schedule.every().day.at(cpu_time).do(cpu_crawling)
schedule.every().day.at(gpu_time).do(gpu_crawling)
schedule.every().day.at(drive_time).do(drive_crawling)
schedule.every().day.at(ram_time).do(ram_crawling)

while True:
    schedule.run_pending()
    time.sleep(1)

# if not os.path.exists("tmp"):
#     os.mkdir("tmp")
# cpu_crawling()