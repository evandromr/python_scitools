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

    fake = np.sin(((2.0*np.pi*x)/3200.0) + 593.5)
    x -= min(x)

    fake *= (y.std()+0.04)
    fake += y.mean()

    plt.errorbar(x, y, yerr=e, fmt='o-', color='k')
    plt.errorbar(x, yb, yerr=eb, fmt='o-', color='b')
    plt.plot(x, fake, 'r--')
    plt.xlim(min(x)-350, max(x)+350)
    plt.xlabel('TIME [s]')
    plt.ylabel('RATE [cts/s]')
    plt.savefig(cam+'_lc_'+eng+'keV_bin'+binsize+'.pdf', orientation='landscape', papertype='a4',
                format='pdf', bbox_inches='tight')
    plt.show()
    plt.clf()
