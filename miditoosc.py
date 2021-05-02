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

def reloadConfig():
	global conf
	conf = configHandler.configHandler(configFile=configFile)
	reconnectOSC()
	reconnectHTTP()
	print(str(datetime.now()) + " Configuration updated")
	print(conf)

#reads configuration from oscconfig.json in the same dir as the python-script
#can be read while running to reconfigure parameters
#def readConfig(fileName):
#	f = open(fileName)
#	data = json.load(f)
#	f.close()
#	return data

#reconnects the OSC object to ip/port in config
def reconnectOSC():
	osc.connect((conf.IP,int(conf.port)))

def reconnectHTTP():
	http.setIP(conf.IP)

#depr?
def getMIDIInputDevice():
	#todo: defaults, mido.get_input_names()[0]
	#testing with usb midi dongle 'CME U2MIDI:CME U2MIDI MIDI 1 20:0'
	return str(config['oscConfig']['midiDeviceInput'])

#depr?
def getMIDIInputChannel():
	#todo: defaults, 0
	return int(config['oscConfig']['midiChannelInput'])-1

def createOscMessage(address, val):
	oscMsg = OSC.OSCMessage()
	oscMsg.setAddress(address)
	oscMsg.append(float(val))
	return oscMsg

def getType(midiNum, midiType):
	mtoData = config['oscConfig'][str(midiType)].get(str(midiNum))
	mtoType = ''
	if(mtoData is None):
		mtoType = 'None'
	else:
		mtoType = mtoData.get("type")
	return mtoType

def getAttribute(midiNum, midiType):
	mtoData = config['oscConfig'][str(midiType)].get(str(midiNum))
	mtoType = ''
	if(mtoData is None):
		mtoType = 'value'
	else:
		mtoType = mtoData.get("attribute")
	return mtoType


def mtoAction(midiNum, midiValue, midiType):
	if(getType(midiNum, midiType) == 'osc'):
		mtoOSC(midiNum, midiValue, midiType)
		return 1
	if(getType(midiNum,midiType) == 'command'):
		if(getCommand(midiNum, midiType) == 'reloadConfig'):
			reloadConfig()
		return 2
	if(getType(midiNum, midiType) == 'http'):
		mtoHTTP(midiNum, midiValue, midiType)
		return 1
	return 0

def mtoCommand(midiNum,midiType):
	return 0

def mtoOSC(midiNum, midiValue, midiType):
	osc.send(getOscMessage(midiNum, midiValue, midiType))
	return 0

def mtoHTTP(midiNum, midiValue, midiType):
	#osc.send(getOscMessage(midiNum, midiValue, midiType))
	#print getHTTPValue(midiNum,midiValue,midiType)
	#print getHTTPValueAttribute(midiNum,midiValue,midiType)
	data = http.getValueList(getHTTPValueAttribute(midiNum,midiValue,midiType), getHTTPValue(midiNum,midiValue,midiType))
	#print data
	#print getHTTPAddress(midiNum,midiType)
	#print "patchdata time here"
	http.patchData(getHTTPAddress(midiNum,midiType), data)
	return 0

#decided against using the cc_OSC as a json-config makes more sense
#repurpose for command-types from json (?)
#keeping it for lazy reference to switchers
def mtoType(argument):
    switcher = {
		"osc": "osc",
		"command": "command",
    	}
    return switcher.get(argument, "None")

def getCommand(midiNum, midiType):
	if(getType(midiNum, midiType) == 'command'):
		return config['oscConfig'][str(midiType)][str(midiNum)].get('command')
	else:
		return 0

def isCC_OSC(midiNum, midiType):
	if(getType(midiNum, midiType) == 'osc'):
		return 1
	else:
		return 0

def getOSCAddress(midiNum, midiType):
	oscaddress = str(config['oscConfig'][str(midiType)][str(midiNum)]['address'])
	return oscaddress

def getOSCValue(midiNum, midiValue, midiType):
	oscMin = float(config['oscConfig'][str(midiType)][str(midiNum)]['min'])
	oscMax = float(config['oscConfig'][str(midiType)][str(midiNum)]['max'])
	return (oscMax-oscMin)/127.0*midiValue+oscMin

def getHTTPAddress(midiNum, midiType):
	address = str(config['oscConfig'][str(midiType)][str(midiNum)]['address'])
	return address

def getHTTPValueAttribute(midiNum, midiValue, midiType):
	valAttr = getAttribute(midiNum, midiType)
	#print valAttr
	if (valAttr is None):
		valAttr = 'value'
	#valMax = float(config['oscConfig'][str(midiType)][str(midiNum)]['max'])
	return valAttr

def getHTTPValue(midiNum, midiValue, midiType):
	valMin = float(config['oscConfig'][str(midiType)][str(midiNum)]['min'])
	valMax = float(config['oscConfig'][str(midiType)][str(midiNum)]['max'])
	return (valMax-valMin)/127.0*midiValue+valMin

""" 
    float oscVal = (float) oscUIDial.getValue();
    float oscScaled = 4*(1 - (log(oscVal)/log(0.0001)));
   // float oscScaled = 4*(exp(oscVal)-1)/(2.71828-1);
    float pwrOf = 200;
    //oscScaled = 4*oscUIDial.getValue();
    oscScaled = 4*(pow(pwrOf,oscVal)-1)/(pwrOf-1);
    oscSendEditor.send ("/mix/chan/35/matrix/fader", (float) oscScaled); 
"""

def getOscMessage(midiNum, midiValue, midiType):
	oscMsg = OSC.OSCMessage()
	oscMsg.setAddress(getOSCAddress(midiNum, midiType))
	oscMsg.append(getOSCValue(midiNum, midiValue, midiType))
	return oscMsg

def debugCommands():
	print getType(2,'control_change')
	print getType(52,'control_change')
	print getType(50,'control_change')

	print isCC_OSC(50,'control_change')
	print isCC_OSC(52,'control_change')

	print getCommand(60,'note_on')
	print getCommand(61,'note_on')

	mtoAction(22,127,'control_change')
	mtoAction(61,127,'note_on')


reloadConfig()

print dir(conf)

osc.connect((conf.IP,int(conf.port)))

print ""
print "Available MIDI Inputs: "
print mido.get_input_names()
print ""

print "Listening on device: "
print conf.midiDeviceInput
print "Listening on channel (0-15), i.e. 0 = midi 1, 15 = midi 16 etc: "
print conf.midiChannelInput

#debugCommands()

with mido.open_input(conf.midiDeviceInput) as inport:
	for msg in inport:
		if(getattr(msg, 'channel', None)==conf.midiChannelInput):
			if(msg.type == 'control_change'):
				mtoAction(msg.control, msg.value, msg.type)
			if(msg.type == 'note_on'):
				mtoAction(msg.note, msg.velocity, msg.type)
			#debug handling to control print
			#print(msg)
		#'panic' reconfigure listen to any note_on events at velocity 126
		# very temporary
		if(msg.type == 'note_on' and msg.velocity == 126):
			reloadConfig()