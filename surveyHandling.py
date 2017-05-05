#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 18:05:40 2017

@author: kasperipalkama
"""
from bed_sensor.preprocess import preprocess_time, dropNans, separateUsers
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import pickle


def dropUnnecessarySurvey(df):
    isStress = df.id == 'stress'
    isAlcohol = df.id == 'alcohol'
    isSports = df.id == 'sports'
    isScreen = df.id == 'bluelight'
    isWork = df.id == 'work'
    isleepquality = df.id == 'sleepquality'
    boolean = isStress | isAlcohol | isSports | isScreen | isWork | isleepquality
    df = df[boolean]
    df.drop('device', 1, inplace = True)
    df.drop('access_time', 1, inplace = True)
    df.drop('question', 1, inplace = True)
    df.drop('order', 1, inplace = True)
    df.drop('choice_text', 1, inplace = True)
    return df

def reorganizeData(subject_dict):
    new_dict = dict()
    for subject in subject_dict:
        survey = subject_dict[subject] 
        startDate = datetime.strptime('2017-03-03', "%Y-%m-%d").date()        
        survey = survey[survey.time.map(lambda x: x.date()) != startDate]
#        survey.time = survey.time.map(lambda x: (x-timedelta(days=1)))
#        survey.time = survey.time.map(lambda x: x.date())
        newTime = survey.time.unique()
        newColNames = survey.id.unique()
        reorganized = np.reshape(survey.answer,(len(newTime),len(newColNames)))
        reorganized_survey = pd.DataFrame(data = reorganized, index = newTime,
                                          columns = newColNames)
        reorganized_survey.index.name = 'datetime'
        new_dict[subject] = reorganized_survey
    return new_dict

def deleteDoubleAnswers(subject_dict):
    new_dict = subject_dict
    for subject in new_dict:
        for idx,date1 in enumerate(new_dict[subject].index):
            for date2 in new_dict[subject].index:
                if date1.date() == date2.date():
                    timeDelta = date2-date1
#                    print(timeDelta)
                    morning = datetime.strptime('04:00:00', "%H:%M:%S").time()
                    sameday = timeDelta.seconds == 0 and timeDelta.days == 0
                    if sameday == False:
#                        print(date1, date2)
#                        print(new_dict[subject].index)
                        try:
                            if date1.time() <= morning:
                                new_dict[subject].drop(date1,inplace = True)
                            if timeDelta.seconds <= 600:
                                new_dict[subject].drop(date2,inplace = True)
                        except:
                            'skip'
    return new_dict
                
                
            
def saveData(data):
    with open('/Users/kasperipalkama/Desktop/survey.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)  

if __name__ == '__main__':
    survey_data = pd.read_csv('/Users/kasperipalkama/Downloads/'\
                            'lst2017_DailySurveyAnswers_2017-03-03-11-59-'\
                            '58-2017-04-02-11-59-59.csv')
    survey_data = survey_data.rename(columns = {'submit_time':'time'})
#    survey_data = dropUnnecessarySurvey(survey_data)
#    survey_data = preprocess_time(survey_data)
#    subject_survey = separateUsers(survey_data)
#    subject_survey_reorganized = reorganizeData(subject_survey)
#    reorganized_deleted_duplicates = deleteDoubleAnswers(subject_survey_reorganized)
#    saveData(subject_survey_reorganized)
    