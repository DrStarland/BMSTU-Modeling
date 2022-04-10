# This Python file uses the following encoding: utf-8
import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QDesktopWidget,QErrorMessage

from model import performModeling


class MyWindow(QMainWindow):
    def __init__(self):
        from gui import Ui_MainWindow
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUi()

    def initUi(self):
        self.center()
        self.connects()  

    def connects(self):
        # self.ui.horizontalSlider_quantity.valueChanged.connect(
        #     lambda x : self.ui.lcdNumber_quantity.display(x)
        # )
        self.ui.pushButton_win.clicked.connect(self.computeQueue)

    def getData(self):
        n = self.ui.horizontalSlider_quantity.value()
        return n

    def computeQueue(self):
        self.ui.lineEdit_length.setText("")
        #requests = self.getData()
        length, score, time, timetable = performModeling()
        self.outputResults(length, time, score)

        self.ui.lineEdit_tutu.setText(str(timetable))
        return

    def outputResults(self, length, time, score):
        hours = str(time // 60)
        minutes = time % 60
        if minutes < 10:
            minutes = '0' + str(minutes)
        else:
            minutes = str(minutes)
        self.ui.lineEdit_length.setText(str(length) + " -- " + hours + ':' + minutes + " -- " + str(score))
        return 

    def showError(self, text):
        QErrorMessage(self).showMessage(text)

    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qr.topLeft())
        return

def main_func():
    print("Start...")
    app = QApplication([])
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main_func()