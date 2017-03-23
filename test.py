#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 11:43:18 2017

@author: kasperipalkama
"""

from bs4 import BeautifulSoup
import urllib
import csv
import time
import signal
import sys
import os
from datetime import datetime

def signal_handler(signal, frame):
    global is_interrupted
    is_interrupted = True
    print("Exiting...")

def getHTMLasString(url):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html)
    return str(soup.findAll(text=True)[0])

def preprocess(texts):
    list_of_variables = texts.split(' ', 9)
    timestamp = list_of_variables[0] +" "+ list_of_variables[1]
    timestamp = timestamp.replace(":","")
    timeStampStruct = time.strptime(timestamp, '%Y-%m-%d %H.%M.%S')
    newTimeStamp = datetime(timeStampStruct[0],timeStampStruct[1],
                            timeStampStruct[2],timeStampStruct[3],
                                           timeStampStruct[4],
                                                          timeStampStruct[5])
    time_and_intensity = [newTimeStamp, list_of_variables[8],\
                          list_of_variables[9].replace("\n","")]
    return time_and_intensity

def writeToLog(path,data):
    with open(path, 'a',newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(data)

if __name__ == "__main__":
    is_interrupted = False
    signal.signal(signal.SIGINT, signal_handler)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    while True:
        data = getHTMLasString('http://outside.aalto.fi/current.txt')
        time_and_intensity = preprocess(data)
        writeToLog(dir_path+'/logfile.csv',time_and_intensity)
        if is_interrupted:
            break
        time.sleep(600)
