# -*- coding: utf-8 -*-
"""
Created on Tue May 10 00:53:00 2022

@author: boy10
"""


import pandas as pd
import os
import zipfile
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
 
path = r"D:\python\7. logger2\logger\data\log\2022-05-09_20-25-23.zip"

def defineSensorList():
    sensorList = ['Accelerometer', 
                  # 'Annotation', 
                  'Gravity', 
                  # 'Gyroscope', 
                  'Light', 
                  'Location', 
                  # 'Metadata', 
                   'Microphone', 
                  # 'Orientation', 
                  ]
    return sensorList


def readData(file) : 
        
    zf = zipfile.ZipFile(file)
    dataDic = {}
    
    for i, sensor in enumerate(defineSensorList()):
        try : 
            df = pd.read_csv(zf.open(sensor + '.csv'))
            dataDic[sensor] = df
        except :
            print('%s th file passed in readData' %i)
            pass
        
    return dataDic

def convertLocationToAddress(latitude, longitude):
    geoLoc = Nominatim(user_agent="GetLoc")
    locname = geoLoc.reverse("%s, %s" %(latitude, longitude))
    return locname.address.split(',')[0]

def convertLocationInDataframe(df):
    
    for i in len(df):
        df['address'].loc[i] = convertLocationToAddress(df['latitude'][i], df['longitude'][i])
        
    return df['address']

if __name__ == "__main__":
        
    df_dic = readData(path)
    df_location = df_dic['Location']
    
    print(df_location.columns)
    
    # plt.plot(df_location['latitude'], df_location['longitude'])
    lines = df_location[['latitude', 'longitude']].values[:].tolist()
    
    # center = [37.561020, 126.923472]
    
    j = 0
    center = [df_location['latitude'][j], df_location['longitude'][j]]
    
    geoLoc = Nominatim(user_agent="GetLoc")
    locname = geoLoc.reverse("%s, %s" %(center[0], center[1]))
    
    print(center[1])
     
    # printing the address/location name
    print(locname.address.split(',')[0])
    
