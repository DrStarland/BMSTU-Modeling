from math import fabs
import numpy as np

TIME_STEP = 1e-3
DURATION = 10
EPS = 10e-4 / 2.0
EPS2 = EPS / 4.0

# производная вероятности - возвращается целая пачка для всех состояний [dp0, dp1, dp2, ..]
def dp(matrix, n, probs):
    return [
        TIME_STEP * sum([
                #if i == j
                    probs[j] * (-sum(matrix[i]) + matrix[i][i]) if i == j
                else
                    probs[j] * matrix[j][i] for j in range(n)
            ]) for i in range(n)
    ]

def compStabilizationTimes(matrix, n, start_probs, lim_probs, end_time = DURATION):
    curr_probs = start_probs.copy()
    stab_times = np.zeros(n, dtype=float)
    times = np.arange(0, end_time, step= TIME_STEP, dtype=float)
    probs_extended = []
    
    for time in times:
        probs_extended.append(curr_probs.copy())
        curr_dp = dp(matrix, n, curr_probs)
        for i in range(n):
            # если время стабилизации ещё не записано, производная крайне мала, а текущая вероятность
            # неумолимо подползла к пределу - сохраняем временную метку
            if (not stab_times[i] and curr_dp[i] <= EPS2 and fabs(curr_probs[i] - lim_probs[i]) <= EPS):
                stab_times[i] = time
            curr_probs[i] += curr_dp[i]
         
    return stab_times, times, probs_extended

def KolmogorovMatrix(matrix, n):
    matrix = np.array(matrix)
    result = np.zeros((n, n))
    for i in range(n - 1):
        for j in range(n):
            result[i, i] -= matrix[i, j]
            result[i, j] += matrix[j, i]
    for j in range(n):
        result[n - 1, j] = 1
    return result

def rightPart(n):
    return np.array([0] * (n - 1) + [1])

def solve(matrix, n):
    return np.linalg.solve(KolmogorovMatrix(matrix, n), rightPart(n))

def startProbabilities(n):
    res = [1] + [0] * (n - 1)
    return res

def computeAll(intensity_matrix, n):
    start_probabilities = startProbabilities(n)
    probabilities = solve(intensity_matrix, n)
    stabilization_time, times, probs_extended = compStabilizationTimes(
        intensity_matrix, n, start_probabilities, probabilities
    )
    return probabilities, probs_extended, times, stabilization_time