from math import *
import black_scholes as bsf


def implied_volatility(ty, S, K, T, r, price_true, q=0):
    # start sigma
    sigma_hat = (2 * abs(log(S / K) + (r - q) * T) / T) ** 0.5

    # NEWTON's method
    tol = 1.0e-8
    sigma = sigma_hat
    sigmadiff = 1
    n = 1
    nmax = 100

    if ty == 'C':
        if (price_true < max((S * exp(-q * T) - K * exp(-r * T)), 0)) \
                or (price_true > S * exp(-q * T)):
            return 'NaN'
    elif ty == 'P':
        if (price_true < max((K * exp(-r * T) - S * exp(-q * T)), 0)) or (price_true > K * exp(-r * T)):
            return 'NaN'

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
    print implied_volatility('C', (1.958 + 1.958) / 2, 1.8, float(8) / 365, 0.04, 0.1547, 0.2)
