#!/usr/env python

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
    xb =  bkg[1].data.field('TIME')
    yb = bkg[1].data.field('RATE')
    src.close()
    bkg.close()

    plt.plot(x, y, 'o-', xb, yb, 'o-')
    plt.xlabel('TIME [s]')
    plt.ylabel('RATE [cts/s]')
    plt.show()
    plt.clf()
