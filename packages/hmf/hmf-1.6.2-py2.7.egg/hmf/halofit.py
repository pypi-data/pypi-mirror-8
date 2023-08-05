import numpy as np
from scipy.integrate import simps
import copy
from scipy.interpolate import InterpolatedUnivariateSpline as spline
import cosmolopy as cp

def _get_spec(lnk, delta_k, sigma_8):
    """
    Calculate nonlinear wavenumber, effective spectral index and curvature
    of the power spectrum.
    """
    k = np.exp(lnk)
    delta_k = np.exp(delta_k)

    # Initialize sigma spline
    if sigma_8 < 1.0 and sigma_8 > 0.6:
        lnr = np.linspace(np.log(0.1), np.log(10.0), 500)
        lnsig = np.empty(500)

        for i, r in enumerate(lnr):
            R = np.exp(r)
            integrand = delta_k * np.exp(-(k * R) ** 2)
            sigma2 = simps(integrand, np.log(k))
            lnsig[i] = np.log(sigma2)

    else:  # # weird sigma_8 means we need a different range of r to go through 0.
        for r in [0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]:
            integrand = delta_k * np.exp(-(k * r) ** 2)
            sigma2 = simps(integrand, np.log(k))
            lnsig1 = np.log(sigma2)

            if lnsig1 < 0:
                try:
                    lnsig1 = lnsig_old
                except:
                    print "WARNING: LOWEST R NOT LOW ENOUGH IN _GET_SPEC. ln(sig) starts below 0: ", lnsig1
                break

            lnsig_old = copy.copy(lnsig1)

        lnr = np.linspace(np.log(0.01), np.log(10 * lnsig1), 500)
        lnsig = np.empty(500)

        for i, r in enumerate(lnr):
            R = np.exp(r)
            integrand = delta_k * np.exp(-(k * R) ** 2)
            sigma2 = simps(integrand, np.log(k))
            lnsig[i] = np.log(sigma2)

    r_of_sig = spline(lnsig[::-1], lnr[::-1], k=5)
    rknl = 1.0 / np.exp(r_of_sig(0.0))

    sig_of_r = spline(lnr, lnsig, k=5)

    try:
        dev1, dev2 = sig_of_r.derivatives(np.log(1.0 / rknl))[1:3]
    except:
        lnr = np.linspace(np.log(0.2 / rknl), np.log(5 / rknl), 100)
        lnsig = np.empty(100)

        for i, r in enumerate(lnr):
            R = np.exp(r)
            integrand = delta_k * np.exp(-(k * R) ** 2)
            sigma2 = simps(integrand, np.log(k))
            lnsig[i] = np.log(sigma2)
        sig_of_r = spline(lnr, lnsig, k=5)
        dev1, dev2 = sig_of_r.derivatives(np.log(1.0 / rknl))[1:3]

    rneff = -dev1 - 3.0
    rncur = -dev2

    return rknl, rneff, rncur

def halofit(k, z, omegam, omegav, w, omegan, neff, rncur, rknl, plin, takahashi=True):
    """
    Halofit routine to calculate pnl and plin.
    
    Basically copies the CAMB routine
    """

    # Define the cosmology at redshift
    omegamz = cp.density.omega_M_z(z, omega_M_0=omegam, omega_lambda_0=omegav, omega_k_0=1 - omegav - omegam, w=w)
    omegavz = omegav / cp.distance.e_z(z, omega_M_0=omegam, omega_lambda_0=omegav, omega_k_0=1 - omegav - omegam, w=w) ** 2

    w = w
    fnu = omegan / omegam

    if takahashi:
        a = 10 ** (1.5222 + 2.8553 * neff + 2.3706 * neff ** 2 +
                    0.9903 * neff ** 3 + 0.2250 * neff ** 4 +
                    - 0.6038 * rncur + 0.1749 * omegavz * (1 + w))
        b = 10 ** (-0.5642 + 0.5864 * neff + 0.5716 * neff ** 2 +
                - 1.5474 * rncur + 0.2279 * omegavz * (1 + w))
        c = 10 ** (0.3698 + 2.0404 * neff + 0.8161 * neff ** 2 + 0.5869 * rncur)
        gam = 0.1971 - 0.0843 * neff + 0.8460 * rncur
        alpha = np.abs(6.0835 + 1.3373 * neff - 0.1959 * neff ** 2 +
                - 5.5274 * rncur)
        beta = (2.0379 - 0.7354 * neff + 0.3157 * neff ** 2 +
                  1.2490 * neff ** 3 + 0.3980 * neff ** 4 - 0.1682 * rncur +
                  fnu * (1.081 + 0.395 * neff ** 2))
        xmu = 0.0
        xnu = 10 ** (5.2105 + 3.6902 * neff)

    else:
        a = 10 ** (1.4861 + 1.8369 * neff + 1.6762 * neff ** 2 +
                    0.7940 * neff ** 3 + 0.1670 * neff ** 4 +
                    - 0.6206 * rncur)
        b = 10 ** (0.9463 + 0.9466 * neff + 0.3084 * neff ** 2 +
                - 0.94 * rncur)
        c = 10 ** (-0.2807 + 0.6669 * neff + 0.3214 * neff ** 2 - 0.0793 * rncur)
        gam = 0.8649 + 0.2989 * neff + 0.1631 * rncur
        alpha = np.abs(1.3884 + 0.3700 * neff - 0.1452 * neff ** 2)
        beta = (0.8291 + 0.9854 * neff + 0.3401 * neff ** 2)
        xmu = 10 ** (-3.5442 + 0.1908 * neff)
        xnu = 10 ** (0.9589 + 1.2857 * neff)


    if np.abs(1 - omegamz) > 0.01:
        f1a = omegamz ** -0.0732
        f2a = omegamz ** -0.1423
        f3a = omegamz ** 0.0725
        f1b = omegamz ** -0.0307
        f2b = omegamz ** -0.0585
        f3b = omegamz ** 0.0743
        frac = omegavz / (1 - omegamz)
        f1 = frac * f1b + (1 - frac) * f1a
        f2 = frac * f2b + (1 - frac) * f2a
        f3 = frac * f3b + (1 - frac) * f3a
    else:
        f1 = f2 = f3 = 1.0

    y = k / rknl

    ph = a * y ** (f1 * 3) / (1 + b * y ** f2 + (f3 * c * y) ** (3 - gam))
    ph = ph / (1 + xmu / y + xnu * y ** -2) * (1 + fnu * (0.977 - 18.015 * (omegam - 0.3)))

    plinaa = plin * (1 + fnu * 47.48 * k ** 2 / (1 + 1.5 * k ** 2))
    pq = plin * (1 + plinaa) ** beta / (1 + plinaa * alpha) * np.exp(-y / 4.0 - y ** 2 / 8.0)
    pnl = pq + ph

    return pnl
