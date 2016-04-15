from math import *


def binomial_option(cp_type, exp_t, s, k, r, sigma, n):
    # cp_type:   option type(call or put)
    # s:         the spot price of asset S(0)
    # sigma:     volatility
    # k:         strike price
    # exp_t:     time to maturity
    # r:         risk - free interest rate
    # n:         number of steps
    #
    # written for american options

    delta_t = float(exp_t) / n
    u = exp(sigma * sqrt(delta_t))
    d = exp(-sigma * sqrt(delta_t))

    p = (exp(r * delta_t) - d) / (u - d)

    pay = []
    for i in range(n + 1):
        if cp_type == 'C':
            pay.append(max(((s * u ** (n - 2 * i)) - k), 0))
        elif cp_type == 'P':
            pay.append(max((k - (s * u ** (n - 2 * i))), 0))
    for j in range(n - 1, -1, -1):
        p_rec = []
        q_rec = []
        for m in range(j + 1):
            if cp_type == 'C':
                q_rec.append((max(((s * u ** (j - 2 * m)) - k), 0)))
            elif cp_type == 'P':
                q_rec.append((max((k - (s * u ** (j - 2 * m))), 0)))
            p_rec.append((pay[m] * p + pay[m + 1] * (1 - p)) * exp(-r * delta_t))
            pay[m] = max(q_rec[m], p_rec[m])
    return pay[0]