#configHandler.py
#
#   format needs more specifying, or possibly reworked to be safe for extending
#
import json

class MidiEvent:
    #todo: do we need to handle undefined, or incorrectly defined events?
    #enough with them being defaulted to None?
    #
    #
    #better way to handle new attributes?
    def __init__(self, midiEvent):
        try:
            self.__dict__ = midiEvent
            self.type = getattr(midiEvent, 'type','Undefined')
            self.command = getattr(midiEvent, 'command','Undefined')
            self.address = getattr(midiEvent, 'address','Undefined')
            self.description = getattr(midiEvent, 'description','Undefined')
            self.max = getattr(midiEvent, 'max', 0.0)
            self.min = getattr(midiEvent, 'min',0.0)
            self.attribute = getattr(midiEvent, 'attribute','Undefined')
            self.multi = getattr(midiEvent, 'multi',0)
            #self.midiEvent = midiEvent
        except:
            #Undefined dummy created
            self.type = 'Undefined'
            self.command = 'Undefined'
            self.address = 'Undefined'
            self.description = 'Undefined'
            self.max = 0.0
            self.min = 0.0
            self.attribute = 'Undefined'
            self.multi = 0
            #self.midiEvent = 'Undefined'
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
