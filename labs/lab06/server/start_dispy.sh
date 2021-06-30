#!/bin/bash
#
# Author: August Frisk
# Course: CmpEt 269 - Spring 2018
# Assign: Lab 04
# File: start_dispy.sh
# 

# start dispy on the chosen interface, usually it's wlan0
# we need to wait until the interface has has a chance to connect
sleep 30

_IP=$(hostname -I)
/usr/local/bin/dispynode.py -i "$_IP" --daemon 

