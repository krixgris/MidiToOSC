#Project URL for information/contact https://github.com/krixgris/MidiToOSC
#

import mido
import OSC
import json
from datetime import datetime

import configHandler
import httpHandler


configFile = 'oscconfig.json'
conf = configHandler.configHandler(configFile=configFile)

osc = OSC.OSCClient()
http = httpHandler.httpHandler()

#generic MidiEvent-getter, can replace getAttribute/Type/Command etc
#returns a configHandler.MidiEvent
def MidiEvent(midiNum, midiType):
	#with no parameters, configHandler.MidiEvent() returns a dummy event
	midiEvent = configHandler.MidiEvent()
	if (midiType == 'control_change'):
		midiEvent = configHandler.MidiEvent(conf.control_change.get(midiNum))
	if (midiType == 'note_on'):
		midiEvent = configHandler.MidiEvent(conf.note_on.get(midiNum))
	if (midiType == 'note_off'):
		midiEvent = configHandler.MidiEvent(conf.note_off.get(midiNum))
	return midiEvent

#add support for loading custom config via config-parameters configName='oscConfig', configFile='oscconfig.json' ?
def reloadConfig():
	global conf
	conf = configHandler.configHandler(configFile=configFile)
	reconnectOSC()
	reconnectHTTP()
	print(str(datetime.now()) + " Configuration updated")

	#ugly, make a nicer result at some point?
	print conf

def quitViolently():
	print "Quitting violently!"
	quit()

#reconnects the OSC object to ip/port in config
def reconnectOSC():
	osc.connect((conf.IP,conf.port))

def reconnectHTTP():
	http.setIP(conf.IP)

#depr?
# def getMIDIInputDevice():
# 	#todo: defaults,? mido.get_input_names()[0]?
# 	#testing with usb midi dongle 'CME U2MIDI:CME U2MIDI MIDI 1 20:0'
# 	return conf.midiDeviceInput

#depr?
#keep for now, to be able to set config to the actual midi channel, and not 0-15
def getMIDIInputChannel():
	#todo: defaults?, 0?
	return conf.midiChannelInput-1

# def createOSCMessage(address, val):
# 	oscMsg = OSC.OSCMessage()
# 	oscMsg.setAddress(address)
# 	oscMsg.append(float(val))
# 	return oscMsg

# def getType(midiNum, midiType):
# 	midiEventEvent = MidiEvent(midiNum,midiType).type
# 	if(midiEventEvent is None):
# 		midiEventEvent = ''
# 	return midiEventEvent
	#return MidiEvent(midiNum,midiType).type

# def getAttribute(midiNum, midiType):
# 	midiEventAttribute = MidiEvent(midiNum,midiType).attribute
# 	if(midiEventAttribute is None):
# 		midiEventAttribute = 'value'
# 	return midiEventAttribute

# def getCommand(midiNum, midiType):
# 	if(getType(midiNum, midiType) == 'command'):
# 		return MidiEvent(midiNum,midiType).command
# 	else:
# 		return 0

#generic handler?
def mtoAction(midiNum, midiValue, midiType):
	#print midiNum, midiValue, midiType
	#print getType(midiNum, midiType)
	midiEventType = MidiEvent(midiNum, midiType).type
	if(midiEventType == 'osc'):
		mtoOSC(midiNum, midiValue, midiType)
	if(midiEventType == 'http'):
		mtoHTTP(midiNum, midiValue, midiType)
	if(midiEventType == 'command'):
		mtoCommand(midiNum, midiValue, midiType)

def mtoOSC(midiNum, midiValue, midiType):
	osc.send(getOSCMessage(midiNum, midiValue, midiType))

def mtoHTTP(midiNum, midiValue, midiType):
	#http can technically send batches of data with json, but only one parameter is currently supported
	data = http.getValueList(getHTTPValueAttribute(midiNum,midiValue,midiType), getEventValue(midiNum,midiValue,midiType))
	#print data
	#print getHTTPAddress(midiNum,midiType)
	http.patchData(getEventAddress(midiNum,midiType), data)

def mtoCommand(midiNum, midiValue, midiType):
	midiEventCommand = MidiEvent(midiNum, midiType).command
	if(midiEventCommand == 'reloadConfig'):
		reloadConfig()
	if(midiEventCommand == 'quitLoop'):
		quitViolently()



#depr, use generic Event-function
# def getOSCAddress(midiNum, midiType):
# 	return getEventAddress(midiNum, midiType)

#depr, use generic Event-function
# def getOSCValue(midiNum, midiValue, midiType):
# 	return getEventValue(midiNum, midiValue, midiType)

#depr, use generic Event-function
# def getHTTPAddress(midiNum, midiType):
# 	return getEventAddress(midiNum, midiType)

def getHTTPValueAttribute(midiNum, midiValue, midiType):
	valAttr = MidiEvent(midiNum, midiType).attribute
	if (valAttr is None):
		valAttr = 'value'
	return valAttr

#depr, use generic Event-function
# def getHTTPValue(midiNum, midiValue, midiType):
# 	#valMin = float(MidiEvent(midiNum,midiType).min)
# 	#valMax = float(MidiEvent(midiNum,midiType).max)
# 	#return (valMax-valMin)/127.0*midiValue+valMin
# 	return getEventValue(midiNum, midiValue, midiType)

#todo: implement scaling options for lin/log/exp
#already defined in config-file and configHandler
def getEventValue(midiNum, midiValue, midiType):
	valMin = float(MidiEvent(midiNum,midiType).min)
	valMax = float(MidiEvent(midiNum,midiType).max)
	return (valMax-valMin)/127.0*midiValue+valMin

def getEventAddress(midiNum, midiType):
	address = MidiEvent(midiNum,midiType).address
	return address

#	copy pasted code from c++-plugin with tests of exponential scaling
#
#     float oscVal = (float) oscUIDial.getValue();
#     float oscScaled = 4*(1 - (log(oscVal)/log(0.0001)));
#    // float oscScaled = 4*(exp(oscVal)-1)/(2.71828-1);
#     float pwrOf = 200;
#     //oscScaled = 4*oscUIDial.getValue();
#     oscScaled = 4*(pow(pwrOf,oscVal)-1)/(pwrOf-1);
#     oscSendEditor.send ("/mix/chan/35/matrix/fader", (float) oscScaled); 


def getOSCMessage(midiNum, midiValue, midiType):
	oscMsg = OSC.OSCMessage()
	oscMsg.setAddress(getEventAddress(midiNum, midiType))
	oscMsg.append(getEventValue(midiNum, midiValue, midiType))
	return oscMsg

#put debug messages to run on launch here
#will only work if debug:1 is set in the json-config
def debugCommands():
	print ''
	print 'Debug messages from debugCommand():'
	print ''


reloadConfig()

print ""
print "Available MIDI Inputs: "
print mido.get_input_names()
print ""

print "Listening on device: "
print conf.midiDeviceInput
print "Listening on channel (0-15), i.e. 0 = midi 1, 15 = midi 16 etc: "
print conf.midiChannelInput

#unused, probably getting removed
def isDefinedMidiLookup(midiNum, midiType, midiCh = -1):
    if(midiCh == conf.midiChannelInput or midiCh == -1):
        if(midiType in conf.definedMidi.keys()):
            if(midiNum in conf.definedMidi[midiType]):
                return True
    return False

def getMidiValue(msg):
	if(msg.type == 'control_change'):
		return msg.value
	if(msg.type == 'note_on' or msg.type == 'note_off'):
		return msg.velocity
	return -1

def getMidiNum(msg):
	if(msg.type == 'control_change'):
		return msg.control
	if(msg.type == 'note_on' or msg.type == 'note_off'):
		return msg.note
	return -1

def isDefinedMidi(msg):
	if(getattr(msg, 'channel', None)==getMIDIInputChannel()):
		if(msg.type in conf.definedMidi.keys()):
			if(getMidiNum(msg) in conf.definedMidi[msg.type]):
				return True
	return False

#debugCommands()
with mido.open_input(conf.midiDeviceInput) as inport:
	for msg in inport:
		if(isDefinedMidi(msg)):
			mtoAction(getMidiNum(msg), getMidiValue(msg), msg.type)
		#debug handling to control print
		
		if(conf.debug == 1):
			print(msg)