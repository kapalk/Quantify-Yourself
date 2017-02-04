#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 12:47:56 2017

@author: kasperipalkama
"""
# Filters and visualizes hearth rate data
import pandas as pd
from screenONOFF import preprocess_time
import matplotlib.pyplot as plt
import numpy as np

def preprocess_hr(df):
    df['hr'] = pd.rolling_mean(df['hr'],1000)
    return df

def visualize(x,y,xlabel,ylabel):
    plt.figure()
    plt.plot(x,y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

if __name__ == "__main__":
    df = pd.read_csv('/Users/kasperipalkama/Downloads/48223c_MurataBSN'\
                 '_MurataBSN_2017-01-23-21-00-00-2017-01-24-09-00-00.csv')
    df = preprocess_hr(df)
    df = preprocess_time(df)
    visualize(x=df['time'],y=df['hr'],xlabel='daytime',ylabel='bpm')
    
