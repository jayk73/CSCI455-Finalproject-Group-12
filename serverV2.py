
import bluetooth, os, sys
from _thread import * #Need thread to listen to stop waiting
import threading
from threading import Thread

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

ser = bluetooth.BluetoothSocket()

# server_sock.setsockopt(server_sock.SOL_SOCKET, server_sock.SO_REUSEADDR, 1)

port = 5 #arbitrary number, there is code to serach for an available port
server_sock.bind(("",port))
server_sock.listen(10) #Allows 10 active connections


list_of_clients = []
def clientThread(connection, address):
    print("thread created")
    connection.send("Welcome to this chatroom!")
    
    while True:
        try:
            data = connection.recv(1024).decode()
            if data:
                print ("<" + address[0] + "> " + data)
                message_to_send = "<" + address[0] + "> " + data
                broadcast(message_to_send, connection)
            else:
                remove(connection)
                print("Removing connection")
                break
        except:
            continue

def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message).encode()
                pass
            except:#for some reason always goes into except state, even when message is sent correctly
                pass 
                # clients.close()
                # print('removing clinet')
                # #if link broken, remove client
                # remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


class socketListner(Thread):
    def run(self):
        while True:
            #Accepts connection request. Store paramteters 'connection' and 'address'
            #which is socket object for that user and bluettooth address they connected from
            connection, address = server_sock.accept()
            
            #Trying to get teh name of the connected device
            # nearby_devices = bluetooth.discover_devices(
            #     duration=2, lookup_names=True, flush_cache=True, lookup_class=False)

            # connectionName = ""
            # for devAddress, name in nearby_devices:
            #     if address == devAddress:
            #         connectionName = name
            #         break
            
            
            #Maintain a list of clients so you can broadcast messages to all clients
            list_of_clients.append(connection)

            #When a user clonnects, print the address of that user
            print ( address[0] +  " connected")

            # creates and individual thread for every user
            # that connects
            print("Creating thread")
            threading.Thread(target= clientThread, args=(connection,address) ).start()
            # start_new_thread(clientThread,(connection,address))

pid = os.getpid()
s1 = socketListner()
s1.start()

while True:
    message = input()
    if message:
        broadcast("<Server> " + message, "Bob")


        


    




