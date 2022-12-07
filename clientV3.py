import bluetooth, sys, select, socket, os
from threading import Thread


class socketListener(Thread):
    def run(self):
        while True:

            sockets_list = [bluetooth.BluetoothSocket(), sock]
            try:
                read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])
            
                for socks in read_sockets:
                    
                    if socks == sock:
                        message = socks.recv(2048).decode()
                        if message:
                            print(message)
                            #continue
                    # else:
                    #     print("hello 2")
                    #     server_sock.send(message).encode()
                    #     sys.stdout.write("<You>")
                    #     sys.stdout.write(message)
                    #     sys.stdout.flush()
            except:
                continue



# start of MAIN

print("Looking for nearby devices .... ")

nearby_devices = bluetooth.discover_devices(
    duration=6, lookup_names=True, flush_cache=True, lookup_class=False)

print("found %d device(s)" % len(nearby_devices))

my_list = []
i = 1
for addr, name in nearby_devices:    
    try:
        #print("  %s - %s" % (addr, name))
        my_list.append(["INDEX: " + str(i),  name,  addr])
        i += 1
    except UnicodeEncodeError:
        #print("  %s - %s" % (addr, name.encode('utf-8', 'replace')))
        my_list.append(["INDEX: " + str(i) ,  name.encode('utf-8', 'replace'), addr])
        i += 1

for element in my_list:
    print(element)
# for element in my_list:
#     print("Looking for servers on " + str(element) + ": ")
#     addressToSearch = element[2]
#     services = bluetooth.find_service( address = addressToSearch )

#     if len(services) <=0:
#         print("no server found :( \n")
#     else:
#         for ser in services:
#             if  "SampleServer" in str(  ser["name"]   ) :
#                 print("Found Running server in " + str(element) )
#                 first_match = ser

choice = input("Select the index of the device you would like to communicate with:   ")
choice = int(choice)

choice = choice-1

bd_addr = my_list[choice][2]
bd_name = my_list[choice][1]

connect_addr = bd_addr 
connect_name = bd_name

# if len(sys.argv) < 2:
#     print("No device specified. Searching all nearby bluetooth devices for "
#           "the SampleServer service...")
# else:
#     connect_addr  = sys.argv[1]
#     print("Searching for SampleServer on {}...".format(connect_addr ))

# search for the SampleServer service
# uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
# uuid = "0E448EB5-3425-ED48-91BE-1AED04C0512D"

service_matches = bluetooth.find_service( address=connect_addr )

first_match = None
if len(service_matches) == 0:
    print("Couldn't find the SampleServer service.")
    sys.exit(0)
else:
    for ser in service_matches:
        if  "SampleServer" in str(  ser["name"]   ) :
            print("Found service: " + str(ser))
            first_match = ser

if first_match is None:
    print("Couldn't find the SampleServer service.")
    sys.exit(0)


port = first_match["port"] 
name = first_match["name"]
host = first_match["host"]

# print("Connecting to \"{}\" on {} with port {}".format(name, host, port))


# Create the client socket
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((host, port))

pid = os.getpid()
s1 = socketListener()
s1.start()





while True:
    data = input()
    if not data:
        break
    print("<YOU> " + data)
    sock.send(data)

sock.close()



# uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
# print("UID is " + uuid + " Looking on address " +bd_addr)

# service_matches = bluetooth.find_service( uuid = uuid, address=bd_addr )
# print(uuid)

# if len(service_matches) == 0:
#     print ("couldn't find the FooBar service")
#     sys.exit(0)

# first_match = service_matches[0]
# port = first_match["port"]
# name = first_match["name"]
# host = first_match["host"]

# print ("connecting to \"%s\" on %s" % (name, host) )

# sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
# sock.connect((host, port))
# sock.send("hello!!")
# sock.close()


# # port = 5 #arbitrary number, there is code to serach for an available port

# server_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )


# server_sock.connect((bd_addr, port))

# server_sock.setblocking(False)

# #Start a thread to listen from the server while main continues to listen for user input

# pid = os.getpid()
# s1 = socketListener()
# s1.start()


# while True:
#     message = input()

#     if message:
#         message = message.encode()
#         server_sock.send(message)

#     #sockets_list = [bluetooth.BluetoothSocket(), server_sock]


# server_sock.close()
#!/usr/bin/env python3
"""PyBluez simple example rfcomm-client.py
Simple demonstration of a client application that uses RFCOMM sockets intended
for use with rfcomm-server.
Author: Albert Huang <albert@csail.mit.edu>
$Id: rfcomm-client.py 424 2006-08-24 03:35:54Z albert $
"""

# import sys

# import bluetooth

