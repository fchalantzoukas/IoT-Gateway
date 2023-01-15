from bluepy.btle import Scanner, DefaultDelegate
from dotenv import load_dotenv
import os
import requests
from ieee754 import ieee754toreal

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewData:
            if dev.addr[-2:].upper() in authBeacons and len(dev.getValueText(255))==52:
                print(dev.getValueText(255))
                closestID = getClosest(dev.getValueText(255))
                kiosk = dev.addr[-2:].upper()
                if close[kiosk]!=closestID:
                    close[kiosk]=closestID
                    r=requests.post(url=URL+'saveclosest', data={'closestID':closestID, 'kiosk':kiosk})
                    print(r.text)
                    print('The closest now:',closestID)

#------------------------------------------------------

load_dotenv()
IP = os.environ.get('IP')
#KEY = os.environ.get('KEY')
URL = 'http://{}/'.format(IP)

def getClosest(data):
    distances = []
    tags = []
    for i in range(0,3):
        distances.append(ieee754toreal(data[20+8*i:28+8*i]))
        tags.append(data[8+2*i:10+2*i])
    print(distances)
    if min(distances)<1.5:
        return tags[distances.index(min(distances))]
    else: return 'Null'

#-----------------------------------------------------------

authBeacons=set()
close = {}

r=requests.get(url=URL+'getauthbeacons')
kiosks = r.json()
for kiosk in kiosks:
    authBeacons.add(kiosk['KioskMACID'])

for beac in authBeacons:
    close[beac]='Null'

scanner=Scanner().withDelegate(ScanDelegate())
devices=scanner.scan(20)

r=requests.get(url=URL+'getclosest/A3')
print('The closest eventually: '+r.text)