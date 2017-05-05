#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 11:50:19 2017

@author: kasperipalkama
"""

import pandas as pd
import numpy as np
from scipy.signal import medfilt

def filterRRAndComputeSDrr(dict_users):
    for subject in dict_users:
        for nigth in dict_users[subject]:
            nigth.rr = medfilt(nigth.rr,299)
            nigth['sd_rr'] = pd.rolling_std(nigth.rr,299)
    return dict_users

def isClean(df):
    if len(df.rr) == 0:
        return False
    else:
        freqZeros = 1- np.count_nonzero(df.rr) / len(df.rr)
        if freqZeros <= 0.1:
            return True
        else:
            return False

def replaceLastZeros(df):
    df.rr = df.rr.replace(0,np.nan)
    df = df.fillna(method='ffill')
    return df

def delZerosInBeginningAndEnd(df):
    df.rr = df.rr.replace(0,np.nan)
    first_idx = df.rr.first_valid_index()
    last_idx = df.rr.last_valid_index()
    df = df.loc[first_idx:last_idx,:]
    df = df.replace(np.nan,0)
    return df
    
def delCorruptedData(data):
    newDict = dict()
    for subject in data:
        newDict[subject] = list()
        for idx, night in enumerate(data[subject]):
            night = delZerosInBeginningAndEnd(night)
            if isClean(night):
                night = replaceLastZeros(night)
                night.rr = pd.rolling_mean(night.rr,300)
                newDict[subject].append(night)          
    return newDict

            
def visualize(data):
    for subject in data:
        for night in data[subject]:
            night.set_index(night.time, inplace = True)
            night.index.name = 'time'
            night.drop('time',axis = 1, inplace = True)
            ax = night.plot(colormap='jet')
            ax.set_ylabel('Respiration Rate (1/min)')
            ax.legend(loc='best')
        

def rrPreprocess(sleepData, visualize_data = False):
    '''
    prerocessing for rr and recalculation of sd_rr
    '''    
    sleepModData = filterRRAndComputeSDrr(sleepData)
    sleepModData = delCorruptedData(sleepData)
    if visualize_data:
        visualize(sleepModData)
    return sleepModData
