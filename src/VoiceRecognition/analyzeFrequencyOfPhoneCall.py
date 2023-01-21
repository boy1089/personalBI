#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 12:55:55 2022

@author: jiyoung
"""

import os
import glob
import json
import datetime as datetime
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

path = f"/Volumes/T7/auto diary/pythonProject/dataAnalyzed/phoneCall_ambient noise adjust_term 5sec"
files = glob.glob(f"{path}/*.json")

df = pd.DataFrame(columns=['name', 'number', 'datetime'])
names = []
numbers = []
datetimes = []


def parseFilename(filename):
    filename = file.split('/')[-1]

    print(filename.split('_'))
    timestamp = filename.split('_')[-1].split('.')[0]
    number = filename.split('_')[-2]

    name = ''
    if (len(filename.split('_')) == 3):
        name = filename.split('_')[0]

    datetime2 = datetime.datetime.strptime(timestamp, "%Y%m%d%H%M%S")

    return name, number, datetime2


for i, file in enumerate(files):

    try:
        filename = file.split('/')[-1]
        name, number, datetime2 = parseFilename(filename)

        # df = df.append(np.asarray([name, number, datetime2]).T)
        # df = df.merge(np.asarray([name, number, datetime2]))
        # df = df.merge([name, number, datetime2])
        names.append(name)
        numbers.append(number)
        datetimes.append(datetime2)

    except:
        print('pass')
        pass

df = pd.DataFrame([names, numbers, datetimes]).T
df.columns = ['name', 'number', 'datetime']
df['day/month'] = df['datetime'].apply(lambda x: "%d/%d" % (x.day, x.month))
df['date'] = df['datetime'].apply(lambda x: "%s" % (x.date()))
df = df.set_index('datetime')

df2 = df[df['name'] == df['name'][0]]

print(df2['day/month'].value_counts())
print(df2['date'].value_counts())
a = df2['date'].value_counts()
a.index = pd.to_datetime(a.index)
a = a.sort_index()

print(a)
plt.plot(a)

df2 = df[df['name'] == df['name'].value_counts().index[2]]
print(df['name'].value_counts().index[3])
# print(df2['day/month'].value_counts())
# print(df2['date'].value_counts())
a = df2['date'].value_counts()
a.index = pd.to_datetime(a.index)
a = a.sort_index()

print(a)
plt.plot(a)
