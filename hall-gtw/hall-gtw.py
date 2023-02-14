from bluepy.btle import Scanner, DefaultDelegate
from dotenv import load_dotenv
import os
import sys
import requests

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        '''Handles the discovery of new devices/data'''
        if isNewData:
            data = dev.getValueText(255)
            if dev.addr[:-3]=='48:23:35:00:00' and len(data)==52:
                if data[-8:-6]=='43':
                    getClosest(data, dev.addr[-2:])
                elif data[-8:-6]=='23':
                    exchangeData(data,dev.addr[-2:])

#------------------------------------------------------

load_dotenv()
IP = os.environ.get('IP')
#KEY = os.environ.get('KEY')
URL = 'http://{}/'.format(IP)


def getClosest(data, ID):
    '''Stores the closest person to a particular kiosk in the DB'''
    closestID=data[18:20].upper()
    kiosk = ID.upper()
    try:
        r=requests.post(url=URL+'saveclosest', data={'closestID':closestID, 'kiosk':kiosk})
        print(r.text)
        print('The closest now:',closestID)
    except requests.exceptions.RequestException as e:
        sys.exit('Server closed\nExiting...')

def exchangeData(data,ID):
    '''Stores a request for data exchange in the DB'''
    closestID=data[18:20].upper()
    initID = ID.upper()
    try:
        r=requests.post(url=URL+'exchangedata', data={'closestID':closestID, 'initID':initID})
        print(r.text)
    except requests.exceptions.RequestException as e:
        sys.exit('Server closed\nExiting...')

#-----------------------------------------------------------

scanner=Scanner().withDelegate(ScanDelegate())
devices=scanner.scan(20)
