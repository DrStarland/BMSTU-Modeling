from matplotlib import pyplot as plt
import numpy as np
from scipy import integrate

eps_ys = 1e-5; eps_energy = 1e-3
coef_relax = 0.1
max_iters = 100

F0 = 100.0
T0 = 300.0
length = 0.2
h = 1e-3
N = int(length / h)
coef_n = 1.4
alpha = 0.05
sigma = 5.668e-12

table_lambda = np.array([
    [300, 500, 800, 1100, 2000, 2400],
    [1.36e-2, 1.63e-2,1.81e-2, 1.98e-2, 2.50e-2, 2.74e-2]
], dtype=np.double)

table_k = np.array([
    [293, 1278, 1528, 1677, 2000, 2400],
    [2.0e-2, 5.0e-2, 7.8e-2, 1.0e-1, 1.3e-1, 2.0e-1],
], dtype=np.double)

table_lambda[0] = np.log(table_lambda[0])
table_lambda[1] = np.log(table_lambda[1])
table_k[0] = np.log(table_k[0])
table_k[1] = np.log(table_k[1])

main_const = 4.0 * coef_n * coef_n * sigma
T0_pow4 = pow(T0, 4)

def get_lambda(T):
    return np.exp(np.interp(T, table_lambda[0], table_lambda[1]))

def get_k(T):
    return np.exp(np.interp(T, table_k[0], table_k[1]))

# эта функция не выделяется, однако я оставил её
# объявления явным (но не использую)
def p(T):
    return 0

def f(T):
    return -main_const * get_k(T) * (pow(T, 4) - T0_pow4)

def cappa(a, b):
    return (2 * a * b) / (a + b)

def left(Ts):
    K0 = cappa(get_lambda(Ts[0]), get_lambda(Ts[1]))
    M0 = -K0
    P0 = h * F0 + h * (f(Ts[0]) + f(Ts[1])) / 4 * h
    return K0, M0, P0

def right(Ts):
    KN = -cappa(get_lambda(Ts[-1]), get_lambda(Ts[-2]))
    MN = alpha * h
    PN = T0 * MN
    MN -= KN
    return KN, MN, PN

def progonka(A, B, C, D, K0, M0, P0, KN, MN, PN):
    n = len(A)
    xi = [- M0 / K0] + [None] * n
    eta = [P0 / K0] + [None] * n

    for i in range(n):
        znam = B[i] - A[i] * xi[i]
        xi[i + 1] = C[i] / znam
        eta[i + 1] = (D[i] + A[i] * eta[i]) / znam

    y = np.empty((n+2,), dtype=float)
    y[n + 1] = (PN - KN * eta[n]) / (MN + KN * xi[n])
    for i in range(n, -1, -1):
        y[i] = xi[i] * y[i + 1] + eta[i]

    return y

def calc_iteration(Ts):
    K0, M0, P0 = left(Ts)
    KN, MN, PN = right(Ts)
    
    A = np.empty(N - 1, dtype=np.double)
    B = np.empty(N - 1, dtype=np.double)
    C = np.empty(N - 1, dtype=np.double)
    D = np.empty(N - 1, dtype=np.double)

    X = np.arange(h, length, h)
    for n, x in enumerate(X):
        lambda_prev = get_lambda(Ts[n])
        lambda_cur = get_lambda(Ts[n + 1])
        lambda_next = get_lambda(Ts[n + 2])

        A[n] = cappa(lambda_prev, lambda_cur) / h
        C[n] = cappa(lambda_cur, lambda_next) / h
        B[n] = A[n] + C[n]
        D[n] = f(Ts[n]) * h
    
    return progonka(A, B, C, D, K0, M0, P0, KN, MN, PN)

def f1(T):
    return F0 - alpha * (T[-1] - T0)

def f2(T):
    x = np.arange(0, length + h, h)
    yi = [get_k(Ti) * (pow(Ti, 4) - T0_pow4) for Ti in T]
    return main_const * integrate.simpson(yi, x)

def not_energy_cond(ys, eps):
    return np.max(abs((f1(ys) - f2(ys)) / f1(ys))) > eps

def not_ys_cond(ys, ys0, eps):
    return np.max(abs((ys - ys0) / ys)) > eps

def calc_model(alpha, ys0, eps1, eps2, maxIter):
    i = 0
    ys = calc_iteration(ys0)
    while not_ys_cond(ys, ys0, eps1) and not_energy_cond(ys, eps2) and i < maxIter:
        ys0 = ys
        ys = (1 - alpha) * ys0 + alpha * calc_iteration(ys0)
        i += 1
    print(f"Итерации: {i}")
    print(f"Максимальная разность у: {round(np.max(abs((ys - ys0) / ys)), 7)}")
    print(f"Баланс энергий: {round(np.max(abs((f1(ys) - f2(ys)) / f1(ys))), 7)}")
    print(f"f1: {round(f1(ys), 7)} f2: {round(f2(ys), 7)}")
    return ys
    
if __name__ == "__main__":
    x = np.arange(0, length + h, h)
    T = np.array([500] * (N + 1), dtype=float)

    T = calc_model(coef_relax, T, eps_ys, eps_energy, max_iters)
    plt.plot(x, T, label='$T_a$')

##    alpha *= 3
##    T = calc_model(coef_relax, T, eps_ys, eps_energy, max_iters)
##    plt.plot(x, T, label='$T_{3a}$')

    plt.ylabel('T, K')
    plt.xlabel('x, см')
    plt.legend()
    plt.grid()
    plt.show()
