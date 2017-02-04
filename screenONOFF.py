#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 10:25:15 2017

@author: kasperipalkama
"""
# visualizes phone screen ON/OFF -data
import pandas as pd
import datetime, pytz
import matplotlib.dates as dates
from matplotlib import pyplot as plt
import numpy as np


def preprocess_time(df):
    timestamps = []
    for ts in df['time']:
        timestamp = datetime.datetime.fromtimestamp(ts,pytz.\
                                                    timezone('Europe/Helsinki')).\
                                                   strftime('%Y-%m-%d %H:%M:%S')
        timestamp = datetime.datetime.strptime(timestamp,'%Y-%m-%d %H:%M:%S')
        timestamps.append(timestamp)
    df['time'] = np.array(timestamps)
    return df

def visualize_screen_OnOFF(df,xlabel,ylabel):
    plt.figure()    
    plt.step(df['time'],df['onoff'])
    plt.xlabel('Daytime')
    plt.ylabel('1 = screen ON, 0 = screen OFF')

if __name__ == "__main__":
    data = pd.read_csv('/Users/kasperipalkama/Downloads/28f136_PurpleRobot_'\
                       'PRScreen_2017-01-21-08-00-00-2017-01-22-08-00-00.csv')
    data = preprocess_time(data)
    visualize_screen_OnOFF(df=data,xlabel='Daytime',\
                           ylabel='1 = screen ON, 0 = screen OFF')
    
