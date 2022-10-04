from datetime import datetime

import apiclient.discovery
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

from services.db import DataBaseSheet, session
from services.helpers import send_message_tg


class GoogleSheetDate:
    """Class for authorization and reading data from Google Sheets"""

    def __init__(self, creds, sheet_id):
        self.creds = creds
        self.spreadsheet_id = sheet_id

    def authorization(self):
        """Authorize and get an access to the API"""
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.creds,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
        self.drive = apiclient.discovery.build('drive', 'v3', http=httpAuth)

    def read_file(self):
        """Read file"""
        self.authorization()
        values = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range='A:D',
            majorDimension='ROWS'
        ).execute()
        return values['values'][1:]

    def check_revision_sheet(self):
        """Check last revision sheet. Return 'False' if there are no updates"""
        update = False
        self.authorization()
        values = self.drive.revisions().list(
            fileId=self.spreadsheet_id,
            fields='*',
            pageSize=1000
        ).execute()

        сurrent_revision = values['revisions'][-1]['id']

        with open('services/revision.txt', 'r+') as f:
            try:
                previous_revision = f.readline().strip()
                
                # Check difference between revisions
                if int(сurrent_revision) > int(previous_revision):
                    update = True
            except ValueError:
                print('Uncorrent PATH for previous revision')
            finally:
                f.seek(0)
                f.write(сurrent_revision)

        return update

    

    @staticmethod
    def diff_order_db_vs_sheet(order_sheet):
        """Try to find which order numbers are in the database and which are not in Google Sheet"""
        set_order_db = set([elem[0] for elem in session.query(DataBaseSheet.number_order).all()])
        set_order_google = set([int(elem[1]) for elem in order_sheet])
        diff_order = list(set_order_db.difference(set_order_google))

        return diff_order

    @staticmethod
    def check_order_date(order_date, number_order):
        """Check the date of the order and the current one. If the deadline has passed, then I send a message in telegram"""
        if datetime.now() > datetime.strptime(order_date, "%d.%m.%Y"):
            send_message_tg(f"The delivery date for order {number_order} has passed.")
