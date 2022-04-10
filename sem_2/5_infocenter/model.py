# This Python file uses the following encoding: utf-8
from random import random
from functools import partial

computer_handling_times = (15.0, 30.0)
# кортеж вида (ожидаемое время, +- разброс)
operator_handling_times = ((20.0, 5.), (40., 10.), (40., 20.))
clients_arriving_time = (10., 2.)

def generateUD(a, b):
    return a + (b - a) * random()

class Operator():
    def __init__(self, times : tuple, storage : list):
        self.free = True
        a, b = times[0] - times[1], times[0] + times[1]
        self.handling = partial(generateUD, a = a, b = b)
        self.storage = storage
    
    def is_free(self):
        return self.free

    def acceptTask(self, current_time):
        # по условию компьютер выполняет работу за константное время
        self.end_time = current_time + self.handling()
        self.free = False

    def completeTask(self):
        # отправка обработанной заявки в накопитель приписанного 
        # за работником компьютера
        self.storage.append(self.end_time)
        self.free = True
        return self.free

    def finishedWorking(self, current_time):
        if self.is_free() or current_time <= self.end_time:
            return False
        return self.completeTask()

class Computer():
    def __init__(self, handling_time=5.):
        self.handling_time = handling_time
        self.request_storage = list()
        self.free = True

    def is_free(self):
        return self.free

    def acceptTask(self, current_time):
        # по условию компьютер выполняет работу за константное время
        self.end_time = current_time + self.handling_time
        self.request_storage.pop(0)
        self.free = False

    def completeTask(self):
        self.free = True
        return self.free

    def finishedWorking(self, current_time):
        if current_time <= self.end_time:
            return False
        return self.completeTask()

    # проверка наличия в накопителе доступных для обработки заявок
    def checkForRequests(self, current_time):
        if self.is_free():
            if self.request_storage:
                self.acceptTask(current_time)
        else:
            # компьютер способен сразу приступить к следующей задаче, как только выполнена
            # текущая. именно это отражает рекурсивный вызов в этой ветке
            if self.finishedWorking(current_time):
                self.checkForRequests(current_time)
            return

# клиент, точнее, генератор потока клиентов, описывается двумя функциями и
# данными о времени появления людей в информационном центре
produceClientTime = partial(generateUD, a = 8., b = 12.)
def choice_operator(operators):
    for i, operator in enumerate(operators):
        if (operator.is_free()):
            return i
    return None

def getComputers():
    return (
        Computer(computer_handling_times[0]),
        Computer(computer_handling_times[1])
    )

def getOperators(computers : tuple):
    return (
        Operator(operator_handling_times[0], computers[0].request_storage),
        Operator(operator_handling_times[1], computers[0].request_storage), 
        Operator(operator_handling_times[2], computers[1].request_storage)
    )

# время измеряется в минутах
def stepModeling(n=300, dt=0.01):
    computers = getComputers()
    operators = getOperators(computers)

    denied_requests = processed_requests = 0
    t = arrival_time = 0
    while (denied_requests + processed_requests) < n:
        if t > arrival_time:
            ind = choice_operator(operators)
            if ind is not None: operators[ind].acceptTask(t)
            else: denied_requests += 1
            arrival_time += produceClientTime()

        for oper in operators:
            if oper.finishedWorking(t):
                processed_requests += 1

        for comp in computers:
            comp.checkForRequests(t)
                
        t += dt
    # дожигаем оставшиеся в компьютерах заявки вне основного цикла, если 300 запросов
    # люди обработали раньше, чем компьютеры выполнили свою работу
    while [comp.is_free() for comp in computers].count(False):
        for comp in computers:
            comp.checkForRequests(t)
        t += dt

    return processed_requests, denied_requests

def performModeling(repeats=1, n=300, dt=0.01):
    def _func():
        processed_requests, denied_requests = stepModeling(n, dt)
        return denied_requests / (denied_requests + processed_requests)

    result_probabilty = [
        round(_func(), 3) for _ in range(repeats)
    ]

    return max(result_probabilty)

    

def test_func():
    print(performModeling())
    return 0

if __name__ == "__main__":
    test_func()