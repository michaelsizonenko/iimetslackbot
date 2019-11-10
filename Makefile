#!/bin/bash

run_bot:
	env FLASK_APP=main.py flask run --host='0.0.0.0'
test:
	python test.py
