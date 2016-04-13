import csv
import math
from datetime import datetime
import black_scholes as bsf


def implied_volatility(ty, S, K, T, r, price_true, q=0):
    # start sigma
    sigma_hat = (2 * abs(math.log(S / K) + (r - q) * T) / T) ** 0.5

    # NEWTON's method
    tol = 1.0e-8
    sigma = sigma_hat
    sigmadiff = 1
    n = 1
    nmax = 100

    while (sigmadiff >= tol and n < nmax):
        price = 0
        if ty == 'C':
            price = bsf.c_price(S, K, T, sigma, r, q)
        else:
            price = bsf.p_price(S, K, T, sigma, r, q)
        vega = bsf.vega(S, K, T, sigma, r, q)
        increment = (price - price_true) / vega
        sigma = sigma - increment
        n = n + 1
        sigmadiff = abs(increment)

    return sigma


if __name__ == "__main__":
    print implied_volatility('C', 1.96, 1.8, 8, 0.04, 0.1522, 0.2)
