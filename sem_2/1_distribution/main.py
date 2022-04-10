# This Python file uses the following encoding: utf-8
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QErrorMessage, QMessageBox
from PyQt5.QtCore    import pyqtSlot, QSize
import pyqtgraph as pg
import numpy as np
from math import sqrt
from scipy.stats import norm

# self.graphicsView = pg.PlotWidget(self.centralwidget, background='white') 

def ud_function(a, b, x):
    result = 1
    if a <= x < b:
        result = (x - a) / (b - a)
    elif x < a:
        result = 0
    return result

def ud_density(a, b, x):
    result = 0
    if a <= x <= b:
        result = 1 / (b - a)
    return result

def norm_function(x, mu, sigma):
    return norm.cdf(x, mu, sqrt(sigma))

def norm_density(x, mu, sigma):
    return norm.pdf(x, mu, sqrt(sigma))

class MyWindow(QMainWindow):
    def __init__(self):
        from gui import Ui_MainWindow
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUi()
        
    def initUi(self):
        self.ui.curve = self.ui.plotView_F.plot(name = "Line", pen=pg.mkPen('r', width=3))
        self.ui.curve2 = self.ui.plotView_f.plot(name = "Line2", pen=pg.mkPen('r', width=3))
        self.ui.pushButton.clicked.connect(self.showPlot)

        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.radioButton_uniform.clicked.connect(
            lambda : self.ui.stackedWidget.setCurrentIndex(0)
        )
        self.ui.radioButton_normal.clicked.connect(
            lambda : self.ui.stackedWidget.setCurrentIndex(1)
        )

    @pyqtSlot()
    def showPlot(self):
        trig = False
        if self.ui.radioButton_uniform.isChecked():
            try:
                a = float(self.ui.lineEdit_A.text())
            except:
                trig = True
                self.showError("Некорректный ввод параметра а!")
            try:
                b = float(self.ui.lineEdit_B.text())
            except:
                trig = True
                self.showError("Некорректный ввод параметра b!")
            if trig:
                return

            if b < a:
                a, b = b, a
            elif a == b:
                self.showError("Невозможно построить графики при таких параметрах.")
                return

            delta = b - a
            x = np.arange(a - delta / 2, b + delta / 2, 0.001)
            y_function = [ud_function(a, b, _x) for _x in x]
            y_density = [ud_density(a, b, _x) for _x in x]

        elif self.ui.radioButton_normal.isChecked():
            try:
                mu = float(self.ui.lineEdit_mu.text())
            except:
                self.showError("Некорректный ввод параметра mu!")
            try:
                sigma = float(self.ui.lineEdit_sigma.text())
            except:
                self.showError("Некорректный ввод параметра sigma!")
            if trig:
                return
            x = np.arange(mu - 10, mu + 10 , 0.001)
            y_function = norm_function(x, mu, sigma)
            y_density = norm_density(x, mu, sigma)
        else:
            print("?_?")
        self.ui.curve.setData(x, y_function)
        self.ui.curve2.setData(x, y_density)
        # pg.plot(x, y, pen=None, symbol='o') 

    def showError(self, text):
        QErrorMessage(self).showMessage(text)

    def showMessage(self, title, text):
        msgBox = QMessageBox(self)
        msgBox.setText(text); msgBox.setWindowTitle(title); msgBox.resize(QSize(400, 200))
        msgBox.exec()

if __name__ == "__main__":
    app = QApplication([])
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
