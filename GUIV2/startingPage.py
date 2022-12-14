# # -*- coding: utf-8 -*-

# # Form implementation generated from reading ui file 'test2.ui'
# #
# # Created by: PyQt5 UI code generator 5.15.7
# #




from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread,  pyqtSignal


########
#This is the code for the starting page GUI. It provide the GUI elements.
# It also provides functionality for the "Search for bluetooth Devices button".
# The code for the "Host Server" and "Attempt Connection" buttons is
# Defined in Main.py
########

import bluetooth, time

#Used to store the list of detected devices.
my_list = []

#Thread which loooks for bluetooth devices nearby. Emits a signal to the main 
#thread for Every device found.
class searchWorker(QObject):
    finished = pyqtSignal()
    numDevices = pyqtSignal(int)
    progress = pyqtSignal(object)
    
    def run(self):
        nearby_devices = bluetooth.discover_devices(
        duration=2, lookup_names=True, flush_cache=True, lookup_class=False)
        
        print("found %d device(s)" % len(nearby_devices))

        i = 1
        for addr, name in nearby_devices:    
            try:

                self.progress.emit(  ["INDEX: " + str(i), "NAME: " + name, "Address: " ,  addr]  )

                i += 1
            except UnicodeEncodeError:

                self.progress.emit(  ["INDEX: " + str(i) , "NAME: " + name.encode('utf-8', 'replace'),"Address: " ,  addr]  )

                i += 1
        time.sleep(2)
        self.finished.emit()


# For each detected device, look for any services it finds. If it 
# Provides a server, emit a signal "GoodProgress". If not, emit the 
# signal "BadProgress"
class serviceSearcher(QObject):
    finished = pyqtSignal()
    goodProgress = pyqtSignal(str)
    badProgress = pyqtSignal(str)
    
    def run(self):
        print("Elemetns to look at " +  str(len(my_list))  )
        for element in my_list:
            addressToSearch = element[3]
            services = bluetooth.find_service( address = addressToSearch )
            if len(services) <=0:
                print("no server found :( on " + str(element))
                self.badProgress.emit( str(element)  )
            else:
                for ser in services:
                    if  "SampleServer" in str(  ser["name"]   ) :
                        print("Found Running server in " + str(element) )
                        # first_match = ser
                        self.goodProgress.emit( str(element) )

        

class Ui_StartingPage(object):
    
    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(810, 615)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.search_Button = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.searching())
        self.search_Button.setGeometry(QtCore.QRect(20, 30, 221, 131))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.search_Button.setFont(font)
        self.search_Button.setObjectName("search_Button")
        self.button_2 = QtWidgets.QPushButton(self.centralwidget)
        self.button_2.setGeometry(QtCore.QRect(20, 200, 221, 131))
        self.button_2.setDisabled(True)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.button_2.setFont(font)
        self.button_2.setObjectName("button_2")
        self.button_3 = QtWidgets.QPushButton(self.centralwidget)
        self.button_3.setGeometry(QtCore.QRect(20, 370, 221, 131))
        # self.button_3.setDisabled(True)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.button_3.setFont(font)
        self.button_3.setObjectName("button_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(280, 0, 341, 71))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget, itemClicked = lambda: self.presentButton())
        self.listWidget.setGeometry(QtCore.QRect(280, 70, 511, 471))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setObjectName("listWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 810, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    


    def searching(self):

        #Clear CURRENT LIST 
        self.listWidget.clear()

        self.label.setText("Searching for nearby devices .... ")
        
        #Thread declaration to search for devices.
        #Declare QThread
        self.thread = QThread()
        #Declare Worker
        self.worker = searchWorker()
        #Move Worker to thread
        self.worker.moveToThread(self.thread)
        #make connection to worker in thread
        self.thread.started.connect(self.worker.run)
        #Setup responses to worker signals
        
        self.worker.progress.connect(self.newDevice) #A new device has connected. Add to list
        self.worker.finished.connect(self.allFound) #Worker claims no more devices discovered

        self.thread.start()

        #Thread delcaration to serach for servers.
        self.serverThread = QThread()
        self.serverWorker = serviceSearcher()
        self.serverWorker.moveToThread(self.serverThread)
        self.thread.started.connect(self.serverWorker.run)

        self.serverWorker.goodProgress.connect(self.serviceFound)
        self.serverWorker.badProgress.connect(self.noServiceFound)

    #called each time searchWorker finds a device
    def newDevice(self, newClient):
        my_list.append(newClient)
        self.listWidget.addItem(str(newClient))

    #called when searchWorker has found all devices
    def allFound(self):
        self.label.setText("Searching for servers......")
        
        #Start searching for services.
        self.serverThread.start()
       
    #Called every time a server is found.
    #update the bluetooth device in the list
    #To let users know a server was found.
    def serviceFound(self, element):
        
        findItem = self.listWidget.findItems(str(element), QtCore.Qt.MatchContains)
        for it in findItem:
            it.setText("Found Server: " + str(element) )

    #Called every time a server isn't found.
    #update the bluetooth device in the list
    #To let users know there is no server.
    def noServiceFound(self, element):
        
        findItem = self.listWidget.findItems(str(element), QtCore.Qt.MatchContains)
        for it in findItem:
            it.setText("No server :( " + str(element) )
       
                  
    #Once a user selects a device to connect to, the "Attempt Connection"
    #Button is enabled.
    def presentButton(self):
        self.button_2.setEnabled(True)
        
    def hostServer(self):
        self.hide()




    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.search_Button.setText(_translate("MainWindow", "Search For\n"
" Bluetooth Devices"))
        self.button_2.setText(_translate("MainWindow", "Attempt Connection\n"
" to Selected Device"))
        self.button_3.setText(_translate("MainWindow", "Host Server"))
        self.label.setText(_translate("MainWindow", "Nearby Devices"))