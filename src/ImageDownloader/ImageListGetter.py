# -*- coding: utf-8 -*-
"""
Created on Sun May  8 15:56:37 2022

@author: boy10
"""

import os
import glob
import pandas as pd


def getImageList(date):
    '''
    check the files in the image folder
    return the dataFrame with file and datetime. 
    '''

    
    folder = r'.\..\data\image\images_%s' %date
    print(folder)
    files = glob.glob(folder + r'\*.jpg')
    print(files)
    df = pd.DataFrame(columns = ['file', 'time'])
    
    for file in files:
        time = file.split('_')[-1][:-4]
        new_data = {
            'file' : file, 
            'time' : date + ' ' + time[:6], 
            }
        df = df.append(new_data, ignore_index = True)        

    df['datetime'] = pd.to_datetime(df['time'], format = '%Y-%m-%d %H%M%S')
    df.drop(['time'], axis = 1, inplace = True)

    return df

if __name__ == '__main__':
    date = '2022-03-06'
    
    getImageList(date)