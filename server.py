
import bluetooth, os
from threading import Thread #Need thread to listen to stop waiting
import threading

# def connectionHandler(connection):
    
#     print("INside connection handler")
#     data = connection.recv(1024)
#     print ("received [%s]" % data)
#     return
    

#Thread which listens on a port and then loops to 
#recivee all messages from that conection
#Thread ends when user enters any key
class socketListener(Thread):
    def run(self):
        server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        port = 5
        server_sock.bind(("",port))
        server_sock.listen(1)
        connection,address = server_sock.accept()
        print ("Accepted connection from ",address)
        while True:
            
            message = connection.recv(1024)
            message = message.decode()
            if message:
                print(message)
        
        #ch.start()
        #print(ch.address)
        
        # client_sock,address = server_sock.accept()
        # print ("Accepted connection from ",address)

        # data = client_sock.recv(1024)
        # print ("received [%s]" % data)


    


#Start the thread and then kill the process
#when any key is pressed
pid = os.getpid()
sl = socketListener()
sl.start()
input('Socket is listening, press any key to abort...\n')
os.kill(pid,9)




#Old code, delete later
#server_sock.listen(1)
# while True:
#     try:
#         client_sock,address = server_sock.accept()
#         print ("Accepted connection from ",address)

#         data = client_sock.recv(1024)
#         print ("received [%s]" % data)
#     except KeyboardInterrupt:
        
#         client_sock.close()
#         server_sock.close()
#         break


