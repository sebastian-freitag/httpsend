# Copyright (c) 2017, Sebastian A. Freitag
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import httplib
import time
import sys

https = 0
quiet = 0

# How-To:
#
# python HTTPSend.py [-s] [-q] filename.http [filename1.http] ...
# Works on files containing http requests in given order
# If -s option is provided, use https
# If -q option is provided, do not print response
#
# freitsabes@gmail.com
#
# Possible future improvements:
#  - When folder is provided instead of files, go through files in folder alphabetically.
#  - add error handling

current_milli_time = lambda: int(round(time.time() * 1000))


def setOptionHttps():
    global https
    https = 1

def setOptionQuiet():
    global quiet
    quiet = 1

class Request:
    def __init__(self):
        self.host = ''
        self.port = ''
        self.target = ''
        self.headers = {}
        self.body = ''
        self.method = ''
        self.httpVersion = ''


def readRequest(filename):
    global https
    myFile = open(filename, 'rb')
    returnRequest = Request()
    while True:
        fieldName = ''
        fieldValue = ''
        line = myFile.readline()
        if line == '\r\n':
            break
        if line == '':
            break
        headerField = line.split(':', 1)
        if len(headerField) < 2:
            # this is either the start line
            # or
            # we have a bad header field
            startLine = line.split(' ')
            if len(startLine) == 3:
                returnRequest.method = startLine[0]
                returnRequest.target = startLine[1]
                returnRequest.httpVersion = startLine[2].strip()
            else:
                print 'WARNING! INVALID HEADER LINE FOUND'
                print startLine[0]
            continue
        else:
            if headerField[0] == 'Content-Length':
                # we ignore this because httplib sets it automatically
                print 'WARNING! Content-Length IS IGNORED'
                print 'HTTPLIB WILL SET IT AUTOMATICALLY'
                continue
            else:
                fieldName = headerField[0]
                fieldValue = headerField[1].strip()
        if fieldName == 'Host':
            # set all the connection stuff
            hostList = fieldValue.split(':')            
            returnRequest.host = hostList[0]
            if len(hostList) == 2:
                returnRequest.port = hostList[1]
        returnRequest.headers[fieldName] = fieldValue
        
    returnRequest.body = myFile.read()
    myFile.close()
    
    if https == 1 and returnRequest.port == '':
        print 'WARNING! NO PORT GIVEN WITH HTTPS FLAG (-s)'
        print 'I SET PORT TO 443'
        returnRequest.port = '443'
    if https == 0 and returnRequest.port == '':
        print 'WARNING! NO PORT GIVEN'
        print 'I SET PORT TO 80'
        returnRequest.port = '80'
    
    return returnRequest

    
def readArgs(args):
    returnArray = []
    options = {'-s': setOptionHttps, '-q': setOptionQuiet}
    for arg in args[1:]:
        if arg[:1] == '-':
            options[arg]()
        else:
            thisrequest = readRequest(arg)
            returnArray.append(thisrequest)
    return returnArray


myArgs = sys.argv
myRequests = readArgs(myArgs)
for request in myRequests:
    startTime = current_milli_time()
    myHost = ':'.join([request.host, request.port])
    if https == 0:
        myConnection = httplib.HTTPConnection(myHost)
    else:
        myConnection = httplib.HTTPSConnection(myHost)
    if len(request.body) == 0:
        myConnection.request(request.method,
                             request.target,
                             headers=request.headers)
    else:
        myConnection.request(request.method,
                             request.target,
                             request.body,
                             request.headers)
    myResponse = myConnection.getresponse()

#    print len(myResponse.read())
    if not quiet:
        print 'Response:'
        print ''
        print myResponse.read()
    print ''
    print 'It took time to perform this request:'
    print str(current_milli_time() - startTime) + ' milliseconds!'    
    myConnection.close()
