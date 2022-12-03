import bluetooth, sys, select, socket, os
from threading import Thread


class socketListener(Thread):
    def run(self):
        while True:

            sockets_list = [bluetooth.BluetoothSocket(), server_sock]
            try:
                read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])
            
                for socks in read_sockets:
                    
                    if socks == server_sock:
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



#start of MAIN

print("Looking for nearby devices .... ")

nearby_devices = bluetooth.discover_devices(
    duration=6, lookup_names=True, flush_cache=True, lookup_class=False)

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

choice = input("Select the index of the device you would like to communicate with:   ")
choice = int(choice)

choice = choice-1

bd_addr = my_list[choice][2]


port = 5 #arbitrary number, there is code to serach for an available port

server_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )


server_sock.connect((bd_addr, port))

server_sock.setblocking(False)

#Start a thread to listen from the server while main continues to listen for user input

pid = os.getpid()
s1 = socketListener()
s1.start()


while True:
    message = input()

    if message:
        message = message.encode()
        server_sock.send(message)

    #sockets_list = [bluetooth.BluetoothSocket(), server_sock]


server_sock.close()
