#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 19:55:10 2017

@author: kasperipalkama
"""
import pandas as pd
import pickle
from datetime import datetime,timedelta

def saveData(data):
     with open('/Users/kasperipalkama/Desktop/light_intensity.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
if __name__ == '__main__':
    data = pd.read_csv('/Users/kasperipalkama/Desktop/logfile.csv',
                       header = None,names = ['unit','intensity'],
                       index_col = 0,usecols = [0,1])
    data.index = data.index.map(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
    startDate = datetime.strptime('2017-03-03 00:00:00', "%Y-%m-%d %H:%M:%S")
    endDate = datetime.strptime('2017-04-02 23:59:59', "%Y-%m-%d %H:%M:%S")
    firstlogical = data.index >= startDate
    lastlogical = data.index <= endDate
    boolean = firstlogical & lastlogical
    data = data.loc[boolean]
    data.index = data.index.map(lambda x: x + timedelta(days = 1))
    dailyAverages = data.resample('1D').mean()
    saveData(dailyAverages)
    