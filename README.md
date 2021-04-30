# MidiToOSC
Python script using mido and pyOSC to translate incoming midi to an OSC address.

Main purpose is to run on a raspberry pi with a midi device for MIDI Input, and translate that according to the config file oscconfig.json.

This should run on anything that have the above python modules though I would imagine.

I included a commented launcher.sh that I use to automatically launch the script on reboot of the pi.
Set it up using a guide on https://www.instructables.com/Raspberry-Pi-Launch-Python-script-on-startup/
