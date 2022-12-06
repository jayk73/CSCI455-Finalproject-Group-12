import time, socket, sys
import bluetooth


# port = 8080
server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
port = 5 #arbitrary number, there is code to serach for an available port


server_sock.bind(("", port))
print("binding success")


name = input('Enter name: ')

server_sock.listen(1) 

conn, add = server_sock.accept()

print("Received connection from ", add[0])
print('Connection Established. Connected From: ',add[0])

client = (conn.recv(1024)).decode()
print(client + ' has connected.')

conn.send(name.encode())
while True:
    message = input('Me : ')
    conn.send(message.encode())
    message = conn.recv(1024)
    message = message.decode()
    print(client, ':', message)