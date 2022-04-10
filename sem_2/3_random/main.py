# This Python file uses the following encoding: utf-8
import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QDesktopWidget,QErrorMessage
from random import randint, seed, sample
from math import log
from itertools import islice

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
        self.computeTable()
        self.ui.pushButton_clean.clicked.connect(self.computeTable)
        self.ui.pushButton_win.clicked.connect(self.computeLine)

    def getData(self):
        string = self.ui.lineEdit_input.text().split()
        state = [self.ui.radioButton_1.isChecked(), self.ui.radioButton_2.isChecked(), self.ui.radioButton_3.isChecked() ]
        state = state.index(True)
        bounds = [ lambda x : 0 <= x <= 9,  lambda x : 10 <= x <= 99, lambda x : 100 <= x <= 999 ]

        try:
            for i, number in enumerate(string):
                temp = int(number)
                if not bounds[state](temp):
                    self.showError("Некорректная размерность одного или нескольких чисел.")
                    return
                string[i] = temp     
        except:
            self.showError("Некорректный ввод чисел.")
            return
       
        return string

    # определение с помощью собственной информации
    def randomnessMeasure(self, numbers):
        n = float(len(numbers))
        if n == 0: return 0.
        # если не отсечь такой случай, получится 
        # основание логарифма, равное единице
        if n == 1: return 1.

        occurrences = {}
        for num in numbers:
            if not (num in occurrences.keys()):
                occurrences.update({num: 1})
            else: occurrences[num] += 1
        
        measure = 0.
        for num in occurrences.keys():
            p = occurrences[num] / n
            measure -= p * log(p, n)
    
        return measure

    def computeLine(self):
        data = self.getData()
        if data:
            res = self.randomnessMeasure(data)
            self.outputLine(res)
        return

    def computeTable(self):
        seed()
        digit1_alg = [randint(0, 9) for i in range(1000)]
        digit2_alg = [randint(10, 99) for i in range(1000)]
        digit3_alg = [randint(100, 999) for i in range(1000)]
        
        try:
            numbers = set()
            with open("source.txt", "rt") as fp:
                digit1_tab = [randint(0, 9) for i in range(1000)]
                digit2_tab = [randint(10, 99) for i in range(1000)]
                digit3_tab = [randint(100, 999) for i in range(1000)]

                lines = islice(fp, 3000)
                for line in lines:
                    numbers.update(set(line.split(" ")[1:]))
                numbers.remove("") 
                numbers = list(numbers)[:3000]
                digit1_tab = list(map(lambda x : int(x) % 10, numbers[0:1000]))          
                digit2_tab = list(map(lambda x : 10 + int(x) % 90, numbers[1000:2000])) 
                digit3_tab = list(map(lambda x : 100 + int(x) % 900, numbers[2000:3000]))
                fp.close()
        except:
            digit1_tab = [0 for i in range(1000)]
            digit2_tab = [10 for i in range(1000)]
            digit3_tab = [100 for i in range(1000)]

        coef_alg = [self.randomnessMeasure(digit1_alg), self.randomnessMeasure(digit2_alg), self.randomnessMeasure(digit3_alg)]
        coef_tab = [self.randomnessMeasure(digit1_tab), self.randomnessMeasure(digit2_tab), self.randomnessMeasure(digit3_tab)]

        self.outputTable(digit1_alg, digit2_alg, digit3_alg, digit1_tab, digit2_tab, digit3_tab)
        self.outputCoef(coef_alg, coef_tab)
        return

    def outputLine(self, line):
        text = " " * 5 + "{:^6.3g}".format(line * 10)
        self.ui.lineEdit_coef.setText(text)
        return

    def outputTable(self, d1_alg, d2_alg, d3_alg, d1_tab, d2_tab, d3_tab):
        h1, h2, h3 = 1, 2, 3
        head1, head2  = "Алгоритм", "Таблица"
        # регулировка отступа от левого края: TextEdit не позволяет штатными 
        # способами выровнять по центру мою таблицу
        spaces = " " * 5

        n = 10
        d1_alg = sample(d1_alg, n)
        d2_alg = sample(d2_alg, n)
        d3_alg = sample(d3_alg, n)
        d1_tab = sample(d1_tab, n)
        d2_tab = sample(d2_tab, n)
        d3_tab = sample(d3_tab, n)

        text = [ f"{spaces} {'_' * 37} ", "{:s}|{:_^18s}|{:_^18s}|".format(spaces, head1, head2),
                 "{0:s}|{1:_^5d}|{2:_^6d}|{3:_^5d}|{1:_^5d}|{2:_^6d}|{3:_^5d}|".format(spaces, h1, h2, h3)]
        for a, b, c, d, e, f in zip(d1_alg, d2_alg, d3_alg, d1_tab, d2_tab, d3_tab):
            text.append("{:s}|{:^5d}|{:^6d}|{:^5d}|{:^5d}|{:^6d}|{:^5d}|".format(spaces, a, b, c, d, e, f))
        self.ui.textEdit_output.setText("\n".join(text))
        return 0

    def outputCoef(self, coef_alg, coef_tab):
        spaces = " " * 3 + '|'
        text = [ spaces ]

        for i in coef_alg + coef_tab:
            text.append("{:^6.3g}|".format(i * 10))
        self.ui.lineEdit_table_coef.setText(''.join(text))
        return

    def clean(self):
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
    
