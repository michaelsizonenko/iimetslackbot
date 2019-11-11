import os
import json
import re


class Config:

    def __init__(self):
        assert os.path.exists("config.json"), "This is weird ! config.json does not exists !"
        with open("config.json", 'r') as conf_file:
            config_data = json.loads(conf_file.read())
            self.slack_client_token = config_data["slack_client_token"]
            self.slack_bot_token = config_data["slack_bot_token"]
            self.department_id = config_data["department_id"]
            self.sheet_url = config_data["sheet_url"]
            self.spreadsheet_id = self.get_spreadsheet_id()
            self.sheet_id = self.get_sheet_id()
            self.range = config_data["range"]

    def get_spreadsheet_id(self):
        return re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", self.sheet_url).group().split('/spreadsheets/d/')[1]

    def get_sheet_id(self):
        return re.search(r"[#&]gid=([0-9]+)", self.sheet_url).group().split("#gid=")[1]


config = Config()
