import sys, os, select, time
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from threading import Thread
from startingPage import Ui_StartingPage
from chatWindow import Ui_ChatRoom
# from testing import Ui_MainWindow
import bluetooth


class Layer1(QObject):
    print("hi in layers 1")
    progress = pyqtSignal(str)
    i = 0
    def run(self):
        # self.progress.emit("WOW. Pased from layer 1")
        print("holly balls")
    
    
    def forwardMessage(self, str):
        self.progress.emit(str + " From layer 1")

class Layer2(QObject):
    # print("Hi in layer 2")
    potato = pyqtSignal(str)
    def run(self):
        # print("Depest layer")
        val = input()
        self.potato.emit(val)

def printMessage(str):
    print(str)


#Main
thread = QThread()
#Create worker of SocketListner
worker = Layer1()
worker.moveToThread(thread)
#connect signals and slots
thread.started.connect(worker.run)
#don't know how many of these you need
# self.worker.finished.connect(self.thread.quit)
# self.worker.finished.connect(self.worker.deleteLater)
# self.thread.finished.connect(self.thread.deleteLater)
worker.progress.connect(printMessage)
thread.start()


i = 0

def create():

    if i == 0:
        #create thread to manage them
        # # #Start a thread to listenm on this connection
        thread1 = QThread()
        worker1 = Layer2()
        # self.worker2 = clientListener()
        worker1.moveToThread(thread1)
        thread1.started.connect(worker1.run)

        #Upon input from the thread, broadcast message
        worker1.potato.connect(printMessage)
        
        thread1.start()
        
    elif i == 1:
            #create thread to manage them
        # # #Start a thread to listenm on this connection
        thread2 = QThread()
        worker2 = Layer2()
        # self.worker2 = clientListener()
        worker2.moveToThread(thread2)
        thread2.started.connect(worker2.run)

        #Upon input from the thread, broadcast message
        worker2.potato.connect(printMessage)
        thread2.start()
        
    i +=1
for values in range(2):
    create()

app = QApplication(sys.argv)

sys.exit(app.exec_())

