from bluepy.btle import Scanner

scanner=Scanner()
devices=scanner.scan(10.0, passive=True)

for dev in devices:
	data=dev.getScanData()
	for (adtype, desc, value) in data:
		if 'Short Local Name' in desc:
			print ("Device %s, RSSI=%d dB" % (dev.addr, dev.rssi))
