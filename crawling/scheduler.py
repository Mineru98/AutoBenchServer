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
g_rank = 1
d_rank = 1
r_rank = 1

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

def file_delete(find):
    list = os.listdir(os.getcwd()+"/.tmp")
    
    if find == "cpu":
        for i in list:
            if i.find("cpu.csv") != -1 :
                os.remove(".tmp/" + i)
    elif find == "gpu":
        for i in list:
            if i.find("gpu.csv") != -1 :
                os.remove(".tmp/" + i)
    elif find == "drive":
        for i in list:
            if i.find("drive.csv") != -1 :
                os.remove(".tmp/" + i)
    elif find == "ram":
        for i in list:
            if i.find("ram.csv") != -1 :
                os.remove(".tmp/" + i)

def merge_csv(type):
    CSV_SEPARATOR = ","
    list = []
    if type == "cpu":
        for i in range(1, 5):
            with open(".tmp/"+str(i)+"_cpu.csv", encoding='UTF8') as f:
                reader = csv.reader(f)
                for r, row in enumerate(reader):
                    dict = {}
                    dict['rank'] = int(row[0])
                    dict['model_name'] = row[1]
                    dict['score'] = int(row[2])
                    list.append(dict)
        jsonfile = open('cpu.json', 'w')
        jsonfile.write(json.dumps(list))
    elif type == "gpu":
        for i in range(1, 5):
            with open(".tmp/"+str(i)+"_gpu.csv", encoding='UTF8') as f:
                reader = csv.reader(f)
                for r, row in enumerate(reader):
                    dict = {}
                    dict['rank'] = int(row[0])
                    dict['model_name'] = row[1]
                    dict['score'] = int(row[2])
                    list.append(dict)
        jsonfile = open('gpu.json', 'w')
        jsonfile.write(json.dumps(list))
    elif type == "drive":
        for i in range(1, 5):
            with open(".tmp/"+str(i)+"_drive.csv", encoding='UTF8') as f:
                reader = csv.reader(f)
                for r, row in enumerate(reader):
                    dict = {}
                    dict['rank'] = int(row[0])
                    dict['model_name'] = row[1]
                    dict['score'] = int(row[2])
                    list.append(dict)
        jsonfile = open('disk.json', 'w')
        jsonfile.write(json.dumps(list))
    elif type == "ram":
        for i in range(1, 5):
            with open(".tmp/"+str(i)+"_ram.csv", encoding='UTF8') as f:
                reader = csv.reader(f)
                for r, row in enumerate(reader):
                    dict = {}
                    dict['rank'] = int(row[0])
                    dict['model_name'] = row[1]
                    dict['score'] = int(row[2])
                    list.append(dict)
        jsonfile = open('ram.json', 'w')
        jsonfile.write(json.dumps(list))

def make_csv_new(name):
    str = []
    tmp = []
    test = ""
    global c_rank

    f = open(".tmp/"+name+".csv", 'r', encoding='UTF8')
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

    f = open(".tmp/"+name+".csv", 'w+', encoding='UTF8')
    for i in tmp:
        f.write(i)
        f.write("\n")

    f.close()

def make_csv_new_g(name):
    str = []
    tmp = []
    count = 1
    global g_rank
    
    f = open(".tmp/"+name+".csv", 'r', encoding='UTF8')
    lines = f.readlines()
    for line in lines[:]:
        str.append(line)
    f.close()
    
    for i in str:
        if len(i) > 1:
            i = i.replace(",","").strip()
            if count%3 == 1:
                str_rank = repr(g_rank)
                tmp.append(str_rank + "," + i)
                g_rank+=1
                count+=1
            elif count%3 == 2:
                tmp.append(i[i.find(')') + 2:])
                count+=1
            elif count%3 == 0:
                count+=1

    count = 1

    f = open(".tmp/"+name+".csv", 'w+', encoding='UTF8')
    for i in tmp:
        if count%2 == 0:
            f.write(i)
            f.write("\n")
            count+=1
        else:
            f.write(i + ",")
            count+=1
    f.close()

def make_csv_new_d(name):
    str = []
    tmp = []
    count = 1
    global d_rank
    
    f = open(".tmp/"+name+".csv", 'r', encoding='UTF8')
    lines = f.readlines()
    for line in lines[:]:
        str.append(line)
    f.close()
    
    for i in str:
        if len(i) > 1:
            i = i.replace(",","").strip()
            if count%3 == 1:
                str_rank = repr(d_rank)
                tmp.append(str_rank + "," + i)
                d_rank+=1
                count+=1
            elif count%3 == 2:
                tmp.append(i[i.find(')') + 2:])
                count+=1
            elif count%3 == 0:
                count+=1

    count = 1

    f = open(".tmp/"+name+".csv", 'w+', encoding='UTF8')
    for i in tmp:
        if count%2 == 0:
            f.write(i)
            f.write("\n")
            count+=1
        else:
            f.write(i + ",")
            count+=1
    f.close()

def cpu_crawling():
    if not os.path.exists(".tmp"):
        os.mkdir(".tmp")
    id = 1
    for url in _site.cpu:
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'lxml')
        try:
            data = soup.find("ul",{"class": "chartlist"}).get_text().split("*")
        except AttributeError:
            print("[%s] CPU Crawling Fail. Checking HTML Tag" % (datetime.today().strftime("%Y/%m/%d %H:%M:%S")))
        _file = str(id)+"_cpu"
        f = open(".tmp/"+_file+".csv", 'w+', encoding='UTF8')
        for i in data:
            f.write(i)
        f.close()
        make_csv_new(_file)
        id += 1
    merge_csv("cpu")
    file_delete("cpu")
    os.rmdir(".tmp")
    # mongo["cpu"]
    

def gpu_crawling():
    if not os.path.exists(".tmp"):
        os.mkdir(".tmp")
    id = 1
    for url in _site.gpu:
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'lxml')
        try:
            data = soup.find("ul",{"class": "chartlist"}).get_text().split("*")
        except AttributeError:
            print("[%s] GPU Crawling Fail. Checking HTML Tag" % (datetime.today().strftime("%Y/%m/%d %H:%M:%S")))
        _file = str(id)+"_gpu"
        f = open(".tmp/"+_file+".csv", 'w+', encoding='UTF8')
        for i in data:
            f.write(i)
        f.close()
        make_csv_new_g(_file)
        id += 1
    merge_csv("gpu")
    file_delete("gpu")
    os.rmdir(".tmp")
    # mongo["gpu"]

def drive_crawling():
    if not os.path.exists(".tmp"):
        os.mkdir(".tmp")
    id = 1
    for url in _site.diskdrive:
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'lxml')
        try:
            data = soup.find("ul",{"class": "chartlist"}).get_text().split("*")
        except AttributeError:
            print("[%s] Drive Crawling Fail. Checking HTML Tag" % (datetime.today().strftime("%Y/%m/%d %H:%M:%S")))
        _file = str(id)+"_drive"
        f = open(".tmp/"+_file+".csv", 'w+', encoding='UTF8')
        for i in data:
            f.write(i)
        f.close()
        make_csv_new_d(_file)
        id += 1
    merge_csv("drive")
    file_delete("drive")
    os.rmdir(".tmp")
    # mongo["diskdrive"]

def ram_crawling():
    # mongo["ram"]
    pass
if __name__ == "__main__":
    # schedule.every().day.at("00:00").do(change_days)
    # schedule.every().day.at(cpu_time).do(cpu_crawling)
    # schedule.every().day.at(gpu_time).do(gpu_crawling)
    # schedule.every().day.at(drive_time).do(drive_crawling)
    # schedule.every().day.at(ram_time).do(ram_crawling)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    cpu_crawling()
    gpu_crawling()
    drive_crawling()
    