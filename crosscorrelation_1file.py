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
    
        For ASCII FILES is assumed that the first line contains the columns
        headers, and the columns are separated by blank spaces.
        Blank lines and lines starting with the carachter '#' are
        ignored.

        For FITS FILES are assumed that the first extension contains the data
        of the columns of interest.

        If indentifying columns by position, start counting from ZERO
    '''

    fmt = str(raw_input('Input file format (ascii/fits): '))

    inpt1 = str(raw_input("File : "))
    tb1 = table.Table.read(inpt1, format=fmt)

    timecol = raw_input("Time column name OR position (starting from zero): ")
    try:
        timecol = int(timecol)
    except ValueError:
        timecol = str(timecol)

    xcol = raw_input("series 1 column name OR position (starting from zero): ")
    try:
        xcol = int(xcol)
    except ValueError:
        xcol = str(xcol)

    ycol = raw_input("series 2 column name OR position (starting from zero): ")
    try:
        ycol = int(ycol)
    except ValueError:
        ycol = str(ycol)

    t = tb1.field(timecol)
    x = tb1.field(xcol)
    y = tb1.field(ycol)
    
    # Exclude NaN and negative values -------------------------
    print ''
    print 'Excluding nan and negative values...'
    print ''
    exclude = []
    for i in xrange(len(rate)):
        if ((x[i] > 0) and (y[i] > 0)):
            pass
        else:
            exclude.append(i)

    exclude = np.array(exclude)
    
    t = np.delete(t, exclude)
    x = np.delete(x, exclude)
    y = np.delete(y, exclude)
    #-----------------------------------------------------------

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
    plt.plot(newt, y, label='shifted series 2')
    plt.xlabel('Time [s]', fontsize=12)
    plt.ylabel('Normalized Count Rate [counts/s]', fontsize=12)

    plt.legend(loc='best')
    plt.show()
    plt.cla()
