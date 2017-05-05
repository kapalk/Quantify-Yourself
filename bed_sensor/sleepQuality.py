#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 11:50:19 2017

@author: kasperipalkama
"""
from rrPreprocess import rrPreprocess
from detect_peaks import detect_peaks
from matplotlib import style, pyplot as plt
style.use('ggplot')
import pandas as pd
import numpy as np
import pickle
from datetime import datetime

def getData(path):
    return pd.read_pickle(path)


def findPeaks(data):
    for subject in data:
        for night in data[subject]:
            threshold = np.mean(night.sd_rr) + np.std(night.sd_rr)
            night.reset_index(drop = True,inplace = True)
            peakIdxs = detect_peaks(night.sd_rr,mph=threshold)
            night['sd_rr_peaks'] = night.sd_rr.loc[peakIdxs]
    return data

def getNightLength(nigth):
    length = nigth.time.iget(-1) - nigth.time.iget(0)
    return length.total_seconds()/ (60*60)

def getPeakCount(data,dictToAppend):
    for subject in data:
        peakCounts = list()
        newTime = list()
        if subject not in dictToAppend.keys():
            dictToAppend[subject] = pd.Series()
        for night in data[subject]:
            nightlength = getNightLength(night)
            night = night.reset_index(drop = True)
            newTime.append(night.time.iget(-1).date())
            peakCounts.append(len(night.sd_rr_peaks.dropna())/nightlength)
        dictToAppend[subject] = dictToAppend[subject].append(
                pd.Series(data = peakCounts, index = newTime))
        dictToAppend[subject].name = 'peak_count'
    return dictToAppend
            
def visualize(data):
    for subject in data:
        for night in data[subject]:
            night.set_index(night.time, inplace = True)
            night.index.name = 'time'
            night.drop('time',axis = 1, inplace = True)
            plt.figure()
            plt.plot(night.index,night.sd_rr)
            plt.plot(night.index,night.sd_rr_peaks,'bo')

def saveData(data):
    with open('/Users/kasperipalkama/Desktop/sleep_quality.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    path1 = '/Users/kasperipalkama/Desktop/nights_3-MAR-13-MAR.pickle'
    path2 = '/Users/kasperipalkama/Desktop/nights_13-MAR-23-MAR.pickle'
    path3 = '/Users/kasperipalkama/Desktop/nights_23-MAR-02-APR.pickle'
    for path in [path1, path2, path3]:
        sleepData = getData(path)
        sleepData = rrPreprocess(sleepData=sleepData,visualize_data=False)
        sleepData = findPeaks(sleepData)
        if path == path1:
            peakCounts = dict()
        peakCounts = getPeakCount(sleepData,peakCounts)
    saveData(peakCounts)
#    visualize(sleepData)

    
    