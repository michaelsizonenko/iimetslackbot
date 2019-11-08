import os
import json
import slack
import requests
from flask import Flask, escape, request, make_response


app = Flask(__name__)

slack_client_token = os.environ["SLACK_CLIENT_TOKEN"]
client_web_client = slack.WebClient(token=slack_client_token)


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


@app.route('/slack/event', methods=["GET", "POST"])
def slack():
    print("Event received !")
    print(f"Event data : {request.data}")
    data = request.json
    return data.get("challenge")


@app.route('/submit-ticket', methods=["GET", "POST"])
def submit_ticket():
    print("Submit ticket received !")


@app.route('/command', methods=["GET", "POST"])
def command():
    print("Command received !")

    data = request.form.to_dict()

    print(f"Command form : {data}")
    text = data.get("text")
    trigger_id = data.get("trigger_id")
    print(f"Trigger ID : {trigger_id}")

    r = requests.post(
        "https://slack.com/api/dialog.open",
        data=json.dumps({
            "dialog": {
                "callback_id": "submit-ticket",
                "title": "Request a Ride",
                "submit_label": "Request",
                "state": "Limo",
                "elements": [
                    {
                        "type": "text",
                        "label": "Pickup Location",
                        "name": "loc_origin"
                    },
                    {
                        "type": "text",
                        "label": "Dropoff Location",
                        "name": "loc_destination"
                    }
                ]
            },
            "trigger_id": trigger_id,
        }),
        headers={
            "Authorization": "Bearer {token}".format(token=slack_client_token),
            "Content-Type": "application/json;charset=utf-8"
        }
    )
    response_status = r.status_code
    print(f"Response status : {response_status}")
    response_json = r.json()
    print(f"Response json : {response_json}")

    return response_json


@app.route('/interactive', methods=["GET", "POST"])
def interactive():
    print("Interactive received !")
    print(f"Request form : {request.form}")
    data = request.form.to_dict()
    type_ = data.get("type")
    if type_ == "dialog_submission":
        return ""
    return ""

