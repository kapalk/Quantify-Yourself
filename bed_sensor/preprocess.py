#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 10:30:39 2017

@author: kasperipalkama
"""

import pytz, pickle, pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm


def preprocess_time(df):
    df.time = [datetime.strptime(datetime.fromtimestamp(ts,pytz.timezone\
            ('Europe/Helsinki')).strftime('%Y-%m-%d %H:%M:%S'),
            '%Y-%m-%d %H:%M:%S') for ts in df.time]
    return df

def dropNans(df):
    '''
    delete rows with nan(s)
    '''
    df.dropna(inplace = True,subset = list(df.columns.values))

def dropUnnecessarySurvey(df):
    isBedTime = df.id == 'bedtime'
    isWakeUpTime = df.id == 'wakeuptime'
    boolean = isBedTime | isWakeUpTime
    df = df[boolean]
    df.drop('device', 1, inplace = True)
    df.drop('access_time', 1, inplace = True)
    df.drop('question', 1, inplace = True)
    df.drop('order', 1, inplace = True)
    df.drop('choice_text', 1, inplace = True)
    df.drop('id', 1, inplace = True)
    return df

def dropUnnecessarySensor(df):
    for columnName in df.columns.values:
        if columnName != 'time' and columnName != 'user' and \
        columnName != 'rr' and columnName != 'ss':
            df.drop(columnName, 1, inplace = True)
    return df

def separateUsers(df):
    '''
    divides df into list of dfs
    each list element containt data from one user
    '''
    users = df.user.unique()
    return {user_id: df[df.user == user_id].drop('user',1) for user_id in users}

def getNights(sensor, wakeUpTimes, bedTimes):
    sensor = sensor.reset_index(drop = True)
    listOfNigths = list()
    for bedtime,wakeuptime in zip(bedTimes,wakeUpTimes):
#        print('bedtime:',bedtime,' wakeuptime:',wakeuptime)
#        print('sens first:',sensor.iloc[0,0],' sens last:',sensor.iloc[-1,0])
        try:
            bedTimeIdx = sensor.index[sensor.time.isin([bedtime])][0]
            wakeUpIdx = sensor.index[sensor.time.isin([wakeuptime])][0]
            start = int(bedTimeIdx)
            end = int(wakeUpIdx) + 1
            listOfNigths.append(sensor.iloc[start:end,:].reset_index(drop = True))
            sensor = sensor.drop(sensor.index[:end]).reset_index(drop = True)
        except:
            print('missing sensor  data')
#            print('bedtime:',bedtime,' wakeuptime:',wakeuptime)
#            print('sens first:',sensor.iloc[0,0],' sens last:',sensor.iloc[-1,0])
            pass

    return listOfNigths


def getBedAndWakeUpTimes(sensor,survey):
    startDate = datetime.strptime('2017-03-03', "%Y-%m-%d").date()
    survey = survey[survey.time.map(lambda x: x.date()) != startDate]
    survey.time = survey.time.map(lambda x: (x-timedelta(days=1)))
    dates_survey = survey.time.map(lambda x: x.date())
    dates_sensor = sensor.time.map(lambda x: x.date())
    wakeUpTimes = list()
    bedTimes = list()
    for date1 in tqdm(dates_sensor.unique()):
        first = True
        for date2 in dates_survey:
            if date1 == date2:
                answers = survey.answer[dates_survey == date2]
                answers = answers.reset_index(drop = True)
                if first and len(answers) == 2:
                    wakeuptime = datetime.strptime(str(date1)+' '+answers[1],
                                                         "%Y-%m-%d %H:%M:%S")
                    bedtime = datetime.strptime(str(date1)+' '+answers[0],
                                                      "%Y-%m-%d %H:%M:%S")
                    morning = datetime.strptime('06:00:00',"%H:%M:%S").time()
                    reasonableBedTime = datetime.strptime('20:00:00','%H:%M:%S').time()
                    if bedtime.time() >= morning:
                        bedTimes.append(bedtime)
                    else:
                        bedTimes.append(bedtime+timedelta(days=1))
                    wakeUpTimes.append(wakeuptime+timedelta(days=1))
#                    print(bedTimes[-1])
                    if bedtime.time() >= morning and \
                        bedtime.time() <= reasonableBedTime:
                        bedTimes.pop()
                        wakeUpTimes.pop()
                first = False
    return wakeUpTimes,bedTimes


def separateNights(users_sensor,users_survey):
    users_sensor_nigths = dict()
    for key1 in users_sensor:
        for key2 in users_survey:
            if key1 == key2:
#                print(key1)
                wakeUpTimes,bedTimes = \
                getBedAndWakeUpTimes(users_sensor[key1],users_survey[key1])

                users_sensor_nigths[key1] = \
                getNights(users_sensor[key1],wakeUpTimes,bedTimes)
    return users_sensor_nigths

def saveData(data):
    with open('/Users/kasperipalkama/Desktop/nights_03-MAR-02-APR.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    if True:
        sensor_data = pd.read_csv('/Users/kasperipalkama/Downloads/lst2017_MurataBSN_2017-03-03-12-00-00-2017-04-02-12-00-00.csv')
        survey_data = pd.read_csv('/Users/kasperipalkama/Downloads/lst2017_DailySurveyAnswers_2017-03-03-12-00-00-2017-04-02-12-00-00.csv')
    dropNans(sensor_data)
    sensor_data = preprocess_time(sensor_data)
    sensor_data = dropUnnecessarySensor(sensor_data)
    user_sensor_data = separateUsers(sensor_data)

    survey_data = survey_data.rename(columns = {'submit_time':'time'})
    survey_data = dropUnnecessarySurvey(survey_data)
    dropNans(survey_data)
    survey_data = preprocess_time(survey_data)
    user_survey_data = separateUsers(survey_data)

    user_sensor_nights = separateNights(user_sensor_data, user_survey_data)
    saveData(user_sensor_nights)
