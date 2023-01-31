
import numpy as np
import datetime
import matplotlib.colors as mcolors
import math

path_log = r"/Volumes/T7/auto diary/data/*"


dataType_sensor = 1
dataType_account = 2
dataType_audio2 = 3
dataType_google = 4
dataType_image = 5
dataType_prev = 6
dataType_phoneCall = 7

locationState_home = 1
locationState_work = 1.2
locationState_moving = 0
locationState_NA = 1.4

latitude_home = 37.3625
longitude_home = 126.721

latitude_work = 37.225
longitude_work = 127.070

locationState_moving_threshold = 0.0005


location_home_threshold = 0.03
location_work_threshold = 0.03
location_else_threshold = 0.03

columns = ['location_std', 'location_home', 'location_work',
           'datetimeArrivedWork', 'datetimeLeavingWork', 'timeSpentInWork',
           'deposit_count', 'withdraw_count', 'accel_std', 'image_count',
           'wakeupTime']

colors = list(mcolors.TABLEAU_COLORS.values())


earthRadius = 6378

def calculateDistance(lat1, long1, lat2, long2):
    a = np.sin((lat1-lat2) * np.pi / 180 / 2) ** 2 + np.cos(lat1 * np.pi / 180) * np.cos( lat2 * np.pi/180) * np.sin((long1-long2) * np.pi/180 / 2) **2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    distance = earthRadius * c
    return distance


def getDates(base, dateRange = 14 ):
    # base = datetime.datetime(2022, 12, 25)
    dates = [(base - datetime.timedelta(days=x)).date().strftime('%Y-%m-%d') for x in range(dateRange)]
    dates.sort()
    return dates

def getSetOfItem(item):
    list2 = list(set(item))
    # list2 = [x for x in list2 if not math.isnan(x)]
    return list2

def find_indices(list_to_check, item_to_find):
    indices = []
    for idx, value in enumerate(list_to_check):
        if value == item_to_find:
            indices.append(idx)
    return indices