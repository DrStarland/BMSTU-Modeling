# This Python file uses the following encoding: utf-8
from random import random, randint
from functools import partial
from numpy.random import normal

def generateUD(a, b):
    return a + (b - a) * random()

def generateNorm(mu, sigma):
    return normal(mu, sigma)

def dice(chance):
    return randint(0, 99) < chance

class Car():
    """
    w - wait - автомобиль в ожидании возможности поехать
    g - going - в движении
    """
    @classmethod
    def genTime(cls, state):
        if state == "g":
            return abs(normal(0.1, 0.05))
        else:
            return abs(normal(0.4, 0.05))

    def __init__(self, priority=None, state="w"):
        self.requaired_time = self.genTime(state)
        self.state = state
        self.end_time = 0
        self.priority = priority

    def setRequiredTime(self, time):
        self.requaired_time = time

    def setEndTime(self, current_time):
        self.end_time = current_time + self.requaired_time

    def getEndTime(self):
        return self.end_time

    def stillGoing(self, current_time):
        return (current_time <= self.end_time)

    # def alreadyGone(self, current_time):
    #     if 

class Train():
    """
    Поезд всегда в движении, без вариаций состояния
    """
    @classmethod
    def genTime(cls):
        return generateNorm(5.4, 1.)

    def __init__(self, current_time=None):
        self.requaired_time = self.genTime()
        if current_time is not None:
            self.setEndTime(current_time)
        self.end_time = 0

    def setEndTime(self, current_time):
        self.end_time = current_time + self.requaired_time

    def getEndTime(self):
        return self.end_time

    def stillGoing(self, current_time):
        return (current_time <= self.end_time)

car_passed = 0
train_passed = 0
class Crossing():
    def __init__(self):
        self.opened = True # состояние шлагбаума -- зависит от поезда
        self.free = True # не перегорожен ли переезд для автомобиля другим автомобилем
        self.end_time = 0
        self.train = None 
        self.car = None

    def is_open(self):
        return self.opened

    def is_free(self):
        return self.free

    def closeBarrier(self):
        self.opened = False
        return self.is_open()

    def openBarrier(self):
        self.opened = True
        return self.is_open()

    def trainPassed(self, current_time):
        # при появлении поезда у машины ещё есть время до закрытия шлагбаума,
        # чтобы завершить своё движение
        # if not self.is_free():
        #     self.carPassed(current_time)

        if self.is_open() or self.train.stillGoing(current_time):
            return False
        return self.trainGone()

    def trainGone(self):
        self.train = None
        self.openBarrier()
        global train_passed
        train_passed += 1
        return True

    def carGone(self):
        self.free = True
        global car_passed 
        car_passed += 1
        return True 

    def carPassed(self, current_time):
        if self.is_free() or not self.car or self.car.stillGoing(current_time):
            return False
        return self.carGone()

    def acceptCar(self, car : Car, current_time): 
        if self.is_free() and self.is_open():
            car.setEndTime(current_time)
            self.car = car
            self.free = False
            

    def acceptTrain(self, train : Train, current_time):
        train.setEndTime(current_time)
        if not self.is_open():
            if self.end_time < train.getEndTime():
                self.end_time = train.getEndTime()
                self.train = train
        else:
            self.end_time = train.getEndTime()
            self.train = train
            self.closeBarrier()

# 2 +- 0.5
cars_time = (0.2, 1.1)
glob_car_counter = 0
class Street():
    @classmethod
    def genTime(cls):
        return generateUD(cars_time[0], cars_time[1])

    def __init__(self, probability):
        self.street_queue = []
        self.state = 'g'
        self.arrival_time = 0

    def __bool__(self):
        return len(self.street_queue) != 0

    def addCar(self, current_time):
        global glob_car_counter
        glob_car_counter += 1

        self.street_queue.append(Car(state=self.state))
        self.arrival_time = current_time + self.genTime()

    def getCar(self, current_time):
        car = self.street_queue.pop(0)
        if self.state == 'w':
            self.move()
        return car

    def move(self):
        self.state = 'g'
        self.updateState

    def stop(self):
        self.state = 'w'
        self.updateState

    def updateState(self):
        for car in self.street_queue:
            car.state = self.state


class Entrance():
    def __init__(self, main_prob=65, side_prob=35):
        self.main = Street(main_prob)
        self.side = Street(side_prob)
        self.main_prob = main_prob
        self.side_prob = side_prob


    def produceCars(self, current_time):
        if current_time > self.main.arrival_time:
            self.main.addCar(current_time)

        if current_time > self.side.arrival_time:
            self.side.addCar(current_time)

    def releaseCar(self, current_time):
        if self.main and not self.side:
            car = self.main.getCar(current_time)
            self.side.stop()
            return car
        elif not self.main and self.side:
            car = self.side.getCar(current_time)
            self.main.stop()
            return car
        elif self.main and self.side:
            main_priority = dice(self.main_prob)
            if main_priority:
                car = self.main.getCar(current_time)
                self.side.stop()
            else:
                car = self.side.getCar(current_time)
                self.main.stop() 
            return car
        else:
            return None


class Rails():
    def genTime(self):
        #print("dlina", len(timetable))
        if self.timetable:
            hours = self.timetable.pop(0) * 60
            minutes = self.timetable.pop(0)
            return hours + minutes
        else:
            return 9999999999

    def __init__(self, timetable):
        self.timetable = timetable
        self.queue = []
        self.arrival_time = 0

    def produceTrains(self, current_time):
        if self.arrival_time < current_time:
            self.addTrain()

    def addTrain(self):
        self.queue.append(Train())
        self.arrival_time = self.genTime()

    def getTrain(self, current_time):
       # print("get train", self.arrival_time, current_time)
        if self.arrival_time < current_time + 0.5:
            if self.queue:
                return self.queue.pop(0)
        return None
        
timetable = [
    4,28, 4,46, 5,4, 5,25, 5,40, 5,51, 6,4, 6,9, 6,22, 6,34, 6,40, 6,48, 
    6,54, 7,5, 7,13, 7,28, 7,40, 7,45, 7,51, 8,6, 8,16
]



# время измеряется в минутах
# извиняюсь за плохой в плане оформления код, пишу в спешке...
def stepModeling(timetable, n=300, dt=0.01):
    #computers = getComputers()
    #operators = getOperators(computers)
    railcrossing = Crossing()
    entrance = Entrance()
    rails = Rails(timetable)

    denied_requests = processed_requests = 0
    t = 0
    max_len = 0
    global cars_time
    while t < 540.0:
        # генерация объектов
        rails.produceTrains(t)
        if (len(entrance.side.street_queue) + len(entrance.main.street_queue) > 150):
            cars_time = (6., 9.)
        if (len(entrance.side.street_queue) + len(entrance.main.street_queue) < 100): 
            cars_time = (0.2, 1.1)
        entrance.produceCars(t)
        
        # обработка

        if railcrossing.is_open() and railcrossing.is_free():
            car = entrance.releaseCar(t)
            if car:
                railcrossing.acceptCar(car, t)

        train = rails.getTrain(t)
        if train:
            railcrossing.acceptTrain(train, t)

        railcrossing.trainPassed(t)
        railcrossing.carPassed(t)

        if len(entrance.side.street_queue) + len(entrance.main.street_queue) > max_len:
            max_len = len(entrance.side.street_queue) + len(entrance.main.street_queue)
            record_time = t

        # подготовка к следующему этапу     
        t += dt

    record_time = int(record_time)
    # print("Макс очередь: ", max_len,
    #     "Осталось в пробках:", len(entrance.side.street_queue) + len(entrance.main.street_queue),
    #     "Машин проехало:", car_passed,
    #     "Поездов уехали и ждут", train_passed, len(rails.queue)
    #     )
    # print(f"Хуже всего пробка в {record_time // 60}:{record_time % 60}")

    return max_len, car_passed, record_time, [
    4,28, 4,46, 5,4, 5,25, 5,40, 5,51, 6,4, 6,9, 6,22, 6,34, 6,40, 6,48, 
    6,54, 7,5, 7,13, 7,28, 7,40, 7,45, 7,51, 8,6, 8,16
]

def performModeling(repeats=1, n=300, dt=0.01):
    timetable = [
        4,28, 4,46, 5,4, 5,25, 5,40, 5,51, 6,4, 6,9, 6,22, 6,34, 6,40, 6,48, 
        6,54, 7,5, 7,13, 7,28, 7,40, 7,45, 7,51, 8,6, 8,16
    ]

    global car_passed
    car_passed = 0
    return stepModeling(timetable, dt=dt)

    

def test_func():
    # test = [True] * 3
    # №print(test.count(False))
    # print(test.index(True))

    stepModeling(dt=0.1)
    return 0

if __name__ == "__main__":
    test_func()