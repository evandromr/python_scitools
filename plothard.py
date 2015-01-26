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

    r = yb/y
    s = yb+y

    slope, mean, rval, pval, stderr =  ss.linregress(r,s)

    print 'slope =', slope
    print 'mean =', mean
    print 'rval =', rval
    print 'pval = ', pval

    plt.errorbar(y+yb, yb/y, xerr=(e+eb), yerr=(((yb*e)-(y*eb))/(y**2)),
                 ls='none', fmt='bo')
    plt.plot(slope*r + mean, r, 'r', linewidth=2)
    plt.xlabel('Cts. s$^{-1}$_{(1+2)}$')
    plt.ylabel('Cts. s$^{-1}$_{(2)}$ / Cts. s$^{-1}$$_{(1)}$')
    plt.xlim(min(s), max(s))
    plt.savefig('plothard.pdf', orientation='landscape', papertype='a4',
                format='pdf', bbox_inches='tight')
    plt.show()
    plt.clf()
