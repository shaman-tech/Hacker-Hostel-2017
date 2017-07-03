from __future__ import print_function
import argparse
import sqlite3
import time

from apiclient import discovery
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'#one or more scopes (strings)
CLIENT_SECRET = 'client_secret.json'

store = file.Storage('storage.json')
credz = store.get()
if not credz or credz.invalid:
    #flow = client.flow_from_clientsecrets(CLIENT_SECRET,SCOPES)
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    flow = client.flow_from_clientsecrets(CLIENT_SECRET,SCOPES)
    credz = tools.run_flow(flow, store, flags)

SHEETS = build('sheets', 'v4', http=credz.authorize(Http()))
data = {'properties': {'title': 'Toy Orders [%s]' % time.ctime()}}
res = SHEETS.spreadsheets().create(body=data).execute()
SHEET_ID = res['spreadsheetId']
print ('Created "%s"' % res['properties']['title'])

FIELDS = ('ID','Customer Name','Product Code', 'Units Ordered', 'Unit Price','Status' 'Created at', 'Uploaded at')
cxn = sqlite3.connect('db.sqlite')
cur = cxn.cursor()
rows = cur.execute('SELECT * FROM orders;').fetchall()
cxn.close()
rows.insert(0,FIELDS)
data = {'values': [row[:6] for row in rows]}

SHEETS.spreadsheets().values().update(spreadsheetId=SHEET_ID, range='A1', body=data, valueInputOption='RAW').execute()
print('Wrote data to sheet')
rows = SHEETS.spreadsheets().values().get(spreadsheetId=SHEET_ID,range= 'Sheet1').execute().get('values',[])
for row in rows:
    print(row)
