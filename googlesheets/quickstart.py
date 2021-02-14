from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient import discovery

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
#SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
spreadsheet_id = "1EZ2cXKFi1xmKNJ0NGqSPbCEDrz_2_oOlDBtChbHVNYQ"
SAMPLE_RANGE_NAME = 'Class Data!A2:E'


def getCreds():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

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

    return creds


def createSpreadsheet():
    creds = getCreds()
    service = build('sheets', 'v4', credentials=creds)

    spreadsheet = {
        'properties': {
            'title': "My first sheet"
        }
    }
    spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                            fields='spreadsheetId').execute()


    print('Spreadsheet ID: {0}'.format(spreadsheet.get('spreadsheetId')))


def getValues():
    creds = getCreds()
    service = build('sheets', 'v4', credentials=creds)
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range="A1").execute()

    rows = result.get('values', [])
    print(rows[0][0])
    print('{0} rows retrieved.'.format(len(rows)))


def writeValues(service):


    values = [
        [
            # Cell values ...
            "Iniyan1","kumar", "Thamarai", "Mummy", "Daddy"
        ],
        # Additional rows ...
    ]
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range="Sheet2!A1:E1",
        valueInputOption="USER_ENTERED",
        body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))


def writeHeader(service):
    values = [
        [
            "ref_id",
            "chain_symbol",
            "expiration_date",
            "strike_price",
            "option_type",
            "side",
            "order_created_at",
            "direction",
            "order_quantity",
            "order_type",
            "opening_strategy",
            "closing_strategy",
            "price",
            "processed_quantity"
        ]
    ]
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range="Sheet1!A1:N1",
        valueInputOption="USER_ENTERED",
        body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))

if __name__ == '__main__':
    creds = getCreds()
    service = build('sheets', 'v4', credentials=creds)
    #createSpreadsheet()
    #getValues()
    #writeValues(service)
    writeHeader(service)