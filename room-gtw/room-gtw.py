from bluepy.btle import Scanner, DefaultDelegate
from dotenv import load_dotenv
import os
import requests
import time

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        '''Handles the discovery of new devices/data'''
        if (isNewData):
            getQuestioners(dev)


#------------------------------------------------------

load_dotenv()

#Get the server IP
IP = os.environ.get('IP')
#KEY = os.environ.get('KEY')
URL = 'http://{}/'.format(IP)

#Lecture/Conference Talk and Room parameters
roomId = 3
talkId = 15

def filterDevices(devices):
    '''Returns a set including only our beacons, ignoring the other BLE devices'''
    beacons=set()
    for dev in devices:
        if dev.addr[:-3]=="48:23:35:00:00":
            beacons.add(dev.addr[-2:])
    return beacons

def scanDevices(scanner):
    '''Scans for BLE Devices, and saves the current viewerlist'''
    devices=scanner.scan(5)
    viewers=filterDevices(devices)
    r=requests.post(url=URL+'saveviewers',data={'viewers':viewers, 'talkId':talkId})
    print(r.text)

def getQuestioners(dev):
    '''Checks for questions when new advertising data are found, and stores any question that is found'''
    if dev.addr[:-3]=="48:23:35:00:00":
        try:
            msg = dev.getValueText(255)
            if len(msg)==52 and msg[-8:-6]=='33':
                r=requests.post(url=URL+'savequestion',data={'questioner':dev.addr[-2:], 'roomId':roomId})
                if str(r.status_code)=='200':
                    print(r.text)
        except Exception as err:
            #Save errors in a new file
            file = open('log.txt', 'a')
            content = str(err)+'\n'
            file.write(content)
            file.close()

#------------------------------------------------------

#Initiate a list of scans
testScans=['First','Second','Third']
scanner=Scanner().withDelegate(ScanDelegate())

try:
    #Delete past questions
    r=requests.post(url=URL+'clear', data={'roomId':roomId})
    scanNum = 1

    for scan in testScans:
        print('{} Scan\n{}'.format(scan,(len(scan)+5)*'-'))
        scanDevices(scanner)
        if scanNum<len(testScans):
            print('Program pausing for 5s to adjust the beacons...\n')
            time.sleep(5)
            scanNum+=1


except requests.exceptions.RequestException as e:
    print('Server closed\nExiting...')