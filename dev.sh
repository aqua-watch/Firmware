#!/bin/bash

APP_ENV="aquawatch-env"

if [ ! -d "$APP_ENV" ]; then
	virtualenv $APP_ENV
	source $APP_ENV/bin/activate
	pip3 install -r requirements.txt
else
	source $APP_ENV/bin/activate
fi
