import os
import json


class Config:

    def __init__(self):
        assert os.path.exists("config.json"), "This is weird ! config.json does not exists !"
        with open("config.json", 'r') as conf_file:
            config_data = json.loads(conf_file.read())
            self.slack_client_token = config_data["slack_client_token"]
            self.slack_bot_token = config_data["slack_bot_token"]
            self.department_id = config_data["department_id"]
            self.ticket_id_delivery_channel = config_data["ticket_id_delivery_channel"]


config = Config()
