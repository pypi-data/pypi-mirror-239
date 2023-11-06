# -*- coding: utf-8 -*-
"""
    femagtools.losscoeffs
    ~~~~~~~~~~~~~~~~~~~~~

    Fitting methods for loss coeffs



"""
import numpy as np
import scipy.optimize as so


def pfe_bertotti(f, B, ch, cw, ce, fo, Bo):
    return (ch*(f/fo) + cw*(f/fo)**2)*(B/Bo)**2 + ce*(f/fo)**1.5*(B/Bo)**1.5


def pfe_jordan(f, B, ch, fh, cw, fw, fb, fo, Bo):
    return (ch*(f/fo)**fh + cw*(f/fo)**fw)*(B/Bo)**fb


def pfe_steinmetz(f, B, cw, fw, fb, fo, Bo):
    return cw*(f/fo)**fw * (B/Bo)**fb


def fitsteinmetz(f, B, losses, Bo, fo, alpha0=1.0):
    """fit coeffs of
    losses(f,B)=cw*(f/fo)**alfa*(B/Bo)**beta
    returns (cw, alfa, beta)
    """
    if np.isscalar(f):
        fbx = [[f]*len(losses), B]
        y = losses
        fitp, cov = so.curve_fit(
            lambda x, cw, beta: pfe_steinmetz(
                x[0], x[1], cw, alpha0, beta, fo, Bo),
            fbx, y, (1.0, 2.0))
        fitp = np.insert(fitp, 1, alpha0)

    else:
        pfe = losses
        z = []
        for i, fx in enumerate(f):
            if fx:
                if isinstance(B[0], float):
                    z += [(fx, bx, y)
                          for bx, y in zip(B, pfe[i])
                          if isinstance(y, float)]
                else:
                    z += [(fx, bx, y)
                          for bx, y in zip(B[i], pfe[i]) if y]

        fbx = np.array(z).T[0:2]
        y = np.array(z).T[2]
        fitp, cov = so.curve_fit(
            lambda x, cw, alpha, beta: pfe_steinmetz(
                x[0], x[1], cw, alpha, beta, fo, Bo),
            fbx, y, (1.0, 1.0, 2.0))
    return fitp


def fitjordan(f, B, losses, Bo, fo):
    """fit coeffs of
    losses(f,B)=(ch*(f/fo)**alpha + ch*(f/fo)**beta)*(B/Bo)**gamma
    returns (ch, alpha, cw, beta, gamma)
    """
    pfe = losses
    z = []
    for i, fx in enumerate(f):
        if fx:
            if isinstance(B[0], float):
                z += [(fx, bx, y)
                      for bx, y in zip(B, pfe[i])
                      if y]
            else:
                z += [(fx, bx, y)
                      for bx, y in zip(B[i], pfe[i])
                      if y]

    fbx = np.array(z).T[0:2]
    y = np.array(z).T[2]
    fitp, cov = so.curve_fit(lambda x, ch, alpha, cw, beta, gamma: pfe_jordan(
        x[0], x[1], ch, alpha, cw, beta, gamma, fo, Bo),
        fbx, y, (1.0, 1.0, 1.0, 2.0, 1.0))
    return fitp

def fitbertotti(f, B, losses, Bo, fo):
    """fit coeffs of
    losses(f,B)=(ch*(f/fo) + ch*(f/fo)**2)*(B/Bo)**2 + ce*(f/fo)**1.5)*(B/Bo)**1.5
    returns (ch, cw, ce)
    """
    pfe = losses
    z = []
    for i, fx in enumerate(f):
        if fx:
            if isinstance(B[0], float):
                z += [(fx, bx, y)
                      for bx, y in zip(B, pfe[i])
                      if y]
            else:
                z += [(fx, bx, y)
                      for bx, y in zip(B[i], pfe[i])
                      if y]

    fbx = np.array(z).T[0:2]
    y = np.array(z).T[2]
    fitp, cov = so.curve_fit(lambda x, ch, cw, ce: pfe_bertotti(
        x[0], x[1], ch, cw, ce, fo, Bo),
        fbx, y, (1.0, 1.0, 1.0))
    return fitp
