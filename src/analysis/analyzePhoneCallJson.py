import glob
import os
import json
import datetime
path = r"/Volumes/T7/auto diary/pythonProject/dataAnalyzed/phoneCall"

files = glob.glob(f'{path}/*')
print(files)

data = {}



def parseFilename(filename):
    filename = filename.split('/')[-1]
    infoList = filename.split('_')
    partner = infoList[0]
    datetimeFromFile = datetime.datetime.strptime( infoList[2].split('.')[0], '%Y%m%d%H%M%S')
    return partner, datetimeFromFile

print(parseFilename(files[0])[1])
partner, datetimeFromFile = parseFilename(files[0])

dataAll = {}

def countNumberOfValue(map, key):
    return len(map[key])


for i, file in enumerate(files):
    with open(file, "r", encoding = 'utf-8-sig') as input:
        try :
            partner, datetimeFromFile = parseFilename(file)
            jsonData = json.load(input)
            if partner not in list(dataAll.keys()):
                dataAll[partner] = {}

            dataAll[partner][datetimeFromFile] = jsonData
        except :
            pass

for j in range(len(dataAll.keys())):
    key = list(dataAll.keys())[j]
    print(key, countNumberOfValue(dataAll, key))
