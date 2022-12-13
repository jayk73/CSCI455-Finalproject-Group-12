import sys, os, select, time
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from threading import Thread
from startingPage import Ui_StartingPage
from chatWindow import Ui_ChatRoom
import threading
import bluetooth
max_connections = 5
client_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )

server_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )

#Listens for any output from print statements.
#Used by server to catch messages from clients.
class EmittingStream(QObject):

    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


#For a client connection; 
#thread to listen for incoming messages from the server
class ClientSocketListener(QObject):
    progress = pyqtSignal(str, bluetooth.BluetoothSocket)
    def run(self):
        while True:
            sockets_list = [bluetooth.BluetoothSocket(), client_sock]
            try:
                read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])
                for socks in read_sockets:
                    if socks == client_sock:
                        mess = socks.recv(2048).decode()
                        if mess:
                            print(mess + " in socket listener")
                            #Send message back to ChatRoom to add to widget
                            self.progress.emit(mess, client_sock)
                           
                            #continue
            except:
                continue
        


#Server thread. Listens for new threads attempting to connect to the server.
# Listens on an availalbe port. For every connection, close the server socket
# and start listening on a new port.   
class NewConnectionListener(QObject):
    # progress = pyqtSignal(str)
    sockets = pyqtSignal(bluetooth.BluetoothSocket, tuple)
    test = pyqtSignal(bluetooth.BluetoothSocket, str)
    clientMessage = pyqtSignal(bluetooth.BluetoothSocket, str)
    clientToRemove = pyqtSignal(bluetooth.BluetoothSocket)

    def run(self):

        while True:
            server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            server_sock.bind(("", bluetooth.PORT_ANY))
            server_sock.listen(1)
            port = server_sock.getsockname()[1]
            uuid =  "0E448EB5-3425-ED48-91BE-1AED04C0512D"
            bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                                        service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                        profiles=[bluetooth.SERIAL_PORT_PROFILE],
                                        # protocols=[bluetooth.OBEX_UUID]
                                        )

            #Accepts connection request. Store paramteters 'connection' and 'address'
            #which is socket object for that user and bluettooth address they connected from
            connection, address = server_sock.accept()
            #Maintain a list of clients so you can broadcast messages to all clients
           
            self.sockets.emit(connection, address)
            #Start listening to that connection
            threading.Thread(target= clientThread, args=(connection,address) ).start()
            bluetooth.stop_advertising(server_sock)
            #Close the socket
            server_sock.close()
    # def forwardMessage(self, message, conn):
        
    #     self.clientMessage.emit(message, conn)
        

    # def deleteClient(self, conn):
    #     self.clientToRemove.emit(conn)

#For server thread.
#Listens on a client connection and print everything it hears.
def clientThread(connection, address):
    
    connection.send("<SERVER> Welcome to this chatroom!")
    
    while True:
        try:
            data = connection.recv(1024).decode()
            if data:
                print (str(connection) + "<" + address[0] + "> " + data)   
            else:
                #If we had more time, this would be a print statement
                #That indicates for the server to remove the connection
                break
        except:
            continue


# For a client connection. 
#Opens a thread to listen to the server.
# At the same time, be ready to send data
# from texbox to the server.
class ChatRoom(QMainWindow, Ui_ChatRoom):
    def __init__(self):
        super(ChatRoom, self).__init__()
        #Setup the GUI elements
        self.setupUi(self)

        #Create QThread
        self.thread = QThread()
        #Create worker of SocketListner
        self.worker = ClientSocketListener()
        #Move worker to thread
        self.worker.moveToThread(self.thread)
        #connect signals and slots
        self.thread.started.connect(self.worker.run)

        self.worker.progress.connect(self.printMessge)
        self.thread.start()

        #Upon button press, send the message from the textbox to the server. 
        #Print the message to the listview
        self.sendMessage_button.clicked.connect(self.sendMessage)
    #Prints message from server
    def printMessge(self, message, conn):
        
        self.chatDisplay_listWidget.addItem(message)
        
    #Send a message to the server.
    def sendMessage(self):
        
        message = self.enterMessage_textBox.toPlainText()
        #Remove new line charachters from text to prevent from breaking the server
        message.replace("\n", "")
        self.enterMessage_textBox.setPlainText("")
        
        message = message.encode()
        client_sock.send(message)


#For Server Connections
#Starts threads to listen for new connections and 
#starts a thread to listen on each of those connections.
#Forwards any user input to every client thats currently connected,
class ChatRoomServer(QMainWindow, Ui_ChatRoom):
    #Maintain list of currently connected clients.
    list_of_clients = []
    def __init__(self):
        super(ChatRoomServer, self).__init__()
        self.setupUi(self)

        #Create QThread to listen for new requests. 
        self.thread1 = QThread()
        #Create worker of SocketListner
        self.worker1 = NewConnectionListener()
        self.worker1.moveToThread(self.thread1)
        #connect signals and slots
        self.thread1.started.connect(self.worker1.run)
        #When Thread sends signal, add client to list of clients
        self.worker1.sockets.connect(self.manageNewConnection) 
        self.worker1.clientMessage.connect(self.broadcast)
        self.worker1.clientToRemove.connect(self.removeFromList)
        
        self.worker1.test.connect(self.serverWelcome) 
        self.thread1.start()

        self.sendMessage_button.clicked.connect(self.sendMessage)
        #Catches print output and forwards to clients.
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
    #Get the message and connection address from the print statement.
    #Broadcast to every client
    def normalOutputWritten(self, text):
        try:
            index = text.index("<")
            index2 = text.index("<",index+1)
            connection = text[index+1:index2-2]
            message = text[index2:]
            self.broadcast(message, connection)
            
        except:
            pass
        
    #Upon detecting a new connection, add them to the list of connected clients,
    #send a welcome message to the client
    # and let everyone know someone new has joined.
    def manageNewConnection(self, connection, address):

        self.addToList(connection, address)
        self.serverWelcome(connection)
        self.broadcast(str(address) + " has joined", connection )
    
    def addToList(self, connection, address):
        #Add client to list
        self.list_of_clients.append(connection)

    def removeFromList(self, client):
        if client in self.list_of_clients:
            self.list_of_clients.remove(client)

    #Sends a message to everyone in the server.
    #Messages consist of who sent them (client var)
    #and the text message (message var)
    def broadcast(self, message, client):
        self.chatDisplay_listWidget.addItem(message)

        for clients in self.list_of_clients:
            if clients != client:
                try:
                    mes = message.encode()
                    clients.send(mes)
                    pass
                except:
                    pass 
    #Used when the server sends a message .
    # Forwards to all clients.  
    def sendMessage(self):
        self.chatDisplay_listWidget.addItem("<YOU> " + self.enterMessage_textBox.toPlainText())
        message = "<SERVER> " + self.enterMessage_textBox.toPlainText()
        
        #Remove new line charachters from text to prevent from breaking the server
        message.replace("\n", "")
        self.enterMessage_textBox.setPlainText("")
        message = message.encode()
        for clients in self.list_of_clients:
            # if clients != client:
                try:
                    clients.send(message)
                    pass
                except:
                    pass 
        
    #Sends welcome message to specific client.
    def serverWelcome(self, connection):
        message = "Welcome to the server"
        
        for clients in self.list_of_clients:
            if clients == connection:
                test = str(connection.send(message)).encode()


#Main start page.
#Allows users to look for nearby devices to connect to
#or choose to host a server.
class StartPage(QMainWindow, Ui_StartingPage):
    def __init__(self):
        super(StartPage, self).__init__()
        self.setupUi(self)
        
        self.button_2.clicked.connect(self.client)
        self.button_3.clicked.connect(self.server)

    #Called when a user attempts to make a connection to join a server
    def client(self):
        #self.listWidget.selectedItems
        for item in self.listWidget.selectedItems():
            print(item.text())
        print("Running client app")
        conn = False
        address = []
        #Get address of selected item
        for item in self.listWidget.selectedItems():
            address = item.text()

        #Address is currently a string in the form: ['INDEX: 3', 'NAME: DESKTOP-EJMNR6P', '6C:94:66:A2:EA:21']
        #Use index and substring to isolate the address at the end
        index1 = address.index("Address: ") +13
        index2 = address.index("'", index1)

        remoteAddress = address[index1:index2]

        #Check for the server service
        service_matches = bluetooth.find_service( address = remoteAddress )

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
            #Can't detect server; quit
            print("Couldn't find the SampleServer service.")
            sys.exit(0)

        port = first_match["port"] 
        name = first_match["name"]
        host = first_match["host"]

        
        client_sock.connect((host, port))

        self.hide()
        self.myChatroom = ChatRoom()
        self.myChatroom.show()
    
    def server(self):
        print("Running server app")
        self.hide()
        self.myChatroom = ChatRoomServer()
        self.myChatroom.show()

if __name__ == '__main__':

    

    app = QApplication(sys.argv)
    varTest = StartPage()
    varTest.show()
    
    

    sys.exit(app.exec_())
