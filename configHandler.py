#configHandler.py
#
#   format needs more specifying, or possibly reworked to be safe for extending
#
import json

dummy_midievent = {'type':'Undefined'
                    ,'command':''
                    ,'address':''
                    ,'description':''
                    ,'max':1.0
                    ,'min':0.0
                    ,'attribute':''
                    ,'multi':0
                    }

class MidiEvent:
    #todo: do we need to handle undefined, or incorrectly defined events?
    #enough with them being defaulted to None?
    #
    #
    #better way to handle new attributes?
    def __init__(self, midiEvent):
        if(midiEvent is None):
            midiEvent = dummy_midievent
        self.__dict__ = midiEvent
        self.type = midiEvent.get('type')
        self.command = midiEvent.get('command')
        self.address = midiEvent.get('address')
        self.description = midiEvent.get('description')
        self.max = midiEvent.get('max')
        self.min = midiEvent.get('min')
        self.attribute = midiEvent.get('attribute')
        self.multi = midiEvent.get('multi')
    def __str__(self):
            return str(self.__class__) + ": " + str(self.__dict__)

class configHandler:
    def __init__(self, configName='oscConfig', configFile='oscconfig.json'):
        f = open(configFile)
        config_json = json.load(f)
        self.__dict__ = config_json[configName]
        f.close()
        self.config_json = config_json
        definedMidiCC = [int(x) for x in self.control_change.keys()]
        definedMidiNoteOn = [int(x) for x in self.note_on.keys()]
        definedMidiNoteOff = [int(x) for x in self.note_off.keys()]
        self.definedMidi = {'control_change':definedMidiCC, 'note_on':definedMidiNoteOn, 'note_off':definedMidiNoteOff}

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    # @property
    # def definedMidi(self):
    #     definedMidiCC = [int(x) for x in self.control_change.keys()]
    #     definedMidiNoteOn = [int(x) for x in self.note_on.keys()]
    #     definedMidiNoteOff = [int(x) for x in self.note_off.keys()]
    #     definedMidi = {'control_change':definedMidiCC, 'note_on':definedMidiNoteOn, 'note_off':definedMidiNoteOff}
    #     return definedMidi

#redundant
#depr?
def getMidiEventConfig(confMidiEvent):
    #todo: do we need to handle undefined, or incorrectly defined events?
    #enough with them being defaulted to None?
    #if confMidiEvent is None:
    #    return MidiEventConfig(configHandler.dummy_midievent)
    return MidiEvent(confMidiEvent)