import slack
from config import config
from utils import *


__all__ = ["get_slack_username_list", "open_dialog"]

OK = "ok"

slack_client = slack.WebClient(token=config.slack_client_token)
bot_client = slack.WebClient(token=config.slack_bot_token)


def get_slack_username_list():
    result = slack_client.users_list()
    if not result.get(OK):
        raise Exception("This is weird ! Please contact the network admin ! Now !")
    return extract_usernames(result.get("members"))


def open_dialog(text, trigger_id):
    r = slack_client.dialog_open(
        dialog={
            "callback_id": "submit-ticket",
            "title": "Create a ticket",
            "submit_label": "Request",
            "state": "Limo",
            "elements": [
                {
                    "type": "text",
                    "label": "Full name",
                    "name": "fullname"
                },
                {
                    "type": "text",
                    "label": "Email",
                    "subtype": "email",
                    "name": "email"
                },
                {
                    "type": "text",
                    "label": "Subject",
                    "name": "subject",
                    "value": text
                },
                {
                    "type": "textarea",
                    "label": "Content",
                    "name": "content"
                }
            ]
        },
        trigger_id=trigger_id
    )
    if r.get("ok"):
        return "Dialog created"
    return "Error occurred"