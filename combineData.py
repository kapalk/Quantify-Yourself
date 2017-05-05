#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 10:36:58 2017

@author: kasperipalkama
"""
import pandas as pd
from datetime import datetime
import pickle

def combineData(sleepQuality,survey,lightIntensity):
    new_dict = survey
    for key1 in sleepQuality:
        for key2 in survey:
            if key1 == key2:
#                print(key1)
                survey[key1].index = survey[key1].index.map(lambda x:x.date())
                new_dict[key1] = pd.concat([new_dict[key1],lightIntensity],
                        axis=1,join = 'inner')
                new_dict[key1] = pd.concat([new_dict[key1], sleepQuality[key1]],
                        axis = 1, join = 'inner')
    return new_dict

def saveData(data):
    with open('/Users/kasperipalkama/Desktop/combined-data.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def saveDataAsSeparateDataFrames(data):
    for key in data:
        data[key].to_csv('/Users/kasperipalkama/Desktop/lst data/'+key)
        print('done')


if __name__ == '__main__':
    sleepQuality = pd.read_pickle('/Users/kasperipalkama/Desktop/sleep_quality.pickle')
    survey = pd.read_pickle('/Users/kasperipalkama/Desktop/survey.pickle')
    lightIntensity = pd.read_pickle('/Users/kasperipalkama/Desktop/light_intensity.pickle')
    lightIntensity.index = lightIntensity.index.map(lambda x:x.date())
    combinedData = combineData(sleepQuality,survey,lightIntensity)
    saveData(data=combinedData)
    saveDataAsSeparateDataFrames(combinedData)
    