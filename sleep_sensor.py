#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 12:47:56 2017

@author: kasperipalkama
"""

import pandas as pd
from screenONOFF import preprocess_time
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks_cwt, medfilt

def preprocess_hr(df):
    df['hr'] = medfilt(df['hr'],299)
    df['hr'] = pd.rolling_mean(df['hr'],100)
    return df

def preprocess_rr(df):
    df['rr'] = medfilt(df['rr'],299)
    return df
    
def count_peaks(var,width):
    peak_list = find_peaks_cwt(var, np.arange(1,width))
                               
    return peak_list

def visualize(x,y,legend = '',xlabel='',ylabel='',mark='-',linewidth = 1):
    plt.figure(1)
    plt.plot(x,y,mark,linewidth = linewidth,label = legend)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    

if __name__ == "__main__":
    df = pd.read_csv('/Users/kasperipalkama/Downloads/48223c_MurataBSN'\
                 '_MurataBSN_2017-02-07-08-00-00-2017-02-09-12-00-00.csv')
    df = preprocess_time(df)
    new_df = df.copy()
    new_df = preprocess_hr(new_df)
    new_df = preprocess_rr(new_df)
#    hr_peaks = np.array(count_peaks(new_df['hr'],width=3600))
#    rr_peaks = np.array(count_peaks(new_df['rr'],width=3600))
    for var,leg,peak_list in zip(
            ['hr','rr'],[['hr','hr filtered'],
             ['rr','rr filtered']],[rr_peaks,hr_peaks]):
        visualize(x=df['time'],y=df[var],xlabel='daytime',
                  ylabel='1/min',legend=leg[0])
        visualize(x=new_df['time'],y=new_df[var],linewidth=3,legend=leg[1])
#        visualize(x=new_df['time'][peak_list],y= new_df[var][peak_list],mark='o')
    