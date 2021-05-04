#testscript.py
import json
import configHandler

conf = configHandler.configHandler()

#reload conf with re-initializing
conf = configHandler.configHandler()

midiNum = str(63)

print conf.definedMidi

definedMidiCC = [51,50,2]
definedMidiNoteOn = [51,50,2]
definedMidiNoteOff = [51,50,2]
definedMidi = {'control_change':definedMidiCC, 'note_on':definedMidiNoteOn
                , 'note_off':definedMidiNoteOff, 'magics':definedMidiNoteOff}

def isDefined(midiNum, midiType, midiCh = -1):
    if(midiCh == conf.midiChannelInput or midiCh == -1):
        if(midiType in conf.definedMidi.keys()):
            if(midiNum in conf.definedMidi[midiType]):
                return True
    return False


def MidiEvent(midiNum):
    return configHandler.MidiEvent(conf.control_change.get(midiNum))

print "MidiEvent(x)"
print MidiEvent('52')

print conf.control_change.get('52')
print "MidiEvent(x)"


print conf.control_change.get('52')

print conf.definedMidi

print 
print conf.control_change.get('52')

print type(definedMidi)

# for mtype in definedMidi:
#     if mtype in conf.definedMidi.keys():
#         print mtype
#         for mnum in filter(lambda mnum: mnum in conf.definedMidi[mtype], definedMidi[mtype]):
#             #if mnum in conf.definedMidi[mtype]
#             print type(mnum)
#             print mnum

print definedMidi


def MidiEvent(midiNum):
    return configHandler.MidiEvent(conf.control_change.get(midiNum))
""" def MidiEvent(midiNum):
    return configHandler.MidiEvent(conf.control_change.get(midiNum))

print "json"
print conf.config_json
print MidiEvent(midiNum)
print "======================"
print "Test MidiEvent output for midi number " + midiNum + ":"
print ("Type: ", MidiEvent(midiNum).type)
print ("Command: ", MidiEvent(midiNum).command)
print ("Address: ", MidiEvent(midiNum).address)
print ("Min: ", MidiEvent(midiNum).min)
print ("Max: ", MidiEvent(midiNum).max)
print ("Multi: ",MidiEvent(midiNum).multi)   
print "======================" """

""" if(o is None):
    print 'Not configured, typo?'
else:
    print o
    print o.get('type')
    print o.get('attribute')

    print type(o)
    print o.keys()
    #print o.keys()[0]
    #print o.keys()[1]
    #for key,value in o.items():
    #    print (key,value)
    #    print key
    #    print value """