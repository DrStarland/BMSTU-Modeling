from matplotlib import pyplot as plt
import numpy as np
from math import sin, cos

length = 10
T0 = 300
R = 0.5
F0 = 50
alpha0 = 0.05
alphaN = 0.01

h = 1e-3
N = int(length / h)
t = 0.5

a1 = 0.0134; b1 = 1; c1 = 4.35e-4; m1 = 1
a2 = 2.049; b2 = 0.563e-3; c2 = 0.528e5; m2 = 1

ab1 = a1 * b1
ac1 = a1 * c1
# поскольку m1 и m2 == 1, нет смысла явно прописывать
# операцию возведения в степень
def k(T):
    # a1 * (b1 + c1 * T ** m1)
    return ab1 + ac1 * T

def c(T):
    # a2 - (c2 / (T * T)) + b2 * T ** m2 
    return a2 - (c2 / (T * T)) + b2 * T

d = (alphaN * length) / (alphaN - alpha0)
c_local = -alpha0 * d
def alpha(x):
    return c_local / (x - d)

def p(x):
    return 2 * alpha(x) / R

def f(x):
    # 2 * alpha(x) / R * T0
    #return 50.0
    return p(x) * T0

def cappa_plus(x, step, func):
    return (func(x) + func(x + step)) / 2

def cappa_minus(x, step, func):
    return (func(x) + func(x - step)) / 2

hdiv8 = h / 8
hdiv4 = h / 4
def left(Ts):
    cappaPlustc = cappa_plus(Ts[0], t, c)
    cappaPlustk = cappa_plus(Ts[0], t, k)
    cTs0 = c(Ts[0])
    ph2 = p(h / 2)

    K0 = hdiv8 * cappaPlustc + hdiv4 * cTs0 + \
        cappaPlustk * t / h + t * (hdiv8 * ph2 + hdiv4 * p(0))
    M0 = hdiv8 * cappaPlustc - cappaPlustk * t / h + t * h * ph2 / 8
    P0 = hdiv8 * cappaPlustc * (Ts[0] + Ts[1]) + \
         hdiv4 * cTs0 * Ts[0] + t * (F0 + hdiv8 * (3 * f(0) + f(h)))
    return K0, M0, P0

def right(Ts):
    cappaMinustc = cappa_minus(Ts[-1], t, c)
    cappaMinustk = cappa_minus(Ts[-1], t, k)

    KN = hdiv8 * cappaMinustc + hdiv4 * c(Ts[-1]) + \
         cappaMinustk * t / h + t * alphaN + \
         t * hdiv8 * p(length - h / 2) + t * hdiv4 * p(length)
    MN = hdiv8 * cappaMinustc - cappaMinustk * t / h + \
         t * h * p(length - h / 2) / 8
    PN = hdiv8 * cappaMinustc * (Ts[-1] + Ts[-2]) + \
         hdiv4 * c(Ts[-1]) * Ts[-1] + t * alphaN * T0 + \
         t * hdiv4 * (f(length) + f(length - h / 2))
    return KN, MN, PN


def progonka(A, B, C, D, K0, M0, P0, KN, MN, PN):
    xi = [0, -M0 / K0]
    eta = [0, P0 / K0]

    for n in range(1, N + 1):
        znam = B[n] - A[n] * xi[n]
        xi.append(C[n] / znam)
        eta.append((D[n] + A[n] * eta[n]) / znam)

    y = np.empty(n + 1, dtype=np.double)
    y[n] = (PN - MN * eta[n]) / (KN + MN * xi[n])
    for i in range(n, 0, -1):
        y[i - 1] = xi[i] * y[i] + eta[i]
    return y

def cond1(T, T_new):
    for t, ts in zip(T, T_new):
        if abs((t - ts) / ts) < 1e-4:
            return False
    return True

def cond2(T, Ts):
    for t, ts in zip(T, Ts):
        if abs((ts - t) / ts) > 1e-2:
            return True
    return False

def calc_iteration(Ts):
    K0, M0, P0 = left(Ts)
    KN, MN, PN = right(Ts)

    A = np.empty(N + 1, dtype=np.double)
    B = np.empty(N + 1, dtype=np.double)
    C = np.empty(N + 1, dtype=np.double)
    D = np.empty(N + 1, dtype=np.double)

    x = np.arange(0, length + h, h)
    tdivh = t / h
    tmulh = t * h
    for n in range(1, N + 1):
        Tn = Ts[n]
        cTmulh = c(Tn) * h
        A[n] = tdivh * cappa_minus(Tn, t, k)
        C[n] = tdivh * cappa_plus(Tn, t, k)
        B[n] = A[n] + C[n] + cTmulh + p(x[n]) * tmulh
        D[n] = f(x[n]) * tmulh + cTmulh * Tn
    
    return progonka(A, B, C, D, K0, M0, P0, KN, MN, PN)

def calc_slice(alpha, ys0, maxIter = 25):
    i = 0
    ys = calc_iteration(ys0)
    while cond1(ys0, ys) and i < maxIter: 
        ys0 = ys
        ys = (1.0 - alpha) * ys0 + alpha * calc_iteration(ys0)
        i += 1
    return ys

def calc_model(T):
    global F0
    time = 0.0; count = 0
    # F0 = 20
    res = [T]
    Ts = calc_slice(0.7, T)
    res.append(Ts)
    time += t
    
    while cond2(T, Ts) and count < 50:
        #F0 += 2 * time ** 2 #15 * sin(time) #
        F0 = 50 + 15 * sin(time)
        # if F0 >= 120:
        #     F0 = 120
        # if time > 3:
        #     F0 = 0
        T = Ts
        Ts = calc_slice(0.7, T)
        res.append(Ts)
        time += t
        count += 1
    return res, time
    

if __name__ == "__main__":
    # Метод простых итераций
    T = [T0] * (N + 1)
    res, time = calc_model(T)

    x = np.arange(0, length, h)
    te = np.arange(0, time, t)

    n = 0
    for i in res:
        if (n % 7 == 0):
            tempora = n * t
            stroka = f'${tempora} sec$'
            plt.plot(x, i[:-1], label=stroka)
        n += 1
    stroka = f'${time} sec$'
    plt.plot(x, res[-1][:-1], label=stroka)
     
    plt.xlabel("x, cm")
    plt.ylabel("T, К")
    plt.legend(loc="upper right")
    plt.grid()
    plt.show()

    step = 0
    while (step < length / 3):
        point = [j[int(step / h)] for j in res]
        stroka = f'${round(step, 2)} cm$'
        plt.plot(te, point[:-1], label=stroka)
        if step > 0.49:
            step += 1
        else:
            step += 0.075
    plt.xlabel("t, sec")
    plt.ylabel("T, К")
    plt.legend(loc="upper right")
    plt.grid()
    plt.show()
