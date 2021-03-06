import re
import json
from threading import Thread

from slack_client import *
import requests
import validators
from lxml import html
from flask import Flask, escape, request

from main_logger import logger
from config import config
from strings import string_instance


app = Flask(__name__)


pattern = r"Your request was submitted sucessfully. The request number is <strong>[a-zA-Z-0-9]+<\/strong>"
re_obj = re.compile(pattern)

session = requests.Session()


def break_lunch(username: str, params: str):
    raise NotImplementedError


def break_help(username: str, params: str):
    return string_instance.menu


break_sub_command_list = {
    "help": break_help,
    "lunch": break_lunch
}


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


@app.route('/slack/event', methods=["GET", "POST"])
def slack():
    logger.info("Event received !")
    logger.debug(f"Event data : {request.data}")
    data = request.json
    return data.get("challenge")


@app.route('/ticket', methods=["GET", "POST"])
def create_ticket():
    logger.info("Create ticket received !")

    data = request.form.to_dict()

    logger.debug(f"Create ticket form : {data}")
    text = data.get("text")
    trigger_id = data.get("trigger_id")
    logger.debug(f"Trigger ID : {trigger_id}")
    return open_dialog(text, trigger_id)


def send_create_ticket_request(fullname: str, email: str, subject: str, content: str):
    r = session.post(
        "http://iimet.wwwshine.supersitedns.com/project/API/examples/ticket_form.php",
        data={
            "page": "general",
            "department_id": config.department_id,
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
    logger.debug(f"Created form response code {r.status_code}")
    text_response = r.text
    logger.debug(f"Created form response text : {text_response}")
    response_message = re_obj.search(text_response)
    if not response_message:
        return "Could not create a ticket !"
    tree = html.fromstring(response_message.group())
    ticket_id = tree.xpath("strong")[0].text_content()
    logger.debug(f"Ticket ID : {ticket_id}")
    bot_client.chat_postMessage(
        channel=config.ticket_id_delivery_channel,
        text=f"New ticket created ! Ticket ID : *{ticket_id}* / http://iimet.wwwshine.supersitedns.com/project/support/staff/index.php?/Tickets/Ticket/View/{ticket_id}"
    )


@app.route('/interactive', methods=["GET", "POST"])
def interactive():
    logger.info("Interactive received !")
    data = request.form.to_dict()
    logger.debug(f"Request form : {data}")
    payload = json.loads(data.get("payload"))
    logger.debug(f"Payload : {payload}")
    submission = payload.get("submission")
    type_ = payload.get("type")
    logger.debug(f"Type {type_}")
    if type_ != "dialog_submission":
        return "something goes wrong"
    if not validators.email(submission.get("email")):
        return "Invalid e-mail ! Please correct your data !"

    thread = Thread(target=send_create_ticket_request, kwargs=submission)
    thread.start()
    return ""


@app.route("/break", methods=["GET", "POST"])
def break_func():
    result = ""
    try:
        logger.info("Break received !")
        data = request.form.to_dict()
        logger.debug(f"Break data : {data}")
        username = data.get("user_name")
        params = data.get("text")
        sub_command = params.split(" ")[0]
        if sub_command.isdigit():
            raise NotImplementedError
        try:
            result = break_sub_command_list[sub_command](username, params)
        except KeyError as unexpected_command:
            result = "Unrecognized command received : {} . Use /break help for information".format(sub_command)
    except Exception as e:
        logger.error(e, exc_info=True)
        result = "Unexpected error. Please contact the admin."
    finally:
        return result


@app.route("/clockin", methods=["GET", "POST"])
def clock_in():
    logger.info("Clock in")
    return "Have a good day!"


@app.route("/clockout", methods=["GET", "POST"])
def clock_out():
    logger.info("Clock out")
    return "Have a good rest!"


@app.route("/lunch", methods=["GET", "POST"])
def lunch():
    logger.info("Lunch")
    return "Have a good lunch!"


@app.route("/brb", methods=["GET", "POST"])
def brb():
    logger.info("Brb")
    return "Yes. Have a break."


@app.route("/end", methods=["GET", "POST"])
def end():
    logger.info("End")
    return "Good bye !"


@app.route("/back", methods=["GET", "POST"])
def back():
    logger.info("Back")
    return "Welcome back !"
