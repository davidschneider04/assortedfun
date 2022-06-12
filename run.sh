#!/bin/bash

source /home/www-data/environment/bin/activate
cd /var/www/assortedfun.com
waitress-serve --port=8008 app:app
