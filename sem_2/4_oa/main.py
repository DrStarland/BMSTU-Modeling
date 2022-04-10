# This Python file uses the following encoding: utf-8
import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QDesktopWidget,QErrorMessage

from random import random, randint, seed
from numpy.random import normal

def event_model(producing, handling, n, repeat_chance):
    seed()
    def dice():
        return randint(1, 100) < repeat_chance

    out_requests = 0
    cur_len = max_len = 0
    events = [ (producing(), 'p') ]
    free_flag, process_flag = True, False

    while out_requests < n:
        event =  events.pop(0)
        if event[1] == 'p':
            cur_len += 1
            if cur_len > max_len:
                max_len = cur_len
            add_event(events, (event[0] + producing(), 'p'))
            if free_flag:
                process_flag = True
        elif event[1] == 'h':
            out_requests += 1
            if dice():
                cur_len += 1
            process_flag = True

        if process_flag:
            if cur_len > 0:
                cur_len -= 1
                add_event(events, (event[0] + handling(), 'h'))
                free_flag = False
            else:
                free_flag = True
            process_flag = False
    return max_len


def add_event(events, event: list):
    i = 0
    while i < len(events) and events[i][0] < event[0]:
        i += 1
    if 0 < i < len(events):
        events.insert(i - 1, event)
    else:
        events.insert(i, event)

def stepModeling(producing, handling, n, repeat_chance, dt):
    seed()
    def dice():
        return randint(1, 100) < repeat_chance

    cur_len, max_len = 0, 0
    free = True
    out_requests = 0
    t = t_waiting = t_proc = t_gen = 0
    while out_requests < n:
        if t > t_gen:
            cur_len += 1
            if cur_len > max_len:
                max_len = cur_len
            t_waiting = t_gen
            t_gen += producing()

        if t > t_proc:
            if cur_len > 0:
                cur_len -= 1
                if free:
                    free = False
                    t_proc = t_waiting
                else:
                    out_requests += 1
                    if dice(): # если заявка идёт в повторную обработку
                        cur_len += 1
                t_proc += handling()
            else:
                free = True
        t += dt
    return max_len

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
        #self.ui.dial_repeats.setValue(0)
        #self.ui.horizontalSlider_quantity.setValue(1000)
        # self.computeQueue()
        

    def connects(self):
        self.ui.dial_repeats.valueChanged.connect(
            lambda x : self.ui.lcdNumber_repeats.display(x)
        )
        self.ui.horizontalSlider_quantity.valueChanged.connect(
            lambda x : self.ui.lcdNumber_quantity.display(x)
        )
        self.ui.pushButton_win.clicked.connect(self.computeQueue)
    
    def test(self, data):
        self.ui.lcdNumber_repeats.display(data)

    def getData(self):
        percent = self.ui.dial_repeats.value()
        n = self.ui.horizontalSlider_quantity.value()
        return percent, n


    def generateUD(self, a, b):
        return a + (b - a) * random()

    def generateNorm(self, mu, sigma):
        return normal(mu, sigma)

    def computeQueue(self):
        self.ui.lineEdit_length.setText("")

        a, b = 0, 10
        mu, sigma = 5, 0.4

        producing_func = lambda : self.generateUD(a, b)
        handling_func = lambda : self.generateNorm(mu, sigma)

        percent, requests = self.getData()
        result_step = [stepModeling(producing_func, handling_func, requests, percent, dt = 0.01) for i in range(5)]
        result_event = [event_model(producing_func, handling_func, requests, percent) for i in range(5)]

        self.outputResults(
            max(result_step),
            max(result_event)
        )
        return

    def outputResults(self, step, event):
        self.ui.lineEdit_length.setText(str(step) + ", " + str(event))
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