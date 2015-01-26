#!/usr/env python

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
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

    x -= min(x)
    x /= 1000

    r = yb/y
    slope, mean, rval, pval, stderr =  ss.linregress(x,r)

    print 'slope =', slope
    print 'mean =', mean
    print 'rval =', rval
    print 'pval = ', pval

    plt.errorbar(x, r, yerr=(((yb*e)-(y*eb))/(y**2)),
                 fmt='ko-')

    plt.plot(x, slope*x + mean, 'r', linewidth=2)
    plt.xlabel('Tempo (ks)')
    plt.ylabel('Cts. s$^{-1}$$_{(2,0-10,0 keV)}$ / Cts. s$^{-1}$$_{(0,3-2,0 keV)}$')
    plt.savefig('hardtime.pdf', orientation='landscape', papertype='a4',
                format='pdf', bbox_inches='tight')
    plt.xlim(min(x), max(x))
    plt.show()
    plt.clf()
