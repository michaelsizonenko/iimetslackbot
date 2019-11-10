#!/bin/bash

run_bot:
	env FLASK_APP=main.py flask run --host='0.0.0.0'
run_bot_debug:
	env FLASK_APP=main.py FLASK_DEBUG=1 flask run --host='0.0.0.0'
test:
	python test.py
