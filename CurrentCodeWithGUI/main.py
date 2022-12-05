import sys, os, select
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from threading import Thread
from startingPage import Ui_StartingPage
from chatWindow import Ui_ChatRoom
# from testing import Ui_MainWindow
import bluetooth

client_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
server_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )

#For a client connection; thread to listen for incoming messages from the server
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
        


#Server thread. Listens for new threads appearnig from server    
class NewConnectionListener(QObject):
    # progress = pyqtSignal(str)
    sockets = pyqtSignal(bluetooth.BluetoothSocket, tuple)
    test = pyqtSignal(bluetooth.BluetoothSocket, str)
    clientMessage = pyqtSignal(bluetooth.BluetoothSocket)

    def run(self):
        while True:
            connection, address = server_sock.accept()
            print("accepting connection")
            
            #Maintain a list of clients so you can broadcast messages to all clients
            self.sockets.emit(connection, address)

            #Welcome them to the server 
            self.test.emit(connection, "Welcome to the server!")

#Server listens to a specifc connection for mesages from client          
class clientListener(QObject):
    progress = pyqtSignal(str)
    sockets = pyqtSignal(str, bluetooth.BluetoothSocket)
    remover = pyqtSignal(bluetooth.BluetoothSocket)
    
    def __init__(self, conn, address, parent = None):
        super(clientListener, self).__init__()
        self.conn = conn
        self.addr = address

        self.run(conn, self.addr)

    def run(self, conn, addrr):
        print("Running")
        print(conn)
        
        while True:
            try:
                data = conn.recv(1024).decode()
                if data:
                    print ("<" + addrr[0] + "> " + data)
                    message_to_send = ("<" + addrr[0] + "> " + data)
                    # broadcast(message_to_send, connection)
                    self.sockets.emit(message_to_send, conn)
                else:
                    # remove(connection)
                    self.remover.emit(conn)
                    print("Removing connection")
                    break
            except:
                continue


class ChatRoom(QMainWindow, Ui_ChatRoom):
    def __init__(self):
        super(ChatRoom, self).__init__()
        
        self.setupUi(self)
        #Create QThread
        self.thread = QThread()
        #Create worker of SocketListner
        self.worker = ClientSocketListener()
        self.worker.moveToThread(self.thread)
        #connect signals and slots
        self.thread.started.connect(self.worker.run)
        #don't know how many of these you need
        # self.worker.finished.connect(self.thread.quit)
        # self.worker.finished.connect(self.worker.deleteLater)
        # self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.printMessge)
        self.thread.start()

        #send the message from the txtbox to the server.
        #Print the message to the listview
        self.sendMessage_button.clicked.connect(self.sendMessage)

    def printMessge(self, message, conn):
        print("In other: " + message)
        self.chatDisplay_listWidget.addItem(message)
        # self.chatDisplay_listWidget.repaint()
        # val = self.chatDisplay_listWidget.count()
        # print("Val is "+ val)
        # QApplication.processEvents()
        # QCoreApplication.processEvents()
        
        print('sending message: ' + message)

    def sendMessage(self):
        
        message = self.enterMessage_textBox.toPlainText()
        print("Sending message: " + message)
        #Remove new line charachters from text to prevent from breaking the server
        message.replace("\n", "")
        self.enterMessage_textBox.setPlainText("")

        client_sock.send(message)
        self.chatDisplay_listWidget.addItem("<YOU> " + message)
    
class ChatRoomServer(QMainWindow, Ui_ChatRoom):
    list_of_clients = []
    def __init__(self):
        super(ChatRoomServer, self).__init__()
        self.setupUi(self)

        port = 5 #arbitrary number, there is code to serach for an available port
        server_sock.bind(("",port))
        server_sock.listen(10) #Allows up to 10 active connections

        #Create QThread to listen for new requests. 
        self.thread1 = QThread()
        #Create worker of SocketListner
        self.worker1 = NewConnectionListener()
        self.worker1.moveToThread(self.thread1)
        #connect signals and slots
        self.thread1.started.connect(self.worker1.run)
        #When Thread sends signal, add client to list of clients
        self.worker1.sockets.connect(self.addToList) 
        self.worker1.test.connect(self.serverWelcome) 
        self.thread1.start()

        self.sendMessage_button.clicked.connect(self.sendMessage)
        
    def addToList(self, connection, address):
        #Add client to list
        self.list_of_clients.append(connection)
        print("Current List: ")
        for val in self.list_of_clients:
            print(val)

        # #Start a thread to listenm on this connection
        # self.thread2 = QThread()
        # self.worker2 = clientListener(connection, address)
        # self.worker2.moveToThread(self.thread2)
        # self.thread2.started.connect(self.worker2.run)

        # #Upon input from the thread, broadcast message
        # self.worker2.sockets.connect(self.broadcast)
        # self.worker2.remover.connect(self.removeFromList)

        # self.thread2.start()
        print("Added to list")


    def removeFromList(self, client):
        if client in self.list_of_clients:
            self.list_of_clients.remove(client)
    #For forwarding a message from one client to others
    def broadcast(self, message, client):
        for clients in self.list_of_clients:
            # if clients != client:
                try:
                    clients.send(message).encode()
                    pass
                except:#for some reason always goes into except state, even when message is sent correctly
                    pass 

    def sendMessage(self):
        message = self.enterMessage_textBox.toPlainText()
        print("Sending message: " + message)
        #Remove new line charachters from text to prevent from breaking the server
        message.replace("\n", "")
        self.enterMessage_textBox.setPlainText("")
        for clients in self.list_of_clients:
            # if clients != client:
                try:
                    clients.send(message).encode()
                    pass
                except:#for some reason always goes into except state, even when message is sent correctly
                    pass 
        # client_sock.send(message)
        self.chatDisplay_listWidget.addItem("<YOU> " + message)

    def serverWelcome(self, connection):
        message = "Welcome to the server"
        print("Sending welcome message")#debugging
        for clients in self.list_of_clients:
            if clients == connection:
                connection.send(message).encode()
                print("Sending " + message + " to " + str(clients))



class StartPage(QMainWindow, Ui_StartingPage):
    def __init__(self):
        super(StartPage, self).__init__()
        self.setupUi(self)
        
        self.button_2.clicked.connect(self.client)
        self.button_3.clicked.connect(self.server)

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
        index1 = address.index("Address: ") +9
        index2 = address.index("'", index1)

        remoteAddress = address[index1:index2]

        while conn != True:
            # print("Address is " + address)
            # print("Remote is is " + remoteAddress)
            #Attempt to form connection
            try:
                port = 5
                
                client_sock.connect((remoteAddress, port))
                conn = True
            except:
                # print("Failed to connect")
                #Let user pick a different port
                busyWait = 5 + 1


        self.hide()
        self.myChatroom = ChatRoom()
        self.myChatroom.show()
    
    def server(self):
        print("Running server app")
        self.hide()
        self.myChatroom = ChatRoomServer()
        self.myChatroom.show()

if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # w = StartPage()
    # w.show()
    # sys.exit(app.exec_())
    

    app = QApplication(sys.argv)
    varTest = StartPage()
    varTest.show()
    
    

    sys.exit(app.exec_())
    # w = myWindow()
    # w.show()
    # sys.exit(app.exc_())