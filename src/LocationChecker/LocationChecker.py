# -*- coding: utf-8 -*-
"""
Created on Tue May 10 00:32:58 2022

@author: boy10
"""

import pandas as pd
import os
from geopy.geocoders import Nominatim

def convertLocationToAddress(latitude, longitude):
    geoLoc = Nominatim(user_agent="GetLoc")
    locname = geoLoc.reverse("%s, %s" %(latitude, longitude))
    address = locname.address.split(',')[0]
    print(address)
    return address

def convertLocationInDataframe(df):
    print(df['latitude'].iloc[0])
    df['address'] = [0]* len(df)
    for i in range(len(df)):
        df['address'].iloc[i] = convertLocationToAddress(df['latitude'].iloc[i], df['longitude'].iloc[i])
        
    print(df.columns)
    return df
