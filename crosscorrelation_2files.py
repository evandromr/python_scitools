#!/usr/env python

import matplotlib.pyplot as plt
import numpy as np
from astropy import table
from scipy import signal

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
    try:
        timecol = int(timecol)
    except ValueError:
        timecol = str(timecol)

    xcol = raw_input("series 1 column name or position (starting from zero): ")
    try:
        xcol = int(xcol)
    except ValueError:
        xcol = str(xcol)

    ycol = raw_input("series 2 column name or position (starting from zero): ")
    try:
        ycol = int(ycol)
    except ValueError:
        ycol = str(ycol)

    t = tb1.field(timecol)
    x = tb1.field(xcol)
    y = tb2.field(ycol)

    # eclude NaN values
    #x2 = x[np.logical_and(~(np.isnan(x)), ~(np.isnan(y)))]
    #y2 = y[np.logical_and(~(np.isnan(y)), ~(np.isnan(x)))]
    #t2 = t[np.logical_and(~(np.isnan(y)), ~(np.isnan(x)))]
    #x = x2
    #y = y2
    #t = t2

    t -= min(t)
    x -= x.mean()
    y -= y.mean()
    x /= x.std()
    y /= y.std()

    corr = signal.correlate(x, y)
    print 'Correlation Coeficients:'
    print corr

    xcorr = np.arange(corr.size)
    lags = xcorr - (t.size - 1)
    tstep = (t[-1]-t[0])/float(t.size)

    offset = lags*tstep

    shift = offset[np.argmax(corr)]
    newt = t + shift

    # correct time intervals
    if min(newt) > (max(t)/2):
        newt = newt - max(t)
        shift = shift - max(t)
    elif max(newt) < (min(t)/2):
        newt = newt + min(t)
        shift = shift + min(t)

    print 'time shift = ', shift

    plt.plot(offset, corr, label='correlation function')
    plt.vlines(shift, min(corr), max(corr), 'k', 'dashed',
            'offset = {0:1f}'.format(shift))
    plt.xlabel('Offset [time units]', fontsize=12)
    plt.ylabel('Correlation coeficient', fontsize=12)
    plt.legend(loc='best')
    plt.show()
    plt.cla()

    plt.plot(t, x, label='series 1')
    plt.plot(t, y, label='series 2')
    plt.xlabel('Time [s]', fontsize=12)
    plt.ylabel('Normalized Count Rate [counts/s]', fontsize=12)
    plt.show()
    plt.cla()

    plt.plot(t, x, label='series 1')
    plt.plot(t, y, label='series 2')
    plt.plot(newt, y, label='shifted series 2')
    plt.xlabel('Time [s]', fontsize=12)
    plt.ylabel('Normalized Count Rate [counts/s]', fontsize=12)

    plt.legend(loc='best')
    plt.show()
    plt.cla()
