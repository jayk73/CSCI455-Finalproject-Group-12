
# import bluetooth, os, sys
# from _thread import * #Need thread to listen to stop waiting
# import threading
# from threading import Thread

# server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

# ser = bluetooth.BluetoothSocket()


# # port = bluetooth.get_available_port( bluetooth.RFCOMM )
# # port = bluetooth.get_available_port( 0 )
# # port = 5
# server_sock.bind(("",bluetooth.PORT_ANY))


# server_sock.listen(10) #Allows 10 active connections
# port = server_sock.getsockname()[1]
# print ("listening on port %d",port)

# # uuid = "4C4C4544-0036-3910-8052-C7C04F344233"
# uuid  = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

# # bluetooth.advertise_service( sock=server_sock, name= "Bob Service")
# bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
#                             service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
#                             profiles=[bluetooth.SERIAL_PORT_PROFILE],
#                             # protocols=[bluetooth.OBEX_UUID]
#                             )


import bluetooth, os
from threading import Thread
import threading
list_of_clients = []

#Listens on a client connection for input from the client.
def clientThread(connection, address):
    print("thread created")
    connection.send("<SERVER> Welcome to this chatroom!")
    
    while True:
        try:
            data = connection.recv(1024).decode()
            if data:
                print ("<" + address[0] + "> " + data)
                message_to_send = "<" + address[0] + "> " + data
                forward(message_to_send, connection)
            else:
                remove(connection)
                print("Removing connection")
                break
        except:
            continue
#Forward a message to every client except the one who sent it
def forward(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                # message = message.encode()
                clients.send(message)
                pass
            except:#for some reason always goes into except state, even when message is sent correctly
                pass 
                # clients.close()
                # print('removing clinet')
                # #if link broken, remove client
                # remove(clients)
#Send a message to all clients
def broadcast(message):
    for clients in list_of_clients:
        try:
            message = message.encode()
            clients.send(message)
        except:#for some reason always goes into except state, even when message is sent correctly
                pass 

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


class socketListner(Thread):
    def run(self):
        while True:
            #Accepts connection request. Store paramteters 'connection' and 'address'
            #which is socket object for that user and bluettooth address they connected from
            connection, address = server_sock.accept()

            #Maintain a list of clients so you can broadcast messages to all clients
            list_of_clients.append(connection)

            #When a user clonnects, print the address of that user
            print ( address[0] +  " connected")
            broadcast (address[0] + " Connected to the server")
            # creates and individual thread for every user
            # that connects
            print("Creating thread")
            threading.Thread(target= clientThread, args=(connection,address) ).start()
            # start_new_thread(clientThread,(connection,address))



server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
#Manages how many unnacepted connections can be managed
server_sock.listen(10)

port = server_sock.getsockname()[1]

# uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

uuid =  "0E448EB5-3425-ED48-91BE-1AED04C0512D"

bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            # protocols=[bluetooth.OBEX_UUID]
                            )

print("Waiting for connection on RFCOMM channel", port)

pid = os.getpid()
s1 = socketListner()
s1.start()

while True:
    message = input()
    
    if message:
        # message = message.encode()
        for clients in list_of_clients:
            try:
                print("<YOU> " + message)
                message = "<Server> " + message
                broadcast(message)
                
                
                pass
            except:#for some reason always goes into except state, even when message is sent correctly
                pass 


print("Disconnected.")

client_sock.close()
server_sock.close()
print("All done.")
        


    




