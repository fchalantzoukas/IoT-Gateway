from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    #Not needed yet
    def handleDiscovery(self, dev, isNewDev, isNewData):
        pass

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


msgTypes={'1':'Exists','2':'Connection','3':'Question'}

scanner=Scanner().withDelegate(ScanDelegate())
devices=scanner.scan(5, passive=True)

beacons=filterDevices(devices)
printBeacons(beacons, msgTypes)
