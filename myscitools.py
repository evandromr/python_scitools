import numpy
import astropy.io.fits as fits


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

    Input
    ----------
    freqs: an array with frequencies in units of 1/s

    time: an array with the time series where to find a period

    harm: [optional] harmonic of the Fourrier analysis use higher harmonics to
    low signals.

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


def makefits(outptname='output.fits', *cols):
    '''
    makefits(outptname, col1[, col2, col3, ...])

    Description
    ----
    Creates a fits file with the giver columns columns and named <outptname>

    Input
    ----
    outptname : a string to name de output file
    cols : one or more lists in the format:
        col1 : [array, 'name-of-the-column', 'format', 'unit']

    Returns
    ----
    Boolean True
    and creates the file <outptname> on the current directory

    '''
    columns = []
    for i in xrange(len(cols)):
        columns.append(fits.Column(name=cols[i][1], format=cols[i][2],
                                   unit=cols[i][3], array=cols[i][0]))
    tbhdu = fits.new_table(columns)
    tbhdu.writeto(outptname)
    print '\n Created file {0} \n'.format(outptname)
    return True


def addlc(input1, input2, output='output.fits'):
    '''
    Add 2 light curves
    '''
    lc1 = fits.open(input1)
    lc2 = fits.open(input2)
    time = lc1[1].data.field('TIME')
    rate1 = lc1[1].data.field('RATE')
    rate2 = lc2[1].data.field('RATE')
    lc1.close()
    lc2.close()
    add = rate1+rate2
    timecol = [time, 'TIME', 'E', 's']
    addcol = [add, 'RATE', 'E', 'count/s']
    makefits(output, timecol, addcol)
    return True


def ratiolc(input1, input2, output='output.fits'):
    '''
    Ratio between 2 light curves
    '''
    lc1 = fits.open(input1)
    lc2 = fits.open(input2)
    time = lc1[1].data.field('TIME')
    rate1 = lc1[1].data.field('RATE')
    rate2 = lc2[1].data.field('RATE')
    lc1.close()
    lc2.close()
    try:
        ratio = rate1/rate2
    except ValueError:
        print " could not divide {0} and {1}!".format(input1, input2)
        return False
    else:
        timecol = [time, 'TIME', 'E', 's']
        ratiocol = [ratio, 'RATE', 'E', '']
        makefits(output, timecol, ratiocol)
    return True
