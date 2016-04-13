import math
from scipy.stats import norm


def d_values(S, K, T, v, r, q=0):
    d1 = (math.log(S / K) + (r - q) * T) / ((T ** 0.5) * v) + (T ** 0.5) * 0.5 * v
    d2 = (math.log(S / K) + (r - q) * T) / ((T ** 0.5) * v) - (T ** 0.5) * 0.5 * v

    return d1, d2


def c_price(S, K, T, v, r, q=0):
    d1, d2 = d_values(S, K, T, v, r, q)
    call_price = S * norm.cdf(d1) * (math.e ** (-q * T)) - norm.cdf(d2) * K * (math.e ** (-r * T))

    return call_price


def p_price(S, K, T, v, r, q=0):
    d1, d2 = d_values(S, K, T, v, r, q)
    put_price = norm.cdf(-d2) * K * (math.e ** (-r * T)) - S * norm.cdf(-d1) * (math.e ** (-q * T))

    return put_price


def vega(S, K, T, v, r, q=0):
    d1, d2 = d_values(S, K, T, v, r, q)
    vega = S * (math.e ** (-q * T)) * (T ** 0.5) * norm.pdf(d1)

    return vega


if __name__ == "__main__":

    cases = [(100.0, 100.0, 0.5, 0.2, 0.01),
             (100.0, 120.0, 0.5, 0.2, 0.01),
             (100.0, 100.0, 1.0, 0.2, 0.01),
             (100.0, 100.0, 0.5, 0.3, 0.01),
             (100.0, 100.0, 0.5, 0.2, 0.02)]

    for case in cases:
        S, K, T, v, r = case
        print c_price(S, K, T, v, r), p_price(S, K, T, v, r)
