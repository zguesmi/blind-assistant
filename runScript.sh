#!/bin/bash

# This file runs the python script automatically at boot
cd /home/pi/workshop
python3 index.py > /tmp/blindGuide.log
