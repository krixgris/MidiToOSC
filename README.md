# MidiToOSC
Python script using mido and pyOSC to translate incoming midi to an OSC address.

Main purpose is to run on a raspberry pi with a midi device for MIDI Input, and translate that according to the config file oscconfig.json.

This should run on anything that have the above python modules.

I have tested this with both a USB-midi dongle and currently running it with the PiSound module from https://blokas.io/pisound/ and it works without any configuration whatsoever, other than adding it to the oscconfig.json file in the project, which is where the entire configuration is handled.

Also keep in mind that the json configuration file validates certain parts of it, but it is certainly possible to crash the script if it's not configured correctly.

Only midi cc/note_on/note_off are supported currently. See config file for examples of how to set it up.

There's a parameter called globalThrottlingOverride which, if enabled, will throttle messages generates if the recipient can't handle a huge amount of messages at once.
Try it with 0 to disable it, but if there are issues, try setting it to 1.

I did set up a throttling: 0/1 parameter for midi events, but it's not currently implemented. Throttling is only controlled by said override parameter.

I included a commented launcher.sh that I use to automatically launch the script on reboot of the pi.
I set it up using a guide on https://www.instructables.com/Raspberry-Pi-Launch-Python-script-on-startup/

