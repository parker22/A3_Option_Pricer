from math import e, log
from scipy.stats import norm


def geo_asian(type, S, K, T, r, v, n):
    sigma_hat = v * (((n + 1) * (2 * n + 1) / (6.0 * n * n)) ** 0.5)
    mu_hat = (r - 0.5 * v * v) * ((n + 1) / (2.0 * n)) + 0.5 * (sigma_hat ** 2)
    d1_hat = log(S / float(K)) / (sigma_hat * (T ** 0.5)) + \
             (mu_hat + 0.5 * (sigma_hat ** 2)) * T / (sigma_hat * (T ** 0.5))
    d2_hat = d1_hat - (sigma_hat * (T ** 0.5))

    c = (e ** (-r * T)) * (S * (e ** (mu_hat * T)) * norm.cdf(d1_hat) - K * norm.cdf(d2_hat))
    p = (e ** (-r * T)) * (K * norm.cdf(-d2_hat) - S * (e ** (mu_hat * T) * norm.cdf(-d1_hat)))

    if type == 'C':
        return c
    elif type == 'P':
        return p
    else:
        return


def geo_basket(type, S1, S2, K, T, r, v1, v2, rou):
    sigma_Bg = ((v1 * v1 + v2 * v2 + 2 * rou * v1 * v2) ** 0.5) / 2
    mu_Bg = r - 0.5 * (v1 * v1 + v2 * v2) * 0.5 + 0.5 * sigma_Bg * sigma_Bg
    Bg0 = (S1 * S2) ** 0.5
    d1_hat = log(Bg0 / float(K)) / (sigma_Bg * (T ** 0.5)) + \
             (mu_Bg + 0.5 * (sigma_Bg ** 2)) * T / (sigma_Bg * (T ** 0.5))
    d2_hat = d1_hat - sigma_Bg * (T ** 0.5)

    c = (e ** (-r * T)) * (Bg0 * (e ** (mu_Bg * T) * norm.cdf(d1_hat)) - K * norm.cdf(d2_hat))
    p = (e ** (-r * T)) * (K * norm.cdf(-d2_hat) - Bg0 * (e ** (mu_Bg * T) * norm.cdf(-d1_hat)))

    if type == 'C':
        return c
    elif type == 'P':
        return p
    else:
        return


if __name__ == "__main__":
    print geo_asian('C', 100, 100, 3, 0.05, 0.3, 50)
    print geo_basket('C', 1.96, 2.04, 2.2, 8, 0.04, 0.3, 0.4, 0.8)
