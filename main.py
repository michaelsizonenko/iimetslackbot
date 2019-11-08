import os
import re
import json
from threading import Thread

import slack
import requests
import validators
from lxml import html
from flask import Flask, escape, request, make_response

app = Flask(__name__)

slack_client_token = os.environ["SLACK_CLIENT_TOKEN"]
client = slack.WebClient(token=slack_client_token)

pattern = r"Your request was submitted sucessfully. The request number is <strong>[a-zA-Z-0-9]+<\/strong>"
re_obj = re.compile(pattern)


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

    r = client.dialog_open(
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


def send_create_ticket_request(fullname, email, subject, content):
    r = requests.post(
        "http://iimet.wwwshine.supersitedns.com/project/API/examples/ticket_form.php",
        data={
            "page": "general",
            "department_id": 1,
            "creator_full_name": fullname,
            "creator_email": email,
            "type_id": 1,
            "priority_id": 1,
            "subject": subject,
            "contents": content,
            "submit_general": "Submit"
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )
    print(f"Created form response code {r.status_code}")
    text_response = r.text
    # print(f"Created form response text : {text_response}")
    response_message = re_obj.search(text_response)
    if not response_message:
        return "Could not create a ticket !"
    tree = html.fromstring(response_message.group())
    ticket_id = tree.xpath("strong")[0].text_content()
    print(f"Ticket ID : {ticket_id}")


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

    thread = Thread(target=send_create_ticket_request, kwargs=submission)
    thread.start()
    return ""
