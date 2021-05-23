#configHandler.py
#
# 
import json

class MidiEvent:
	#undefined midiEvent returns a dict({'type':'dummy'})
	#dynamically added properties in the config should appear automatically, but their datatype may need to be specified
	def __init__(self, midiEvent = None):
		if(midiEvent is None):
			midiEvent = dict({'type':'dummy'})
		self.__dict__ = midiEvent
		self.type = midiEvent.get('type','Undefined')
		self.command = midiEvent.get('command','Undefined')
		self.address = midiEvent.get('address','Undefined')
		self.description = midiEvent.get('description','Undefined')
		self.max = midiEvent.get('max',127.0)
		self.min = midiEvent.get('min',0.0)
		self.attribute = midiEvent.get('attribute','Undefined')
		self.multi = midiEvent.get('multi',1)
		self.valueScaling = midiEvent.get('valueScaling','lin')
		self.valueScalingBase = midiEvent.get('valueScalingBase',10)
		self.throttling = midiEvent.get('throttling',1)#throttling of values on by default
		self.prevValue = -1 #0-127 7-bit values 
		self.prevTime = 0 #time of execution will be stored from time.time()


	def __str__(self):
			return str(self.__class__) + ": " + str(self.__dict__)
	def __repr__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

class configHandler:
	def __init__(self, configName='oscConfig', configFile='oscconfig.json'):
		f = open(configFile)
		config_json = json.load(f)
		self.__dict__ = config_json[configName]
		f.close()
		self.config_json = config_json

		#re-key dictionaries for cc, note_on, note_off to be integer based, for easier querying
		
		self.control_change = { int(key):value for key,value in self.control_change.items()}
		self.note_on = { int(key):value for key,value in self.note_on.items()}
		self.note_off = { int(key):value for key,value in self.note_off.items()}

		self.definedMidi = {'control_change':self.control_change.keys(), 'note_on':self.note_on.keys(), 'note_off':self.note_off.keys()}
		
		MidiEventList = dict()
		for midiType in self.definedMidi:
			MidiEventList[midiType] = dict()
			for midiNum in self.definedMidi[midiType]:
				if(midiType == 'control_change'):
					MidiEventList[midiType][midiNum] = MidiEvent(self.control_change.get(midiNum))
				if midiType == 'note_on':
					MidiEventList[midiType][midiNum] = MidiEvent(self.note_on.get(midiNum))
				if(midiType == 'note_off'):
					MidiEventList[midiType][midiNum] = MidiEvent(self.note_off.get(midiNum))
		self.MidiEventList = MidiEventList

		self.configfile = configFile

# configHandler.MidiEvent(conf.control_change.get(midiNum))


	def __str__(self):
		return str(self.__class__) + ": " + str(self.configfile)
	def __repr__(self):
		return str(self.__class__) + ": " + str(self.__dict__)