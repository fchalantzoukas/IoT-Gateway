from bluepy.btle import Scanner, DefaultDelegate
from dotenv import load_dotenv
import os
import requests
import time

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if (isNewData):
            getQuestioners(dev)

#------------------------------------------------------

load_dotenv()
IP = os.environ.get('IP')
#KEY = os.environ.get('KEY')
URL = 'http://{}/'.format(IP)

def filterDevices(devices):
    beacons=set()
    for dev in devices:
        if dev.addr[:-3]=="48:23:35:00:00":
            beacons.add(dev.addr[-2:])
    return beacons

def scanDevices(scanner):
    devices=scanner.scan(5)
    viewers=filterDevices(devices)
    r=requests.post(url=URL+'saveviewers',data={'viewers':viewers})
    print(r.text)

def getQuestioners(dev):
    if dev.addr[:-3]=="48:23:35:00:00":
        try:
            msg = dev.getValueText(255)
            if len(msg)==52 and msg[-8:-6]=='33':
                r=requests.post(url=URL+'savequest',data={'questioner':dev.addr[-2:]})
                if r.text!='Fail' and r.text!='Pass':
                    print(r.text)
        except Exception as err:
            file = open('log.txt', 'a')
            content = str(err)+'\n'
            file.write(content)
            file.close()

#------------------------------------------------------

testScans=['First','Second','Third']
scanner=Scanner().withDelegate(ScanDelegate())

try:
    r=requests.post(url=URL+'clear')
    scanNum = 1
    for scan in testScans:
        print('{} Scan\n{}'.format(scan,(len(scan)+5)*'-'))
        scanDevices(scanner)
        if scanNum<len(testScans):
            print('Program pausing for 5s to adjust the beacons...\n')
            time.sleep(5)
            scanNum+=1
    r=requests.get(url=URL+'viewers')
    r1=requests.get(url=URL+'viewquest')
    print('\nResults\n{}'.format('-'*7))
    time.sleep(2)
    print('Viewers and their respective viewing duration \n{}'.format(r.text))
    print('Questioners: \n{}'.format(r1.text))


except requests.exceptions.RequestException as e:
    print('Server closed\nExiting...')