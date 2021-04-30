import mido
import OSC
import json

configFile = 'oscconfig.json'
osc = OSC.OSCClient()
config = object

def reloadConfig():
	global config
	config = readConfig(configFile)
	reconnectOSC()
	print("Configuration updated")
	print(config)

#reads configuration from oscconfig.json in the same dir as the python-script
#can be read while running to reconfigure parameters
def readConfig(fileName):
	f = open(fileName)
	data = json.load(f)
	f.close()
	return data

#reconnects the OSC object to ip/port in config
def reconnectOSC():
	ip = str(config['oscConfig']['IP'])
	port = int(config['oscConfig']['port'])
	osc.connect((ip,port))

def getOSCIP():
	#todo: defaults
	return str(config['oscConfig']['IP'])

def getOSCPort():
	#todo: defaults
	return int(config['oscConfig']['port'])

def getMIDIInputDevice():
	#todo: defaults, mido.get_input_names()[0]
	#testing with usb midi dongle 'CME U2MIDI:CME U2MIDI MIDI 1 20:0'
	return str(config['oscConfig']['midiDeviceInput'])

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

def mtoAction(midiNum, midiValue, midiType):
	if(getType(midiNum, midiType) == 'osc'):
		mtoOSC(midiNum, midiValue, midiType)
		return 1
	if(getType(midiNum,midiType) == 'command'):
		if(getCommand(midiNum, midiType) == 'reloadConfig'):
			reloadConfig()
		return 2
	return 0

def mtoCommand(midiNum,midiType):
	return 0

def mtoOSC(midiNum, midiValue, midiType):
	osc.send(getOscMessage(midiNum, midiValue, midiType))
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


#config = readConfig(configFile)
reloadConfig()
osc.connect((getOSCIP(),getOSCPort()))

print ""
print "Available MIDI Inputs: "
print mido.get_input_names()
print ""

print "Listening on device: "
print getMIDIInputDevice()
print "Listening on channel: "
print getMIDIInputChannel()

#debugCommands()

#todo: need to catch and handle more types
#		neater handling
#		proper handling function to make it clearer to read
#
#	#print(msg.type)
#	#print(msg.value)
#	#print(msg.note)
#	#print(msg.control)
#if(msg.channel==15):


with mido.open_input(getMIDIInputDevice()) as inport:
	for msg in inport:
		if(getattr(msg, 'channel', None)==getMIDIInputChannel()):
			if(msg.type == 'control_change'):
				mtoAction(msg.control, msg.value, msg.type)
			if(msg.type == 'note_on'):
				mtoAction(msg.note, msg.velocity, msg.type)
			print(msg)
		#'panic' reconfigure listen to any note_on events at velocity 126
		# very temporary
		if(msg.type == 'note_on' and msg.velocity == 126):
			reloadConfig()
		#if(msg.type == 'note_on'):
		#	print(msg)
		#	config = readConfig(configFile)
		#if(isDebug()):
		#	print(msg)