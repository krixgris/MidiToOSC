# MidiToOSC
Python script using mido and pyOSC to translate incoming midi to an OSC address.

Main purpose is to run on a raspberry pi with a midi device for MIDI Input, and translate that according to the config file oscconfig.json.

This should run on anything that have the above python modules though I would imagine.

I have only tested it on the MIDI USB-device I have, so I can't say how it works with others. There's comments included in the script that should make it somewhat easy to figure out what to set your device to though.
Also keep in mind that the json configuration file isn't validated by the script, so unless you follow similar setup to what is included in the file in this repository it might just crash for some reason or another.
This is a planned update for the future, so the config is validated, or at least all the incorrect entries get filtered out.

I included a commented launcher.sh that I use to automatically launch the script on reboot of the pi.
Set it up using a guide on https://www.instructables.com/Raspberry-Pi-Launch-Python-script-on-startup/

Note (literally):
If you have no way to reload the configuration because you messed up your config, the config will be reloaded if you send a note_on with velocity 126 on any channel.
This will/should be updated to a smarter panic solution, but not sure when that would happen.
