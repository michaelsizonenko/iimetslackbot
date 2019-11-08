import os
import slack
from flask import Flask, escape, request

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


@app.route('/command', methods=["GET", "POST"])
def command():
    print("Command received !")
