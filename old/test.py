# file: inquiry.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: performs a simple device inquiry followed by a remote name request of
#       each discovered device
# $Id: inquiry.py 401 2006-05-05 19:07:48Z albert $
#

#Detects nearby devices

import bluetooth

print("performing inquiry...")
nearby_devices = bluetooth.discover_devices(
    duration=1, lookup_names=True, flush_cache=True, lookup_class=False)

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

print(my_list[choice][2])
