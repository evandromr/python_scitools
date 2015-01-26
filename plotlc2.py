#!/usr/env python

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits


if __name__ == "__main__":
    '''
    shows the plot 2 given coluns of a fits file
    '''

    cam = str(raw_input("Camera: "))
    eng = str(raw_input("Energy: "))
    binsize = str(raw_input("Bin: "))

    inptname1 = cam+"_lc_net_"+eng+"keV_bin"+binsize+".ds"
    inptname2 = cam+"_lc_bkg_"+eng+"keV_bin"+binsize+".ds"
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
    x /= 1000.0

    plt.errorbar(x, y, yerr=e, fmt='o-', color='k')
    plt.errorbar(x, yb, yerr=eb, fmt='o-', color='b')
    plt.xlim(min(x), max(x))
    plt.xlabel('Tempo (ks)')
    plt.ylabel('Cts. s$^{-1}$')
    #plt.savefig(cam+'_lc_'+eng+'keV_bin'+binsize+'.pdf', orientation='landscape', papertype='a4',
    plt.savefig('lightcurve.pdf', orientation='landscape', papertype='a4',
                format='pdf', bbox_inches='tight')
    plt.show()
    plt.clf()
