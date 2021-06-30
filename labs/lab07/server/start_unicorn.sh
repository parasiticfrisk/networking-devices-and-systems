#!/bin/bash
#
# Author: August Frisk
# Course: CmpEt 269 - Spring 2018
# Assign: Lab 04
# File: start_dispy.sh
#  

# get the ID of the instance of python if present
PYTHON_ID=$(ps -e | grep python | awk -F' ' '{print $1}')
if [ $PYTHON_ID ]; then
    # kill this instance of python if present (a really nasty thing to do)
    sudo kill -9 $PYTHON_ID
fi

# run the required python script
sudo python $1 > /dev/null
