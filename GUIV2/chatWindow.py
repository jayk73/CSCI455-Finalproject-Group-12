# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chatWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# 

from PyQt5 import QtCore, QtGui, QtWidgets


############
## This is the GUi for the main chatroom window. It only defines the GUI elements;
## The actual functionality for the buttons is provided in Main.py
###########
class Ui_ChatRoom(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(811, 671)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.sendMessage_button = QtWidgets.QPushButton(self.centralwidget)
        self.sendMessage_button.setGeometry(QtCore.QRect(470, 510, 141, 101))
        self.sendMessage_button.setObjectName("sendMessage_button")
        self.enterMessage_textBox = QtWidgets.QTextEdit(self.centralwidget)
        self.enterMessage_textBox.setGeometry(QtCore.QRect(20, 530, 431, 81))
        self.enterMessage_textBox.setObjectName("enterMessage_textBox")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 490, 181, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.quit_Button = QtWidgets.QPushButton(self.centralwidget)
        self.quit_Button.setGeometry(QtCore.QRect(640, 510, 151, 101))
        self.quit_Button.setObjectName("quit_Button")
        self.chatDisplay_listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.chatDisplay_listWidget.setGeometry(QtCore.QRect(20, 10, 771, 491))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chatDisplay_listWidget.sizePolicy().hasHeightForWidth())
        self.chatDisplay_listWidget.setSizePolicy(sizePolicy)
        self.chatDisplay_listWidget.setWordWrap(True)
        self.chatDisplay_listWidget.setObjectName("chatDisplay_listWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 811, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.sendMessage_button.setText(_translate("MainWindow", "Send Message"))
        self.label.setText(_translate("MainWindow", " Type Message Here: "))
        self.quit_Button.setText(_translate("MainWindow", "Quit"))


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
