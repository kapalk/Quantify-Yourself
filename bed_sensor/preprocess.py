#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 12:47:56 2017

@author: kasperipalkama
"""


import sys, os

currentDir = os.getcwd()
phone_app_path = currentDir[::-1][10:][::-1] + 'phone_app/'
if phone_app_path not in sys.path:
    sys.path.append(phone_app_path)

import pandas as pd   
from screenONOFF import preprocess_time
from matplotlib import style,pyplot as plt
import numpy as np
from scipy.signal import find_peaks_cwt, medfilt


def preprocess_hr(df):
    df.hr = medfilt(df.hr,299)
#    df.hr = pd.rolling_mean(df.hr,500)
    return df

def preprocess_rr(df):
    df.rr = medfilt(df.rr,299)
    return df

def bedOccupied(df):
    '''
    cuts signal when subject goes to bed and gets up
    '''
    df.status = medfilt(df.status,299)
    occupyedStartIdx = df.status[df.status == 1].index[0]
    occupyedEndIdx = df.status[df.status == 1].index[-1]
    return df.iloc[occupyedStartIdx:occupyedEndIdx+1,:]

def replaceZeros(df):
    '''
    replace zeros with preceeding value
    '''
    df.hr = df.hr.replace(to_replace=0, method='ffill')
    df.rr = df.rr.replace(to_replace=0,method='ffill')
    return df
    
def count_peaks(var,width):
    peak_list = find_peaks_cwt(var, np.arange(1,width))
                               
    return peak_list

def visualize(x,y,legend = '',xlabel='',ylabel='',mark='-',linewidth = 1):
    style.use('ggplot')
    plt.figure(1)
    plt.plot(x,y,mark,linewidth = linewidth,label = legend)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    

if __name__ == "__main__":
    df = pd.read_csv('/Users/kasperipalkama/Downloads/48223c_MurataBSN_'\
                     'MurataBSN_2017-03-19-23-00-00-2017-03-20-08-30-00.csv')
    df = preprocess_time(df)
    
    new_df = df.copy()
    new_df = preprocess_hr(new_df)
    new_df = preprocess_rr(new_df)
    new_df = bedOccupied(new_df)
    new_df = replaceZeros(new_df)
#    hr_peaks = np.array(count_peaks(new_df['hr'],width=3600))
#    rr_peaks = np.array(count_peaks(new_df['rr'],width=3600))
    for var,leg in zip(['hr','rr'],[['hr','hr filtered'],['rr','rr filtered']],):
        visualize(x=df.time,y=df[var],xlabel='daytime',
                  ylabel='1/min',legend=leg[0])
        visualize(x=new_df['time'],y=new_df[var],linewidth=3,legend=leg[1])
#        visualize(x=new_df['time'][peak_list],y= new_df[var][peak_list],mark='o')    
