from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    #Not needed yet
    def handleDiscovery(self, dev, isNewDev, isNewData):
        pass

#------------------------------------------------------

def filterDevices(devices):
    beacons=set()
    for dev in devices:
        if dev.addr[:-3]=="48:23:35:00:00":
            beacons.add(dev)
    return beacons

def printBeacons(beacons, msgTypes):
    for beac in beacons:
        msg=beac.getScanData()[0][2]
        msgType=msgTypes[msg[-8]]
        print ("Device: {}\nMAC Address: {}\nRSSI={} dB\nMessage Type: {}\n".format(beac.addr[-2:].upper(),beac.addr, beac.rssi,msgType))

def scanDevices(scanner, msgTypes, testScans):
    viewersList=set() #Total viewers
    viewTime=dict()
    for scan in testScans:
        print('{} Scan\n{}'.format(scan,(len(scan)+5)*'-'))
        viewers=doScan(scanner,msgTypes) #Single Scan viewers
        for viewer in viewers:
            if viewer in viewersList:
                viewTime[viewer]+=10
            else:
                viewersList.add(viewer)
                viewTime[viewer]=10
    return viewTime

#Single scan
def doScan(scanner, msgTypes):
    devices=scanner.scan(5, passive=True)
    beacons=filterDevices(devices)
    printBeacons(beacons, msgTypes)
    viewers=set()
    for beac in beacons:
        viewers.add(beac.addr)
    return viewers

#------------------------------------------------------

msgTypes={'1':'Exists','2':'Connection','3':'Question'}
testScans=['First','Second','Third']

scanner=Scanner().withDelegate(ScanDelegate())

viewTime = scanDevices(scanner, msgTypes, testScans)

print('Watchtime:\n'+10*'-')
for viewer in viewTime:
    print('{}: {} minutes'.format(viewer[-2:].upper(), viewTime[viewer]))
