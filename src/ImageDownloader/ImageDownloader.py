

from __future__ import print_function
import os, time, sys, datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import wget
    
import pandas as pd
# If modifying these scopes, delete the file token.json.
SCOPES = "https://www.googleapis.com/auth/photoslibrary.readonly"

# [
        # "https://www.googleapis.com/auth/photoslibrary",
          # "https://www.googleapis.com/auth/photoslibrary.readonly",
          # "https://www.googleapis.com/auth/photoslibrary.readonly.appcreateddata"
          # ]
def response_media_items_by_filter(service, request_body: dict):
    try:
        response_search = service.mediaItems().search(body=request_body).execute()
        lstMediaItems = response_search.get('mediaItems')
        nextPageToken = response_search.get('nextPageToken')

        while nextPageToken:
            request_body['pageToken'] = nextPageToken
            response_search = service.mediaItems().search(body=request_body).execute()

            if not response_search.get('mediaItem') is None:
                lstMediaItems.extend(response_search.get('mediaItems'))
                nextPageToken = response_search.get('nextPageToken')
            else:
                nextPageToken = ''
        return lstMediaItems
    except Exception as e:
        print(e)
        return None
    
def splitDate(date):
    dateSplitted = date.split('-')
    year = dateSplitted[0]
    month = dateSplitted[1]
    day = dateSplitted[2]
    return year, month,  day

def main(date):

    year, month, day = splitDate(date)
    
    # os.chdir(os.path.dirname(os.path.abspath(__file__)))

    #create directory for download
    print("Check image directory...")
    # imagePath = r'.\..\..\data\image\images_%s-%s-%s' %(year, month, day)
    # imagePath = r'.\..\..\data\image\imagesAll'
    imagePath = r'./../../data/imagesAll'

    if not os.path.exists(imagePath):
        os.makedirs(imagePath)

    #OAuth2 authentication process
    print("OAuth2 authentication process...")

    store = file.Storage(r'..\token-for-google.json')
    creds = store.get()
    
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(os.path.join(os.path.dirname(__file__), 'client_id.json'), SCOPES)
        creds = tools.run_flow(flow, store)
        
    service = build("photoslibrary", "v1", http=creds.authorize(Http()),static_discovery=False)
    
    # years = [2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015]
    years = [year]
    results = []
    for year in years:
            
        request_body = {
        'pageSize': 100,
        'filters': {
            'dateFilter': {
    
                'dates': [
                    {
                        'year': year,
                        'month': month,
                        'day': day
                    },
    
                    ]
                }
            }
        }

        df_search_result = pd.DataFrame(response_media_items_by_filter(service, request_body))
        results.append(df_search_result)
    print("Dowload & Convert image files...")
    for j, df in enumerate(results):
        try : 
            for i, baseUrl in enumerate(df['baseUrl']):
                filename = df['filename'][i].encode("utf8")
                print(f'processing {i} th file..')
            #     #check duplication & download
            #     file_full_path = os.path.join(b"%s" %imagePath.encode("utf8"), filename)
                file_full_path = b"%s\\%s" % (imagePath.encode("utf8"), filename)

                if not os.path.isfile(file_full_path): 
                    wget.download(baseUrl, r'%s/%s' %(imagePath, filename.decode()))
                # print(file_full_path, imagePath.encode("utf8"))

        except : 
            print("error in processing %s th result" %j)

if __name__ == "__main__":

    years = ['2022',]
    months = [ '08', '09']
    
    days = [str(x) for x in range(1, 32)]     
    for i, a in enumerate(days):
        if len(a) ==1:
            days[i] = '0' + a
    
    # date = '2022-03-06'
    for year in years : 
        for month in months:
            for day in days:
                date = f'{year}-{month}-{day}' 
                print(date)
                main(date)
    