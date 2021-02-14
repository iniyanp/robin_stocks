from __future__ import print_function

import os
import os.path
import pickle

from funfacts import getPLBySymbols
from getmyorders import getOrders
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from robinorders import get_completed_option_orders

import robin_stocks as r

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

spreadsheet_id = "1EZ2cXKFi1xmKNJ0NGqSPbCEDrz_2_oOlDBtChbHVNYQ"


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


def writeHeader(service, sheet_name):
    values = [
        [
            "ref_id",
            "chain_symbol",
            "expiration_date",
            "strike_price",
            "order_created_at",
            "direction",
            "order_quantity",
            "price",
            "opening_strategy",
            "closing_strategy",
            "side"
        ]
    ]
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=sheet_name + "!A1:K1",
        valueInputOption="USER_ENTERED",
        body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))


def extractMyOrderObj(my_order_obj):
    list = []
    list.append(my_order_obj.ref_id)
    list.append(my_order_obj.symbol)
    list.append(my_order_obj.exp_date)
    list.append(my_order_obj.strike_price)
    list.append(my_order_obj.created_at)
    list.append(my_order_obj.direction)
    list.append(my_order_obj.quantity)
    list.append(my_order_obj.price)
    list.append(my_order_obj.opening_strategy)
    list.append(my_order_obj.closing_strategy)
    list.append(my_order_obj.side)
    return list


def extractMyOrdersProfitLoss(my_order_obj_pl):
    final_list = []
    for my_order_obj in my_order_obj_pl:
        count = 0
        for order in my_order_obj.orders:
            count = count + 1
            list = []
            list.append(order.symbol)
            list.append(order.exp_date)
            list.append(order.strike_price)
            list.append(order.created_at)
            list.append(order.direction)
            list.append(order.quantity)
            list.append(order.price)
            list.append(order.opening_strategy)
            list.append(order.closing_strategy)
            list.append(order.side)
            if count < len(my_order_obj.orders):
                list.append(None)
            else:
                list.append(my_order_obj.pl)

            # attach profit only in last object. other objects has None. Otherwise pl would be repeated in a group which we don't want.
            final_list.append(list)

        final_list.append(
            [])  # append empty list for every symbol + exp combination so that it looks nice in spread sheet.

    return final_list


def writeAllOrders(service, data, sheetName):
    total_row = len(data)
    total_col = len(data[0])
    total_col_letter = chr(ord('@') + total_col)

    body = {
        'values': data
    }
    # Sheet2!A1:E1
    range_val = sheetName + "!A2:" + str(total_col_letter) + str(total_row + 1)
    print("range val is " + range_val)
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_val,
        valueInputOption="USER_ENTERED",
        body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))


def writeTotal(sheet_name, total, position):
    body = {
        'values': [
            [
                total
            ]
        ]
    }
    range_val = sheet_name + "!" + position
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_val,
        valueInputOption="USER_ENTERED",
        body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))


def extract_data():
    r.login(os.getenv('robin_username'), os.getenv('robin_password'))
    completed_orders = get_completed_option_orders()
    list_of_objs = completed_orders.values()
    list_of_rows = [extractMyOrderObj(obj) for obj in list_of_objs]
    return list_of_rows


def writeHeaderForClosedOrders(service, sheet_name):
    values = [
        [
            "chain_symbol",
            "expiration_date",
            "strike_price",
            "order_created_at",
            "direction",
            "order_quantity",
            "price",
            "opening_strategy",
            "closing_strategy",
            "side",
            "profit"
        ]
    ]
    body = {
        'values': values
    }
    total_col = len(values[0])
    total_col_letter = chr(ord('@') + total_col)
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=sheet_name + "!A1:" + total_col_letter + "1",
        valueInputOption="USER_ENTERED",
        body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))


def writeClosedOrders(service, all_closed_orders, sheet_name):
    closed_orders_pl = extractMyOrdersProfitLoss(all_closed_orders)
    writeAllOrders(service, closed_orders_pl, sheet_name)


def writeHeaderForPLBySymbols(service, sheet_name):
    values = [
        [
            "Symbol",
            "Profit"
        ]
    ]
    body = {
        'values': values
    }

    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=sheet_name + "!A1:B2",
        valueInputOption="USER_ENTERED",
        body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))


def writePLBySymbols(service, all_closed_orders, sheet_name):
    sorted_dict = getPLBySymbols(all_closed_orders)
    writeHeaderForPLBySymbols(service, sheet_name)
    writeAllOrders(service, list(sorted_dict.items()), sheet_name)
    total = sum(sorted_dict.values())
    position = "B" + str(len(sorted_dict) + 3) # add header and one blank line
    writeTotal(sheet_name, total, position)


if __name__ == "__main__":
    extract_data()
    creds = getCreds()
    service = build('sheets', 'v4', credentials=creds)
    # writeHeader(service, "Sheet1")
    # all_wheeling_orders = extract_data()
    # writeAllOrders(service, all_wheeling_orders, "Sheet1")
    all_closed_orders = getOrders()
    # always create a sheet before writing headers and values.
    # writeHeaderForClosedOrders(service, "Closed-CSP")
    # writeClosedOrders(service, all_closed_orders, "Closed-CSP")
    # TODO: Write one sheet for covered call
    # 2 more sheets for current openings.
    writePLBySymbols(service, all_closed_orders, "PL-by-Symbols")
