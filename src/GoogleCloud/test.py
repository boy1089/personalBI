
from __future__ import print_function

import os

import zipfile
import shutil
import io
import google.auth
import datetime
import glob
import os.path

from googleapiclient.http import MediaIoBaseDownload
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/drive.readonly']
# token_path = r'/Volumes/T7/auto diary/personalBI/src/ImageDownloader/token-for-google.json'
token_path = 'token.json'
# token_path = r'/Volumes/T7/auto diary/personalBI/src/ImageDownloader/client_secret_135403068198-c7m3u9ghrcn14rnhhavttivjkb8dqfc7.apps.googleusercontent.com.json'
client_path = r'/Volumes/T7/auto diary/personalBI/src/client_id.json'
# cilent_path = r'/Volumes/T7/auto diary/personalBI/src/ImageDownloader/client_secret_135403068198-c7m3u9ghrcn14rnhhavttivjkb8dqfc7.apps.googleusercontent.com.json'

flag_inProcess = False

def get_files():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        results = service.files().list(q= f"name contains 'takeout'",
            pageSize=50, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
        return items
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')

def download_file(real_file_id):
    """Downloads a file
    Args:
        real_file_id: ID of the file to download
    Returns : IO object with location.

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds = None

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("cred expired?")
            creds.refresh(Request())
        else:
            print('else')
            flow = InstalledAppFlow.from_client_secrets_file(
                client_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())


    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
        file_id = real_file_id

        # pylint: disable=maybe-no-member
        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        print('download started')
        while done is False:
            status, done = downloader.next_chunk()
            print(F'Download {int(status.progress() * 100)}.')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.getvalue()


def refreshTakeoutData(file):
    print('converting byte to zip')
    zf = zipfile.ZipFile(io.BytesIO(file), "r")
    foldername = f"takeout_{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
    print('start extracting..')
    zf.extractall(path = f'/Volumes/T7/auto diary/data/{foldername}')
    print('extract done')

    folders_takeout = glob.glob('/Volumes/T7/auto diary/data/takeout*')
    folders_toRemove = [x for x in folders_takeout if x.find(foldername) == -1]

    for folder in folders_toRemove:
        shutil.rmtree(folder)
    print('previous folders removed')


if __name__ == '__main__':
    flag_inProcess = True
    listOfFiles = get_files()
    print(listOfFiles)
    file = download_file(listOfFiles[0]['id'])

    refreshTakeoutData(file)
    # zf = zipfile.ZipFile(io.BytesIO(file), "r")
    #
    # foldername = f"takeout_{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
    # zf.extractall(path = f'/Volumes/T7/auto diary/data/{foldername}')
    # import glob
    # print(glob.glob('/Volumes/T7/auto diary/data/takeout*'))

    flag_inProcess = True