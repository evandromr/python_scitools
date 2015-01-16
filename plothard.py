#!/usr/env python

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import scipy.optimize as so
import scipy.stats as ss

if __name__ == "__main__":
    '''
    shows the plot 2 given coluns of a fits file
    '''

    cam = str(raw_input("Camera: "))
    eng = str(raw_input("Energy1 : "))
    eng2 = str(raw_input("Energy2: "))
    binsize = str(raw_input("Bin: "))

    inptname1 = cam+"_lc_net_"+eng+"keV_bin"+binsize+".ds"
    inptname2 = cam+"_lc_net_"+eng2+"keV_bin"+binsize+".ds"
    src = fits.open(inptname1)
    bkg = fits.open(inptname2)
    x = src[1].data.field('TIME')
    y = src[1].data.field('RATE')
    e = src[1].data.field('ERROR')
    yb = bkg[1].data.field('RATE')
    eb = bkg[1].data.field('ERROR')
    src.close()
    bkg.close()

    #x -= min(x)

    # def contfunc(x, a):
    #     return a
    # def linfunc(x, a, b):
    #     return (a*x) + b
    # def sqrfunc(x, a, b, c):
    #     return a*(x**2) + b*x + c

    r = yb/y
    s = yb+y

    slope, mean, rval, pval, stderr =  ss.linregress(r,s)

    #popt, pcov = so.curve_fit(contfunc, r, s)
    #popt, pcov = so.curve_fit(linfunc, r, s)
    #perr = np.sqrt(np.diag(pcov))

    print 'slope =', slope
    print 'mean =', mean
    print 'rval =', rval
    print 'pval = ', pval

    plt.errorbar(y+yb, yb/y, xerr=(e+eb), yerr=(((yb*e)-(y*eb))/(y**2)),
                 ls='none', fmt='bo')
    plt.plot(slope*r + mean, r, 'r', linewidth=2)
    plt.xlabel('Rate$_1$ + Rate$_2$ (cts/s)')
    plt.ylabel('Rate$_2$/Rate$_1$')
    plt.xlim(min(s), max(s))

    plt.savefig(cam+'_hard_'+eng+'keV_'+eng2+'keV_bin'+binsize+'.pdf',
                orientation='landscape', papertype='a4',
                format='pdf', bbox_inches='tight')
    plt.show()
    plt.clf()
