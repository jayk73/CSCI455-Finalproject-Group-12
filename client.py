import bluetooth

print("Looking for nearby devices .... ")

nearby_devices = bluetooth.discover_devices(
    duration=8, lookup_names=True, flush_cache=True, lookup_class=False)

print("found %d device(s)" % len(nearby_devices))

my_list = []
i = 1
for addr, name in nearby_devices:    
    try:
        #print("  %s - %s" % (addr, name))
        my_list.append(["INDEX: " + str(i), "NAME: " + name,  addr])
        i += 1
    except UnicodeEncodeError:
        #print("  %s - %s" % (addr, name.encode('utf-8', 'replace')))
        my_list.append(["INDEX: " + str(i) , "NAME: " + name.encode('utf-8', 'replace'), addr])
        i += 1

for element in my_list:
    print(element)

choice = input("Select the index of the device you would like to communicate with ")
choice = int(choice)

choice = choice-1

bd_addr = my_list[choice][2]


port = 5

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )


sock.connect((bd_addr, port))

while True:
    
    inp = input("Enter a message to send (enter 'quit' to quit):\n")
    print(inp)
    if (inp == "quit"):
        break
    else:
        sock.send(inp)


sock.close()