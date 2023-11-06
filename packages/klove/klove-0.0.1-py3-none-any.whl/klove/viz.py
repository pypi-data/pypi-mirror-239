#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Benjamin Vial
# This file is part of klove
# License: GPLv3
# See the documentation at benvial.gitlab.io/klove

from itertools import accumulate

import matplotlib.pyplot as plt

from . import backend as bk


def init_bands(sym_points, nband):
    Gamma_point, X_point, M_point = sym_points
    _kx = bk.linspace(Gamma_point[0], X_point[0], nband)
    _ky = bk.linspace(Gamma_point[1], X_point[1], nband)
    kGammaX = bk.vstack([_kx, _ky])
    _kx = bk.linspace(X_point[0], M_point[0], nband)
    _ky = bk.linspace(X_point[1], M_point[1], nband)
    kXM = bk.vstack([_kx, _ky])
    _kx = bk.linspace(M_point[0], Gamma_point[0], nband)
    _ky = bk.linspace(M_point[1], Gamma_point[1], nband)
    kMGamma = bk.vstack([_kx, _ky])
    ks = bk.vstack([kGammaX[:, :-1].T, kXM[:, :-1].T, kMGamma.T])
    return ks


def init_bands_plot(sym_points, nband):
    Gamma_point, X_point, M_point = sym_points
    dMGamma = bk.linalg.norm(bk.array(Gamma_point) - bk.array(M_point))
    dGammaX = bk.linalg.norm(bk.array(X_point) - bk.array(Gamma_point))
    dXM = bk.linalg.norm(bk.array(M_point) - bk.array(X_point))
    _kx = bk.linspace(0, dGammaX, nband)[:-1]
    _kx1 = dGammaX + bk.linspace(0, dXM, nband)[:-1]
    _kx2 = dXM + dGammaX + bk.linspace(0, dMGamma, nband)
    # _ky = bk.linspace(M_point[1], Gamma_point[1], nband)
    # kMGamma = bk.vstack([_kx, _ky])
    ksplot = bk.hstack([_kx, _kx1, _kx2])

    kdist = [dGammaX, dXM, dMGamma]

    return ksplot, kdist


def init_bands_3D(sym_points, nbands):
    k_bands = []
    _q = 0
    for i in range(len(sym_points) - 1):
        _a = sym_points[i][1] if len(sym_points[i]) == 2 else sym_points[i]
        _b = sym_points[i + 1][0] if len(sym_points[i + 1]) == 2 else sym_points[i + 1]
        _k = bk.linspace(_a, _b, nbands)
        k_bands.append(_k)

    k_bands = bk.vstack(k_bands)
    return k_bands


def init_bands_plot_3D(sym_points, nbands):
    k_bands_plot = []
    marks = []
    _q = 0
    for i in range(len(sym_points) - 1):
        _a = sym_points[i][1] if len(sym_points[i]) == 2 else sym_points[i]
        _b = sym_points[i + 1][0] if len(sym_points[i + 1]) == 2 else sym_points[i + 1]
        _k = bk.linspace(_a, _b, nbands)
        _p = bk.linalg.norm(_k[-1] - _k[0])
        _kplot = bk.linspace(_q, _q + _p, nbands)
        k_bands_plot.append(_kplot)
        marks.append(_q)
        _q += _p
    marks.append(_q)

    k_bands_plot = bk.array(k_bands_plot).ravel()
    return k_bands_plot, marks


def plot_bands(
    sym_points,
    nband,
    eigenvalues,
    xtickslabels=[r"$\Gamma$", r"$X$", r"$M$", r"$\Gamma$"],
    color=None,
    **kwargs,
):
    # nband = int((len(eigenvalues)-2)/3)

    if color == None:
        color = "#4d63c5"
        if "color" in kwargs:
            kwargs.pop("colors")
        if "c" in kwargs:
            kwargs.pop("c")

    ksplot, kdist = init_bands_plot(sym_points, nband)
    plt.plot(ksplot, eigenvalues, color=color, **kwargs)
    # xticks = bk.cumsum(bk.array([0] + kdist))
    xticks = list(accumulate([0] + kdist))
    plt.xticks(xticks, xtickslabels)
    for x in xticks:
        plt.axvline(x, c="#8a8a8a")

    plt.xlim(xticks[0], xticks[-1])

    plt.ylabel(r"$\omega$")
