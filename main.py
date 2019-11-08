import os
import json
import slack
import requests
import validators
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


@app.route('/ticket', methods=["GET", "POST"])
def create_ticket():
    print("Create ticket received !")

    data = request.form.to_dict()

    print(f"Create ticket form : {data}")
    text = data.get("text")
    trigger_id = data.get("trigger_id")
    print(f"Trigger ID : {trigger_id}")

    r = requests.post(
        "https://slack.com/api/dialog.open",
        data=json.dumps({
            "dialog": {
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
    if not response_json.get("ok"):
        return "Error occurred"
    return "Dialog created"


@app.route('/interactive', methods=["GET", "POST"])
def interactive():
    print("Interactive received !")
    data = request.form.to_dict()
    print(f"Request form : {data}")
    payload = json.loads(data.get("payload"))
    print(f"Payload : {payload}")
    submission = payload.get("submission")
    type_ = payload.get("type")
    print(f"Type {type_}")
    if type_ != "dialog_submission":
        return "something goes wrong"
    if not validators.email(submission.get("email")):
        return "Invalid e-mail ! Please correct your data !"
    r = requests.post(
        "http://iimet.wwwshine.supersitedns.com/project/API/examples/ticket_form.php",
        data={
            "page": "general",
            "department_id": 1,
            "creator_full_name": submission.get("fullname"),
            "creator_email": submission.get("email"),
            "type_id": 1,
            "priority_id": 1,
            "subject": submission.get("subject"),
            "contents": submission.get("content"),
            "submit_general": "Submit"
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )
    print(f"Created form response code {r.status_code}")
    print(f"Created form response content {r.content}")
    return ""
