from scipy import integrate
from numpy import linspace, interp
from math import pi
import matplotlib.pyplot as plt

# раздел ужасных глобальных переменных, зачем? затем.

endTime = 1000
##endTime = 5000
##endTime = 21

h = 1e-6

R = 0.35 # cm
le = 12 # cm
Lk = 187e-6 # Gn
Ck = 268e-6 # F
Rk = 0.25 # Om
U0 = 1400 # V
I0 = 1.2 #  A
Tw = 2000 # K

Rp_I = []

table1 = {'I' : [0.5, 1, 5, 10, 50, 200, 400, 800, 1200],
          'T0' : [6730, 6790, 7150, 7270, 8010, 9185, 10010, 11140, 12010],
          'm' : [0.5, 0.55, 1.7, 3, 11, 32, 40, 41, 39]}

table2 = {'T' : [4e+3, 5e+3, 6e+3, 7e+3, 8e+3, 9e+3,
                   10e+3, 11e+3, 12e+3, 13e+3, 14e+3],
          'get_sigma' : [0.031, 0.27, 2.05, 6.06, 12.0, 19.9,
               29.6, 41.1, 54.1, 67.7, 81.5]}

def f(y, z, Rp):
    return (z - (Rk + Rp) * y) / Lk
    return (z - (0) * y) / Lk
    return (z - (200) * y) / Lk
    return (z - (2) * y) / Lk

def g(y):
    return -y / Ck

def runge_kutta(x, y, z):
    Rp = get_Rp(y)

    k1 = h * f(y, z, Rp)
    q1 = h * g(y)

    k2 = h * f(y + k1 / 2, z + q1 / 2, Rp)
    q2 = h * g(y + k1 / 2)

    k3 = h * f(y + k2 / 2, z + q2 / 2, Rp)
    q3 = h * g(y + k2 / 2)

    k4 = h * f(y + k3, z + q3, Rp)
    q4 = h * g(y + k3)

    y1 = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6
    z1 = z + (q1 + 2 * q2 + 2 * q3 + q4) / 6
    return y1, z1

def interpolate(x, columnX, columnY):
    return interp(x, columnX, columnY)

pi2 = pi * 2
def get_Rp(I):
    z = linspace(0.0, 1.0, 20)
    s = [z * get_sigma(get_T(z, I)) for z in z]
    Rp = le / (pi2 * (R * R) * integrate.simps(s, z))
    Rp_I.append(Rp)
    return Rp

def get_sigma(T):
    return interpolate(T, table2['T'], table2['get_sigma'])

def get_m(I):
    return interpolate(I, table1['I'], table1['m'])

def get_T0(I):
    return interpolate(I, table1['I'], table1['T0'])

def get_T(z, I):
    T0 = get_T0(I)
    return T0 + (Tw - T0) * (z ** get_m(T0))


def plot(timings, first, xlabel, title, legend1):
    plt.plot(timings, first)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.legend((legend1, legend1))
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    I = []; Uc = []; ImultRp_I = []
    T0_I = []

    In = I0; Un = U0
    for t in range(endTime):
        In, Un = runge_kutta(h, In, Un)
        I.append(In)
        Uc.append(Un)
        ImultRp_I.append(In * Rp_I[t])
        T0_I.append(get_T0(In))

    timings = [0, h]
    for i in range(2, endTime):
        timings.append(timings[i - 1] + h)

    temp = max(I)
    print(0.35*temp, temp)

    plot(timings, I, 't', 'I(t)', "Runge-Kutta")
    plot(timings, Uc, 't', 'U(t)', "Runge-Kutta")    
##    plot(timings, Rp_I, 't', 'Rp(t)', "Runge-Kutta")
##    plot(timings, ImultRp_I, 't', 'I(t) * Rp(t)', "Runge-Kutta")
##    plot(timings, T0_I, 't', 'T0(t)', "Runge-Kutta")

    

