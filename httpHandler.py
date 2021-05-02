#may need to install some additional packages on your device for this to work
#i had to install the following on my raspberry pi
#try: sudo apt-get install libcurl4-gnutls-dev librtmp-dev

import pycurl
import json
import random
from StringIO import StringIO


class httpHandler:
    def __init__(self,IP = '192.168.1.167', timeoutMS = 500):
        self.IP = IP
        self.timeoutMS = timeoutMS

    def getIP(self):
        print self.IP

    def setIP(self,IP):
        self.IP = IP

    def setTimeoutMS(self,timeoutMS):
        self.timeoutMS = timeoutMS

    data = {'value':1.000000}
    address = '/datastore/mix/group/4/matrix/mute'
    timeoutMS = 500

    def getValueList(self, parameter, value):
        data = {parameter:value}
        return data

    def patchData(self, address, data, formfieldName = 'json'):
        
        #print address
        #print data
        c = pycurl.Curl()
        c.setopt(c.URL, 'http://' + self.IP + address + '?client=' + str(random.randrange(0,2147483647)))
        jData = json.dumps(data)
        jData = formfieldName + '=' + json.dumps(data)
        #print jData
        c.setopt(pycurl.POSTFIELDS, jData)
        c.setopt(c.CUSTOMREQUEST, 'PATCH')
        c.perform()

    def getData(self, address):
        c = pycurl.Curl()
        responseData = StringIO()
        c.setopt(c.URL, 'http://' + self.IP + address + '?client=' + str(random.randrange(0,2147483647)))
        c.setopt(c.CUSTOMREQUEST, 'GET')

        c.setopt(c.WRITEFUNCTION, responseData.write)
        c.setopt(c.VERBOSE,0)
        #c.setopt(c.HEADER,0)
        #c.setopt(c.NOBODY,0)
        c.setopt(c.TIMEOUT_MS,500)
        try:
            c.perform()
        except:
            responseData.write('{"error":"connection error, timeout? max time allowed is ' + str(self.timeoutMS) +'ms. Trying to retrieve a single value that has just been set? That will result in an empty GET and this error."}')

        #print('Time: %f' % c.getinfo(c.TOTAL_TIME))

        try:
            responseJson = json.loads(responseData.getvalue())
        except:
            responseJson = json.loads('{"error":"failed to load json from responseData"}')
        return responseJson

def httpAction():
    print 'do HTTP things'
""" 

buncha testing 

def doCurlyThings():

    c = pycurl.Curl()
    c.setopt(c.URL, 'http://192.168.1.167/datastore/mix/group/4/matrix/mute?client=123123')

    post_data = {'value':1.000000}
    jData = json.dumps(post_data)
    jData = 'json=' + json.dumps(post_data)
    
    c.setopt(pycurl.POSTFIELDS, jData)
    c.setopt(pycurl.VERBOSE, 0)

    print jData

    responseData = StringIO()


    c.setopt(c.CUSTOMREQUEST, 'PATCH')
    c.perform()
    # HTTP response code, e.g. 200.
    print('Status: %d' % c.getinfo(c.RESPONSE_CODE))
    # Elapsed time for the transfer.
    print('Time: %f' % c.getinfo(c.TOTAL_TIME))

    #c.setopt(c.URL, 'http://192.168.1.167/datastore/avb?client=123123')
    c.setopt(c.URL, 'http://192.168.1.167/datastore/mix/chan/4/matrix/aux?client=1231234')

    c.setopt(c.CUSTOMREQUEST, 'GET')
    c.setopt(c.WRITEFUNCTION, responseData.write)
    c.perform()

    body = responseData.getvalue()
    responseJson = json.loads(body)

    print body

    print ""
    #print body['0001f2fffe00a5f6/url']
    print responseJson #['0001f2fffe00a5f6/url']


    # HTTP response code, e.g. 200.
    print('Status: %d' % c.getinfo(c.RESPONSE_CODE))
    # Elapsed time for the transfer.
    print('Time: %f' % c.getinfo(c.TOTAL_TIME))
    print ""

    c.close() """