#!/bin/bash
#source venv/bin/activate
nohup python3 manage.py runserver --host 0.0.0.0 --port 9008 > /tmp/subview.file 2>&1 &
