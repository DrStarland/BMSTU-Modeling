# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(360, 380)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(360, 380))
        MainWindow.setMaximumSize(QtCore.QSize(360, 380))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 0, 341, 321))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.pushButton_win = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_win.setGeometry(QtCore.QRect(10, 250, 321, 31))
        self.pushButton_win.setObjectName("pushButton_win")
        self.lineEdit_length = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_length.setGeometry(QtCore.QRect(10, 90, 321, 31))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        self.lineEdit_length.setFont(font)
        self.lineEdit_length.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_length.setReadOnly(True)
        self.lineEdit_length.setObjectName("lineEdit_length")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 321, 61))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.groupBox = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox.setGeometry(QtCore.QRect(10, 140, 141, 101))
        self.groupBox.setObjectName("groupBox")
        self.dial_repeats = QtWidgets.QDial(self.groupBox)
        self.dial_repeats.setGeometry(QtCore.QRect(70, 20, 71, 71))
        self.dial_repeats.setMinimum(0)
        self.dial_repeats.setProperty("value", 1)
        self.dial_repeats.setOrientation(QtCore.Qt.Vertical)
        self.dial_repeats.setObjectName("dial_repeats")
        self.lcdNumber_repeats = QtWidgets.QLCDNumber(self.groupBox)
        self.lcdNumber_repeats.setGeometry(QtCore.QRect(10, 30, 51, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lcdNumber_repeats.setFont(font)
        self.lcdNumber_repeats.setFrameShape(QtWidgets.QFrame.Box)
        self.lcdNumber_repeats.setLineWidth(2)
        self.lcdNumber_repeats.setDigitCount(2)
        self.lcdNumber_repeats.setProperty("intValue", 1)
        self.lcdNumber_repeats.setObjectName("lcdNumber_repeats")
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_4.setGeometry(QtCore.QRect(170, 139, 161, 101))
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalSlider_quantity = QtWidgets.QSlider(self.groupBox_4)
        self.horizontalSlider_quantity.setGeometry(QtCore.QRect(10, 80, 141, 18))
        self.horizontalSlider_quantity.setMinimum(10)
        self.horizontalSlider_quantity.setMaximum(10000)
        self.horizontalSlider_quantity.setSingleStep(100)
        self.horizontalSlider_quantity.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_quantity.setObjectName("horizontalSlider_quantity")
        self.lcdNumber_quantity = QtWidgets.QLCDNumber(self.groupBox_4)
        self.lcdNumber_quantity.setGeometry(QtCore.QRect(10, 30, 141, 41))
        self.lcdNumber_quantity.setLineWidth(2)
        self.lcdNumber_quantity.setProperty("intValue", 10)
        self.lcdNumber_quantity.setObjectName("lcdNumber_quantity")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(10, 290, 321, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 360, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Lab 4"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Моделирование обслуживающего аппарата"))
        self.pushButton_win.setText(_translate("MainWindow", "Вычислить"))
        self.label_2.setText(_translate("MainWindow", "Длина очереди* при моделировании\n"
"пошаговом, событийном:"))
        self.groupBox.setTitle(_translate("MainWindow", "Повторные заявки, %"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Количество заявок"))
        self.label.setText(_translate("MainWindow", "*при которой заявки не теряются"))
