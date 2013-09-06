#!/usr/env python

import numpy


def z2n(freqs, time, harm=1):
    '''
    z2n(freqs,time[, harm])

    Description
    -----------
    A python implementation of the Rayleigh Z_n^2 method to calculate the power
    spectrum of a time series in a given range of frequencies

    Caculates a periodogram, using Fourrier-analysis trough
    a method using the statistical variable Z^2_n wich has a
    probability density funcion equal to that of a X^2 (chi-squared)
    with 2n degrees of freedom

    Returns
    ----------
      Z2n: An array with the powerspectrum of the time series
    '''
    N = len(time)
    Z2n = []
    for ni in freqs:
        aux = 0
        for k in xrange(harm):
            Phi = (ni*time) % 1
            arg = (k+1)*Phi*2.0*numpy.pi
            phicos = numpy.cos(arg)
            phisin = numpy.sin(arg)
            aux = aux + (phicos.sum())**2 + (phisin.sum())**2
        Z2n.append(2.0*aux/N)
    return Z2n
