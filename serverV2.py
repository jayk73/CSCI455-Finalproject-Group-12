
import bluetooth, os
from threading import Thread #Need thread to listen to stop waiting
import threading

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
port = 5 #arbitrary number, there is code to serach for an available port
server_sock.bind(("",port))
server_sock.listen(10) #Allows 10 active connections

list_of_clients = []
def clientThread(connection, address):
    while True:
        try:
            print("INside connection handler")
            data = connection.recv(1024)
            if data:
                print ("<" + address[0] + "> " + data)
                message_to_send = "<" + address[0] + "> " + data
                broadcast(message_to_send, connection)
            else:
                remove(connection)
        except:
            continue

def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message)
            except:
                clients.close()

                #if link broken, remove client
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    #Accepts connection request. Store paramteters 'connection' and 'address'
    #which is socket object for that user and bluettooth address they connected from
    connection, address = server_sock.accept()
    
    #Maintain a list of clients so you can broadcast messages to all clients
    list_of_clients.append(connection)

    #When a user clonnects, print the address of that user
    print (address[0] + " connected")

    # creates and individual thread for every user
    # that connects
    threading.Thread(target= clientThread, args=(connection,address) ).start()
    # start_new_thread(clientThread,(connection,address))


        


    




