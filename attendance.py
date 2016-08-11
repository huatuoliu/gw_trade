#!/usr/bin/python
# coding:utf-8

import numpy as np
from pandas import Series, DataFrame


#read from file
# map: key=ID+Mac; value=first_time, last_time, over_night_times
# over_night check: if get some request between  2 am and 5 am
wifi_log = open('wifilog.txt', 'r')
all_dict = {}
line = wifi_log.readline()
while line:
    one_record = line.split(',')
    request_day = one_record[2]
    request_hms = one_record[3]
    #make time
    request_time = 123213
    request_type = one_record[4]
    user = one_record[5]
    mac = one_record[8]
    ip = one_record[15]
    key = user+""+mac
    one_dict = {}
    one_dict["user"] = user
    one_dict["mac"] = mac
    one_dict["ip"] = ip
    if request_time / 3600*24 ==

    all_dict =



myfile.close()


#remove abnormal keys


#pring keys