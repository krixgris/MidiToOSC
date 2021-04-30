#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home
# Project URL https://github.com/krixgris/MidiToOSC

#this is launched on reboot after 60 seconds by this statement in crontab
#@reboot sleep 60 && sh /home/pi/MidiToOSC/launcher.sh >/home/pi/logs/cronlog 2>&1

#to edit this behaviour, use sudo crontab -e
#to kill the script, you need to either check ps -A for running python events and kill those
#or for an easier view, something like ps-ejH or pstree or ps axjf
#or implement a midi listen thing that can stop the script with midi in


cd /
cd home/pi/MidiToOSC/
sudo python miditoosc.py
cd /
