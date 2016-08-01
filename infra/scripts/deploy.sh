#!/bin/bash

rsync -R . /opt/houseofdota
cd /opt/houseofdota
source venv/bin/activate
pip install -r requirements.txt
