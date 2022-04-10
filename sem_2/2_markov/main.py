# This Python file uses the following encoding: utf-8
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QDesktopWidget
from random import random
import matplotlib.pyplot as plt

import algs

RANDOM_OR_NOT = True
 
class MyWindow(QMainWindow):
    def __init__(self):
        from gui import Ui_MainWindow
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.PRECISION = 3
        self.initUi()

    def initUi(self):
        self.center()
        self.initInputTable()
        self.ui.pushButton_clean.clicked.connect(self.clean)
        self.ui.spinBoxN.valueChanged.connect(self.initInputTable)
        self.ui.pushButton_win.clicked.connect(self.compute)
    
    def initInputTable(self):
        def _fn(x):
            return "{:<5.2f}".format(x)
        self.n = self.ui.spinBoxN.value()
        first_string = [' '.join(['{:^6s}'.format('Si')] + ["S{:<5d}".format(i) for i in range(self.n)])]
        if RANDOM_OR_NOT:
            matrix = self.generateMatrix(self.n)
            # превращаем матрицу в массив строк (как тип данных) строк (как атрибут матрицы)
            for i in range(self.n):
                matrix[i] = " ".join(
                    ["S{:<4d}".format(i)] + [_fn(j) for j in matrix[i]]
                )
            matrix = first_string + matrix
        else:
            matrix = first_string + [' '.join(["S{:<4d}".format(i)] + [_fn(0)] * self.n) for i in range(self.n)]

        self.ui.textEdit_input.setText('\n'.join(matrix)) 
        return

    def getData(self):
        n = self.ui.spinBoxN.value()
        text = self.ui.textEdit_input.toPlainText().split('\n')[1:]
        for i in range(n):
            text[i] = text[i].split()[1:]
            if len(text[i]) != n:
                raise(ValueError)
        for i in range(n):
            for j in range(n):
                text[i][j] = float(text[i][j])

        return text, n

    def drawPlot(self, probabilities, stabilization_time, times, probabilities_over_time):
        for i_node in range(len(probabilities_over_time[0])):
            plt.plot(times, [i[i_node] for i in probabilities_over_time])
            plt.scatter(stabilization_time[i_node], probabilities[i_node])

        plt.legend(range(len(probabilities)))
        plt.xlabel('Время t, c')
        plt.ylabel('Вероятности p')
        plt.show()

    def outputTable(self, times, probs):
        temp = ['Время стабилизации, у.е. (и вероятность p):\n']
        for i in range(len(times)):
            temp.append("t{:d} = {:5.2f} ({:4.2f})\n".format(i, times[i], probs[i]))
        self.ui.textEdit_output.setText( "".join(temp) )
        return

    def compute(self):
        try:
            intensity, n = self.getData()
        except:
            self.ui.textEdit_output.setText( "Не совпадает указанный размер матрицы с фактическим." )
            return
        try:
            probabilities, probs_extended, times, stabilization_time = algs.computeAll(intensity, n)
        except:
            return self.ui.textEdit_output.setText("Некорректный ввод матрицы.")

        self.outputTable(stabilization_time, probabilities)
        self.drawPlot(probabilities, stabilization_time, times, probs_extended)
        return

    def clean(self):
        self.initInputTable()
        self.ui.textEdit_output.clear()

    def generateMatrix(self, n):
        return [
            [round(random(), self.PRECISION) if i != j else 0.0 for j in range(n)] for i in range(n)
        ]

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
    
