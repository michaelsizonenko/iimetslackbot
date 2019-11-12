from clock_row_model import ClockRowItem
from config import config
import pickle
import os.path
from slack_client import *
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from main_logger import logger


USER_ENTERED = "USER_ENTERED"


class UnknownSlackUser(Exception):
    pass


class GoogleSheetWrapper:
    data = []
    sheet_scopes = [
        'https://www.googleapis.com/auth/spreadsheets.readonly',
        'https://www.googleapis.com/auth/spreadsheets',
    ]
    sheet_service = None

    def get_sheet_service(self):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
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
                    'credentials.json', self.sheet_scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build('sheets', 'v4', credentials=creds)

    def __init__(self):
        self.sheet_service = self.get_sheet_service()
        self.spreadsheet_id = config.spreadsheet_id
        self.range = config.range
        self.data = self.get_existed_data()
        if not self.data:
            self.add_header()
        self.existed_users = get_slack_username_list()

    def get_existed_data(self):
        result = self.sheet_service.spreadsheets().values().get(
            spreadsheetId=config.spreadsheet_id, range=config.range).execute()
        logger.debug(f"Sheet data : {result}")
        rows = result.get('values', [])[1:]
        logger.info('{0} rows retrieved.'.format(len(rows)))
        return rows

    def add_header(self):
        values = [
            [
                # Cell values ...
                "Slack username",
                "Clock in",
                "Breaks",
                "Clock out"
            ],
            # Additional rows ...
        ]
        body = {
            'values': values
        }
        self.sheet_service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id, range=self.range,
            valueInputOption=USER_ENTERED, body=body).execute()

    def check_slack_user_exists(self, username):
        if username not in self.existed_users:
            self.existed_users = get_slack_username_list()
            if username not in self.existed_users:
                raise UnknownSlackUser("Unknown user")
        return True

    def get_data_by_user(self, username):
        self.check_slack_user_exists(username)
        all_data = self.get_existed_data()
        logger.debug(f"All data : {all_data}")
        return ClockRowItem()

    def clock_in(self, username):
        clock_row_item = self.get_data_by_user(username)
        clock_row_item.set_clock_in()
        self.append_row(clock_row_item)
        return clock_row_item

    def append_row(self, item):
        body = {
            "values": [
                item.to_google_list()
            ]
        }
        request = self.sheet_service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=self.range,
            valueInputOption=USER_ENTERED,
            body=body
        )
        response = request.execute()


google_sheet_wrapper = GoogleSheetWrapper()
