from bluepy.btle import Scanner

scanner=Scanner()
devices=scanner.scan(10.0, passive=True)

for dev in devices:
  print("Device %s, RSSI=%d dB" % (dev.addr, dev.rssi))
