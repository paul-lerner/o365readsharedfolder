from __future__ import print_function
import pickle
import os.path
import io
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
from apiclient import errors
from apiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    """# Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

"""
    #google_folder_name = 'Apartment' #sys.argv[1]
    local_file_fullname = sys.argv[1]
    #local_file_fullname = 'c:\\temp\\gdrive\\bnp.csv'
    #local_file_fullname = "blah"
    google_file_name = os.path.basename(local_file_fullname)
    #download = sys.argv[2]
    download = True
    #google_file_fullname = google_folder_name + '/' + google_file_name

    if download:
        #file_id = '1ALezRziCpQ9CedhlVNFFwD_bRFYTkUml'
        file_id = '1ix_BuMfdgVH_DIIxcXfy1RBL3RId47nm'
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        with open(local_file_fullname, 'wb') as out:
            out.write(fh.getvalue())
        fh.close()
        
    else:
        file_metadata = {
            'name': google_file_name,
            'mimeType': 'text/plain',
            'parents': ['1MP9xwweC-xxa69MduSawI6P5FXoLlFtE']#1IU5WBnRxu_I2B-Z8CQSOsh-mFFYu8I1o']
        }
        media = MediaFileUpload(local_file_fullname,
                                mimetype='text/plain',
                                resumable=True)
        
        file = service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        print('File ID: %s' % file.get('id'))
#""

if __name__ == '__main__':
    main()
