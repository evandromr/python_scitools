#!/usr/env python

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits


if __name__ == "__main__":
    '''
    shows the plot 2 given coluns of a fits file
    '''

    cam = 'epic'
    eng = '0.3-10'
    binsize = '350'

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

    fake = np.sin(((2.0*np.pi*x)/11931.0) + 100.5)
    x -= min(x)

    fake *= (y.std()+0.04)
    fake += y.mean()
    
    plt.rcParams['figure.figsize'] = (8.0, 5.0)

    plt.errorbar(x, y, yerr=e, fmt='o-', color='k')
    plt.errorbar(x, yb, yerr=eb, fmt='o-', color='b')
    #plt.plot(x, fake, 'r--')

    plt.annotate('Brightness drop', xy=(18250, 0.3), xytext=(16000, 0.8),
                 weight='bold', arrowprops=dict(facecolor='black', alpha=0.6,
                 shrink=0.08, width=2, headwidth=9))
    plt.annotate('bkg', xy=(10000,0.05), xytext=(10000, 0.09), color='blue')
    plt.annotate('(b) 2012', xy=(100,0.55), xytext=(100, 0.93), color='black',
                 weight='bold', fontsize=18)
    plt.xlim(-350, 21000)
    plt.ylim(0, 1)
    plt.xlabel('Time (s)')
    plt.ylabel('Cts/s (0.3-10keV)')
    plt.savefig(cam+'_lc_'+eng+'keV_bin'+binsize+'.pdf', orientation='landscape', papertype='a4',
                format='pdf', bbox_inches='tight')
    plt.show()
    plt.clf()
