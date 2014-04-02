#!/usr/env python

import matplotlib.pyplot as plt  # plot library
import numpy as np  # array manipulation
from astropy import table  # handle data tables
from scipy import signal  # signal processing tools
from collections import Counter  # used only to create a histogram


def gausfunc(x, mu, sigma):
    ''' Return a gaussian distribution in the x range
        with mean "mu" and sigma "sigma"
    '''
    return (1.0/(sigma*np.sqrt(2.0*np.pi)))*np.exp(-(x-mu)**2/(2.0*(sigma**2)))


def corrfunc(x, y, t):
    ''' Caluclate the cross correlation function and timeshifts for a
        pair of time series x,y
    '''

    # normalize input series
    x -= x.mean()
    y -= y.mean()
    x /= x.std()
    y /= y.std()

    # calculate cross-correlation function
    corr = signal.correlate(x,y)/float(len(x))

    # transform time axis in offset units
    lags = np.arange(corr.size) - (t.size - 1)
    tstep = (t[-1] - t[0])/float(t.size)
    offset = lags*tstep

    # time shift is found for the maximum of the correlation function
    shift = offset[np.argmax(corr)]

    # new time axis to plot shifted time series
    newt = t + shift

    # correct time intervals if shift bigger than half the interval
    if min(newt) > (max(t)/2):
         newt = newt - max(t)
         shift = shift - max(t)
    elif max(newt) < (min(t)/2):
         newt = newt + min(t)
         shift = shift + min(t)

    return corr, offset, newt, shift


if __name__ == "__main__":
    '''
    Correlation of 2 time series in an ascii file
    '''
    print '''

    Time delay calculation between 2 time series

    NOTE FOR USING 2 FILES:
    The first input file must contains the time column and the first series

        For ASCII FILES is assumed that the first line contains the columns
        headers, and the columns are separated by blank spaces.
        Blank lines and lines starting with the carachter '#' are
        ignored.

        For FITS FILES are assumed that the first extension contains the data
        of the columns of interest.

        If indentifying columns by position, start counting from ZERO
    '''

    fmt = str(raw_input("Input files format (ascii/fits): "))

    inpt1 = str(raw_input("File 1: "))
    inpt2 = str(raw_input("File 2: "))


    tb1 = table.Table.read(inpt1, format=fmt)
    tb2 = table.Table.read(inpt2, format=fmt)

    timecol = raw_input("Time column name or position (starting from zero): ")
    xcol = raw_input("series 1 column name or position (starting from zero): ")
    xerr = raw_input("errors 1 column name or position (starting from zero): ")
    ycol = raw_input("series 2 column name or position (starting from zero): ")
    yerr = raw_input("errors 2 column name or position (starting from zero): ")

#   check if columns is an integer (column position)
#   if not assume its a string (column name)
    try:
        timecol = int(timecol)
    except ValueError:
        timecol = str(timecol)

    try:
        xcol = int(xcol)
    except ValueError:
        xcol = str(xcol)

    try:
        xerr = int(xerr)
    except ValueError:
        xerr = str(xerr)

    try:
        ycol = int(ycol)
    except ValueError:
        ycol = str(ycol)

    try:
        yerr = int(yerr)
    except ValueError:
        yerr = str(yerr)

#   Store columns in variables x(t), y(t), t
    t = tb1.field(timecol)
    x = tb1.field(xcol)
    xe = tb1.field(xerr)
    y = tb2.field(ycol)
    ye = tb2.field(yerr)

#   Exclude NaN and negative values -------------------------
    print ''
    print 'Excluding nan and negative values...'
    print ''
    exclude = []
    for i in xrange(len(x)):
        if ((x[i] > 0) and (y[i] > 0)):
            pass
        else:
            exclude.append(i)

    exclude = np.array(exclude)

    t = np.delete(t, exclude)
    x = np.delete(x, exclude)
    xe = np.delete(xe, exclude)
    y = np.delete(y, exclude)
    ye = np.delete(ye, exclude)
#   -----------------------------------------------------------

#   start time from Zero
    t -= min(t)

### MONTE CARLO  =========================================
    nsimulations = 100*len(x)

#   for each point in x and y, generates a 'nsimulation' new points
    aux1 = []
    aux2 = []
    for i, meanx in enumerate(x):
        newx = xe[i]*np.random.randn(nsimulations) + meanx
        aux1.append(newx)
    for j, meany in enumerate(y):
        newy = ye[j]*np.random.randn(nsimulations) + meany
        aux2.append(newy)

#   rearange itens, newxses will contain one time series in each element
    newxses = []
    newyses = []
    for n in xrange(nsimulations):
        newxses.append(np.array([aux1[m][n] for m in xrange(len(aux1))]))
    for n in xrange(nsimulations):
        newyses.append(np.array([aux2[m][n] for m in xrange(len(aux2))]))

#   plot new x lightcurves and original on top to check
#   for simulated in newxses:
#        plt.plot(t, simulated)
#    plt.plot(t, x, 'k--', linewidth='5.0')
#    plt.show()

#   plot new y lightcurves and original on top to check
#   for simulated in newxses:
#        plt.plot(t, simulated)
#    plt.plot(t, y, 'k--', linewidth='5.0')
#    plt.show()

#   store calculated time shift for each simulated curve
    shiftes = []
    for newx, newy in zip(newxses, newyses):
        newcorr, newoffset, nnewt, newshift = corrfunc(newx, newy, t)
        shiftes.append(newshift)

#   create a histogram from the simulated time shifts
    histogram = Counter(shiftes)

    distribution = []
    distbins = []
    for key in sorted(histogram.keys()):
        distribution.append(float(histogram[key]))
        distbins.append(key)

    distribution = np.array(distribution)
    mu = distribution.mean()
    sigma = distribution.std()
    norm = distribution.sum()

    print 'mean =', mu
    print 'std =', sigma

#   gaussian distribution for plot
    gaussian = gausfunc(distbins, mu, sigma)

#   normalize ditribution
    distribution /= norm

#######
#  BUG ???
#  Should the normalized distribution and gaussian be in the same scale?
#  Need Test with well behavioured funcitons
#######

#   plot distribution and gaussian
    plt.step(distbins, distribution)
    plt.plot(distbins, gaussian)
    plt.show()
    plt.cla()
# =======================================================

#   Calculates correlation of x and y time series
    corr, offset, newt, shift = corrfunc(x, y, t)

#   visualize calculated time shift
    print 'time shift = ', shift

#   open file to write results
    out = open('crosscorr.dat', 'w')
#   write offset and corr to file 'crosscorr.dat' in 2 columns
    for i in xrange(len(x)):
        out.write('{0} {1} \n'.format(offset[i], corr[i]))
    out.close()

#   plot correlation function
    plt.plot(offset, corr, label='correlation function')
    # position of maximum
    plt.vlines(shift, min(corr), max(corr), 'k', 'dashed',
            'offset = {0:1f}'.format(shift))
    plt.xlabel('Offset [time units]', fontsize=12)
    plt.ylabel('Correlation coeficient', fontsize=12)
    plt.legend(loc='best')
    plt.show()
    plt.cla()

#   plot original time series
    plt.plot(t, x, label='series 1')
    plt.plot(t, y, label='series 2')
    plt.xlabel('Time [s]', fontsize=12)
    plt.ylabel('Normalized Count Rate [counts/s]', fontsize=12)
    plt.show()
    plt.cla()

#   plot original time series plus shifted time series
    plt.plot(t, x, label='series 1')
    plt.plot(t, y, label='series 2')
    plt.plot(newt, y, label='shifted series 2')
    plt.xlabel('Time [s]', fontsize=12)
    plt.ylabel('Normalized Count Rate [counts/s]', fontsize=12)
    plt.legend(loc='best')
    plt.show()
    plt.cla()
