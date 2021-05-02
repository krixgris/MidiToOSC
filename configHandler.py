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
        self.__dict__ = midiEvent
        self.type = midiEvent.get('type')
        self.command = midiEvent.get('command')
        self.address = midiEvent.get('address')
        self.max = midiEvent.get('max')
        self.min = midiEvent.get('min')
        self.attribute = midiEvent.get('attribute')
        self.multi = midiEvent.get('multi')
        self.midiEvent = midiEvent

class configHandler:
    def __init__(self, configName='oscConfig', configFile='oscconfig.json'):
        self.configFile = configFile
        f = open(configFile)
        self.config_json = json.load(f)
        self.__dict__ = self.config_json[configName]
        f.close()
    dummy_midievent = {'type':'None','command':'None','address':'None','max':0,'min':0,'attribute':'None','multi':'None'}
def getMidiEventConfig(confMidiEvent):
    #todo: do we need to handle undefined, or incorrectly defined events?
    #enough with them being defaulted to None?
    #if confMidiEvent is None:
    #    return MidiEventConfig(configHandler.dummy_midievent)
    return MidiEvent(confMidiEvent)
