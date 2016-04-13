import math
from math import log, e
from scipy.stats import norm
from numpy import std, multiply, mean, var
from numpy.random import normal
from closed_form import geo_basket


def ari_asian(type, S, K, T, r, v, N, M, option):
    Dt = T / float(N)
    sigsqT = (v ** 2) * T * (N + 1) * (2 * N + 1) / (6 * N * N)
    muT = 0.5 * sigsqT + (r - 0.5 * (v ** 2)) * T * (N + 1) / (2 * N)
    d1 = (math.log(S / K) + (muT + 0.5 * sigsqT)) / (sigsqT ** 0.5)
    d2 = d1 - sigsqT ** 0.5
    N1 = norm.cdf(d1)
    N2 = norm.cdf(d2)
    N3 = norm.cdf(-d1)
    N4 = norm.cdf(-d2)
    geo = 0
    if type == 'C':
        geo = math.exp(-r * T) * (S * math.exp(muT) * N1 - K * N2)
    elif type == 'P':
        geo = math.exp(-r * T) * (K * N4 - S * math.exp(muT) * N3)
    drift = math.exp((r - 0.5 * (v ** 2)) * Dt)

    Spath = [0] * N
    arithPayoff = [0] * M
    geoPayoff = [0] * M
    for i in xrange(M):

        growthFactor = drift * math.exp(v * (Dt ** 0.5) * normal(0, 1))
        Spath[0] = S * growthFactor

        for j in xrange(1, N):
            growthFactor = drift * math.exp(v * (Dt ** 0.5) * normal(0, 1))
            Spath[j] = Spath[j - 1] * growthFactor

        # Arithmetic mean
        arithMean = mean(Spath)
        if type == 'C':
            arithPayoff[i] = math.exp(-r * T) * max(arithMean - K, 0)
        elif type == 'P':
            arithPayoff[i] = math.exp(-r * T) * max(K - arithMean, 0)

        # Geometric mean
        geoMean = math.exp(sum([math.log(item) for item in Spath]) / float(N))
        if type == 'C':
            geoPayoff[i] = math.exp(-r * T) * max(geoMean - K, 0)
        elif type == 'P':
            geoPayoff[i] = math.exp(-r * T) * max(K - geoMean, 0)

    # Standard Monte Carlo
    Pmean = mean(arithPayoff)
    Pstd = std(arithPayoff)
    confmc = (Pmean,Pmean - 1.96 * Pstd / (M ** 0.5), Pmean + 1.96 * Pstd / (M ** 0.5))

    # Control Variate
    covXY = mean(multiply(arithPayoff, geoPayoff)) - \
            mean(arithPayoff) * mean(geoPayoff)
    theta = covXY / var(geoPayoff)

    # control variate version
    Z = [arithPayoff[k] + theta * (geo - geoPayoff[k]) for k in xrange(M)]
    Zmean = mean(Z)
    Zstd = std(Z)
    confcv = (Zmean,Zmean - 1.96 * Zstd / (M ** 0.5), Zmean + 1.96 * Zstd / (M ** 0.5))

    if option == "STD":
        return confmc  # for no control variate
    elif option == "GEO":
        return confcv  # for geometric asian option
    else:
        return


def ari_basket(type, S1, S2, K, T, r, v1, v2, rou, M, option):
    arithPayoff = [0] * M
    geoPayoff = [0] * M
    for i in xrange(M):

        z1 = normal(0, 1)
        z2 = rou * z1 + ((1 - rou * rou) ** 0.5) * normal(0, 1)
        S1T = S1 * math.exp((r - 0.5 * v1 * v1) * T + v1 * (T ** 0.5) * z1)
        S2T = S2 * math.exp((r - 0.5 * v2 * v2) * T + v2 * (T ** 0.5) * z2)

        arithMean = 0.5 * (S1T + S2T)
        if type == "C":
            arithPayoff[i] = math.exp(-r * T) * max(arithMean - K, 0)
        elif type == "P":
            arithPayoff[i] = math.exp(-r * T) * max(K - arithMean, 0)

        geoMean = (S1T * S2T) ** 0.5
        if type == "C":
            geoPayoff[i] = math.exp(-r * T) * max(geoMean - K, 0)
        elif type == "P":
            geoPayoff[i] = math.exp(-r * T) * max(K - geoMean, 0)

    # Standard Monte Carlo
    Pmean = mean(arithPayoff)
    Pstd = std(arithPayoff)
    confmc = (Pmean, Pmean - 1.96 * Pstd / (M ** 0.5), Pmean + 1.96 * Pstd / (M ** 0.5))

    # Control Variate
    covXY = mean(multiply(arithPayoff, geoPayoff)) - \
            mean(arithPayoff) * mean(geoPayoff)
    theta = covXY / var(geoPayoff)

    # control variate version
    geo = geo_basket(type, S1, S2, K, T, r, v1, v2, rou)
    Z = [arithPayoff[k] + theta * (geo - geoPayoff[k]) for k in xrange(M)]
    Zmean = mean(Z)
    Zstd = std(Z)
    confcv = (Zmean ,Zmean - 1.96 * Zstd / (M ** 0.5), Zmean + 1.96 * Zstd / (M ** 0.5))

    if option == "STD":
        return confmc  # for no control variate
    elif option == "GEO":
        return confcv  # for geometric basket asian
    else:
        return


if __name__ == "__main__":
    print ari_asian('C', 1.96, 1.8, 8, 0.04, 0.3, 50, 10000, "STD")
    print ari_basket('C', 100, 100, 100, 3, 0.05, 0.3, 0.3, 0.5, 100000, "GEO")
